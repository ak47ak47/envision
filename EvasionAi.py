import mysql.connector
import json
from flask import Flask, request, jsonify
import secrets
import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import base64
import calendar;
import time;
import datetime
from dt import w

HOST = "smtp-mail.outlook.com"
PORT = 587



app = Flask(__name__)
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="auth"
)
mycursor = mydb.cursor(buffered=True)


CORS(app, supports_credentials=True)



@app.route('/registration',methods=['GET','POST'])
def Registration():
   
    x=request.json
    First_Name=x['First_Name']
    Last_Name=x['Last_Name']
    User_Name=x['User_Name']
    Email = x['Email']
    Password =x['Password']
    Phone_No=x['Phone_No']
    Gender=x['Gender']
    
    try:
            query ='select * from registration where Email = "' + Email +'"' 
            print(query)
            mycursor.execute(query)
            rows = mycursor.fetchall()
            result = []
            for row in rows:
                d = {}
                for i, col in enumerate(mycursor.description):
                    d[col[0]] = row[i]
                result.append(d)
            global response
            if not result:
                try:
                        query ="""
                            INSERT INTO `registration` 
                            ( `id`, `First_Name`, `Last_Name`, `User_Name`, `Email`, `Password`, `Phone_No`,`Gender`,status) 
                            VALUES 
                            (NULL, %s, %s, %s, %s, %s, %s,%s,%s)
                            """
                        print(query)
                        global response
                        mycursor.execute(query, (First_Name, Last_Name, User_Name, Email, Password, Phone_No,Gender,'0'))
                        mydb.commit()
                        response = {'success':True,'status':200}
                except Exception as e:
                        response = {'success':False,'status':400}
                        print(f"Error: {e}")
            else:
                    response = {'success': False, 'status': 400}
            print(x)
    except Exception as e:
        print(f"Error: {e}")
    return response
   
   
@app.route('/login',methods=['GET','POST'])
def Login():
    x=request.json
    print(x)
    Email = x['Email']
    Password = x['Password']
    print(Email,Password)
    print('select * from registration where Email = "' + Email +'" And Password = "'+ Password +'"')
    mycursor.execute('select * from registration where Email = "' + Email +'" And Password = "'+ Password +'"')
    rows = mycursor.fetchall()
    result = []
    for row in rows:
        d = {}
        for i, col in enumerate(mycursor.description):
            d[col[0]] = row[i]
        result.append(d)

# Convert the list of dictionaries to JSON and print it
    
    json_result = json.dumps(result) 
    return json_result

@app.route('/forgetPass',methods=['GET','POST'])
def ForgetPass():
    x=request.json
    Email = x['Email']
    try:
            query ='select * from registration where Email = "' + Email +'"' 
            print(query)
            mycursor.execute(query)
            rows = mycursor.fetchall()
            result = []
            for row in rows:
                d = {}
                for i, col in enumerate(mycursor.description):
                    d[col[0]] = row[i]
                result.append(d)
            print(result)
            global response
            if not result: 
                    response = {'success': False, 'status': 400}
                    print('none')     
            else:
                try:
                    letters = string.ascii_letters
                    digits = string.digits
                    special_chars = string.punctuation
                    selection_list = letters + digits
                    password_len = 7
                    password = ''
                    for i in range(password_len):
                        password+= ''.join(secrets.choice(selection_list))
                    password+= ''.join(secrets.choice(special_chars))
                    print(password)
                    #Email Upadated Password
                    FROM_EMAIL = "sheikhajeem2@gmail.com"
                    PASSWORD = 'Aze3536'
                    
                    message = MIMEMultipart("alternative")
                    message['Subject'] = "Updated Password"
                    message['From'] = FROM_EMAIL
                    message['To'] = Email
                    message['Cc'] = FROM_EMAIL
                    message['Bcc'] = FROM_EMAIL
                    
                    html = '<h1>Hello Everone</h1></br><h2>EvasionAi<h2><h3>Your Updated Password</h3><h4>'+password+'</h4>'
                    

                    html_part = MIMEText(html, 'html')
                    message.attach(html_part)

                    smtp = smtplib.SMTP(HOST, PORT)

                    status_code, response = smtp.ehlo()
                    print(f"[*] Echoing the server: {status_code} {response}")

                    status_code, response = smtp.starttls()
                    print(f"[*] Starting TLS connection: {status_code} {response}")

                    status_code, response = smtp.login(FROM_EMAIL, 'Aze3536!')
                    print(f"[*] Logging in: {status_code} {response}")

                    smtp.sendmail(FROM_EMAIL, Email, message.as_string())
                    smtp.quit()
                    
                    
                    #Password Update in database
                    query ='update registration set Password = "' + password +'" where Email = "' + Email +'"'
                    print(query)
                    mycursor.execute(query)
                    mydb.commit()
                    response = {'success':True,'status':200}
                except Exception as e:
                    response = {'success':False,'status':400}
                    print(f"Error: {e}") 
            print(x)
    except Exception as e:
        print(f"Error: {e}")
    return response



