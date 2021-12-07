
from flask import Flask,render_template,request,session,redirect,flash,current_app,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import json
import re
import random
import os
import razorpay
import secrets
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, send, emit
with open("config.json","r") as c:
 params=json.load(c)["params"]
app = Flask(__name__)
CORS(app)

app.secret_key = 'your secret key'
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'auction'

mysql = MySQL(app)

UPLOAD_FOLDER = r'C:/Users/Beast-PC/PycharmProjects/E-auction final/static/clogimg'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





@app.route('/' ,methods=['GET', 'POST'])
def home1():
    if 'loggedin' in session:

            isLog = True
            cursor0 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor0.execute('SELECT * FROM product')
            item = cursor0.fetchall()



        # User is loggedin show them the home page
            return render_template('index.html',isLog=isLog,item=item)
    elif 'loggedindoc' in session:
        isLogDoc=True
        cursor0 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor0.execute('SELECT * FROM product')
        item = cursor0.fetchall()
        return render_template('index.html',isLogDoc=isLogDoc,item=item)
    return render_template('index.html')


@app.route('/contact' ,methods=['GET', 'POST'])
def contact():
    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('contact.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('contact.html',isLogDoc=isLogDoc)
    return render_template('contact.html')

@app.route('/about' ,methods=['GET', 'POST'])
def about():
    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('about.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('about.html',isLogDoc=isLogDoc)
    return render_template('about.html')

@app.route('/product' ,methods=['GET', 'POST'])
def product():
    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('product.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('product.html',isLogDoc=isLogDoc)
    return render_template('index.html')

@app.route('/register1' ,methods=['GET', 'POST'])
def register1():
    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('index.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('index.html',isLogDoc=isLogDoc)
    return render_template('sign-up.html')

@app.route('/register' ,methods=['GET', 'POST'])
def register():
    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('index.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('index.html',isLogDoc=isLogDoc)

    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        name=request.form['name']

        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']

        datapat = {
            # 'firstname' : my_profile_data.getfirstname(),
            'name': name,

            'email': email,
            'password': password,

            'mobile': mobile,


        }

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM buyer WHERE  email=%s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not name or not password or not email:
            msg = 'Please fill out the Important details!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'


        elif len(mobile) != 10:
            msg = 'Mobile Number must be of 10 digits'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO buyer VALUES (%s, %s, %s,%s)',
                           (name, email,mobile, password))
            mysql.connection.commit()
            mymsg = "Registration Successfull! You Can Now Login To Your Account"

    return render_template('index.html')

@app.route('/sregister1' ,methods=['GET', 'POST'])
def sregister1():
    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('index.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('index.html',isLogDoc=isLogDoc)
    return render_template('ssignup.html')

@app.route('/sregister' ,methods=['GET', 'POST'])
def sregister():
    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('index.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('index.html',isLogDoc=isLogDoc)

    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        name=request.form['name']

        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']

        datapat = {
            # 'firstname' : my_profile_data.getfirstname(),
            'name': name,

            'email': email,
            'password': password,

            'mobile': mobile,


        }

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM seller WHERE  email=%s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not name or not password or not email:
            msg = 'Please fill out the Important details!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'


        elif len(mobile) != 10:
            msg = 'Mobile Number must be of 10 digits'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO seller VALUES (%s, %s, %s,%s)',
                           (name, email,mobile, password))
            mysql.connection.commit()
            mymsg = "Registration Successfull! You Can Now Login To Your Account"

    return render_template('index.html')




@app.route('/login' ,methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('index.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('index.html',isLogDoc=isLogDoc)
    return render_template('sign-in.html')

@app.route('/login2',methods=['GET', 'POST'])
def login2():

    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('index.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('index.html',isLogDoc=isLogDoc)


    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        dmsg = ''
        # Create variables for easy access
        Email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM buyer WHERE email = %s AND password = %s', (Email, password,))
        # Fetch one record and return result
        daccount = cursor.fetchone()
        # If account exists in accounts table in out database
        if daccount:
            # Create session data, we can access this data in other routes
            session['loggedin'] = daccount["email"]
            isLog=True
            session['name']=daccount["name"]
            session['email'] = daccount["email"]

            return render_template('index.html',isLog=isLog)
        else:
            # Account doesnt exist or username/password incorrect
            dmsg = 'Incorrect username/password!'
            return render_template('sign-in.html',dmsg=dmsg,retain=True)

    # Show the login form with message (if any)
    return render_template('sign-in.html')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin')
   session.pop('email')
   return redirect("/")

@app.route('/slogin' ,methods=['GET', 'POST'])
def slogin():
    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('index.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('index.html',isLogDoc=isLogDoc)
    return render_template('slogin.html')

@app.route('/slogin2',methods=['GET', 'POST'])
def slogin2():

    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('index.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('index.html',isLogDoc=isLogDoc)


    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        dmsg = ''
        # Create variables for easy access
        Email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM seller WHERE email = %s AND password = %s', (Email, password,))
        # Fetch one record and return result
        saccount = cursor.fetchone()
        # If account exists in accounts table in out database
        if saccount:
            # Create session data, we can access this data in other routes
            session['loggedindoc'] = saccount["email"]
            isLogDoc=True
            session['name']=saccount["name"]
            session['email']=saccount["email"]

            return render_template('index.html',isLogDoc=isLogDoc)
        else:
            # Account doesnt exist or username/password incorrect
            dmsg = 'Incorrect username/password!'
            return render_template('slogin.html',dmsg=dmsg,retain=True)

    # Show the login form with message (if any)
    return render_template('slogin.html')

@app.route('/slogout')
def slogout():
    # Remove session data, this will log the user out
   session.pop('loggedindoc')
   session.pop('email')
   return redirect("/")

@app.route('/spost')
def spost():
    if 'loggedin' in session:
            isLog = True
        # User is loggedin show them the home page
            return render_template('index.html',isLog=isLog)
    elif 'loggedindoc' in session:
        isLogDoc=True
        return render_template('spost.html',isLogDoc=isLogDoc)
    # Remove session data, this will log the user out
    return render_template('spost.html')
"""""""""""
def saveBlogImages(photo):
    hashPhoto=secrets.token_urlsafe(10)
    _,fileExtension=os.path.splitext(photo.filename)
    photoName=hashPhoto+fileExtension
    print("photoname is :",photoName)
    filePath=os.path.join(current_app.root_path,'static/blogimg',photoName)
    try:
        photo.save(filePath)
    except AttributeError:
        print("Couldn't save image {}".format(photo))

    return photoName
"""

@app.route('/ewaste')
def ewaste():
    if 'loggedin' in session:
            isLog = True
            cursor0 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor0.execute('SELECT * FROM ewaste')
            item = cursor0.fetchall()
        # User is loggedin show them the home page
            return render_template('ewaste.html',isLog=isLog,item=item )

@app.route('/ewpost')
def ewpost():
    if 'loggedindoc' in session:
            isLogDoc = True

        # User is loggedin show them the home page
            return render_template('ewpost.html',isLogDoc=isLogDoc)

@app.route('/addpost',methods=['POST'])
def addpost():
    if request.method == 'POST':
        if 'img1' not in request.files:
            return 'there is no file1 in form!'
        if 'img2' not in request.files:
            return 'there is no file2 in form!'
        if 'img3' not in request.files:
            return 'there is no file3 in form!'
        file1 = request.files['img1']
        path = os.path.join(app.config['UPLOAD_FOLDER'],file1.filename)
        file1.save(path)

        file2 = request.files['img2']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
        file2.save(path)

        file3 = request.files['img3']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file3.filename)
        file3.save(path)

        Title = request.form.get('title')
        slug = request.form.get('slug')
        sbid=request.form.get('sbid')
        bidinc = request.form.get('bidinc')



        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO product VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)', (Title,slug,sbid,bidinc,file1.filename,file2.filename,file3.filename,0,0,""))



        mysql.connection.commit()
        return redirect("/spost")



@app.route('/ewaddpost',methods=['POST'])
def ewaddpost():
    if request.method == 'POST':
        if 'img1' not in request.files:
            return 'there is no file1 in form!'
        if 'img2' not in request.files:
            return 'there is no file2 in form!'
        if 'img3' not in request.files:
            return 'there is no file3 in form!'
        file1 = request.files['img1']
        path = os.path.join(app.config['UPLOAD_FOLDER'],file1.filename)
        file1.save(path)

        file2 = request.files['img2']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
        file2.save(path)

        file3 = request.files['img3']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file3.filename)
        file3.save(path)

        Title = request.form.get('title')
        eslug = request.form.get('eslug')
        category = request.form.get('category')
        weight = request.form.get('weight')
        sbid=request.form.get('sbid')
        bidinc = request.form.get('bidinc')



        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO ewaste VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (Title,eslug,category,weight,sbid,bidinc,file1.filename,file2.filename,file3.filename,0,0,""))



        mysql.connection.commit()
        return redirect("/")



@app.route('/viewproduct/<slug>',methods=['GET','POST'])
def viewproduct(slug):
 if 'loggedin' or 'loggedindoc' in session:
    isLog=True
    isLogDoc=True
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from product where slug=%s", (slug,))
    datablog = cur.fetchone()

    return render_template("product-details.html",datablog=datablog,isLog=isLog,isLogDoc=isLogDoc)
 else:
    return redirect("/")

@app.route('/vieweproduct/<eslug>',methods=['GET','POST'])
def vieweproduct(eslug):
 if 'loggedin' or 'loggedindoc' in session:
    isLog=True
    isLogDoc=True
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from ewaste where eslug=%s", (eslug,))
    datablog = cur.fetchone()

    return render_template("eproductdetails.html",datablog=datablog,isLog=isLog,isLogDoc=isLogDoc)
 else:
    return redirect("/")

@app.route('/startb/<slug>/<sbid>',methods=['GET','POST'])
def startb(slug,sbid):
    if 'loggedin' in session:
        isLog = True
        print(sbid,slug)
        cur4 = mysql.connection.cursor()
        query2 = "UPDATE product SET hbid = %s,hbidder=%s,bstart=1 WHERE slug = %s"
        adr = (sbid,session['loggedin'],slug,)
        cur4.execute(query2, adr)
        mysql.connection.commit()
        return redirect("/")
    return redirect("/")

@app.route('/starteb/<eslug>/<sbid>',methods=['GET','POST'])
def starteb(eslug,sbid):
    if 'loggedin' in session:
        isLog = True

        cur4 = mysql.connection.cursor()
        query2 = "UPDATE ewaste SET hbid = %s,hbidder=%s,bstart=1 WHERE eslug = %s"
        adr = (sbid,session['loggedin'],eslug,)
        cur4.execute(query2, adr)
        mysql.connection.commit()
        return redirect("/ewaste")
    return redirect("/ewaste")

@app.route('/bidincre/<slug>/<bidinc>/<hbid>',methods=['GET','POST'])
def bidincre(slug,bidinc,hbid):
    if 'loggedin' in session:
        isLog = True

        cur4 = mysql.connection.cursor()
        query2 = "UPDATE product SET hbid = %s,hbidder=%s WHERE slug = %s"
        adr = ((int(hbid)+int(bidinc)),session['loggedin'],slug,)
        cur4.execute(query2, adr)
        mysql.connection.commit()
        return redirect("/")
    return redirect("/")

@app.route('/ebidincre/<eslug>/<bidinc>/<hbid>',methods=['GET','POST'])
def ebidincre(eslug,bidinc,hbid):
    if 'loggedin' in session:
        isLog = True

        cur4 = mysql.connection.cursor()
        query2 = "UPDATE ewaste SET hbid = %s,hbidder=%s WHERE eslug = %s"
        adr = ((int(hbid)+int(bidinc)),session['loggedin'],eslug,)
        cur4.execute(query2, adr)
        mysql.connection.commit()
        return redirect("/ewaste")
    return redirect("/ewaste")

@app.route('/mypro/<email>',methods=['GET','POST'])
def mypro(email):
 if 'loggedin' or 'loggedindoc' in session:
    isLog=True
    isLogDoc=True
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from buyer where email=%s", (session['loggedin'],))
    datablog = cur.fetchone()


    return render_template("profile.html",isLog=isLog,isLogDoc=isLogDoc,datablog=datablog)
 else:
    return redirect("/")


@app.route('/pay',methods=['GET','POST'])
def pay():
    if 'loggedin' in session:
        client = razorpay.Client(auth=("rzp_test_tjyjVaDuWJQOG1","4Tjf8OgwurENejpYcOP0ejgo"))
        payment=client.order.create({'amount':int(220000),'currency':'INR', 'payment_capture':'1'})



        return render_template("pay.html",payment=payment)

@app.route('/success',methods=['GET','POST'])
def success():
    return redirect("/")

@app.route('/winbid',methods=['GET','POST'])
def winbid():
    if 'loggedin' or 'loggedindoc' in session:
        isLog = True
        isLogDoc = True
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select * from buyer where email=%s", (session['loggedin'],))
        datablog = cur.fetchone()
        return render_template("winning-bids.html",isLog=isLog,isLogDoc=isLogDoc,datablog=datablog)

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if 'loggedinad' in session:
        isLogAdmin=True
        return redirect("/dashboard")
    else:
        isLogAdmin = False
        return render_template("adminlogin.html")
    return render_template("dashboard.html", params=params, isLogAdmin=isLogAdmin)

@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
        if 'loggedinad' in session:
            isLogAdmin=True

            cur1=mysql.connection.cursor()
            cur1.execute("select * from product")
            item=cur1.fetchall()

            curb = mysql.connection.cursor()
            curb.execute("select * from buyer")
            itemb = curb.fetchall()

            curs = mysql.connection.cursor()
            curs.execute("select * from seller")
            items = curs.fetchall()

            cur2 = mysql.connection.cursor()
            cur2.execute("select COUNT(*) FROM buyer")
            item1 = cur2.fetchone()
            cur3 = mysql.connection.cursor()
            cur3.execute("select COUNT(*) FROM seller")
            item2 = cur3.fetchone()
            cur4 = mysql.connection.cursor()
            cur4.execute("select COUNT(*) FROM product")
            item3 = cur4.fetchone()

            ispatient=True;
            return render_template("dashboard.html", isLogAdmin=isLogAdmin,ispatient=ispatient,item=item,item1=item1,item2=item2,item3=item3,itemb=itemb,items=items)
        if request.method == "POST":
         username = request.form.get("uname")
         userpass = request.form.get("pass")
         if (username == params["admin_user"] and userpass == params["admin_password"]):
            session['loggedinad'] = username
            isLogAdmin = True
            cur1 = mysql.connection.cursor()
            cur1.execute("select * from product")
            item = cur1.fetchall()

            curb = mysql.connection.cursor()
            curb.execute("select * from buyer")
            itemb = curb.fetchall()

            curs = mysql.connection.cursor()
            curs.execute("select * from seller")
            items = curs.fetchall()

            cur2 = mysql.connection.cursor()
            cur2.execute("select COUNT(*) FROM buyer")
            item1 = cur2.fetchone()
            cur3 = mysql.connection.cursor()
            cur3.execute("select COUNT(*) FROM seller")
            item2 = cur3.fetchone()
            cur4 = mysql.connection.cursor()
            cur4.execute("select COUNT(*) FROM product")
            item3 = cur4.fetchone()

            ispatient = True;
            return render_template("dashboard.html", isLogAdmin=isLogAdmin, ispatient=ispatient, item=item, item1=item1,
                                   item2=item2, item3=item3, itemb=itemb, items=items)
         else:
            isLogAdmin = False
            admsg="Incorrect Credentials"
            return render_template("adminlogin.html",params=params,isLogAdmin=isLogAdmin,admsg=admsg)

        return render_template("adminlogin.html")

@app.route('/adlogout')

def adlogout():
   session.pop('loggedinad')
   return redirect("/adminlogin")
if __name__ == '__main__':
    app.run(debug=True)

