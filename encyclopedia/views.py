import markdown2 # Convert markdown text to html
from random import choice # Generate random numbers

#from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util


def index(request):
 
    # Post: searchbar
    if request.method == "POST":
        query = request.POST.get('q')
        
        # Check if query doesn't exist
        if query not in util.list_entries():

            # Check for substring
            results=[]
            for entry in util.list_entries():
                if entry.find(query) != -1:
                    results.append(entry)
            # Display results if found:
            if len(results) != 0:
                return render(request, f"encyclopedia/results.html", {
                    "results": results
                })

            # Display an error if no substring is found
            return render(request, f"encyclopedia/notfound.html", {
                "query": query
            })
        
        # If query exists, redirect to display
        return HttpResponseRedirect(reverse("encyclopedia:result", kwargs={'query':query}))
    
    # Get    
    else: 
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
        })

def display(request, query):
    
    # Post: edit 
    if request.method == "POST":
          
        # Save markdown file
        text = request.POST.get('text')
        f = open(f'entries/{query}.md', 'w')
        f.write(text)
        f.close()

        # Write html file
        md = util.get_entry(query) # Get md text
        html = markdown2.markdown(md) # Convert to html
        
        f = open(f'encyclopedia/templates/encyclopedia/{query}.html', 'w') # Write file
        f.write("""{% extends "encyclopedia/layout.html" %} {% block title %}{{query}}{% endblock %}{% block body %}""")
        f.write(html)
        f.write(f"""<a href="{query}/edit">Edit</a>""")
        f.write("""{% endblock %}""")
        f.close()

        return render(request, f"encyclopedia/{query}.html")
    
    # Get
    # Display an error if not found
    if query not in util.list_entries():
        return render(request, f"encyclopedia/notfound.html", {
            "query": query
        })

    # If found display page
    entry = util.get_entry(query) # Get md content
    html = markdown2.markdown(entry) # Convert md to html

    # Write html file
    f = open(f'encyclopedia/templates/encyclopedia/{query}.html', 'w') # Open file to write content
    f.write("""{% extends "encyclopedia/layout.html" %} {% block title %}{{query}}{% endblock %}{% block body %}""")
    f.write(html)
    f.write(f"""<a href="{query}/edit">Edit</a>""")
    f.write("""{% endblock %}""")
    f.close()

    # Display result
    return render(request, f"encyclopedia/{query}.html", {
        "entry": util.get_entry(query),
        "query": query
    })

def new(request):

    # Post: add new entry
    if request.method == "POST":
        entry = request.POST.get('title')

        # If entry exists, render an error
        if entry in util.list_entries():  
            return render(request, f"encyclopedia/exists.html",{
                "entry": entry
            })      

        # If not, add entry
        text = request.POST.get('text') # Get text

        # Write markdown content
        f = open(f'entries/{entry}.md', 'w')
        f.write(f"# {entry}\n\n")
        f.write(text)
        f.close()

    # Get 
    # Display New Page 
    return render(request, "encyclopedia/newpage.html")

def edit(request, query):
    # Get
    text = util.get_entry(query) # Get markdown text

    # Render edit page with actual title and text 
    return render(request, "encyclopedia/edit.html", {
        "entry": query,
        "text": text,
    })

def random(request):
    # Retrieve list of entries
    list = util.list_entries()
    # Select one randomly
    random = choice(list)
    # Return random page
    return HttpResponseRedirect(reverse("encyclopedia:result", kwargs={'query':random}))