@app.route('/Creation',methods=['GET','POST'])
def Creation():
    x=request.json
    Email = x['Email']
    print(x)
    
    try:
            query ='select * from data where Email = "' + Email +'"ORDER BY Img_id DESC LIMIT 10' 
            print(query)
            mycursor.execute(query)
            rows = mycursor.fetchall()
            row_count = mycursor.rowcount
            print(rows)
            result=[]
            results=[]
            d = {}
            s = {}
            for x in range(int(row_count)):
                li=list(rows[x])
                li[2]=rows[x][2].decode("utf-8")
                results.append(li)
            print(results)
            for row in results:
                d = {}
                for i, col in enumerate(mycursor.description):
                    d[col[0]] = row[i]
                result.append(d)

        # Convert the list of dictionaries to JSON and print it
            json_result = json.dumps(result)
            print(json_result)
            return result
    except Exception as e:
        print(f"Error: {e}")
        return({'success':False,'status':400,'Message':'For Some reason Data is Not Found'})
    
@app.route('/Users',methods=['GET','POST'])
def Fetch_Users():
    global response
    try:
            query ='select * from registration' 
            print(query)
            mycursor.execute(query)
            rows = mycursor.fetchall()
            result = []
            for row in rows:
                d = {}
                for i, col in enumerate(mycursor.description):
                    d[col[0]] = row[i]
                result.append(d)
            print(result)
            response = result
    except Exception as e:
            response = {'success':False,'status':400}
            print(f"Error: {e}")
    return response
@app.route('/Follow',methods=['GET','POST'])
def Follow_Users():
    x=request.json
    print(x)
    Email = x['Email']
    password = x['Password']
    follower = x['Follower_Email']
    follower_id = x['id']
    print(x)
    true = int(1)
    global response
    global Follow
    if (x['Follow'] == 0):
        Follow='true'
    else:
        Follow='false'
    try:
            query ='update registration set Follow = ' + Follow +' where Email = "' + Email +'" And Password = "' + password +'"' 
            print(query)
            mycursor.execute(query)
            mydb.commit() 
            if (x['Follow'] == 0):
                try:
                    query ="""
                        INSERT INTO `followers` 
                        ( `Follow`, `Follower`, `User_id`) 
                        VALUES 
                        (%s, %s, %s)
                        """
                    print(query)
                    mycursor.execute(query, (Email, follower, follower_id))
                    mydb.commit()
                    response = {'success':True,'meassage':'Record in Inserted','status':200}
                except Exception as e:
                    response = {'success':False,'status':400}
                    print(f"Error: {e}")
            else:
                try:
                    query ='DELETE FROM followers WHERE User_id ='+ str(follower_id)
                    print(query)
                    mycursor.execute(query)
                    mydb.commit()
                    response = {'success':True,'status':200}
                except Exception as e:
                    response = {'success':False,'meassage':'Record is Deleted','status':400}
                    print(f"Error: {e}")
    except Exception as e:
            response = {'success':False,'status':400}
            print(f"Error: {e}")
    return response


@app.route('/generate',methods=['GET', 'POST'])
def generate():
    data = request.get_json()
    textPrompt = data["textPrompt"]
    Width = data["Width"]
    Height = data["Height"]
    Cfg_Scale = data["Cfg_Scale"]
    IGS = data["IGS"]
    print((textPrompt),(Width),(Height),(Cfg_Scale),(IGS))
    try:
        API_ENDPOINT = "https://5706-34-69-161-244.ngrok-free.app"
        Api_data = {"textPrompt": textPrompt, "Width": Width, "Height": Height, "Cfg_Scale": 3.5, "IGS": IGS}
        data = json.dumps(Api_data)

        # Send the POST request and get the response
        headers = {'Content-type': 'application/json'}
        r = requests.post(url=API_ENDPOINT, data=data, headers=headers)

        # You can then extract the response text
        my_new_string_value = r.content.decode("utf-8")
        my_json = json.loads(my_new_string_value)
        #print(my_json['data'])

        def dequote(s):
            if (len(s) >= 2 and s[0] == s[-1]) and s.startswith(("'", '"')):
                return s[1:-1]
            return s
        string = dequote(my_json['data'])
        string1 = string[1:]
        string2 = dequote(string1)


        image = base64.b64decode(string2, validate=True)
        gmt = time.gmtime()
        ts = calendar.timegm(gmt)
        file_to_save = f"D:/React-expo Authentication/Ne w\EnvsisionAi/assets/my_image_{ts}.png"
        with open(file_to_save, "wb") as f:
            f.write(image)
        print('done')
        response = {'success':True,'meassage':'Image is Generated','status':200 ,'content':string2}
    except Exception as e:
            response = {'success':False,'status':400}
            print(f"Error: {e}")
    
    return response



