'''
Author: Dr Lam, Yipeng Liu 014057498
HW2
Oct 18, 2023
'''
import os
from flask import Flask, flash,  render_template, request, redirect, url_for, session
# Import packages above

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# index
@app.route("/")
def index():
    if len(session) == 0:
        return render_template("login.html")
    else:
        return redirect(url_for("homepage"))

# homepage action code
@app.route("/homepage_action",methods = ["POST","GET"])
def homepage_action():
    if request.method == "POST":
        inputtext = request.form["inputtext"]
        if len(inputtext) > 0:
            blogfile = open("blog.txt", "a") # append
            blogfile.write(":" + inputtext + "|\n")
            blogfile.close()
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        else:
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            blogfile = open("blog.txt", "a") # append
            blogfile.write(";" + app.config['UPLOAD_FOLDER'] + "/" + file.filename + "|\n")
            blogfile.close()
    return homepage()

# homepage
@app.route("/homepage")
def homepage():
    webpage = '''
    <html>
    <head>
    <title>Home</title>
    </head>
    <body>
    <p style='text-align:left;'>
    <h1>Welcome to the TECH 136 blog by LIU@sjsu
    <span style='float:right;'>
    Username:
    ''' + session["username"] + " <a href='" + "logout" + "'>Logout</a></h1></span></p>"
    # comment section
    webpage += '''
    <form action = 'homepage_action' enctype=multipart/form-data method = 'post'>
    Enter your comment here:
    <br>
    <textarea id='inputtext' name='inputtext' rows='2' cols='100'></textarea>
    <br>
    <input type = 'submit' value = 'Submit' />
    <input type=file name=file>
    <input type=submit value=Upload>
    <br>
    '''
    with open("blog.txt", "r") as blogfile:
        blog = blogfile.read().rstrip().rstrip("|")
    blogfile.close()
    bloglist = blog.split("|\n")
    if len(bloglist) > 0:
        for i in range(len(bloglist)-1, -1, -1):
            if len(bloglist[i]) > 0 and bloglist[i][0] == ":":
                webpage += "<br><textarea id='blogtext" + str(i) + "' name='blogtext" + str(i) + "' rows='2' cols='100'>" + bloglist[i][1:] + "</textarea>"
            else:
                webpage += "<br><img id='blogimage" + str(i) + "' name='blogimage" + str(i) + "' src='" + bloglist[i][1:] + "'><br>"
    return webpage

# login action code
@app.route("/login_action", methods = ["POST","GET"])
def login_action():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # User validation
        accounts = dict()
        with open("users.txt", "r") as user_file:
            for line in user_file.readlines():
                acc_li = line.split()
                accounts[acc_li[0]] = acc_li[1]

        if username in accounts and password == accounts[username]:
           session["username"] = username
           return redirect(url_for("homepage"))

    return render_template("login.html")

# signup action
@app.route("/signup_action", methods = ["POST", "Get"])
def signup_action():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with open("users.txt", "a") as user_file:
            user_file.write(username + ' ' + password + "\n")
    return render_template("login.html")

# signup
@app.route("/signup")
def signup():
    signup_page = '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Sign Up</title>
    </head>
    <script>
        function signupValidation() {
            done = false;
        // Get the value of the input field with id="username"
        let username = document.getElementById("username").value;
        // Get the value of the input field with id="password"
        let password = document.getElementById("password").value;
        // If the user did not enter anything
        let text;
        if (username.length == 0 || password.length == 0) {
            text = "Input is not valid";
            alert("both username and password cannot be empty");
        } else if (username.indexOf(' ') >= 0 || password.indexOf(' ') >= 0) {
            text = "Account username or password contains white spaces"
        } else {
            text = "";
            done = true;
        }
        document.getElementById("msg").innerHTML = text;
        return done;
        }
    </script>
    <body>
    <div style="text-align:center;">
    <form id="signup_form" name="signup_form" action="signup_action" onsubmit="return signupValidation()" method="post">
        Account:
        <input id="username" type="text" name="username" value=""/>
        <br>
        Password:
        <input id="password" type="password" name="password" value=""/>
        <br>
        <input type="submit" value="Submit">
        <div id="msg" style="color:red"></div>
    </form>
    </div>
    </body>
    </html>
    '''
    return signup_page

# logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("login.html")

# main driver function
if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5091)
