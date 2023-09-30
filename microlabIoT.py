#TODO Drop Table instead of database to avoid giving all previlages to gnostis

from flask import Flask,request, render_template
import mysql.connector 
from datetime import datetime, timedelta
import pytz
import webbrowser

#pip3 install mysql-connector-python==8.0.29
#pip3 install DateTime
#pip3 install flask
#pip3 install pytz

#sudo apt install mariadb-server
#sudo mysql_secure_installation
#set password and answer yes to all
#Then run mysql -u root -p
#and login
#then give permissions to gnostis
#CREATE USER 'gnostis'@'localhost' IDENTIFIED BY 'gnostis'; 
#GRANT ALL PRIVILEGES ON *.* TO 'gnostis'@'localhost' WITH GRANT OPTION; 

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="gnostis",
    password="gnostis"
    )

mycursor = mydb.cursor()
mycursor.execute("DROP DATABASE IF EXISTS microlabIoT")
mycursor.execute("CREATE SCHEMA IF NOT EXISTS microlabIoT DEFAULT CHARACTER SET utf8")
mycursor.execute("USE microlabIoT")
mycursor.execute("CREATE DATABASE IF NOT EXISTS microlabIoT")
#mycursor.execute("CREATE TABLE IF NOT EXISTS teams (team VARCHAR(255), temperature VARCHAR(255), pressure VARCHAR(255), status VARCHAR(255))")
mycursor.execute("CREATE TABLE IF NOT EXISTS teams (team VARCHAR(255), temperature VARCHAR(255), pressure VARCHAR(255), status VARCHAR(255), timestamp DATETIME, PRIMARY KEY (team))")
#timeNow = datetime.now(pytz.timezone('Europe/Athens'))
#timeNow = timeNow.strftime('%Y-%m-%d %H:%M:%S')
#mycursor.execute("INSERT INTO teams (team, temperature,pressure,status,timestamp) VALUES (%s, %s, %s, %s, %s)", ('1', '20C','10%','help',timeNow))
#mycursor.execute("INSERT INTO teams (team, temperature,pressure,status) VALUES ('2', '25C','20%','OK')")
#mycursor.execute("INSERT INTO teams (team, temperature,pressure,status) VALUES ('3', '30C','30%','OK')")

@app.route('/')
def home():
    try:
        mycursor = mydb.cursor()
        #mycursor.execute("SELECT * FROM teams")
        timeNow = datetime.now(pytz.timezone('Europe/Athens'))
        time30MinutesAgo=timeNow-timedelta(minutes=30)
        time30MinutesAgo = time30MinutesAgo.strftime('%Y-%m-%d %H:%M:%S')
        mycursor.execute("SELECT * FROM teams WHERE timestamp >='"+time30MinutesAgo+"'")
        myresult = mycursor.fetchall()

        #for x in myresult:
        #    print(x)

        #print (myresult[0])
        
        return render_template('home.html',data=myresult)
    except:
        print("MY SQL IS BUSY")
        return ("<head><meta http-equiv=\"refresh\" content=\"5\"></head>")
    

@app.route('/data', methods = ['GET', 'POST', 'DELETE'])
def data():
    #mycursor.execute("INSERT INTO teams (team, temperature,pressure,status) VALUES ('4', '20C','10%','help')")
    if request.method == 'GET':
        """return the information for <user_id>"""
        #print("GET")
        return(200)
    if request.method == 'POST':
        if request.headers.get('Content-Type'):
            #print(request.headers['Content-Type'])
            try:
                data=request.get_json()
            except:
                return('400 corrupted json')
            #for x in data:
                #print(str(x).replace("'",'\"'))
            #datadict=json.loads(str(data).replace("'",'\"'))
            datadict={
                "temperature":"None",
                "pressure":"None",
                "team":"None",
                "status":"None"
            }
            for object in data:
                #print(object)
                try:
                    #if object["name"]=="team" and object["value"]=="3":
                    #    object["value"]=u'\xfb9'
                    #object["name"].encode('utf-8')
                    #object["value"].encode('utf-8')
                    if(object["name"].replace(".","").isalnum() == False):
                        print("name problem")
                        return('400 Invalid chars in json')
                    if(object["value"].replace(".","").isalnum() ==False):
                        print("value problem")
                        return('400 Invalid chars in json')
                    datadict[object["name"]]=object["value"]
                except:
                    print(object["name"])
                    print(object["value"])
                    return('400 Invalid chars in json')
            if datadict['team']=="None" or datadict['team']=="":
                print("Invalid team selected")
                return('400 Invalid team')
            #print(datadict)
            mycursor.execute("SELECT * FROM teams WHERE team='"+str(datadict['team'])+"'")
            exists=mycursor.fetchall()
            timeNow = datetime.now(pytz.timezone('Europe/Athens'))
            timeNow = timeNow.strftime('%Y-%m-%d %H:%M:%S')
            if (exists==[]):
                mycursor.execute("INSERT INTO teams (team, temperature,pressure,status,timestamp) VALUES (%s, %s, %s, %s, %s)",(str(datadict['team']), str(datadict['temperature']),str(datadict['pressure']),str(datadict['status']),timeNow))
            else:
                mycursor.execute("UPDATE teams SET temperature=%s,pressure=%s,status=%s,timestamp=%s WHERE team=%s",(str(datadict['temperature']),str(datadict['pressure']),str(datadict['status']),timeNow,str(datadict['team'])))

            return('200 OK')
        else:
            data= request.form
            #check if team exists
            mycursor.execute("SELECT * FROM teams WHERE team='"+str(data.get('team'))+"'")
            exists=mycursor.fetchall()
            timeNow = datetime.now(pytz.timezone('Europe/Athens'))
            timeNow = timeNow.strftime('%Y-%m-%d %H:%M:%S')
            if (exists==[]):
                mycursor.execute("INSERT INTO teams (team, temperature,pressure,status,timestamp) VALUES (%s, %s, %s, %s, %s)",(str(data.get('team')), str(data.get('temperature')),str(data.get('pressure')),str(data.get('status')),timeNow))
            else:
                mycursor.execute("UPDATE teams SET temperature=%s,pressure=%s,status=%s,timestamp=%s WHERE team=%s",(str(data.get('temperature')),str(data.get('pressure')),str(data.get('status')),timeNow,str(data.get('team'))))
            
            print("Received Data:")
            print(data)
            print("End of Data")
            return('200 OK')
    else:
        # POST Error 405 Method Not Allowed
        print("405 Method Not Allowed")



if __name__ == '__main__':
    #app.run(host='0.0.0.0',debug=False)
    webbrowser.open('http://localhost:5000') 
    app.run(debug=False)