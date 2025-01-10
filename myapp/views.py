
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DocumentForm
from .models import Document
from .utils import reverse_index,clean_text
from .BooleanModel import boolean_search
from .ExtentedBooleanModel import extended_boolean_search
from .VectorModel import vector_search
from django.core.paginator import Paginator


def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save()
            reverse_index(document.question, document.answer, document.id)
            return redirect('add_document')
    else:
        form = DocumentForm()
    return render(request, 'myapp/add_document.html', {'form': form})


def list_questions(request):
    documents = Document.objects.all()
    paginator = Paginator(documents, 10)  
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'myapp/list_questions.html', {'page_obj': page_obj})


def search_documents(request):
    # Get search indicators
    query = request.GET.get('q', '')
    algorithm = request.GET.get('algorithm', 'boolean')

    # Execute the search based on the user's choice
    if algorithm == 'boolean':
        documents = boolean_search(query)
    elif algorithm == 'extended_boolean':
        documents = extended_boolean_search(query)
    elif algorithm == 'vector':
        documents = vector_search(query)    
    else:        
        documents = Document.objects.none()
        
    # Clean the query and hash it into tokens
    tokens = clean_text(query).split()

    # Pass the results to the template
    return render(request, 'myapp/search_results.html', {
        'documents': documents,
        'query': query,
        'algorithm': algorithm,
        'tokens': tokens,
    })


def delete_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if request.method == 'POST':
        document.delete()
        return redirect('list_questions')
    return render(request, 'myapp/list_questions.html', {'documents': Document.objects.all()})
