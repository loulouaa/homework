import os
import re
import math
from collections import defaultdict
from .Read import read_doc_file
def read_documents():
    list_files = ['1.docx','2.docx','3.docx','4.docx','5.docx','6.docx','7.docx','8.docx','9.docx','10.docx','11.docx','12.docx',
                  '13.docx','14.docx','15.docx','16.docx','17.docx','18.docx','19.docx','20.docx','21.docx','22.docx','23.docx','24.docx']
    documents = {}
    for file in list_files:
             
            documents[file] = read_doc_file(file)
    return documents

def preprocess(text):
    return re.findall(r'\b\w+\b', text.lower())

def calculate_weight(term, document, documents):
    tf = document.count(term)
    idf = math.log(len(documents) / (sum(term in d for d in documents.values()) + 1e-10))
    return tf * idf


def create_index(documents):
    index = defaultdict(dict)
    for filename, content in documents.items():
        for term in set(preprocess(content)):
            index[term][filename] = calculate_weight(term, content, documents)
    return index

def parse_query(query):
    operators = {'or': 0, 'and': 1, 'not': 2}
    stack = []
    output = []
    for term in query.split():
        if term not in operators:
            output.append(term)
        else:
            while stack and stack[-1] in operators and operators[term] <= operators[stack[-1]]:
                output.append(stack.pop())
            stack.append(term)
    while stack:
        output.append(stack.pop())
    return output
def evaluate_query(expression, index, all_docs):
    stack = []
    for term in expression:
        if term in {'and', 'or', 'not'}:
            if not stack:
                print(f"Error: operator '{term}' without sufficient operands.")
                return
            b = stack.pop()
            if term == 'not':
                stack.append(not_operation(b, all_docs))
            else:
                if not stack:
                    print(f"Error: operator '{term}' without sufficient operands.")
                    return
                a = stack.pop()
                stack.append(boolean_operation(a, b, term))
        else:
            stack.append(index.get(term, {}))
    return sorted(stack[0], key=stack[0].get, reverse=True) if stack else []



def not_operation(docs, all_docs):
    return {doc: weight for doc, weight in all_docs.items() if doc not in docs}


def boolean_operation(docs1, docs2, op):
    if op == 'and':
        return {doc: min(docs1.get(doc, 0), docs2.get(doc, 0)) for doc in set(docs1) & set(docs2)}
    elif op == 'or':
        return {doc: max(docs1.get(doc, 0), docs2.get(doc, 0)) for doc in set(docs1) | set(docs2)}

def show_a( query ):
    documents = read_documents()
    index = create_index(documents)
    all_docs = {doc: 1 for doc in documents}
    while True:
       
        if query.lower() == 'exit':
            break
        expression = parse_query(query)
        result = evaluate_query(expression, index, all_docs)
        result_text = ", ".join(result) if result else "None"
        return result_text.encode("utf-8", "replace").decode("utf-8")
        
       

