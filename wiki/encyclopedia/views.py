from tabnanny import check
from django.shortcuts import render
from markdown2 import Markdown
from matplotlib.pyplot import title
from random import choice
from . import util




def convert(title):
    content = util.get_entry(title)
    changer = Markdown()
    if content == None:
        return None
    else:
        return changer.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show(request, title):
    content = util.get_entry(title)
    converted_content = convert(title)
    if content == None:
        return render(request, "encyclopedia/none.html", {
            "first": "Error 404",
            "second": f"{title} was not found"
        })
    else:
        return render(request, "encyclopedia/result.html", {
            "title": title,
            "text": converted_content
        })
        
def search(request):
    title = request.POST['q']
    converted_content = convert(title)
    requested_title = util.get_entry(title)
    if requested_title != None:
        return render(request, "encyclopedia/result.html", {
            "title": title,
            "text": converted_content
        })
    else:
        items = util.list_entries()
        suggested = []
        for item in items:
            if title.lower() in item.lower():
                suggested.append(item)
        return render(request, "encyclopedia/search.html", {
            "suggested": suggested
        })
        
def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST['title']
        content = request.POST['wiki']
        check = util.get_entry(title)
        if check != None:
            return render(request, "encyclopedia/none.html", {
                "first": "Ooops",
                "second": f"{title} has been existed"
            })
        else:
            util.save_entry(title, content)
            converted_content = convert(title)
            return render(request, "encyclopedia/result.html", {
                "title": title,
                "text": converted_content
            })
            
def edit(request):
    title = request.POST['hidden_title']
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "text": content
    })
    
def save(request):
    title = request.POST['title']
    content = request.POST['wiki']
    util.save_entry(title, content)
    converted_content = convert(title)
    return render(request, "encyclopedia/result.html", {
        "title": title,
        "text": converted_content
    })
    
def random(request):
    list_title = util.list_entries()
    title = choice(list_title)
    content = convert(title)
    return render(request, "encyclopedia/randompage.html", {
        "title": title,
        "text": content
    })