import os
import re
from .Read import read_doc_file
def read_documents():
    list_files = ['1.docx','2.docx','3.docx','4.docx','5.docx','6.docx','7.docx','8.docx','9.docx','10.docx','11.docx','12.docx',
                  '13.docx','14.docx','15.docx','16.docx','17.docx','18.docx','19.docx','20.docx','21.docx','22.docx','23.docx','24.docx']
    documents = {}
    for file in list_files:
             
            documents[file] = read_doc_file(file)
    return documents

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    return set(words)

def create_index(documents):
    index = {}
    for doc, text in documents.items():
        words = preprocess(text)
        for word in words:
            index.setdefault(word, []).append(doc)
    return index

def parse_query(query):
    query = preprocess(query)
    stack = []
    precedence = {"not": 3, "and": 2, "or": 1}
    for word in query:
        if word in precedence:
            while stack and stack[-1] in precedence and precedence[word] <= precedence[stack[-1]]:
                yield stack.pop()
            stack.append(word)
        else:
            yield word
    while stack:
        yield stack.pop()

def evaluate_query(query, index):
    query = parse_query(query)
    stack = []
    for word in query:
        if word in {"not", "and", "or"}:
            if stack:
                a = stack.pop()
            else:
                a = set()
            if stack:
                b = stack.pop()
            else:
                b = set()
             
            if word == "not":
                stack.append(a - b)
            elif word == "and":
                stack.append(a & b)
            elif word == "or":
                stack.append(a | b)
        else:
            stack.append(set(index.get(word, [])))
    return stack.pop() if stack else set()

# Read the documents from a folder
documents = read_documents()

# Create an inverted index from the documents
index = create_index(documents)



def show( query):
    result = evaluate_query(query, index)
    result_text = ", ".join(result) if result else "None"
    return result_text.encode("utf-8", "replace").decode("utf-8")



