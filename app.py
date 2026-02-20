# import flask and its component
from flask import *
#import the pymysql module - it helps us to create a connnection between python flask and mysql database
import pymysql
# create an application and give it a name

app = Flask(__name__)

#below is the sign up route
@app.route("/api/signup",methods=["POST"])
def signup():
    if request.method == "POST":
        #Extract the different details entererd on the form
         username = request.form["username"]
         email = request.form["email"]
         password = request.form["password"]
         phone = request.form["phone"]
         
         #by use of the print function lets print all those details sent with the upcoming request
        #  print(username,email,password,phone)
        #establish a connection btn flask and mysql
         connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")
         #create a cursor to execute the sql queries
         cursor = connection.cursor()

         #structure an sql too insert the details received from the formthe percentage holder ->A place holder it stands in places of actual values  i.e we shall replace later
         sql="INSERT INTO users(username,email,phone,password) VALUES(%s,%s,%s,%s)"
        
         #create tuple that will hold all the data gotten from the form
         data = (username,email,phone,password)
         #by use of the cursor ,execute the sql as you replce the placeholder with the actual values
         cursor.execute(sql,data)

         # commit the changes
         connection.commit()


#below is the log in/sign in route
@app.route("/api/signin",methods=["POST"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

     #print out the details 
        # print(email,password)
        connection = pymysql.connect(host="localhost",user="root",password="",database="sokogardenonline")

        #create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        #structure the sql query that will check whether the email and the password enterd are correct 
        sql= "SELECT * FROM users WHERE email = %s AND password = %s"
        # put the data received from the form into a tuple 
        data = (email, password)

        #by use of the cursor execute the sql 
        cursor.execute(sql,data)
     
        # check whether there row returned and stored 
        count = cursor.rowcount
        
       
        #if there are records return it means the password and the email are correct otherwise it means they are wrong

        if count == 0:
            return jsonify({"message":"login failed"})
        else: 
        
            #there must be a user so we create a variable that will hold the details of the user fetched from the database
            user=cursor.fetchone()

            #return the details to the frontend as well as a message 
            return jsonify({"message":"user looged in succesfully","user":user})
    
    
    









# run the application
app.run(debug=True)