from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


class NewTaskForm(forms.Form):
    task=forms.CharField(label="New Task")

# Create your views here.
def index(request):
    #if we look inside the session which contains all data about the user if 
    # list of tasks is not in that session i.e. user has never added any task
    if "tasks"  not in request.session:
        #the create an empty list for the user
        request.session["tasks"]=[]
    return render(request,"tasks/index.html",{
        #pass the list of task that's saved in the session i.e users already added tasks 
        #will be there
        "tasks":request.session["tasks"]
    })

#another page for adding tasks
'''this add fuction gets called in two different ways depending upon the request method
if we try to gets the add page by just clicking on the link to add a new task by going through
url add/ then we just want to render a new blank form but if we post data in this page by 
using POST request method instead of GET that means that means we are trying to submit the form
add we want to add a new task to the list of tasks, so we must add a check for that to check
that whether we are accessing add page just to view the form or we are submitting the form'''
def add(request):
    if request.method=="POST":
        #then process the result of the request by creating a new blank form 
        form=NewTaskForm(request.POST)
        #populate the data;request.post contains all the data that user submitted
        if form.is_valid():
            #get access to all data that user submitted and save it in variable task
            task=form.cleaned_data["task"]
            request.session["tasks"]+=[task]
            #give the name of route(index) and tell the http response to go ahead & reverse 
            #engineer what the route actually is
            return HttpResponseRedirect(reverse("index"))
            #reverse(index)-will say to fix out the url of the index url for the tasks app is 
            #and use that url to which we redirect to when we return http response redirect
        #if the form is not valid 
        else:
            #display  the add tasks page again 
            return render(request,"tasks/add.html",{
                "form":form})
            #return them the same form that they have filled alongwith errors
    #if method was not post then just display a form
    return render(request,"tasks/add.html",{
        "form":NewTaskForm()
    })
#by "form":NewTaskForm() we are saying that give add.html access to a variablr called form
#which will just be a newtaskform