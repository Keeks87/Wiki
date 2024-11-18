'''
This file contains the functions that are used to interact with the entries in
the encyclopedia.

The functions are:

- list_entries: Returns a list of all names of encyclopedia entries.
- save_entry: Saves an encyclopedia entry, given its title and Markdown
content. If an existing entry with the same title already exists, it is
replaced.
- get_entry: Retrieves an encyclopedia entry by its title. If no such entry
exists, the function returns None.
'''
import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


# List all entries
def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


# Save an entry
def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


# Get an entry
def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
