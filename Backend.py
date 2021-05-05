import sqlite3 # used to connect to sqlite database
import csv # used for exporting results to a csv file, for the admin's collection

db_connection = None # connection to the database, empty at initialization

def createTables(): # a function to create the two tables needed to run the database
	# run two queries to create the two tables (if they don't exist) for the database, with the required attributes
	db_cursor.execute("CREATE TABLE IF NOT EXISTS Exhibits(name NOT NULL, exhibitID NOT NULL, initialDate NOT NULL, finalDate NOT NULL, briefDescription NOT NULL, hyperlink NOT NULL, externalLinks NOT NULL)")
	db_cursor.execute("CREATE TABLE IF NOT EXISTS Feedback(comment NOT NULL, rating NOT NULL, timestamp NOT NULL, exhibitID NOT NULL)")
	db_cursor.execute("CREATE TABLE IF NOT EXISTS Login(username NOT NULL, password NOT NULL)")
	db_connection.commit() # commit it so the change goes live
	return; # exit function

def insertToExhibit(): # a function to insert a tuple into the exhibit table, asking for input on each attribute of the exhibit table
	eName = input("Exhibit Name, STRING: ")
	eID = input("Exhibit ID, INT: ")
	eInitialDate = input("Exhibit Initial Date, DATE: ")
	eFinalDate = input("Exhibit Final Date, DATE: ")
	eAbstract = input("Exhibit Brief Description, STRING: ")
	eHyperlink = input("Exhibit Hyperlinks, STRING: ")
	eExternalLink = input("Exhibit External Links, STRING: ")
	db_cursor.execute("INSERT INTO Exhibits(name, exhibitID, initialDate, finalDate, briefDescription, hyperlink, externalLinks) VALUES(?, ?, ?, ?, ?, ?, ?)", [eName, eID, eInitialDate, eFinalDate, eAbstract, eHyperlink, eExternalLink]) # Run a query to insert the input attributes into a new entry of the table
	db_connection.commit() # commit it so the change goes live
	return; # exit function

def insertToFeedback(): # a function to insert a tuple into the feedback table, asking for input on each attribute of the feedback table
	fComment = input("Feedback Comment, STRING: ")
	fRating = input("Feedback Rating, INT: ")
	fTimestamp = input("Feedback Timestamp, DATETIME: ")
	fID = input("Exhibit ID, INT: ")
	db_cursor.execute("INSERT INTO Feedback(comment, rating, timestamp, exhibitID) VALUES(?, ?, ?, ?)", [fComment, fRating, fTimestamp, fID]) # Run a query to insert the input tuple as a new entry in the Feedback table
	db_connection.commit() # commit it so the change goes live
	return; # exit function

def insertToLogin(): # a function to insert a tuple into the login table, asking for input on each attribute of the login table
	lUsername = input("Login Username, STRING: ")
	lPassword = input("Login Password, STRING: ")
	db_cursor.execute("INSERT INTO Login(username, password) VALUES(?, ?)", [lUsername, lPassword]) # Run a query to insert the input tuple
	db_connection.commit() # commit it so the change goes live
	return; # exit function

def extractFeedback(): # a function to extract certain ranges of feedback for each exhibit
	exhibitID = input("Which exhibit would you like to extract the data for?: ")
	# Select everything in the feedback table that has the same exhibit ID as input
	db_cursor.execute("SELECT * FROM Feedback WHERE exhibitID = ?", [exhibitID]) # Execute user made query
	table = db_cursor.fetchall()
	for row in table: # print every row in the table generated from our query
		print(row)
	with open('results.csv', 'wb') as write_file: # for simplicity sake, define this command as 'write_file'
		cursor = db_connection.cursor() # use a different cursor from initial
		headers = ["Comment", "Rating", "Timestamp", "ExhibitID"] # the column headers for each attribute in the feedback table
		writeRow = ",".join([str(i) for i in headers]) + "\n" # we want to write the headers to every csv file created
		write_file.write(writeRow.encode()) # write the headers to the csv file
		for row in cursor.execute("SELECT * FROM Feedback WHERE exhibitID = ?", [exhibitID]): # select every tuple that applies here
			writeRow = ",".join([str(i) for i in row]) + "\n" # join all tuple elements, separate them with a comma, and put each into a column
			write_file.write(writeRow.encode()) # write the tuples to the csv file
	return; # exit function


def deleteExhibit(): # a function to delete everything from the exhibit table
	query = "DELETE FROM Exhibits"
	db_cursor.execute(query) # execute the delete query
	db_connection.commit() # commit changes
	return; # exit function

def deleteFeedback(): # a function to delete everything from the feedback table
	query = "DELETE FROM Feedback"
	db_cursor.execute(query) # execute the delete query
	db_connection.commit() # commit changes
	return; # exit function

def deleteLogin(): # a function to delete everything from the login table
	query = "DELETE FROM Login"
	db_cursor.execute(query) # execute the delete query
	db_connection.commit() # commit changes
	return; # exit function

def updateExhibit(): # a function update specific tuples from the exhibits table
	query = input("Enter a query in the form of 'UPDATE table_name SET conditions WHERE conditions':\n") # user input update query, used if necessary
	db_cursor.execute(query) # execute the update query
	db_connection.commit() # commit changes
	return; # exit function

def disconnect(): # a function to disconnect from the database
	db_cursor.close() # close the cursor to free up memory
	db_connection.close() # close the connection to exit the database
	return; # exit function

item = 100 # used to check which method the user would like to call

while item != 0:
	# Which method will be called by the frontend?
	item = input("Enter 1 - Connect to Database, \nEnter 2 - Create a new Exhibit tuple, \nEnter 3 - Create a new Feedback tuple, \nEnter 4 - Extract data from the Feedback table, \nEnter 5 - Delete from Exhibit table, \nEnter 6 - Delete from Feedback table, \nEnter 7 - Update the Exhibit table, \nEnter 8 - Create a new Login tuple, \nEnter 9 - Delete from Login table, \nEnter 10 - Disconnect from the Database:\n")
	if item == '1': # connect to the database
		try:
			db_connection = sqlite3.connect('exhibits.db') # create a database (if it doesn't exist) called exhibits.db and connect to it
			db_cursor = db_connection.cursor() # define the cursor that will look through the database
			createTables()
		except sqlite3.Error as err: # print an error message if you can't connect
			print(err)
	if item == '2': # create a new entry in the 'Exhibit' table
		insertToExhibit()
	if item == '3': # create a new entry in the 'Feedback' table
		insertToFeedback()
	if item == '4': # extract data from the table
		extractFeedback()
	if item == '5': # delete all the data in the exhibit table
		deleteExhibit()
	if item == '6': # delete all the data in the feedback table
		deleteFeedback()
	if item == '7': # update data in the exhibit table
		updateExhibit()
	if item == '8': # create a new entry in the 'Login' table
		insertToLogin()
	if item == '9': # delete all data in the login table
		deleteLogin()
	if item == '10': # disconnect from the database
		disconnect()

###### Always close cursor and connection ######
db_cursor.close()
db_connection.close()