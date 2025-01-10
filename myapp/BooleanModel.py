from .utils import clean_text
from .models import Term, TermDocument, Document


def boolean_search(query):
    # Step 1: Clean and tokenize the query
    cleaned_query = clean_text(query)
    tokens = cleaned_query.split()

    if not tokens:
        return Document.objects.none()  # Return no documents if query is empty

    # Step 2: Fetch document IDs from reverse index
    document_sets = []
    for token in tokens:
        try:
            term = Term.objects.get(term=token)
            term_documents = TermDocument.objects.filter(term=term)
            document_ids = set(term_documents.values_list('document_id', flat=True))
            document_sets.append(document_ids)
        except Term.DoesNotExist:
            return Document.objects.none()  # If any token is not found, no documents can match

    # Step 3: Find common document IDs containing all tokens
    if document_sets:
        common_document_ids = set.intersection(*document_sets)
    else:
        common_document_ids = set()

    # Step 4: Retrieve and return documents
    return Document.objects.filter(id__in=common_document_ids)