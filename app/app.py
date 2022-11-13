
from flask import Flask, render_template, request, session, redirect, url_for
import db          

app = Flask(__name__)    #create Flask object
app.secret_key = b"hehe"

@app.route("/")
def welcome():
    if "username" in session: 
        return redirect("/homepage")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        if db.register_user(request.form["username"], request.form["password"]):
            return redirect("/")
        else:
            return render_template("register.html", error = "INVALID USERNAME!!")
@app.route("/login", methods=["GET","POST"])
def login():
    #check if username exists and then if password matches
    if request.method == 'POST':
        if db.login_user(request.form["username"], request.form["password"]):
            session["username"] = request.form["username"]
            return redirect("/homepage")
            #return render_template("response.html", username = session["username"], stories = contributed_stories)
        else:
            session["error"] = "Username or password incorrect!" 
            return redirect("/")
    else: 
        return redirect("/")

@app.route("/homepage", methods=["GET","POST"])
def homepage():
    #check if username exists and then if password matches
    if "username" in session:
        print("Username in session")
        contributed_stories = db.contributed_stories(session["username"])
        print("collected contributed stories, if any")
        return render_template("response.html", username = session["username"], stories = contributed_stories)
        #return render_template("response.html", username = session["username"], stories = contributed_stories)
    else:
        return redirect("/")
    #input faiyaz into a method that will return all contributed and uncontributed stories, right now it is static 
    # contributed_stories = db.user_data[2] #data returned using .fetchall() in db.py is a list of tuples, hard to work with so convert into a normal list
    # contributed_stories = [x for y in contributed_stories for x in y] #look at the comment above

@app.route("/find_stories", methods=["GET","POST"]) #when you click a story button, this takes you to the correct story
def find_stories():
    if "username" in session:
        title_of_story = request.form["title"]
        return redirect(url_for("stories", title = title_of_story)) #stories is the name of the function, not route ??
    else:
        return redirect("/")

@app.route("/stories/<title>", methods=["GET","POST"])
def stories(title): #apparently methods cannot have the same name even if there are different parameters, so storied instead of stories to avoid conflict
    #method to input the story name to return all fields 
    if "username" in session:
        full_story = db.full_story(title)
        print (full_story)
        return render_template("story.html", story = full_story, title = title)
    else:
        return redirect("/")

@app.route("/create_story")
def create_story():
    if "username" in session:
        if request.method == 'GET':
            return render_template("create_story.html")
        elif request.method == 'POST':
            redirect("/homepage")
    else:
        return redirect("/")
@app.route("/logout")
def logout():
    session.pop("username", None) #pop to remove things from session 
    return redirect("/")

@app.route("/check")
def check():
    print (db.all_users())
    return redirect("/")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()

