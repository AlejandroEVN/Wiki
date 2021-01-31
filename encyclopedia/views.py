from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import markdown as md
import secrets


# Local python files with helpers and classes to import and use
from . import util
from . import forms


# Home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # If the entry doesn't exist:
    if not util.get_entry(title):
        # Displays alert page for "entry not found"
        return render(request, "encyclopedia/no-entry.html", {
            "title": title
        })
    # if entry exists:
    else:
        # Redirect the user to said entry's page
        return render(request, "encyclopedia/entry.html", {
            "entry": md.markdown(util.get_entry(title)),
            "title": title
        })

def search(request):
    # If form was submitted:
    if request.method == "POST":
        # Store the title searched for in 'query'
        query = request.POST.get("q")
        # Check if 'query' is an empty str
        if query:
            # Check if there is an entry with that value
            entry = util.get_entry(query)
            if entry is not None:
                # Redirect the user to that entry's page
                url = reverse('encyclopedia:entry', args=[query])
                return HttpResponseRedirect(url)
            else:
                # Stores the values of all the entries in 'entries'
                entries = util.list_entries()
                # Creates an empty list to keep track of entries that
                # contain the substring 'query'
                partialMatch = []
                # Loop thorugh the entries list:
                for entry in entries:
                    # Checks for query substring in entry
                    # Uses .lower() to be case insensitive
                    if query.lower() in entry.lower():
                        # Adds the matched entry to the list
                        partialMatch.append(entry)
                # If there are entries containing the query value
                # as a substring:
                if len(partialMatch) != 0:
                    # Render 'search.html', displaying all the entries
                    # as a list
                    return render(request, "encyclopedia/search.html", {
                        "entries": partialMatch
                    })
                else:
                    # Displays alert page for "entry not found"
                    return render(request, "encyclopedia/no-entry.html", {
                        "title": query
                    })
        # if the form is submitted without a value
        else:
            # Redirects the user to the main page
            return HttpResponseRedirect(reverse("encyclopedia:index"))
    # if the route '/search' is introduced in the browser, 
    # redirects to index
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))

def add_entry(request):

    # If request method is "POST":
    if request.method == "POST":

        # Create a form instance and populate it with data from the request
        form = forms.Entry(request.POST)

        # Check if the form is valid
        if form.is_valid():

            # Retrieve the title introduced by the user
            title = form.cleaned_data["title"]

            # If the title already exists in the wiki as an entry
            if util.get_entry(title) is not None:

                # Create an error message to display
                msg_error = "The entry already exists"

                # Render the "new.html" with the error message as an alert
                # and the link to the existing entry
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "msg_error": msg_error,
                    "title": title
                }) 

            # If the entry doesn't exist
            else:                
                # Retrieve the text introduced in the textarea
                content = form.cleaned_data["text"]
                util.save_entry(title, content)

                # Redirect to the new entry's page
                url = reverse("encyclopedia:entry", args=[title])
                return HttpResponseRedirect(url)
        
        # if the form is not valid:
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    # If request method is "GET"
    else:
        # Create an empty form to display in the HTML "new.html"
        form = forms.Entry()
        return render(request, "encyclopedia/new.html", {
            "form": form
        })

def edit(request, title):
    if request.method == "GET":

        # Initial values for the form
        initial_values = {
            "title": title,
            "text": util.get_entry(title)
        }

        # Creates a form with the values of the entry
        form = forms.Entry(initial = initial_values)

        # Renders edit.html with generated form
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": title
        })

    # If form is validated:
    else:
        # Create a form instance and populate it with data from the request
        form = forms.Entry(request.POST)

        # Check if the form is valid
        if form.is_valid():

            # Retrieve title and content
            title = form.cleaned_data["title"]
            content = form.cleaned_data["text"]

            # Save the modified entry
            util.save_entry(title, content)

            # Redirect user to the entry's page
            url = reverse("encyclopedia:entry", args=[title])
            return HttpResponseRedirect(url)
        
        # if the form is not valid:
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

        return HttpResponseRedirect(reverse("encyclopedia:index"))

def random(request):
    # Get the list of entries
    entries = util.list_entries()

    # Select a random one
    selected_page = secrets.choice(entries)

    # Pass it through as an argument for reverse
    url = reverse("encyclopedia:entry", args=[selected_page])
    return HttpResponseRedirect(url)