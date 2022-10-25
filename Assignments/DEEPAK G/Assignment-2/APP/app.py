from flask import Flask, render_template,url_for,redirect,request
import ibm_db
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLservercertiicate=DigiCertGlobalRootCA.crt;UID=vyq79202;PWD=sdL7FAq13svpnAm9",'','')
print(conn)
print("connection successful")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():  
   return render_template("login.html")

@app.route("/login",methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        sql = "SELECT * FROM SIGNUP WHERE email=?"
        prep_stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(prep_stmt, 1, email)
        ibm_db.execute(prep_stmt)
        dictionary = ibm_db.fetch_assoc(prep_stmt)

        if password == dictionary['PASSWORD']:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

    return redirect(url_for('login'))
@app.route("/register")
def register():
    return render_template("register.html")    

@app.route("/register",methods=['GET', 'POST'])
def signup():
    
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]

        sql = "INSERT INTO SIGNUP VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, password)
        ibm_db.bind_param(prep_stmt, 4, username)
        ibm_db.execute(prep_stmt)
        print("Inserted Successfully")

    return redirect(url_for('home'))

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)    