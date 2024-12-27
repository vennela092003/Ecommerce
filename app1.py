from flask import Flask,render_template,request,flash,url_for,redirect,session
import mysql.connector
from otp import genotp
from cmail import sendmail
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='ecom1'
)
app1=Flask(__name__)
app1.secret_key='aabbccdd'
@app1.route('/')
def base():
    return render_template('homepage.html')
@app1.route('/admit_signup',methods=['GET','POST'])
def admit_signup():
    if request.method=="POST":
        admit_name=request.form['admit_name']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute("select email from admitsignup")
        data=cursor.fetchall()
        cursor.execute('select mobile from admitsignup')
        edata=cursor.fetchall()
        if(mobile,) in edata:
            flash("admit already exist")
            return render_template('signup.html')
        if(email,) in data:
            flash("Email address already exists")
            return render_template('signup.html')
        cursor.close()
        otp=genotp()
        subject="thanks for registering to the application"
        body=f'use this otp to admitsignup {otp}'
        sendmail(email,subject,body)
        return render_template('admitotp.html',otp=otp,admit_name=admit_name,mobile=mobile,email=email,address=address,password=password)
    else:
        return render_template('signup.html')
@app1.route('/admitotp/<otp>/<admit_name>/<mobile>/<email>/<address>/<password>',methods=['GET','POST'])
def admitotp(otp,admit_name,mobile,email,address,password):
    if request.method=="POST":
        uotp=request.form['otp']
        if otp==uotp:
            cursor=mydb.cursor()
            lst=[admit_name,mobile,email,address,password]
            query='insert into admitsignup values(%s,%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mydb.commit()
            cursor.close()
            flash('Details signuped')
            return redirect(url_for('login'))
        else:
            flash('Wrong otp')
            return render_template('admitotp.html',otp=otp,admit_name=admit_name,mobile=mobile,email=email,address=address,password=password)
@app1.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        admitname=request.form['admit_name']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select count(*) from admitsignup where admit_name=%s and password=%s',[admitname,password])
        count=cursor.fetchone()[0]
        print(count)
        if count==0:
            flash("Invaild email or password")
            return render_template('admitlogin.html')
        else:
            session['admit']=admitname
            if not session.get(admitname):
                session[admitname]={}
            return redirect(url_for('base'))
    return render_template('admitlogin.html')
@app1.route('/logout')
def logout():
    if session.get('admit'):
        session.pop('admit')
        return redirect(url_for('base'))
    else:
        flash("already logged out!")
        return redirect(url_for('login'))

app1.run(debug=True)