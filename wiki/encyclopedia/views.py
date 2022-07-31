from django.shortcuts import render

from . import util

from django.http import Http404


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    if util.get_entry(entry_name) == None:
        raise Http404
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_name": entry_name,
            "display_entry": util.get_entry(entry_name)
        })
def query(request): 
    query = request.GET.get('q')
    if query in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "entry_name": query,
            "display_entry": util.get_entry(query)
        })
    else:
        entries = []
        for item in util.list_entries():
            if query in item:
                 entries.append(item)
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })
               