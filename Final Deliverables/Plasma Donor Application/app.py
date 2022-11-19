from flask import render_template
import requests
from flask import Flask
from flask import request,redirect,url_for,session,flash
from flask_wtf import Form
import ibm_db
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLservercertiicate=DigiCertGlobalRootCA.crt;UID=ymv17936;PWD=4miHcNLYiftKlnkL",'','')

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

from wtforms import TextField
app = Flask(__name__)

load_dotenv()
FROM_EMAIL=os.getenv('FROM_EMAIL')
SENDGRID_API_KEY=os.getenv('SENDGRID_API_KEY')
IMB_DB_URL=os.getenv('IMB_DB_URL')
SECRET_KEY=os.getenv('SECRET_KEY')

app.secret_key=SECRET_KEY



@app.route('/')
def hel():
    
     if session.get('username')==True:
        messages = session['username']

     else:
        messages = ""
        user = {'username': messages}
     return redirect(url_for('index',user=user))
   


@app.route('/reg')
def add():
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   
   if request.method == 'POST':
         name = request.form['name']
         address = request.form['address']
         city = request.form['city']
         pincode = request.form['pincode']
         bloodgroup = request.form['bloodgroup']
         pdate = request.form['pdate']
         ndate = request.form['ndate']
         email = request.form['email']
         password = request.form['password']
         sql = "INSERT INTO USERS VALUES (?,?,?,?,?,?,?,?,?)"
         prep_stmt = ibm_db.prepare(conn, sql)
         ibm_db.bind_param(prep_stmt, 1, name)
         ibm_db.bind_param(prep_stmt, 2, address)
         ibm_db.bind_param(prep_stmt, 3, city)
         ibm_db.bind_param(prep_stmt, 4, pincode)
         ibm_db.bind_param(prep_stmt, 5, bloodgroup)
         ibm_db.bind_param(prep_stmt, 6, pdate)
         ibm_db.bind_param(prep_stmt, 7, ndate)
         ibm_db.bind_param(prep_stmt, 8, email)
         ibm_db.bind_param(prep_stmt, 9, password)
         ibm_db.execute(prep_stmt)
         message = Mail(
         from_email=FROM_EMAIL,
         to_emails=email,
         subject='Plasma Donor',
         html_content='<p>Hello, Your Registration was successfull. <br><br> Thank you for choosing us.</p>')
         sg = SendGridAPIClient(
         api_key=SENDGRID_API_KEY)
         try:
            response=sg.send(message)
         except Exception:
                pass
         print("Mail Sent and response code is ",response.status_code)
         print("Inserted Successfully")
         return redirect(url_for('index'))


     
@app.route('/index',methods = ['POST', 'GET'])
def index():
    
      if request.method == 'POST':
        if session.get('username') is not None:
            messages = session['username']

        else:
            messages = ""
        user = {'username': messages}
        print(messages)
        val = request.form['search']
        print(val)
        type = request.form['type']
        print(type)
        if type=='blood':
         sql="SELECT * FROM users where bloodgroup =?",(val,)
         prep_stmt = ibm_db.prepare(conn, sql)
         ibm_db.bind_param(prep_stmt, 1, val)
         ibm_db.execute(prep_stmt)
         search = ibm_db.fetch_assoc(prep_stmt)
         
         sql="select * from users"
         prep_stmt = ibm_db.prepare(conn, sql)
         ibm_db.execute(prep_stmt)
         rows = ibm_db.fetch_assoc(prep_stmt)
         
         return render_template('index.html', title='Home', user=user,rows=rows,search=search)
         
        if type=='donorname':
         sql="select * from users where name=?",(val,)
         prep_stmt = ibm_db.prepare(conn, sql)
         ibm_db.bind_param(prep_stmt, 1, val)
         ibm_db.execute(prep_stmt)
         search = ibm_db.fetch_assoc(prep_stmt)
         
         sql="select * from users"
         prep_stmt = ibm_db.prepare(conn, sql)
         ibm_db.execute(prep_stmt)
         rows = ibm_db.fetch_assoc(prep_stmt)
         
         return render_template('index.html', title='Home', user=user,rows=rows,search=search)
     
      if session.get('username') is not None:
        messages = session['username']

      else:
        messages = ""
        user = {'username': messages}
        print(messages)
      if request.method=='GET':
         sql="select * from users"
         prep_stmt = ibm_db.prepare(conn, sql)
         ibm_db.execute(prep_stmt)
         rows = ibm_db.fetch_assoc(prep_stmt)
         
      return render_template('index.html', title='Home',  rows=rows)
         
 
@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')
    if request.method == 'POST':
            email = request.form["email"]
            password = request.form["password"]
            
            if email == 'admin@plasmabank.com' and password == 'admin':
                a = 'yes'
                session['username'] = email
                #session['logged_in'] = True
                session['admin'] = True
                return redirect(url_for('index'))
                #print((password,email))
            sql = "SELECT * FROM USERS WHERE email= ? "
            prep_stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(prep_stmt, 1, email)
            ibm_db.execute(prep_stmt)
            email = ibm_db.fetch_assoc(prep_stmt)
          
            

            a = ["email"]
            session['username'] = a
            session['logged_in'] = True
            print(a)
            u = {'username': a}
            p = ['password']
            print(p)
            if email == a and password == p:
                return redirect(url_for('index'))
            else:
                return render_template('/index.html')
    

    
