## A website for open reservation

These website is been built using GAE along with Flask.

You can find the website live at this url:

```https://open-sreservation-ost.appspot.com/```

If you want to run it locally, clone this project and run:

```dev_appserver.py .```(You need to have google app engine installed with the bin path added to the PATH environment)

There is another branch called "experiment" and it basically remove the rss function.


## Web functionalities
Pretty much everything covered in the rubic file of the final project. Namely the following points:

1. Multi-user system. User can login, logout, register a new user. All infomation will be stored in cookies during one session. What I extrally did is taht Password has been encoded by encryption algorithm and only store the encoded version. So user's data can keep safe even if the entire data base is stolen.

2. Create a resource and set an available start and end time. End time has to been later than the start time otherwise leed to an error.

3. User can either make or delete a reservation. Reservation can't span two days and can't conflit with all the previously made reservation. Only upcoming reservation by some certain user will be shown on the front paeg.

4. Tag system. Click the tag of a resource too see a list of all resource with this tag.


## Code structure

Pretty much follow the MVC pattern.

M: You can find every data model in the database directory. I have 3 tables namely reservation, resource, tag.

V: It is separated to html files which is in the template folder and css and js files which can be found in the static folder.

C: Controller stuff. It's all in main.py in the root directory.

Tools folder include some utility functions I wrote for this project.
