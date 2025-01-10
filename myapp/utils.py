from collections import defaultdict
from .models import Term, TermDocument, Document
import re
from math import log


# Cleans text by removing special characters, extra spaces, and converting to lowercase
def clean_text(text):
    text = re.sub(r'[.,!?;:]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()


# Calculates the weight of a term using TF-IDF
def calculate_weight_for_term(term, term_count, total_docs):
    # Count docs containing the term
    doc_count_with_term = TermDocument.objects.filter(term=term).count() + 1
    # Term frequency
    tf = term_count
    # Inverse document frequency
    idf = log(total_docs / doc_count_with_term)

    # Calculate weight
    weight = tf * idf
    return weight


# Builds a reverse index for a document using question and answer text
def reverse_index(question_text, answer_text, document_id):
    # Merge and clean text
    all_text = clean_text(question_text) + ' ' + clean_text(answer_text)

    term_counts = defaultdict(int)
    # Count term frequencies
    for token in all_text.split():
        term_counts[token] += 1

    # Get total number of documents
    total_docs = Document.objects.count() + 1
    # 
    for token, count in term_counts.items():
        term, created = Term.objects.get_or_create(term=token)

        #Weight calculation
        weight = calculate_weight_for_term(term, count, total_docs)

        # Add or update record in Terms Document with calculated weight
        term_document, created = TermDocument.objects.get_or_create(term=term, document_id=document_id)
        term_document.weight = weight
        term_document.save()


# Retrieves the weight of a term in a specific document
def calculate_weight(term, document_id):
    try:
        # Fetch term weight
        term_document = TermDocument.objects.get(term=term, document_id=document_id)
        return term_document.weight
    # If term is not found
    except TermDocument.DoesNotExist:
        return 0
    
###############################################
