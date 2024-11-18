'''Views for the encyclopedia app of the wiki project.'''

import random
import markdown2

from django.shortcuts import render, redirect
from . import util


# Index page
def index(request):
    '''Return the index page with all the entries'''
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# New entry page
def create(request):
    '''Create a new page'''
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {"message": "Page already exists."})

        util.save_entry(title, content)
        return redirect("view_entry", title=title)

    return render(request, "encyclopedia/create.html")


# Random page
def random_entry(request):
    '''Redirect to a random entry'''
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {"message": "No entries available."})
    random_title = random.choice(entries)
    return redirect("view_entry", title=random_title)


# View an entry
def view_entry(request, title):
    '''View an entry by title'''
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {"message": "Page not found."})
    content = markdown2.markdown(entry)
    return render(request, "encyclopedia/entry.html", {"title": title, "content": content})


# Search for an entry
def search(request):
    '''Search for an entry by title'''
    query = request.GET.get('q', '').lower()
    entries = [entry for entry in util.list_entries() if query in entry.lower()]
    if len(entries) == 1 and entries[0].lower() == query:
        return redirect("view_entry", title=entries[0])
    return render(request, "encyclopedia/search_results.html", {"query": query, "entries": entries})


# Edit an entry
def edit_entry(request, title):
    '''Edit an entry by title'''
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("view_entry", title=title)

    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {"message": "Page not found."})
    return render(request, "encyclopedia/edit.html", {"title": title, "content": content})
