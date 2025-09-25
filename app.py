from flask import Flask,render_template,request,session,redirect,jsonify
from pymongo import MongoClient
from bson import ObjectId
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json


cluster=MongoClient("mongodb://127.0.0.1:27017")
db=cluster['traveler']
users=db['users']
travel=db['travel']
hotels=db['hotels']


app=Flask(__name__)
app.secret_key='500000'

@app.route('/')
def land():
    return render_template('land.html')

@app.route('/uhome')    
def uhome():
    return render_template('index.html')

@app.route('/ahome')
def ahome():
    return render_template('adminhome.html')

@app.route('/admin')
def admin():
    return render_template('adminlogin.html')

@app.route('/events')
def events():
    return render_template('localevents.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/locations')
def get_locations():
    with open('data.json') as f:
        locations_data = json.loads(f.read())
    return jsonify(locations_data)


@app.route('/log')
def log():
    return render_template('login.html')

@app.route('/reg')
def regis():
    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/travel')
def travel1():
    return render_template('travel.html')

@app.route('/adminlogin',methods=['post','get'])
def login1():
    user=request.form['username']
    password=request.form['password']
    if user=='admin' and password=='1234567890':
        return render_template('adminhome.html')
    else:
        return render_template('adminlogin.html',status='User does not exist or wrong password')

@app.route('/travelbook',methods=['post','get'])
def travelbook():
    name=session['name']
    from1=request.form['from']
    to=request.form['to']
    date=request.form['date']
    time=request.form['time']
    clas=request.form['class']
    passengers=request.form['passengers']
    vehicle=request.form['vehicle']
    data=users.find_one({"username":session['name']})['mail']
    travel.insert_one({"name":name,"from":from1,"to":to,"date":date,"time":time,"email":data,"class":clas,"passengers":passengers,"vehicle":vehicle})
    return render_template('travel.html',status="Booking successful")

@app.route('/hotelbook',methods=['post','get'])
def hotelbook():
    name=session['name']
    state=request.form['state']
    city=request.form['city']
    place=request.form['place']
    rt=request.form['room-type']
    ci=request.form['check-in']
    co=request.form['check-out']
    guests=request.form['guests']
    data=users.find_one({"username":session['name']})['mail']
    hotels.insert_one({"name":name,"state":state,"city":city,"place":place,"email":data,"room":rt,"ci":ci,"co":co,"guests":guests})
    return render_template('hotel.html',status="Booking successful")


@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/register',methods=['post','get'])
def register():
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
    confirmpass=request.form['cpassword']
    k={}
    k['username']=username
    k['mail']=email
    k['password']=password 
    res=users.find_one({"username":username})
    mail=users.find_one({"email":email})
    if res:
        return render_template('register.html',status="Username already exists")
    else:
        if mail:
            return render_template('register.html',status='Email already exists')
        elif password != confirmpass:
            return render_template('register.html',status='Passwords do not match')
        elif len(password)<8:
            return render_template('register.html',status="Password must be greater than 7 characters")
        else:
            users.insert_one(k)
            return render_template('register.html',stat="Registration successful")

@app.route('/login',methods=['post','get'])
def login():
    user=request.form['username']
    password=request.form['password']
    res=users.find_one({"username":user})
    if res and dict(res)['password']==password:
        session['name']=user
        return redirect('/index')
    else:
        return render_template('login.html',status='User does not exist or wrong password')


@app.route('/hb')
def hb():
    return render_template('hotel.html')

@app.route('/tb')
def tb():
    return render_template('travel.html')

@app.route('/hbs')
def hbs():
    data=hotels.find()
    return render_template('hotelbookings.html',data=data)

@app.route('/tbs')
def tbs():
    data=travel.find()
    return render_template('travelbookings.html',res=data)

@app.route('/mybookings')
def mybookings():
    data=hotels.find({"name":session['name']})
    res=travel.find({"name":session['name']})
    return render_template('mybookings.html',data=data,res=res)

@app.route('/hdelete')
def hdelete():
    id=request.args.get('id')
    hotels.delete_one({"_id":ObjectId(id)})
    data=hotels.find({"name":session['name']})
    res=travel.find({"name":session['name']})
    return render_template('mybookings.html',data=data,res=res)

@app.route('/tdelete')
def tdelete():
    id=request.args.get('id')
    travel.delete_one({"_id":ObjectId(id)})
    data=hotels.find({"name":session['name']})
    res=travel.find({"name":session['name']})
    return render_template('mybookings.html',data=data,res=res)

@app.route('/traveldelete')
def tdel():
    id=request.args.get('id')
    travel.delete_one({"_id":ObjectId(id)})
    data=travel.find()
    return render_template('travelbookings.html',res=data)

@app.route('/hoteldelete')
def hdel():
    id=request.args.get('id')
    hotels.delete_one({"_id":ObjectId(id)})
    data=hotels.find()
    return render_template('hotelbookings.html',data=data)

@app.route('/Accept')
def accept():
    tid = request.args.get('tid')
    hid = request.args.get('hid')
    if(tid):
        data = travel.find_one({"_id":ObjectId(tid)})
        send_email(f"your Travel booking from {data['from']} to {data['to']} on {data['date']} in {data['vehicle']} for {data['passengers']} passengers is BOOKED successfully",data['email'])
        return redirect('traveldelete?id='+tid)
    elif(hid):
        data = hotels.find_one({"_id":ObjectId(hid)})
        send_email(f"Your Hotel booking request at {data['place']},{data['city']}, {data['state']} for {data['room']} Room is booked Successfully",data['email'])
        return redirect('/hoteldelete?id='+hid)

@app.route('/Deny')
def deny():
    tid = request.args.get('tid')
    hid = request.args.get('hid')
    if(tid):
        data = travel.find_one({"_id":ObjectId(tid)})
        send_email(f"your Travel booking from {data['from']} to {data['to']} on {data['date']} in {data['vehicle']} for {data['passengers']} passengers is Rejected",data['email'])
        return redirect('traveldelete?id='+tid)
    elif(hid):
        data = hotels.find_one({"_id":ObjectId(hid)})
        send_email(f"Your Hotel booking request at {data['place']},{data['city']}, {data['state']} for {data['room']} Room is Rejected",data['email'])
        return redirect('/hoteldelete?id='+hid)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

def send_email(msg,mail):
    # Email configuration
    r_email = 'bomma.chiru@gmail.com'  # Change this to your email address
    s_email = mail  # Change this to the recipient's email address
    password = 'cxds xnfo vkha qmlo'  # Change this to your email password

    message = MIMEMultipart("alternative")
    message["Subject"] = "Travel Planner"
    message["From"] = r_email
    message["To"] = s_email

    # Email content
    html = f"<p> {msg} </p>"

    part2 = MIMEText(html, "html")

    message.attach(part2)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(r_email, password)
        server.sendmail(r_email, s_email, message.as_string())


if __name__=="__main__":
    app.run(debug=True)
