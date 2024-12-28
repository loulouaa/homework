from django.shortcuts import render
from .BooleanModel import show
from .ExtentedBooleanModel import show_a
from .VectorsModel import show_b
from .Read import read_doc_file
import os

list_files = ['1.docx','2.docx','3.docx','4.docx','5.docx','6.docx','7.docx','8.docx','9.docx','10.docx','11.docx','12.docx',
              '13.docx','14.docx','15.docx','16.docx','17.docx','18.docx','19.docx','20.docx','21.docx','22.docx','23.docx','24.docx']

def home(request):
    search_results = []
    content = ''

    if request.method == 'POST':
        search_input = request.POST.get('search-input', '')
        search_option = request.POST.get('select-option')

        if search_input:
            if search_option == 'Boolean Model':
                search_results_str = show(search_input)
            elif search_option == 'Extended Boolean':
                search_results_str = show_a(search_input)
            elif search_option == 'Vector Model':
                search_results_str = show_b(search_input)
            else:
                pass

            # Split the string into a list using ',' as the separator
            search_results = search_results_str.split(', ')
            
            # Check if the first search result is in list_files
            if search_results[0] in list_files:
                x = list_files.index(search_results[0])
                content = read_doc_file(list_files[x])
            else:
                # Handle the case where the search result is not in list_files
                content = "Document not found."
           
    return render(request, 'index.html', {'search_results': search_results, 'CONT': content})

def read(request, pk):
    search_phrase = request.GET.get('search_word', '')  # Bring the word searched for
    content = read_doc_file(pk, search_phrase)  # Read text with tags
    return render(request, 'content.html', {'CONT': content, 'pk': pk})
