
from .utils import   calculate_weight
from .models import Term, TermDocument, Document


# Parses a query into Reverse Polish Notation (RPN)
def parse_query(query):
    # Define operator precedence
    operators = {'or': 0, 'and': 1, 'not': 2}
    stack = []
    output = []
    for term in query.lower().split():
        # If it's a term, add to the output
        if term not in operators:
            output.append(term)
        # Handle operators based on precedence
        else:
            while stack and operators.get(term, -1) <= operators.get(stack[-1], -1):
                output.append(stack.pop())
            stack.append(term)

    # Add remaining operators to the output
    while stack:
        output.append(stack.pop())

    return output


# Performs the NOT operation to find documents not in the given results
def not_operation(docs, all_docs):
    all_doc_ids = {doc.id for doc in all_docs}

    if not isinstance(docs, dict):
        return {doc.id: 1 for doc in all_docs}

    # Find the difference between all document IDs and the IDs in docs
    result = {doc_id: 1 for doc_id in all_doc_ids if doc_id not in docs}

    return result


# Performs logical operations AND/OR on two sets of documents
def boolean_operation(docs1, docs2, operator):
    # Validate inputs
    if not isinstance(docs1, dict) or not isinstance(docs2, dict):
        return {}
    # Intersection
    if operator == 'and':
        return {doc: min(docs1.get(doc, 0), docs2.get(doc, 0)) for doc in set(docs1) & set(docs2)}
    # Union
    elif operator == 'or':
        return {doc: max(docs1.get(doc, 0), docs2.get(doc, 0)) for doc in set(docs1) | set(docs2)}
    return {}


def extended_boolean_search(query):
    # Get all documents
    all_docs = Document.objects.all()  
    # Parse the query into Reverse Polish Notation
    parsed_query = parse_query(query)  
    
    # Ensure parsed_query is a list
    if not parsed_query:
        return Document.objects.none()

    stack = []

    for token in parsed_query:
        # Process each token in the query
        if token == 'not':
            if not stack:
                return Document.objects.none()
            # Get the operand
            operand = stack.pop()  
            # Perform NOT operation
            result = not_operation(operand, all_docs)  
            if stack:
                # Get the previous operand
                previous_operand = stack.pop()  
                # Combine results using AND
                result = boolean_operation(previous_operand, result, 'and')  
            stack.append(result)
        elif token in {'and', 'or'}:
            if len(stack) < 2:
                return Document.objects.none()
            # Get the right operand
            right = stack.pop()  
            # Get the left operand
            left = stack.pop()  
            # Perform AND or OR operation
            result = boolean_operation(left, right, token)  
            stack.append(result)
        else:
            try:
                # Search for the term in the database
                term = Term.objects.get(term=token)  
                # Get documents related to the term
                related_docs = TermDocument.objects.filter(term=term)  
                # Calculate weights
                doc_weights = {td.document_id: calculate_weight(term, td.document_id) for td in related_docs}  
                stack.append(doc_weights)
            except Term.DoesNotExist:
                stack.append({})

    if stack:
        # Get the final results
        final_result = stack.pop()  
        final_result_ids = final_result.keys()
        # Return the final documents
        return Document.objects.filter(id__in=final_result_ids)  

    return Document.objects.none()