@app.route('/logout')
def logout():
     
   session.pop('username', None)
   session.pop('logged_in',None)
   try:
       session.pop('admin',None)
   except KeyError as e:
       print("I got a KeyError - reason " +str(e))


   return redirect(url_for('index'))
   


@app.route("/dashboard")
def dashboard():
    sql = "SELECT COUNT(*), (SELECT COUNT(*) FROM blood WHERE type= 'O+'), (SELECT COUNT(*) FROM blood WHERE type='A+'), (SELECT COUNT(*) FROM blood WHERE type='B+'), (SELECT COUNT(*) FROM blood WHERE type='AB+'), (SELECT COUNT(*) FROM blood WHERE type='O-'), (SELECT COUNT(*) FROM blood WHERE type='A-'), (SELECT COUNT(*) FROM blood WHERE type='B-'), (SELECT COUNT(*) FROM blood WHERE type='AB-') FROM blood"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
        
        
    users = []
    sql = "SELECT * FROM BLOOD"
    prep_stmt = ibm_db.exec_immediate(conn, sql)
    rows = ibm_db.fetch_assoc(prep_stmt)
    
    while rows != False:
        users.append(rows)
        rows = ibm_db.fetch_assoc(prep_stmt)
    
    if users:
        return render_template("dashboard.html",b=account ,users = users)


@app.route('/plasmadonate')
def bl():
    return render_template('/adddonor.html')


@app.route('/addb',methods =['POST','GET'])
def addb():   
        msg = ""
        if request.method == 'POST':
           type = request.form['bloodgroup']
           donorname = request.form['donorname']
           donorsex = request.form['gender']
           qty = request.form['qty']
           dweight = request.form['dweight']
           email = request.form['email']
           phone = request.form['phone']
           sql = "INSERT INTO BLOOD VALUES (?,?,?,?,?,?,?)"
           prep_stmt = ibm_db.prepare(conn, sql)
           ibm_db.bind_param(prep_stmt, 1, type)
           ibm_db.bind_param(prep_stmt, 2, donorname)
           ibm_db.bind_param(prep_stmt, 3, donorsex)
           ibm_db.bind_param(prep_stmt, 4, qty)
           ibm_db.bind_param(prep_stmt, 5, dweight)
           ibm_db.bind_param(prep_stmt, 6, email)
           ibm_db.bind_param(prep_stmt, 7, phone)
           ibm_db.execute(prep_stmt)
           msg = "Record successfully added"
           print("Inserted Successfully")
 
        return redirect(url_for('dashboard'))



@app.route('/registerdonor')
def registerdonor():
    

    users = []
    sql = "SELECT * FROM USERS"
    prep_stmt = ibm_db.exec_immediate(conn, sql)
    rows = ibm_db.fetch_assoc(prep_stmt)
    
    while rows != False:
        users.append(rows)
        rows = ibm_db.fetch_assoc(prep_stmt)
    
    if users:
        return render_template("registerdonor.html" ,users = users)


   

@app.route('/contactforplasma/<emailid>')
def contactforplasma(emailid):
     if request.method=="GET":
    
        sql="SELECT * FROM REQUEST"
        prep_stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(prep_stmt)
    
        fromemail = session['username']
        name = request.form['name']
        address = request.form['address']
        
       # print(fromemail,emailid)
        sql=("INSERT INTO request (toemail,formemail,toname,toaddr) VALUES (?,?,?,?)",(emailid,fromemail,name,address) )
        prep_stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param ( prep_stmt, 1,(emailid,fromemail,name,address))
        ibm_db.execute(prep_stmt)
        
        flash('request sent')
        return redirect(url_for('index'))
    
     if request.method == 'POST':
       
        fromemail = session['username']
        name = request.form['name']
        address = request.form['address']
        
  
        sql=("INSERT INTO request (toemail,formemail,toname,toaddr) VALUES (?,?,?,?)",(emailid,fromemail,name,address) )
        prep_stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param ( prep_stmt, 1,(emailid,fromemail,name,address))
        ibm_db.execute(prep_stmt)
      
        flash('request sent')
        return redirect(url_for('index'))
   

@app.route('/notifications',methods=('GET','POST'))
def notifications():
   
    return render_template('notifications.html')


@app.route('/deleteuser/<useremail>',methods=['GET', 'POST'])
def deleteuser(useremail):
    if request.method == "GET":
        
        sql=f"DELETE FROM BLOOD WHERE EMAIL='{useremail}'"
        try:
            ibm_db.exec_immediate(conn,sql)
        except Exception:
            pass
       
        return redirect(url_for('dashboard'))

     
  
if __name__ == '__main__':
    app.run(debug=True)          