from collections import defaultdict
from .utils import clean_text, calculate_weight_for_term
from .models import Term, TermDocument, Document
from math import sqrt


# Function to calculate cosine similarity
def cosine_similarity(vector1, vector2):
    # Calculate the dot product between the two vectors
    dot_product = sum([float(vector1[i]) * float(vector2[i]) for i in range(len(vector1))])
    # Calculate the magnitude of the first vector
    magnitude1 = sqrt(sum([float(val) ** 2 for val in vector1]))
    # Calculate the magnitude of the second vector
    magnitude2 = sqrt(sum([float(val) ** 2 for val in vector2]))
    # If the magnitude of either vector is zero, return similarity as zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    # Calculate the cosine similarity
    return dot_product / (magnitude1 * magnitude2)


# Function to convert document terms to a vector
def get_vector(document_terms, all_terms):
    # Create a vector of zeros with the length of all terms
    vector = [0] * len(all_terms)
    # Create a dictionary mapping terms to indices in the vector
    term_index = {term: idx for idx, term in enumerate(all_terms)}
    # Set the weights in the vector according to the terms in the document
    for term, weight in document_terms.items():
        index = term_index.get(term)
        if index is not None:
            vector[index] = weight
    return vector


# Function to get the vector for a specific document
def get_document_vector(document_id, all_terms):
    try:
        # Extract the terms for a specific document
        term_documents = TermDocument.objects.filter(document_id=document_id)
        document_terms = {td.term.term: td.weight for td in term_documents}
        # Convert the terms to a vector
        return get_vector(document_terms, all_terms)
    except ValueError as e:
        print(f"ValueError in get_document_vector: {e}")
        # Return a vector of zeros in case of an error
        return [0] * len(all_terms)


# Function to convert query text to a vector
def get_query_vector(query, all_terms):
    # Clean the text and split it into a list of terms
    query_terms = clean_text(query).split()
    # Count the terms in the query
    query_term_counts = defaultdict(int)
    for term in query_terms:
        query_term_counts[term] += 1
    
    query_weights = {}
    total_docs = Document.objects.count()

    for term in query_terms:
        try:
            term_obj = Term.objects.get(term=term)
            # Calculate the weight of each term in the query
            query_weights[term] = calculate_weight_for_term(term_obj, query_term_counts[term], total_docs)
        except Term.DoesNotExist:
            # If the term does not exist in the documents, set its weight to zero
            query_weights[term] = 0
    
    # Convert the terms to a vector
    return get_vector(query_weights, all_terms)


# Function to search for similar documents
def vector_search(query):
    # Extract all terms from the database
    all_terms = Term.objects.values_list('term', flat=True)
    # Convert the query to a vector
    query_vector = get_query_vector(query, all_terms)
    
    documents = Document.objects.all()
    results = []

    for document in documents:
        # Convert the document to a vector
        document_vector = get_document_vector(document.id, all_terms)
        # Calculate the similarity between the query vector and the document vector
        similarity = cosine_similarity(query_vector, document_vector)
        if similarity > 0:
            # Add the document and its similarity score to the results
            results.append((document, similarity))
    
    # Sort the results based on similarity scores
    results.sort(key=lambda x: x[1], reverse=True)
    # Return the sorted documents
    return [result[0] for result in results]
