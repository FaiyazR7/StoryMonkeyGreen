#Team Green Monkeys; Daniel He, Faiyaz Rafee
#SoftDev  
#P00-SCENARIO ONE
#2022-10-26

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
DB_FILE="world.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#===========================MOCK STATIC DATABASE TO POPULATE ROUTES W/ DATA=============================== 
def genesis():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    c.execute("DROP TABLE if exists users") #drop so no need to delete database each time the code changes
    c.execute("DROP TABLE if exists daniel_contributed_stories")
    c.execute("DROP TABLE if exists faiyaz_contributed_stories")
    c.execute("DROP TABLE if exists Cinderella")
    c.execute("DROP TABLE if exists The_Bible")
    c.execute("DROP TABLE if exists all_stories")
    users = [ #a list of tuples, look at .executemany command for sqlite
        ("daniel", "abcde"),
        ("faiyaz", "12345")
    ]
    daniel_contributed_stories = [
        ("Cinderella",) #Comma at the end to create a tuple, or else error in .executemany 
    ]
    faiyaz_contributed_stories = [
        ("The Bible",)
    ]
    Cinderella = [
        ("daniel", "2016-8-16", "She was.", "fantasy")
    ]
    The_Bible = [
        ("faiyaz", "2016-8-16", "In the beginning...", "drama")
    ]
    all_stories = [
        ("Cinderella", "fantasy"),
        ("The Bible", "drama")
    ]
    #create all necessary tables
    c.executescript(""" 
        CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL);
        CREATE TABLE daniel_contributed_stories (story TEXT PRIMARY KEY);
        CREATE TABLE faiyaz_contributed_stories (story TEXT PRIMARY KEY);
        CREATE TABLE Cinderella (username TEXT PRIMARY KEY, date TEXT NOT NULL, body TEXT NOT NULL, genre TEXT);
        CREATE TABLE The_Bible (username TEXT PRIMARY KEY, date TEXT NOT NULL, body TEXT NOT NULL, genre TEXT);
        CREATE TABLE all_stories (story TEXT PRIMARY KEY, genre TEXT NOT NULL)
    """
    )
    #insert all necessary data
    c.executemany("INSERT INTO users VALUES(?, ?)", users) #users is a list of tuples, each element in the tuple correlates to a column, each tuple in the list correlates to a row 
    c.executemany("INSERT INTO daniel_contributed_stories VALUES(?)", daniel_contributed_stories)
    c.executemany("INSERT INTO faiyaz_contributed_stories VALUES(?)", faiyaz_contributed_stories)
    c.executemany("INSERT INTO Cinderella VALUES(?, ?, ?, ?)", Cinderella)
    c.executemany("INSERT INTO The_Bible VALUES(?, ?, ?, ?)", The_Bible)
    c.executemany("INSERT INTO all_stories VALUES(?, ?)", all_stories)
    #access all data 
    users_data = c.execute("SELECT * FROM users").fetchall() 
    daniel_contributed_stories_data = c.execute("SELECT * FROM daniel_contributed_stories").fetchall()
    faiyaz_contributed_stories_data = c.execute("SELECT * FROM faiyaz_contributed_stories").fetchall()
    Cinderella_data = c.execute("SELECT * FROM Cinderella").fetchall()
    The_Bible_data = c.execute("SELECT * FROM The_Bible").fetchall()
    all_stories_data = c.execute("SELECT * FROM all_stories").fetchall()
    db.commit() #save changes
    db.close()  #close database
    return (users_data, daniel_contributed_stories_data, faiyaz_contributed_stories_data, Cinderella_data, The_Bible_data, all_stories_data) #return all as a tuple 
#==========================================================
#genesis()
#==========================================================
def exodus():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    c.execute("DROP TABLE if exists users") #drop so no need to delete database each time the code changes
    c.execute("DROP TABLE if exists daniel_contributed_stories")
    c.execute("DROP TABLE if exists faiyaz_contributed_stories")
    c.execute("DROP TABLE if exists Cinderella")
    c.execute("DROP TABLE if exists The_Bible")
    c.execute("DROP TABLE if exists all_stories")
    c.executescript(""" 
        CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL);
        CREATE TABLE daniel_contributed_stories (story TEXT PRIMARY KEY);
        CREATE TABLE faiyaz_contributed_stories (story TEXT PRIMARY KEY);
        CREATE TABLE Cinderella (username TEXT PRIMARY KEY, date TEXT NOT NULL, body TEXT NOT NULL, genre TEXT);
        CREATE TABLE The_Bible (username TEXT PRIMARY KEY, date TEXT NOT NULL, body TEXT NOT NULL, genre TEXT);
        CREATE TABLE all_stories (story TEXT PRIMARY KEY, genre TEXT NOT NULL)
    """
    )
    db.commit() #save changes
    db.close()  #close database
    return True
#==========================================================
#the_world = exodus()
#==========================================================
def user_exists(a): #determines if user exists
    c = db.cursor()
    results = c.execute(f"SELECT username, password FROM users WHERE username = '{a}'").fetchall() #needs to be in ' ', ? notation doesnt help with this 
    if len(results) > 0:
        return True
    else: 
        return False
def register_user(username, password): #determines if input is valid to register, adds to users table if so
    c = db.cursor()
    if user_exists(username):
        return False
    else:
        inserter = [(username, password)]
        c.executemany("INSERT INTO users VALUES(?, ?)", inserter)
        results = c.execute("SELECT * FROM users").fetchall()
        return True
def login_user(username, password):
    c = db.cursor()
    if user_exists(username):
        results = c.execute(f"SELECT password FROM users WHERE username = '{username}'").fetchall()
        return password == results[0][0]
    return False
print(login_user('daniel', "abcde"))