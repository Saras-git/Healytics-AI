from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for, jsonify
import os
import base64
import cv2
import PIL.Image
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
import mysql.connector
import joblib
from flask_mail import Mail, Message
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="organ_donation"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
chatbot_df = pd.read_csv("chatbot_dataset.csv")

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(chatbot_df['question'])


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'projectbased2k26@gmail.com'
app.config['MAIL_PASSWORD'] = 'stsb nann lpnx sskg'
app.config['MAIL_DEFAULT_SENDER'] = 'projectbased2k26@gmail.com'

mail = Mail(app)
ai_model = joblib.load("organ_match_model.pkl")


def read_dataset():
    return pd.read_csv("data/dataset.csv")

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""

      
    #val="1"
    #v=val.rjust(4, "0")
    #print(v)
    return render_template('index.html',msg=msg,act=act)

@app.route('/login',methods=['POST','GET'])
def login():
    cnt=0
    act=""
    msg=""

    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM od_donor where donor_id=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        print(myresult)
        if myresult>0:
            session['username'] = username1
            ff=open("user.txt",'w')
            ff.write(username1)
            ff.close()
            result=" Your Logged in sucessfully**"
            return redirect(url_for('userhome')) 
        else:
            msg="Invalid Username or Password!"
            result="Your logged in fail!!!"
        

    return render_template('login.html',msg=msg,act=act)

@app.route('/login_admin',methods=['POST','GET'])
def login_admin():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM od_login where username=%s && password=%s && utype='admin'",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('admin')) 
        else:
            msg="Your logged in fail!!!"
        
    return render_template('login_admin.html',msg=msg,act=act)

@app.route('/login_opo',methods=['POST','GET'])
def login_opo():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM od_login where username=%s && password=%s && utype='opo'",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('opo_home')) 
        else:
            msg="Your logged in fail!!!"
        

    return render_template('login_opo.html',msg=msg,act=act)

