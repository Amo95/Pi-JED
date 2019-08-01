# Pi-JED

@jameaamo@gmail.com

@AJHakM3

----------------------------

Co-partners:

Diana Blankson

Enoch Sarpong

# ----- Requirements -----

To keep the flask server started, type the following:


1. Type ```"pip3 install -r requirements.txt"```

2. then type ```"apt install sqlite3" and press Enter"```

3. navigate to the Pi-JED directory by typing ```"cd route-to-folder/Pi-JED"``` and press enter

Afterwards we have to create a database using sqlite3 to manage user data entries:

4. from the terminal type ```"sqlite3 preferred_database_name.db"``` and press enter
	in the sqlite3 cli type: 
	```=>.table and press enter to create a user table...```
	 ```  => Then, type ".exit" to exit```

5. Type, ```"python3"``` and press enter to enter into the python cli
	```=> From the python3 cli, type "from app import db" and press enter
	   => Then type, "db.create_all()" and press enter
	   => Type "exit()" to exit the python3 cli

6. now you can start flask (python3 app.py)


THANK YOU FOR TIME.... DOnt forget to comment issues regarding codes deployed in the project
