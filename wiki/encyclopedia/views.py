from django import forms

from django.shortcuts import render

from . import util

from django.http import Http404, HttpResponseRedirect

from django.urls import reverse

class NewPageForm(forms.Form):
    new_page_title = forms.CharField(label="New Page title")
    new_page_text = forms.CharField(widget=forms.Textarea)

    


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
def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            new_page_title = form.cleaned_data["new_page_title"]
            print(type(new_page_title))
            new_page_text = form.cleaned_data["new_page_text"]
            util.save_entry(new_page_title, new_page_text)
            return HttpResponseRedirect(reverse("wiki:entry", args= f"{new_page_title}"))

        else:
            return render(request, "encyclopedia/new_page.html",{
                "form": form
            })
    return render(request, "encyclopedia/new_page.html", {
        "form":NewPageForm() 
    })
               