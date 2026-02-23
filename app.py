# import flask and its component
from flask import *
import os 
#import the pymysql module - it helps us to create a connnection between python flask and mysql database
import pymysql
# create an application and give it a name

app = Flask(__name__)

#configure the location to where youre product images will be saved on your application
app.config["UPLOAD_FOLDER"] = "static/images"

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
    
# Below is the route for running the application

@app.route("/api/add_product",methods = ["POST"])
def Addproducts():
    if request.method == "POST":
        #extract the data enterd on the form
        product_name =request.form["product_name"]
        product_description =request.form["product_description"]
        product_cost =request.form["product_cost"]
        #for the product photo we shall fetch it from the files as shown below

        product_photo =request.files["product_photo"]

        # extract the file name of the product photo
        filename = product_photo.filename
        # by use of the os mudule(operating system) we can extract the file path where the image is currently saved 
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        #save the product photo image into the new location
        product_photo.save(photo_path)


        #print them out to test you are are receiving the details sent with the request
        # print(product_name,product_description,product_cost,product_photo)

        #establish a connection
        connection = pymysql.connect(host="localhost",user="root",password="",database="sokogardenonline")

        #create a cursor
        cursor = connection.cursor()

        #structure the sql query to insert the details to the database
        sql = "INSERT INTO product_details(product_name, product_description, product_cost, product_photo) VALUES (%s, %s, %s, %s)"

        #create the tuple that will hold the data from the which are current held onto the different variables declared.
        data = (product_name,product_description,product_cost,filename)

        # use the cursor to execute the sql you replace the placeholders with the actual data.
        cursor.execute(sql, data)

        #commit the changes to the database
        connection.commit()


        return jsonify({"message" : "product added successfully"})

#below is a route to fetch products
@app.route("/api/get_products")
def get_products():

    #create a cursor
     connection = pymysql.connect(host="localhost",user="root",password="",database="sokogardenonline")

    #create cursor
     cursor = connection.cursor(pymysql.cursors.DictCursor)

     #structure the query
     sql = "SELECT * FROM product_details"

     # Execute the query
     cursor.execute(sql)
     #Create a variable that will hold the data fetched from the table
     products = cursor.fetchall()



     return jsonify(products)


    









# run the application
app.run(debug=True)