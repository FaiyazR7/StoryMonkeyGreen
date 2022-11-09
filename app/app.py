
from flask import Flask, render_template, request, session, redirect, url_for
import db          

app = Flask(__name__)    #create Flask object
app.secret_key = b"hehe"

@app.route("/")
def welcome():
    if "username" in session: 
        return render_template("response.html", username = session["username"])
    else:
        return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/homepage", methods=["GET","POST"])
def homepage():
    #check if username exists and then if password matches, right now it will just assume everyone is faiyaz
    session["username"] = "faiyaz"
    #input faiyaz into a method that will return all contributed and uncontributed stories, right now it is static 
    contributed_stories = db.user_data[2] #data returned using .fetchall() in db.py is a list of tuples, hard to work with so convert into a normal list
    contributed_stories = [x for y in contributed_stories for x in y] #look at the comment above
    return render_template("response.html", username = session["username"], stories = contributed_stories)

@app.route("/find_stories", methods=["GET","POST"]) #when you click a story button, this takes you to the correct story
def find_stories():
    print(request.method)
    title_of_story = request.form["title"]
    return redirect(url_for("stories", title = title_of_story)) #stories is the name of the function, not route ??

@app.route("/stories/<title>", methods=["GET","POST"])
def stories(title): #apparently methods cannot have the same name even if there are different parameters, so storied instead of stories to avoid conflict
    #method to input the story name to return all fields 
    return render_template("story.html", title = title)

@app.route("/logout")
def logout():
    session.pop("username", None) #pop to remove things from session 
    return redirect("/")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()

