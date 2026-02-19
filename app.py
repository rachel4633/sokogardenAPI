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


    return jsonify({"message":"user registered successfully."})









# run the application
app.run(debug=True)