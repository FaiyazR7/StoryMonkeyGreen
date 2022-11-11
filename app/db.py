#Team Green Monkeys; Daniel He, Faiyaz Rafee
#SoftDev  
#P00-SCENARIO ONE
#2022-10-26

import sqlite3   #enable control of an sqlite database
DB_FILE="world.db"
               #facilitate db ops -- you will use cursor to trigger db events

#===========================MOCK STATIC DATABASE TO POPULATE ROUTES W/ DATA=============================== 
def genesis(): #outdated 
    db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
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
    db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    c.execute("DROP TABLE if exists users") #drop so no need to delete database each time the code changes
    c.execute("DROP TABLE if exists stories")
    c.execute("DROP TABLE if exists daniel_contributed_stories")
    c.execute("DROP TABLE if exists faiyaz_contributed_stories")
    c.execute("DROP TABLE if exists contributed_stories")
    c.execute("DROP TABLE if exists Cinderella")
    c.execute("DROP TABLE if exists The_Bible")
    c.execute("DROP TABLE if exists all_stories")
    c.executescript(""" 
        CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL);
        CREATE TABLE stories (title TEXT NOT NULL, username TEXT NOT NULL, date TEXT NOT NULL, body TEXT NOT NULL, genre TEXT NOT NULL);
    """
    ) #Primary key is implicityly NOT NULL
    db.commit() #save changes
    db.close()  #close database
    return True
#==========================================================
def sample(): #adds sample data
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    register_user("daniel", "abcde")
    register_user("faiyaz", "12345")
    date = c.execute("SELECT DATETIME('now');").fetchall()
    print(date)
    contribution = [
        ("Cinderella", "daniel", date[0][0], "Once upon a time...", "good" ),
        ("The Bible", "daniel", date[0][0], "In the beginning...", "good" ),
        ("The Bible", "faiyaz", date[0][0], "God created the...", "good")
    ]
    c.executemany("INSERT INTO stories VALUES(?, ?, ?, ?, ?)", contribution)
    db.commit() #save changes
    db.close()
    return True
#==========================================================
def user_exists(a): #determines if user exists
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    results = c.execute("SELECT username, password FROM users WHERE username = ?", (a,)).fetchall() #needs to be in ' ', ? notation doesnt help with this 
    db.close()
    if len(results) > 0:
        return True
    else: 
        return False
#==========================================================
def register_user(username, password): #determines if input is valid to register, adds to users table if so
    if user_exists(username):
        return False
    else:
        db = sqlite3.connect(DB_FILE, check_same_thread=False) 
        c = db.cursor()
        inserter = [(username, password)]
        print(inserter)
        c.executemany("INSERT INTO users VALUES(?, ?);", inserter)
        db.commit() #save changes
        db.close()
        return True
#==========================================================
def login_user(username, password): 
    if user_exists(username):
        db = sqlite3.connect(DB_FILE, check_same_thread=False) 
        c = db.cursor()
        results = c.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchall()
        db.close()
        return password == results[0][0]
    return False
#==========================================================
def all_users(): #for printing all users and stories 
    db = sqlite3.connect(DB_FILE, check_same_thread=False) 
    c = db.cursor()
    results = c.execute("SELECT * FROM stories;").fetchall()
    db.close()
    return results
#==========================================================
def reset():
    the_world = exodus()
    sample()
    print(all_users())
#==========================================================
def contributed_stories(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False) 
    c = db.cursor()
    results = c.execute("SELECT title, date, body, genre FROM stories WHERE username = ?", (username,)).fetchall()
    return results

def full_story(title):
    db = sqlite3.connect(DB_FILE, check_same_thread=False) 
    c = db.cursor()
    results = c.execute("SELECT username, date, body, genre FROM stories WHERE title = ? ORDER BY date", (title,)).fetchall()
    return results

# reset()
# print(contributed_stories("daniel"))
#CREATE TABLE stories (title TEXT NOT NULL, username TEXT PRIMARY KEY, date TEXT NOT NULL, body TEXT NOT NULL, genre TEXT NOT NULL);
