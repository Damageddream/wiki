from django import forms

from django.shortcuts import render

from . import util

from django.http import Http404, HttpResponseRedirect

from django.urls import reverse

from django.contrib import messages



class NewPageForm(forms.Form):
    new_page_title = forms.CharField(label="New Page title")
    new_page_text = forms.CharField(widget=forms.Textarea)

class EditForm(forms.Form):
    edited_text = forms.CharField(widget=forms.Textarea(attrs={"placeholder":""}))

    


def index(request):
    if "entry" not in request.session:
        request.session["entry"] = util.list_entries()
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
            if new_page_title in util.list_entries():
                messages.error(request, "entry with that title already exists")
                return HttpResponseRedirect(reverse("wiki:new_page"))
            new_page_text = form.cleaned_data["new_page_text"]
            util.save_entry(new_page_title, new_page_text)
            request.session["entry"] = util.list_entries()
            return HttpResponseRedirect(reverse("wiki:entry", kwargs= {'entry_name':new_page_title}))
            

        else:
            return render(request, "encyclopedia/new_page.html",{
                "form": form
            })
    return render(request, "encyclopedia/new_page.html", {
        "form":NewPageForm() 
    })

def edit(request):
    edit_title = request.GET.get("entry_name")
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            edited_text = form.cleaned_data["edited_text"]
            util.save_entry(edit_title, edited_text)
            return HttpResponseRedirect(reverse("wiki:entry", kwargs= {'entry_name':edit_title}))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form":form
            })




    return render(request, "encyclopedia/edit.html",{
        "form":EditForm()

    })
               