@app.route('/login_hospital',methods=['POST','GET'])
def login_hospital():
    cnt=0
    act=""
    msg=""

    
    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM od_hospital where uname=%s && pass=%s && status=1",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            result=" Your Logged in sucessfully**"
            return redirect(url_for('hos_home')) 
        else:
            msg="Invalid Username or Password!"
            result="Your logged in fail!!!"
        

    return render_template('login_hospital.html',msg=msg,act=act)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    
    if request.method=='POST':
        hospital=request.form['hospital']
        
        address=request.form['address']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        

        mycursor.execute("SELECT count(*) FROM od_hospital where uname=%s",(uname,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM od_hospital")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO od_hospital(id,hospital,address,city,mobile,email,uname,pass,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,hospital,address,city,mobile,email,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"

            ###
            mycursor.execute('SELECT * FROM od_hospital WHERE uname=%s', (uname,))
            dd = mycursor.fetchone()
            dtime=str(dd[10])
            bdata="ID:"+str(maxid)+", Username:"+uname+", Status:Registered, Date: "+dtime
            ###
            
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='fail'
            
    
    return render_template('register.html', msg=msg,bc=bc,bdata=bdata)



@app.route('/admin')
def admin():
    mycursor = mydb.cursor()

    # =========================
    # HANDLE HOSPITAL APPROVAL
    # =========================
    act = request.args.get('act')
    hid = request.args.get('hid')

    if act == 'yes' and hid:
        # Update hospital status to approved (assuming status column is 'approved' or similar)
        mycursor.execute("UPDATE od_hospital SET status=1 WHERE id=%s", (hid,))
        mydb.commit()

    # =========================
    # HOSPITAL DATA (MISSING BEFORE)
    # =========================
    mycursor.execute("SELECT * FROM od_hospital")
    data = mycursor.fetchall()

    # =========================
    # BASIC COUNTS
    # =========================
    mycursor.execute("SELECT COUNT(*) FROM od_donor")
    total_donors = mycursor.fetchone()[0]

    mycursor.execute("""
        SELECT COUNT(*) FROM od_request
        WHERE status = 2 AND donor_id != '' AND trans_date IS NOT NULL
    """)
    successful_transplants = mycursor.fetchone()[0]

    mycursor.execute("""
        SELECT COUNT(*) FROM od_request WHERE status = 0
    """)
    pending_requests = mycursor.fetchone()[0]

    # =========================
    # 📈 MONTHLY TRANSPLANTS
    # =========================
    mycursor.execute("""
        SELECT DATE_FORMAT(trans_date, '%b') AS month, COUNT(*)
        FROM od_request
        WHERE status = 2 AND trans_date IS NOT NULL
        GROUP BY MONTH(trans_date)
        ORDER BY MONTH(trans_date)
    """)
    monthly_data = mycursor.fetchall()

    months = [row[0] for row in monthly_data]
    month_counts = [row[1] for row in monthly_data]

    # =========================
    # 🧠 AI MATCH ACCURACY
    # =========================
    mycursor.execute("SELECT COUNT(*) FROM od_request")
    total_requests = mycursor.fetchone()[0]

    mycursor.execute("SELECT COUNT(*) FROM od_request WHERE status = 2")
    accepted_requests = mycursor.fetchone()[0]

    ai_accuracy = round(
        (accepted_requests / total_requests) * 100, 2
    ) if total_requests > 0 else 0

    # =========================
    # 🏥 HOSPITAL-WISE TRANSPLANTS
    # =========================
    mycursor.execute("""
        SELECT hospital, COUNT(*)
        FROM od_request
        WHERE status = 2
        GROUP BY hospital
    """)
    hospital_data = mycursor.fetchall()

    hospitals = [row[0] for row in hospital_data]
    hospital_counts = [row[1] for row in hospital_data]

    return render_template(
        "admin.html",
        data=data,  # ✅ THIS WAS MISSING
        total_donors=total_donors,
        successful_transplants=successful_transplants,
        pending_requests=pending_requests,
        months=months,
        month_counts=month_counts,
        ai_accuracy=ai_accuracy,
        hospitals=hospitals,
        hospital_counts=hospital_counts
    )

@app.route('/process1')
def process1():


    df = read_dataset()

    # Hide decision columns in preview
    hide_cols = ['matched_status', 'matched_score']
    df_view = df.drop(columns=hide_cols, errors='ignore')

    df_view = df_view.head(20)

    data = df_view.values.tolist()
    columns = df_view.columns.tolist()

    return render_template(
        'process1.html',
        data=data,
        columns=columns
    )

@app.route('/process2')
def process2():


    df = read_dataset()

    # Remove target/decision columns
    hide_cols = ['matched_status', 'matched_score']
    df = df.drop(columns=hide_cols, errors='ignore')

    summary = []
    for col in df.columns:
        summary.append([
            col,
            int(df[col].count()),
            str(df[col].dtype)
        ])

    return render_template(
        'process2.html',
        summary=summary,
        rows=len(df),
        cols=len(df.columns)
    )

# -------- FEATURE GROUPS FOR ORGAN MATCHING -------- #

DONOR_FEATURES = [
    "donor_age", "donor_blood_group",
    "donor_organ", "donor_location"
]

RECIPIENT_FEATURES = [
    "recipient_age", "recipient_blood_group",
    "recipient_organ"
]

MATCH_FEATURES = [
    "urgency_level", "tissue_compatibility", "distance_km"
]

TARGETS = ["matched_status", "matched_score"]

@app.route('/process3')
def process3():


    return render_template(
        'process3.html',
        donor_features=DONOR_FEATURES,
        recipient_features=RECIPIENT_FEATURES,
        match_features=MATCH_FEATURES,
        targets=TARGETS
    )

@app.route('/process4')
def process4():


    df = read_dataset()

    # Show only important numeric features for ML
    selected_cols = [
        "donor_age", "recipient_age",
        "tissue_compatibility", "distance_km",
        "compatibility_score", "matched_status"
    ]

    df = df.head(100)

    data = df.values.tolist()
    columns = df.columns.tolist()

    return render_template(
        'process4.html',
        data=data,
        columns=columns
    )

@app.route('/process5')
def process5():


    df = read_dataset()

    # Create prediction-style column (simulating ML output)
    df["predicted_status"] = df["matched_status"]

    status_counts = df["predicted_status"].value_counts().to_dict()

    # Separate matched & unmatched samples (top 20 each)
    classified = {
        "Matched": df[df["predicted_status"] == "Matched"].head(20).to_dict(orient="records"),
        "Unmatched": df[df["predicted_status"] == "Unmatched"].head(20).to_dict(orient="records")
    }

    return render_template(
        "process5.html",
        status_labels=list(status_counts.keys()),
        status_values=list(status_counts.values()),
        classified=classified,
        columns=df.columns.tolist()
    )


@app.route('/hos_home', methods=['GET', 'POST'])
def hos_home():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM od_hospital where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    return render_template('hos_home.html',data=data,act=act)


@app.route('/hos_donor', methods=['GET', 'POST'])
def hos_donor():
    msg = ""
    act = ""
    
    # Optional: keep username for display/logging
    uname = session.get('username', '')

    mycursor = mydb.cursor()

    # Get all donors in the database
    mycursor.execute("SELECT * FROM od_donor")
    data = mycursor.fetchall()

    return render_template('hos_donor.html', data=data, act=act)


@app.route('/hos_pat', methods=['GET', 'POST'])
def hos_pat():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM od_hospital where uname=%s",(uname,))
    hdata = mycursor.fetchall()

    
    mycursor.execute("SELECT * FROM od_patient where hospital=%s",(uname,))
    data = mycursor.fetchall()

    
    return render_template('hos_pat.html',data=data,act=act)

@app.route('/add_donor', methods=['GET', 'POST'])
def add_donor():
    msg=""
    filename=""
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    email=""
    mess=""
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        aadhar=request.form['aadhar']
        pancard=request.form['pancard']
        guardian=request.form['guardian']
        mobile2=request.form['mobile2']
        blood_grp=request.form['blood_grp']
        organ=request.form.getlist('organ[]')

        og=",".join(organ)

        
        pass1="123456"

        mycursor.execute("SELECT count(*) FROM od_donor where aadhar=%s || pancard=%s || mobile=%s",(aadhar,pancard,mobile))
        myresult = mycursor.fetchone()[0]

        mycursor.execute("SELECT count(*) FROM od_patient where mobile=%s",(mobile,))
        myresult2 = mycursor.fetchone()[0]
        if myresult==0 and myresult2==0:
            mycursor.execute("SELECT max(id)+1 FROM od_donor")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                fname = file.filename
                filename = secure_filename(fname)
                photo="D"+str(maxid)+filename
                file.save(os.path.join("static/upload", photo))

            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            yy=rdate[6:10]
            val=str(maxid)
            v=val.rjust(4, "0")

            b1=dob.split('-')
            b2=b1[0]
            b3=int(yy)-int(b2)
            age=str(b3)
            regno="343000234"+str(maxid)
            
            donor_id="DN"+yy+v
            mess="Dear "+name+", Donor ID: "+donor_id+", Password: "+pass1+", Register by "+uname

            ######
            fn="C"+str(maxid)+".jpg"
            image = cv2.imread('static/img/ogcert.jpg',cv2.IMREAD_UNCHANGED)
            position = (300,172)
            cv2.putText(image, rdate, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
            cv2.imwrite("static/upload/"+fn, image)

            position = (632,172)
            cv2.putText(image, regno, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
            cv2.imwrite("static/upload/"+fn, image)

            position = (262,206)
            cv2.putText(image, name, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
            cv2.imwrite("static/upload/"+fn, image)

            position = (282,248)
            cv2.putText(image, age, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
            cv2.imwrite("static/upload/"+fn, image)

            position = (348,361)
            cv2.putText(image, og, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
            cv2.imwrite("static/upload/"+fn, image)

            position = (145,476)
            cv2.putText(image, blood_grp, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
            cv2.imwrite("static/upload/"+fn, image)

            position = (191,526)
            cv2.putText(image, aadhar, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
            cv2.imwrite("static/upload/"+fn, image)
            ######
            sql = "INSERT INTO od_donor(id,name,gender,dob,address,city,mobile,email,aadhar,pancard,guardian,mobile2,blood_grp,organ,photo,donor_id,pass,create_date,hospital) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,gender,dob,address,city,mobile,email,aadhar,pancard,guardian,mobile2,blood_grp,og,photo,donor_id,pass1,rdate,uname)
            mycursor.execute(sql, val)
            mydb.commit()
            
            print(mycursor.rowcount, "Registered Success")
            msg="success"

            ###
            mycursor.execute('SELECT * FROM od_donor WHERE donor_id=%s', (donor_id,))
            dd = mycursor.fetchone()
            dtime=str(dd[19])
            bdata="ID:"+str(maxid)+", Donor ID:"+donor_id+", Status: Donor-"+name+" by "+uname+", Donation: #"+og+"#, Date: "+dtime
            ###
        else:
            msg="fail"
        
       
    
    return render_template('add_donor.html', msg=msg,bc=bc,bdata=bdata,mess=mess,email=email)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    msg=""
    filename=""
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    email=""
    mess=""
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        aadhar=request.form['aadhar']
        
        guardian=request.form['guardian']
        mobile2=request.form['mobile2']
        blood_grp=request.form['blood_grp']
        

        mycursor.execute("SELECT count(*) FROM od_patient where aadhar=%s or mobile=%s",(aadhar,mobile))
        myresult = mycursor.fetchone()[0]

        mycursor.execute("SELECT count(*) FROM od_donor where mobile=%s",(mobile,))
        myresult2 = mycursor.fetchone()[0]
        if myresult==0 and myresult2==0:
            mycursor.execute("SELECT max(id)+1 FROM od_patient")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            yy=rdate[8:10]
            val=str(maxid)
            v=val.rjust(4, "0")
        
            pat_id="PT"+v
            mess="Dear "+name+", Patient ID: "+pat_id+", Register by "+uname
            
            sql = "INSERT INTO od_patient(id,name,gender,dob,address,city,mobile,email,aadhar,guardian,mobile2,blood_grp,patient_id,create_date,hospital) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,gender,dob,address,city,mobile,email,aadhar,guardian,mobile2,blood_grp,pat_id,rdate,uname)
            mycursor.execute(sql, val)
            mydb.commit()
            
            print(mycursor.rowcount, "Registered Success")
            msg="success"

            ###
            mycursor.execute('SELECT * FROM od_patient WHERE patient_id=%s', (pat_id,))
            dd = mycursor.fetchone()
            dtime=str(dd[15])
            bdata="ID:"+str(maxid)+", Patient ID:"+pat_id+", Status: Patient-"+name+" by "+uname+", Date: "+dtime
            ###
        else:
            msg="fail"
        
       
    
    return render_template('add_patient.html', msg=msg,bc=bc,bdata=bdata,mess=mess,email=email)


@app.route('/hos_pat_req', methods=['GET', 'POST'])
def hos_pat_req():
    msg=""
    act=""
    pid=request.args.get("pid")
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM od_hospital where uname=%s",(uname,))
    hdata = mycursor.fetchall()

    
    mycursor.execute("SELECT * FROM od_patient where id=%s",(pid,))
    data = mycursor.fetchone()
    pat_id=data[12]
    hospital=data[14]

    if request.method=='POST':
        organ=request.form['organ']

        # ✅ NEW: urgency level (added, nothing removed)
        urgency=request.form['urgency']

        mycursor.execute("SELECT max(id)+1 FROM od_request")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        # ✅ UPDATED: urgency column added (others unchanged)
        sql = """INSERT INTO od_request
                 (id,pat_id,hospital,organ,urgency,status,donor_id,trans_date)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

        val = (maxid,pat_id,hospital,organ,urgency,'0','','')
        mycursor.execute(sql, val)
        mydb.commit()

        ###
        mycursor.execute('SELECT * FROM od_request WHERE id=%s', (maxid,))
        dd = mycursor.fetchone()
        dtime=str(dd[7])
        bdata="ID:"+str(maxid)+", Patient ID:"+pat_id+", Status: Organ Require - "+organ+" ("+urgency+") by "+hospital+", Date: "+dtime
        ###
        msg="success"
        
        return redirect(url_for('organ_match', rid=maxid))
    
    return render_template(
        'hos_pat_req.html',
        msg=msg,
        data=data,
        act=act,
        pid=pid,
        bc=bc,
        bdata=bdata
    )

@app.route('/organ_match/<int:rid>')
def organ_match(rid):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM od_request WHERE id=%s", (rid,))
    req = mycursor.fetchone()
    organ_needed = req[3].lower()

    mycursor.execute("SELECT * FROM od_donor WHERE trans_st=0")
    donors = mycursor.fetchall()

    matched_donors = []

    for d in donors:
        donor_organs = [o.strip().lower() for o in d[13].split(',')]
        if organ_needed in donor_organs:
            matched_donors.append({
                "donor_id": d[15],
                "name": d[1],
                "age": datetime.datetime.now().year - int(d[3][:4]),
                "blood": d[12],
                "city": d[5]
            })

    return render_template(
        "organ_matched_donors.html",
        donors=matched_donors,
        rid=rid
    )

@app.route('/ai_match/<int:rid>')
def ai_match(rid):
    import numpy as np
    import joblib
    import random

    model = joblib.load("organ_match_model.pkl")
    le_urg = joblib.load("urgency_encoder.pkl")

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM od_request WHERE id=%s", (rid,))
    req = mycursor.fetchone()
    organ_needed = req[3].lower()
    urgency = req[4]

    mycursor.execute(
        "SELECT * FROM od_patient WHERE patient_id=%s",
        (req[1],)
    )
    pat = mycursor.fetchone()

    patient_age = datetime.datetime.now().year - int(pat[3][:4])
    patient_blood = pat[11]

    mycursor.execute("SELECT * FROM od_donor WHERE trans_st=0")
    donors = mycursor.fetchall()

    results = []

    for d in donors:
        donor_organs = [o.strip().lower() for o in d[13].split(',')]
        if organ_needed not in donor_organs:
            continue

        donor_age = datetime.datetime.now().year - int(d[3][:4])
        donor_blood = d[12]

        blood_match = 1 if donor_blood == patient_blood else 0
        organ_match = 1
        tissue_score = round(random.uniform(0.6, 1.0), 2)

        urgency_encoded = le_urg.transform([urgency])[0]

        features = np.array([[
            donor_age,
            patient_age,
            blood_match,
            organ_match,
            tissue_score,
            urgency_encoded
        ]])

        prob = model.predict_proba(features)[0][1]
        final_score = round(prob * 100, 2)

        results.append({
            "donor_id": d[15],
            "name": d[1],
            "email": d[7],
            "mobile": d[8],  # assuming mobile is in column 8
            "blood": donor_blood,
            "ai_score": final_score,
            "confidence": "High" if final_score > 80 else "Medium" if final_score > 50 else "Low"
        })

    results.sort(key=lambda x: x['ai_score'], reverse=True)

    return render_template(
        "ai_results.html",
        donors=results,
        rid=rid
    )




@app.route('/confirm_donor/<int:rid>/<donor_id>')
def confirm_donor(rid, donor_id):
    mycursor = mydb.cursor()

    # Update request with selected donor
    mycursor.execute("""
        UPDATE od_request
        SET donor_id=%s, status='1'
        WHERE id=%s
    """, (donor_id, rid))
    mydb.commit()

    # Get donor email
    mycursor.execute(
        "SELECT email FROM od_donor WHERE donor_id=%s",
        (donor_id,)
    )
    donor_email = mycursor.fetchone()[0]

    # Send email to donor
    msg = Message(
        subject="Organ Donation Request Confirmation",
        recipients=[donor_email]
    )

    msg.body = f"""
Dear Donor,

You have been selected by our AI system for an organ donation request.

Please confirm your availability by clicking below:

http://127.0.0.1:5000/donor_action/{rid}/{donor_id}

Thank you for saving lives.
"""
    mail.send(msg)

    # Redirect back to AI match page
    return render_template(
        'confirm_success.html',
        rid=rid,
        donor_id=donor_id
    )


@app.route('/donor_action/<int:rid>/<donor_id>', methods=['GET', 'POST'])
def donor_action(rid, donor_id):
    mycursor = mydb.cursor()

    if request.method == 'POST':
        action = request.form['action']

        if action == 'accept':
            mycursor.execute("""
                UPDATE od_request
                SET status=2,
                    donor_id=%s,
                    trans_date=CURDATE()
                WHERE id=%s
            """, (donor_id, rid))
            status_text = "ACCEPTED"
        else:
            mycursor.execute("""
                UPDATE od_request
                SET status=3
                WHERE id=%s
            """, (rid,))
            status_text = "REJECTED"

        mydb.commit()

        # fetch hospital email
        mycursor.execute("""
            SELECT h.email
            FROM od_request r
            JOIN od_hospital h ON r.hospital = h.uname
            WHERE r.id=%s
        """, (rid,))
        hospital_email = mycursor.fetchone()[0]

        # send mail ONLY if accepted
        if status_text == "ACCEPTED":
            msg = Message(
                subject="Organ Donation Accepted",
                recipients=[hospital_email]
            )
            msg.body = f"""
Donor {donor_id} has ACCEPTED the organ donation request.

Request ID : {rid}
Organ      : Confirmed
Status     : Ready for transplant

Please login to hospital dashboard for further action.
"""
            mail.send(msg)

        return render_template('donor_result.html', status=status_text)

    return render_template('donor_action.html', rid=rid, donor_id=donor_id)

@app.route('/donor_match/<donor_id>')
def donor_match(donor_id):
    import numpy as np
    import joblib
    import random
    import datetime

    model = joblib.load("organ_match_model.pkl")
    le_urg = joblib.load("urgency_encoder.pkl")

    mycursor = mydb.cursor()

    # Get logged-in hospital
    uname = session.get('username')

    # Get donor info
    mycursor.execute("SELECT * FROM od_donor WHERE donor_id=%s", (donor_id,))
    donor = mycursor.fetchone()
    donor_organs = [o.strip().lower() for o in donor[13].split(',')]
    donor_age = datetime.datetime.now().year - int(donor[3][:4])
    donor_blood = donor[12]

    # Get all patient requests for donor's organs and this hospital
    placeholders = ','.join(['%s']*len(donor_organs))
    sql = f"""SELECT * FROM od_request 
              WHERE organ IN ({placeholders}) 
              AND status='0'
              AND hospital=%s"""
    mycursor.execute(sql, donor_organs + [uname])
    requests = mycursor.fetchall()

    results = []
    seen_patients = {}  # patient_id -> highest score result

    for req in requests:
        pat_id = req[1]

        # Patient info
        mycursor.execute("SELECT * FROM od_patient WHERE patient_id=%s", (pat_id,))
        pat = mycursor.fetchone()
        if not pat:
            continue

        patient_age = datetime.datetime.now().year - int(pat[3][:4])
        patient_blood = pat[11]
        organ_needed = req[3].lower()
        urgency = req[4]

        blood_match = 1 if donor_blood == patient_blood else 0
        organ_match = 1
        tissue_score = round(random.uniform(0.6, 1.0), 2)
        urgency_encoded = le_urg.transform([urgency])[0]

        features = np.array([[donor_age, patient_age, blood_match, organ_match, tissue_score, urgency_encoded]])
        prob = model.predict_proba(features)[0][1]
        final_score = round(prob*100, 2)

        result = {
            "req_id": req[0],
            "pat_id": pat_id,
            "patient_id": pat[15],  # Patient ID column
            "name": pat[1],
            "age": patient_age,
            "blood": patient_blood,
            "organ": organ_needed,
            "urgency": urgency,
            "ai_score": final_score,
            "confidence": "High" if final_score > 80 else "Medium" if final_score > 50 else "Low"
        }

        # Keep only the highest score per patient
        if pat_id not in seen_patients or final_score > seen_patients[pat_id]['ai_score']:
            seen_patients[pat_id] = result

    # Convert dict to list and sort by AI score descending
    results = list(seen_patients.values())
    results.sort(key=lambda x: x['ai_score'], reverse=True)

    return render_template("donor_ai_results.html", donor=donor, results=results)



@app.route('/confirm_patient/<int:rid>/<donor_id>')
def confirm_patient(rid, donor_id):
    mycursor = mydb.cursor()
    
    # Update request with donor selection
    mycursor.execute("""
        UPDATE od_request
        SET donor_id=%s, status='1'
        WHERE id=%s
    """, (donor_id, rid))
    mydb.commit()

    # Optional: Send email to patient
    mycursor.execute("SELECT email, name FROM od_patient WHERE patient_id=(SELECT pat_id FROM od_request WHERE id=%s)", (rid,))
    pat = mycursor.fetchone()
    patient_email = pat[0]
    patient_name = pat[1]

    msg = Message(
        subject="Organ Donation Confirmed",
        recipients=[patient_email]
    )
    msg.body = f"""
Dear {patient_name},

You have been matched with a donor for your organ request.

Donor ID: {donor_id}

Please contact the hospital for further steps.
"""
    mail.send(msg)

    return render_template('confirm_success.html', rid=rid, donor_id=donor_id)


@app.route('/hos_pat_check', methods=['GET', 'POST'])
def hos_pat_check():
    msg=""
    act=""
    ss=""
    pid=request.args.get("pid")
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM od_hospital where uname=%s",(uname,))
    hdata = mycursor.fetchall()

    
    mycursor.execute("SELECT * FROM od_patient where id=%s",(pid,))
    data = mycursor.fetchone()
    pat_id=data[12]
    hospital=data[14]

    if request.method=='POST':
        status=request.form['status']

        mycursor.execute("update od_patient set status=%s where id=%s",(status,pid))
        mydb.commit()
        ###
        if status=="1":
            ss="Treatment Going on"
        elif status=="2":
            ss="Near by Death"
        elif status=="3":
            ss="Died"
        elif status=="4":
            ss="Cured"

        mycursor.execute("SELECT * FROM od_patient where id=%s",(pid,))
        d3 = mycursor.fetchone()
        dtime=str(d3[15])
        bdata="ID:"+pid+", Patient ID:"+pat_id+", Status: "+ss+" by "+hospital+", Date: "+dtime
        ###
        msg="success"

    
    return render_template('hos_pat_check.html',msg=msg,data=data,act=act,pid=pid,bc=bc,bdata=bdata)

@app.route('/hos_verify', methods=['GET', 'POST'])
def hos_verify():
    msg=""
    act=request.args.get("act")
    st=""
    st1=""
    rs=[]
    data2=[]
    pid=request.args.get("pid")
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM od_hospital where uname=%s",(uname,))
    hdata = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM od_patient where id=%s",(pid,))
    data = mycursor.fetchone()
    pat_id=data[12]
    hospital=data[14]
    aadhar=data[8]

    mycursor.execute("SELECT count(*) FROM od_donor where aadhar=%s",(aadhar,))
    c1 = mycursor.fetchone()[0]

    if c1>0:
        st="1"
        mycursor.execute("SELECT * FROM od_donor where aadhar=%s",(aadhar,))
        rs = mycursor.fetchone()
        donor_id=rs[15]
        mycursor.execute("SELECT count(*) FROM od_agreement where donor_id=%s",(donor_id,))
        ds1 = mycursor.fetchone()[0]
        if ds1>0:
            st1="1"
            mycursor.execute("SELECT * FROM od_agreement where donor_id=%s",(donor_id,))
            data2 = mycursor.fetchone()
        
    else:
        st="2"

    if act=="trans":
        did=request.args.get("did")
        mycursor.execute("update od_donor set trans_st=1 where id=%s",(did,))
        mydb.commit()
        
        mycursor.execute("SELECT * FROM od_donor where id=%s",(did,))
        d2 = mycursor.fetchone()
        donor_id=d2[15]
        dtime=str(d2[19])
        bdata="ID:"+did+", Patient ID:"+pat_id+", Status: Donor ID: "+donor_id+", Organ transplant to OPTN by "+hospital+", Date: "+dtime
        msg="success"
    
    return render_template('hos_verify.html',msg=msg,data=data,act=act,pid=pid,bc=bc,bdata=bdata,st=st,st1=st1,rs=rs,data2=data2)


@app.route('/hos_req', methods=['GET', 'POST'])
def hos_req():
    msg=""
    act=""
    st=""
    rs=[]
    data2=[]
    pid=request.args.get("pid")
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM od_hospital where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM od_request where status=0")
    data1 = mycursor.fetchall()

    return render_template('hos_req.html',msg=msg,data=data,data1=data1)

@app.route('/hos_optn', methods=['GET', 'POST'])
def hos_optn():
    msg=""
    act=""
    st=""
    rs=[]
    data2=[]
    rid=request.args.get("rid")
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM od_hospital where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM od_donor where trans_st=0")
    data1 = mycursor.fetchall()
    

    return render_template('hos_optn.html',msg=msg,data=data,data1=data1,rid=rid)

@app.route('/hos_receive', methods=['GET', 'POST'])
def hos_receive():
    msg=""
    act=""
    st=""
    rs=[]
    data2=[]
    rid=request.args.get("rid")
    did=request.args.get("did")
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM od_hospital where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM od_donor where trans_st=1")
    data1 = mycursor.fetchall()

    now = date.today() #datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
            
    if request.method=='POST':
        pat_id=request.form['pat_id']
        
        mycursor.execute("SELECT * FROM od_donor where id=%s",(did,))
        dd1 = mycursor.fetchone()
        donorid=dd1[15]

        mycursor.execute("update od_donor set trans_st=1 where donor_id=%s",(donorid,))
        mydb.commit()
    
        mycursor.execute("update od_request set status=1,donor_id=%s,trans_date=%s where id=%s",(donorid,rdate,rid))
        mydb.commit()
        
        mycursor.execute("SELECT * FROM od_donor where id=%s",(did,))
        d2 = mycursor.fetchone()
        donor_id=d2[15]
        dtime=str(d2[19])
        bdata="ID:"+did+", Patient ID:"+pat_id+", Status: Donor ID: "+donor_id+", Organ transplanted, by "+uname+", Date: "+dtime
        msg="success"

    return render_template('hos_receive.html',msg=msg,data=data,data1=data1,bc=bc,bdata=bdata)


@app.route('/hos_trans')
def hos_trans():
    if 'username' not in session:
        return redirect('/login')

    uname = session['username']
    mycursor = mydb.cursor()

    # hospital info
    mycursor.execute(
        "SELECT * FROM od_hospital WHERE uname=%s",
        (uname,)
    )
    data = mycursor.fetchone()

    # transplanted organs (status = 2)
    mycursor.execute("""
        SELECT *
        FROM od_request
        WHERE hospital=%s AND status=2
        ORDER BY trans_date DESC
    """, (uname,))
    data1 = mycursor.fetchall()

    return render_template(
        'hos_trans.html',
        data=data,
        data1=data1
    )



@app.route('/opo_home', methods=['GET', 'POST'])
def opo_home():
    msg=""
    act=""
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    uname=""
    hdata=[]
    st=""
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    

    if request.method=='POST':
        donor_id=request.form['donor_id']

        mycursor.execute("SELECT count(*) FROM od_donor where donor_id=%s",(donor_id,))
        cnt = mycursor.fetchone()[0]

        if cnt>0:
            st="1"
            mycursor.execute("SELECT * FROM od_donor where donor_id=%s",(donor_id,))
            hdata = mycursor.fetchone()

        else:
            st="2"

        

       

    
    return render_template('opo_home.html',msg=msg,act=act,bc=bc,bdata=bdata,rs=hdata,st=st)

@app.route('/opo_view', methods=['GET', 'POST'])
def opo_view():
    msg=""
    act=""
    donor=request.args.get("donor")
    data=[]
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    uname=""
    hdata=[]
    st=""
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT count(*) FROM od_agreement where donor_id=%s",(donor,))
    cn = mycursor.fetchone()[0]

    if cn>0:
        st="1"
        mycursor.execute("SELECT * FROM od_agreement where donor_id=%s",(donor,))
        data = mycursor.fetchone()
    
    return render_template('opo_view.html',msg=msg,act=act,data=data,st=st)


@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    act=""
    st=""
    data=[]
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM od_donor where donor_id=%s",(uname, ))
    rs = mycursor.fetchone()

    mycursor.execute("SELECT count(*) FROM od_agreement where donor_id=%s",(uname,))
    cn = mycursor.fetchone()[0]

    if cn>0:
        st="1"
        mycursor.execute("SELECT * FROM od_agreement where donor_id=%s",(uname,))
        data = mycursor.fetchone()
    
    return render_template('userhome.html',rs=rs,act=act,data=data,st=st)

@app.route('/add_proof', methods=['GET', 'POST'])
def add_proof():
    msg=""
    filename=""
    bdata=""
    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    email=""
    mess=""
    act=request.args.get("act")
    did=request.args.get("did")
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM od_donor where id=%s",(did, ))
    data = mycursor.fetchone()
    donor_id=data[15]

    if request.method=='POST':
        name1=request.form['name1']
        relation1=request.form['relation1']

        name2=request.form['name2']
        relation2=request.form['relation2']
        


        mycursor.execute("SELECT max(id)+1 FROM od_agreement")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        file1 = request.files['file1']
        file2 = request.files['file2']
        file3 = request.files['file3']
        file4 = request.files['file4']
        
        f1 = file1.filename
        ff1 = secure_filename(f1)
        proof1="P1"+str(did)+ff1
        file1.save(os.path.join("static/upload", proof1))

        f2 = file2.filename
        ff2 = secure_filename(f2)
        sign1="S1"+str(did)+ff2
        file2.save(os.path.join("static/upload", sign1))

        f3 = file3.filename
        ff3 = secure_filename(f3)
        proof2="P2"+str(did)+ff3
        file3.save(os.path.join("static/upload", proof2))
        
        f4 = file4.filename
        ff4 = secure_filename(f4)
        sign2="S2"+str(did)+ff4
        file4.save(os.path.join("static/upload", sign2))

        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        
        sql = "INSERT INTO od_agreement(id,donor_id,name1,proof1,sign1,name2,proof2,sign2,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,donor_id,name1,proof1,sign1,name2,proof2,sign2,rdate)
        mycursor.execute(sql, val)
        mydb.commit()
        
        print(mycursor.rowcount, "Registered Success")
        msg="success"

        ###
        mycursor.execute('SELECT * FROM od_agreement WHERE donor_id=%s', (donor_id,))
        dd = mycursor.fetchone()
        dtime=str(dd[9])
        bdata="ID:"+str(maxid)+", Donor ID:"+donor_id+", Status: Agreement by OPO, Date: "+dtime
        ###
  
    
    return render_template('add_proof.html', msg=msg,bc=bc,bdata=bdata)

@app.route('/cus_img', methods=['GET', 'POST'])
def cus_img():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_customer where uname=%s",(uname,))
    data = mycursor.fetchone()
    ptype=data[5]
    aid=data[0]

    if request.method=='POST':
        
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            photo="C"+str(aid)+filename
            file.save(os.path.join("static/upload", photo))
            mycursor.execute("update cc_customer set photo=%s where uname=%s",(photo,uname))
            mydb.commit()
            msg="success"
        
    return render_template('cus_img.html',data=data,msg=msg)

@app.route('/verify_donor', methods=['GET', 'POST'])
def verify_donor():
    msg=""
    cnt=0
    uname=""
    mess=""
    act=request.args.get("act")
    st=""
    pmode=""
    if 'username' in session:
        uname = session['username']
    #uname="raj"
    mycursor = mydb.cursor()
    #mycursor.execute("SELECT * FROM ds_register where uname=%s",(uname,))
    #data = mycursor.fetchone()
    #vid=data[0]
    key="xyz123"
    
    return render_template('verify_donor.html',msg=msg,mess=mess,act=act,uname=uname,key=key)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text.strip()

def chatbot_response(user_input):
    if not user_input:
        return "Please type a message 😊"

    user_input = clean_text(user_input)

    # ✅ Greetings (rule-based)
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    if user_input in greetings:
        return "Hello 👋 I am your AI Organ Donation Assistant. How can I help you?"

    # ✅ Intent rule (prevents mismatch)
    if "become" in user_input and "donor" in user_input:
        return "You can become an organ donor by registering at a government hospital or official organ donation portal."

    # ✅ TF-IDF similarity
    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, X)

    best_match = similarity.argmax()
    confidence = similarity[0][best_match]

    # ✅ Confidence threshold
    if confidence < 0.25:
        return (
            "Sorry, I couldn't understand that clearly 🤔\n"
            "You can ask about:\n"
            "• Organ donation process\n"
            "• Eligibility to donate\n"
            "• Patient or donor request status"
        )

    return chatbot_df.iloc[best_match]["answer"]

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()

    # Safety check
    if not data or "message" not in data:
        return jsonify({"reply": "Please send a valid message."})

    user_msg = data.get("message")
    reply = chatbot_response(user_msg)

    return jsonify({"reply": reply})

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
