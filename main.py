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

@app.route('/switch_bookings')
def switch(idA, idB):
    switch1 = bookingsCollection.find_one({"_id":idA})
    switch2 = bookingsCollection.find_one({"_id":idB})
    switch1Username = switch1["username"]
    switch2Username = switch2["username"]
    test_db.bookingsCollection.update_one({
        '_id': switch1['_id']
    }, {
        '$set': {
            'username': switch2["username"]
        }
    }, upsert=False)
    test_db.bookingsCollection.update_one({
        '_id': switch2['_id']
    }, {
        '$set': {
            'username': switch1Username
        }
    }, upsert=False)
    user1 = usersCollection.find_one({"username": switch1Username})
    user2 = usersCollection.find_one({"username": switch2Username})
    user1BookingId = user1["booking_ids"]
    user2BookingId = user2["booking_ids"]
    for booking_id in user1BookingId:
        if booking_id == idA:
            test_db.usersCollection.update_one({
                '_id': user1["_id"]
            }, {
                '$set': {
                    'booking_id': idB
                }
            }, upsert=False)
    for booking_id in user2BookingId:
        if booking_id == idB:
            test_db.usersCollection.update_one({
                '_id': user2["_id"]
            }, {
                '$set': {
                    'booking_id': idA
                }
            }, upsert=False)

# usersCollection.close()
# bookingsCollection.close()
# flightsCollection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))