@app.route('/ImageData',methods=['GET','POST'])
def ImageData():
    x=request.json
    Email = x['Email']
    TextPromt = x['TextPromt']
    Base64 = x['base64']
    
    try:
        saved_date = datetime.date.today()
        query ="""
        INSERT INTO `data` 
        ( `Img_id`, `TextPrompt`, `Email`, `Base64`) 
        VALUES 
        (NULL, %s, %s, %s)
        """
        print(query)
        
        mycursor.execute(query, (TextPromt, Email, Base64))
        mydb.commit()
        response = {'success':True,'status':200}
    except Exception as e:
        response = {'success':False,'status':400}
        print(f"Error: {e}")
    return response

@app.route('/UpdatePass',methods=['GET','POST'])
def updatepass():
    x = request.json
    print(x)
    email = x['Email']
    currentPass =x ['currentPass']
    updatepass = x['updatedPassword']
    try:
            query ='SELECT * FROM registration WHERE PASSWORD = "' + str(currentPass) +'"  AND Email = "' + str(email) +'"' 
            print(query)
            mycursor.execute(query)
            rows = mycursor.fetchall()
            print(rows)
            if not rows:
                return ({'success':False,'status':200,'msg':'Current Password is not Matched'})
            else:
                try:
                    query ='update registration set PASSWORD = "' + str(updatepass) +'" where Email = "' + str(email) +'"'
                    print(query)
                    mycursor.execute(query)
                    mydb.commit() 
                    response = {'success':True,'status':400,'msg':'Password is Successfully Updated'}
                except Exception as e:
                    response = {'success':False,'status':400}
                    print(f"Error: {e}")
    except Exception as e:
            response = {'success':False,'status':400}
            print(f"Error: {e}")
    return response


@app.route('/profile',methods=['GET','POST'])
def profile():
    x = request.json
    email = x['Email']
    global response
    try:
            query ='select * from registration WHERE Email = "' + str(email) +'"' 
            print(query)
            mycursor.execute(query)
            rows = mycursor.fetchall()
            result = []
            for row in rows:
                d = {}
                for i, col in enumerate(mycursor.description):
                    d[col[0]] = row[i]
                result.append(d)
            response = result
    except Exception as e:
            response = {'success':False,'status':400}
            print(f"Error: {e}")
    try:
            query ='SELECT COUNT(Follow) AS follower FROM followers where Follow ="' + str(email) +'"' 
            print(query)
            mycursor.execute(query)
            rows = mycursor.fetchall()
            print(result)
            response[0]['followers']=rows[0][0] 
            print(type(response[0]))
            print(response)
            
    except Exception as e:
            response = {'success':False,'status':400}
            print(f"Error: {e}")
    try:
            query ='SELECT COUNT(Follow) AS follower FROM followers where Follower ="' + str(email) +'"' 
            print(query)
            mycursor.execute(query)
            rows = mycursor.fetchall()
            print(result)
            response[0]['following']=rows[0][0] 
            print(type(response[0]))
            print(response)
            
    except Exception as e:
            response = {'success':False,'status':400}
            print(f"Error: {e}")
    return response

@app.route('/updateProfile',methods=['GET','POST'])
def updateProfile():
    x= request.json
    email = x['Email']
    last_name = x['Last_Name']
    first_name = x['First_Name']
    user_name = x['User_Name']
    try:
        print('Update Query')
        query = (
                    'UPDATE registration SET First_Name = "' + first_name + '",Last_Name = "' + last_name + '", User_Name = "' + user_name + '" WHERE Email = "' + email + '"' )
        print(query)
        mycursor.execute(query)
        return json.dumps({'success': True, 'status': 200,
                        'message': 'Account is Successfully Updated'})
    except Exception as e:
        print(f"Error: {e}")
        return json.dumps({'success': False, 'status': 400,
                        'message': 'For Some Reason Account is Not '
                                    'Updated'})
                            
if __name__ == '__main__':
    app.run(port=8000)