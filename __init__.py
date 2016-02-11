from flask import Flask, render_template, url_for, redirect, request, flash
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from MySQLdb import escape_string as thwart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


import gc, csv, smtplib, ssl, os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:yourSQLdb@localhost/students'
db = SQLAlchemy(app)



class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String(80), unique=False)
    school = db.Column(db.String(80), unique=False)
    instructor = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), unique=False)
    submit_time = db.Column(db.DateTime)
    #submit_time = db.Column(db.DateTime(timezone=True), default=datetime.now())
    
    def __init__(self, student, school, instructor, email, submit_time=None):
        self.student = student
        self.school = school
        self.instructor = instructor
        self.email = email
        if submit_time is None:
            submit_time = datetime.utcnow()
        self.submit_time = submit_time
        
    def __repr__(self):
        return '<Student: %r>' % self.student


class FormInfo(Form):
    name = StringField('name')
    school = SelectField(u'School', choices=[('', 'Please select...'),
        ('ISU', 'Illinois State University'),
        ('FSU', 'Florida State University'),
        ('USA', 'University of South Alabama'),
        ('MHU', 'Mercyhurst University')])
    instructor = StringField('instructor')
    email = StringField('email')


@app.route("/", methods=['POST', 'GET'])
def home_page():
    form = FormInfo()

    name = None
    school = None
    instructor = None
    now = None
    email = None
    
    if request.method == "POST" and request.form['name']:
        name = thwart(request.form['name'])
        school = thwart(request.form['school'])
        instructor = thwart(request.form['instructor'])
        email = thwart(request.form['email'])
        now = str(datetime.utcnow())
        
        dbq = Student.query.all()
        for item in dbq:
            if name == item.student and school == item.school:
                name = None
                school = None
                instructor = None
                now = None
                email = None
                return(render_template("main.html", name_warning="Name already on file. Thanks!", form=form))
        
        current_student = Student(name, school, instructor, email, now)
        if name != None:
            db.session.add(current_student)
            db.session.commit()

        gc.collect()
        
        return(render_template('thanks.html', name=name))

    name = None
    school = None
    instructor = None
    now = None
    email = None
    
    return(render_template("main.html", form=form))

@app.route("/getoutput", methods=['POST', 'GET'])
def get_output():

    filepath = os.getcwdu() + "/FlaskApp/FlaskApp/data/names.csv"

    print str(filepath)

    if request.method == "POST" and request.form['pw'] == "passwordForDBpull":

        dbq = Student.query.all()

        try:
    
            with open(filepath, 'w') as csvfile:
                headers = ['id', 'Student Name', 'School', 'Instructor', 'Email', 'Time(UTC)']
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                
                writer.writeheader()
                for item in dbq:
                     writer.writerow({'id': item.id,
                                      'Student Name': item.student,
                                      'School': item.school,
                                      'Instructor': item.instructor,
                                      'Email': item.email,
                                      'Time(UTC)': item.submit_time })

        except Exception as e:

            return str(e)

        fromaddr = 'sendingGmailAddress@gmail.com'
        toaddrs = 'receivingGmailAddress@gmail.com'
        
        msg = MIMEMultipart()
        msg['Subject'] = "CSV pull from web app run at: " + str(datetime.now())
        msg['From'] = "sendingGmailAddress@gmail.com"

        #msg = "CSV requested at " + str(datetime.now())

        try:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(filepath, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename=names.csv')
            msg.attach(part)

        except Exception as e:

            return str(e)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login('sendingGmailAddress@gmail.com','GmailPassword')
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()
    
        #os.remove(filepath)
    
        return(render_template("output.html",pw_warning="Please check your email"))

    elif request.method == "POST" and request.form['pw'] != "passwordForDBpull":

        return(render_template("output.html",pw_warning="Incorrect Password"))

    else:

	    return(render_template("output.html"))
	
	
if __name__ == "__main__":
	app.debug = True
	app.run()
