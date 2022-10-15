
from distutils.log import debug
from email import message


from flask import Flask,redirect, render_template,request,redirect,url_for
import pymysql
import requests, re

# route to bind url to function

loginpage=Flask(__name__) #app=Flask(__name__) Constructor

con=None
cur=None



user_api = '6ab876d4179e96cd71abb0bdac048333' 


def connectDb():
    global con,cur,cur,data
    con=pymysql.connect(host='localhost',user='root',password='rds@king',database='py_project')
    cur=con.cursor()

def closeDb():
    cur.close()
    con.close()
    
def getAllWeatherData(city,temp,humidity,wind_speed,descr,visibility,temp_max,temp_min):
    global data
    connectDb()
    selectquery = "select * from weather2 order by times desc limit 7;"
    cur.execute(selectquery)
    data = cur.fetchall()
    insertQuery = 'insert into weather2 values (curdate(),"{}",{},{},{},"{}",{},{},{},CURRENT_TIME());'.format(city,temp,humidity,wind_speed,descr,visibility,temp_max,temp_min)
    cur.execute(insertQuery)
   
    con.commit()
    return data
    


                   # Small Programme For Testing Purpose only

# @loginpage.route('/input',methods=['GET','POST'])
# def login():
#     msg=''
#     msg2=''
#     if request.method == 'POST':
#         global a,b
#         global temp,humidity,wind_speed,descr,visibility,temp_max,temp_min,city

     
#         city =(request.form['city'])
      
#         x=str(city)
        
#         url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(x,user_api)
#         r = requests.get(url)
#         api_data = r.json()
   
#         temp = ((api_data['main']['temp']) - 273.15)
#         temp=round(temp,4)
#         humidity = api_data['main']['humidity']
#         wind_speed = api_data['wind']['speed']
#         descr = api_data['weather'][0]['description']
#         visibility=api_data['visibility']
#         temp_max=api_data['main']['temp_max']
#         temp_min=api_data['main']['temp_min']
#         city=api_data['name']
#         msg='temp:-{}, humidity:-{}, Wind seppd:= {},desc :- "{}",visibility:- {}, max:- {},min:- {}'.format(temp,humidity,wind_speed,descr,visibility,temp_max,temp_min)
        
#         msg2="temp    {}  descr       {}".format(temp,descr)

#     return render_template('input.html',msg=msg,msg2=msg2)


@loginpage.route("/") # Bind a function to an URL path Using - app.route decoder
def demo():
    return render_template('profile.html')

@loginpage.route('/Register',methods=['GET','POST'])
def Register():
    msg=''
    if request.method=='POST':
        value=request.form
        ID=value['id']
        NAME=value['name']
        EMAIL=value['email_id']
        MOBILENO=value['mobileNo']
        PASSWORD=value['password']
        connectDb()
        cur.execute("select * from weather_ID where ID ={}".format(ID))
        status=cur.fetchone()
        if status:
            msg = '**Account Id already exists**!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',EMAIL):
            # https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
            # Means- it has exactly one @ sign, and at least one . in the part after the @:
            msg = 'Invalid email address !'
        elif not ID or not PASSWORD or not EMAIL:
            msg = 'Please fill out the form !'
            # https://stackoverflow.com/questions/3813195/regular-expression-for-indian-mobile-numbers
            # ^     #Match the beginning of the string
            # [789] #Match a 7, 8 or 9
            # \d    #Match a digit (0-9 and anything else that is a "digit" in the regex engine)
            # {9}   #Repeat the previous "\d" 9 times (9 digits)
            # $     #Match the end of the string
        elif not re.match(r'^[7-9]\d{9}', MOBILENO):
            msg = 'Enter correct mobile number !'
        else:
            insertdata(ID,NAME,EMAIL,MOBILENO,PASSWORD)

            msg = 'You have successfully registered !'
            print('data inserted')


    return render_template('Register.html',msg=msg)

def insertdata(id,name,email_id,mobileNo,password):
    try:
        connectDb()
        query = "insert into weather_ID values({},'{}','{}','{}','{}');".format(id,name,email_id,mobileNo,password)
        cur.execute(query)
        con.commit()
        print('Registred successfully')
        return True
    except pymysql.DatabaseError:
        return False
        # closeDb()
    

@loginpage.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST':
        id =(request.form['id'])
        password =(request.form['password'])
        connectDb()
        query =("select * from weather_ID where id={};".format(id))
        cur.execute(query)
        global data,l
        data=cur.fetchone()


        l=data
        if data!=None:
            if data[0] == int(id):
                if data[4] == str(password):
                    msg = 'Looged In....'
                    return redirect('http://127.0.0.1:5000/climawatch')
                else:
                    msg = 'inccorect password'
                    return render_template('login.html', msg=msg)
        else:
            msg = 'id dose not matched'
            closeDb()
            return render_template('login.html', msg=msg)
    return render_template('login.html',msg=msg)

@loginpage.route("/")
@loginpage.route('/climawatch',methods=['GET','POST'])
def weather():
    msg=''
    msg2=''
    data=''
    city=''
    temp='' 
    humidity='' 
    wind_speed='' 
    descr='' 
    visibility='' 
    temp_max='' 
    temp_min=''
    
    if request.method == 'POST':
        city =(request.form['city'])
        x=str(city)      
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(x,user_api)
        r = requests.get(url)
        api_data = r.json()
   
        temp = ((api_data['main']['temp']) - 273.15) # kelvin to celcius
        temp=round(temp,4)
        humidity = api_data['main']['humidity']
        wind_speed = api_data['wind']['speed']
        descr = api_data['weather'][0]['description']
        visibility=api_data['visibility']
        temp_max=api_data['main']['temp_max']
        temp_min=api_data['main']['temp_min']
        city=api_data['name']
        msg='city:- {},  temp:-{}, humidity:-{}, Wind seppd:= {},desc :- "{}",visibility:- {}, max:- {},min:- {}'.format(city,temp,humidity,wind_speed,descr,visibility,temp_max,temp_min)
        
        msg2="temp    {}  descr       {}".format(temp,descr)
        
        data = getAllWeatherData(city,temp,humidity,wind_speed,descr,visibility,temp_max,temp_min)# it returns in tuple form



    return render_template('climawatch.html',data=data,city=city,msg=msg,msg2=msg2,temp=temp,humidity=humidity,visibility=visibility,wind_speed=wind_speed,descr=descr,temp_max=temp_max,temp_min=temp_min)
    # return render_template('climawatch.html')


if __name__ == '__main__':
    loginpage.run(debug=True)