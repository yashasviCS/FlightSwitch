from flask import Flask
app = Flask(__name__)
import os
import pymongo
from bson import ObjectId


client = pymongo.MongoClient("mongodb+srv://admin:hacktx@cluster0-idfxg.mongodb.net/test?retryWrites=true&w=majority")
test_db = client.test
usersCollection = test_db.Users
bookingsCollection = test_db.Bookings

print("Database connected")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/create_test_user')
def create_test_user():
    usersCollection.insert_one({"username": "testusername", "password": "bad_password" })
    return "Successfully inserted test user"

# usersCollection.close()
# bookingsCollection.close()
# flightsCollection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))
