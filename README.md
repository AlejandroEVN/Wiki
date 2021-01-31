### Wiki  

Wikipedia like website. Users can add, edit or get a random wiki entry.  
This was my first project made with Django. This app doesn't use Django models, instead a .md file is created/modified everytime a user adds/edits an entry.
The main objective of this project was to get a grasp on the basic concepts of the Django framework.

#### Demo
<img src="./encyclopedia/demo/wiki-demo1.gif" width="960" height="540" />
<img src="./encyclopedia/demo/wiki-demo2.gif" width="960" height="540" />

#### Routes

`url: /`
Main page. Displays a list of the entries in the wiki.  

`url: /wiki/<str:title>`  
Page for the entry with the specified title.  

`url: /search`  
Allows the user to search for an entry by introducing it's title.  

`url: /add`  
Allows user to add an entry. If successful, redirects to said entry's page.  

`url: /edit/<str:title>`  
Allows user to edit the entry with the specified title.  

`url: /random`  
Redirects the user to a random wiki entry.  

#### Installation

- Clone into your machine
- Open a terminal
- Cd into projects' folder
- Run `pip install requirements.txt` (ideally in a virtual environment)
- Run `py manage.py runserver`
- Open browser and navigate to `127.0.0.1:<your Django local port>`

#### Tech Stack
- Python
- Django
- Bootstrap
- CSS
