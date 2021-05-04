from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from django.http import HttpResponse
from . import util
from django.core.files.storage import default_storage
import random

class SearchForm(forms.Form):
    #all the feilds the form must have
    query=forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':"Search"}))

class CreateForm(forms.Form):
    #for create page
    new_entry=forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': "Enter title",'required':True}))
    data=forms.CharField(label="",widget=forms.Textarea(attrs={'placeholder': 'Enter the content','required':True}))

class EditForm(forms.Form):
    title = forms.CharField(label="Edit Title")
    body = forms.CharField(label="Edit Body", widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 10}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":SearchForm()
    })

def entrypage(request,title):
    page=util.get_entry(title)
    if page is None:
        return render(request,"encyclopedia/error.html",{
           "lform":SearchForm() 
        })

    else:
        
        data=markdown2.markdown(page)
        return render(request,"encyclopedia/content.html",
        {"title":title,"content":data,"lform":SearchForm()})
def search(request):
    #for returning results for search for an encyclopedia entry
    if request.method=="POST":
        sform=SearchForm(request.POST) #gets data from the form filled
        entries=list(util.list_entries())
        found_entries=[]
        if sform.is_valid():
                query=sform.cleaned_data["query"]
                for i in entries:

                    if (query.lower() ==i.lower()):
                        #redirect to entrypage
                        page=util.get_entry(query)
                        data=markdown2.markdown(page)
                        return render(request,"encyclopedia/content.html",
                        {"title":query,"content":data,"lform":SearchForm()})
                    elif query.lower() in i.lower():
                        found_entries.append(i)
                if len(found_entries)>0:

                    return render(request,"encyclopedia/index.html",{"entries":found_entries, "lform":sform})
                else:
                    return render(request,"encyclopedia/error.html",{"lform":SearchForm() })
        else:
            return render(request,"",{"form":SearchForm()})  
#if user manually enters for /search
    else:

        return render(request, "encyclopedia/search.html", {
            "query": "",
            "form": SearchForm()
        })
def create(request):
    if request.method=="POST":
        cform=CreateForm(request.POST) # stores create form data in form
        if cform.is_valid():
            title=cform.cleaned_data["new_entry"]
            content=cform.cleaned_data["data"]
            if title in list(util.list_entries()):
                return render(request,"encyclopedia/create.html",{"csform":CreateForm(),"error":'Error: This page already exists.Please enter a different title'})                           # HttpResponse("Error :This entry already exists")

            else:
                mtitle= "#" + title
                mdata= "\n" + content
                mcontent =mtitle + mdata
                util.save_entry(title,mcontent)
                page=util.get_entry(title)
                new_data=markdown2.markdown(page)
                return render(request,"encyclopedia/content.html",{"title":title,"content":new_data,"form":SearchForm()}) 
    else:
        return render(request,"encyclopedia/create.html",{"form":SearchForm(),"csform":CreateForm()})
def randompage(request):
    entrylist=list(util.list_entries())
    random_entry=random.choice(entrylist)
    page=util.get_entry(random_entry)
    return render(request,"encyclopedia/content.html",
        {"title":random_entry,"content":markdown2.markdown(page),"form":SearchForm()})
def edit(request,title):
    #pre populate with page name and content
    if request.method == "POST":
        #get the data for the given title
        data=util.get_entry(title)
        #display the data in the form
        #initial used to declare initial values of form
        eform=EditForm(initial={'title':title,'body':data})
        #return this page
        return render(request,"encyclopedia/edit.html",{"editform":eform,"title":title})
def save(request,title):
    if request.method == "POST":
        # Extract information from form
        edit_entry = EditForm(request.POST)
        if edit_entry.is_valid():
            # Extract 'data' from form
            content = edit_entry.cleaned_data["body"]
            # Extract 'title' from form
            title_edit = edit_entry.cleaned_data["title"]
            # If the title is edited, delete old file
            if title_edit != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            # Save new entry
            util.save_entry(title_edit, content)
            # Get the new entry 
            entry = util.get_entry(title_edit)
            msg_success = "Successfully updated!"
        # Return the edited entry
        return render(request, "encyclopedia/content.html", {
            "title": title_edit,
            "content": markdown2.markdown(entry),
            "form": SearchForm(),
            "msg_success": msg_success
        })



            




            
            
        
    