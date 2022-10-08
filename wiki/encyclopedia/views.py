from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random



def convertmdToHTML(title):
    data=util.get_entry(title)
    markdowner = Markdown()
    if data == None:
        return None
    else:
        return markdowner.convert(data)

def entry(request,title):
    content=convertmdToHTML(title)
    if content == None:
        return render(request, "encyclopedia/error.html",{
            "message" : "This entry has not yet been added to the database and does not exist."
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "title": title,
            "content": content
        })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):
    if request.method== "POST":
        entry_search=request.POST['q']
        content1=convertmdToHTML(entry_search)
        if content1 is not None:
            return render(request,"encyclopedia/entry.html",{
            "title": entry_search,
            "content": content1,
        })
        else:
            all =util.list_entries()
            x=[]
            for entry in all:
                if entry_search.lower() in entry.lower():
                    x.append(entry)
            return render(request,"encyclopedia/search.html",{
                "recommendation": x
            })

def new(request):
    if request.method=="GET":
        return render(request,"encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        all =util.get_entry(title)
        if all is not None:
            return render(request,"encyclopedia/error.html",{
                "message": "entry already exists" 
            })
        else:
            util.save_entry(title,content)
            contentinhtml=convertmdToHTML(title)
            return render(request,"encyclopedia/entry.html",{
                "title":title,
                "content":contentinhtml
            })



def edit(request):
    if request.method=='POST':
        title=request.POST['entry_title']
        content= util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title": title,
            "content": content 
        })

def save_edit(request):
    if request.method=="POST":
        title=request.POST['title']
        content=request.POST['content']
        util.save_entry(title,content)
        contentinhtml=convertmdToHTML(title)
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":contentinhtml
        })
    return

def randomentry(request):
    all=util.list_entries()
    rand= random.choice(all)
    content=convertmdToHTML(rand)
    return render(request,"encyclopedia/entry.html",{
            "title":rand,
            "content":content
        })
