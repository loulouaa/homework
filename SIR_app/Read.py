import textract
import os
from docx import Document
import re

def read_doc_file(doc_path, search_phrase=None):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doc_path = os.path.join(BASE_DIR, 'SIR_app/Data/{0}'.format(doc_path))

    try:
        if doc_path.endswith('.docx'):
            # For .docx files, use the python-docx library
            doc = Document(doc_path)
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            text = '\n'.join(paragraphs)
        elif doc_path.endswith('.doc'):
            # For .doc files, use the textract library
            text = textract.process(doc_path).decode('utf-8')
        else:
            print(f"Unsupported file format: {doc_path}")
            return None

        # If there is a search word
        if search_phrase:
            # Find and replace the searched word with the addition of span to distinguish it
            highlighted_text = re.sub(
                fr'({re.escape(search_phrase)})',  # Word Search
                r'<span class="highlighted">\1</span>',  # Add span with class to highlight the word
                text,
                flags=re.IGNORECASE  # Search is case insensitive
            )
            return highlighted_text
        
        return text

    except Exception as e:
        print(f"Error reading document: {e}")
        return None
