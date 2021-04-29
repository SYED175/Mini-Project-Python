from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import pytest



app =Flask("__name__")
app.config["MONGO_DBNAME"]="goals";
app.config["MONGO_URI"]="mongodb://localhost:27017/goals"

mongo = PyMongo(app)
db = mongo.db #used to acces collections within databases

@app.route('/adduser', methods=['POST'])
def add_user():
    #bucketList= mongo.db.bucketList
    req_data=request.get_json()
    user = req_data['usname']
    print(user)

    if db.users.find({'username':user}).count() >0:
        return "User Already Exist"
    else:
        db.users.insert({"username":user})
        #db[user].insert({"goal":"nothing"})
        return "User Added Succesfully"




@app.route('/users', methods=['GET'])
def get_users():
    #bucketList= mongo.db.bucketList
    users = [] #empty list
    user =db.users.find() # return all the docs present inside it currently
    for j in user:
        j.pop('_id')
        users.append(j)
    return jsonify(users)


"""
@app.route('/users/viewBucketList', methods=['GET'])
def lekoao_bucketList():
    bucketList= mongo.db.bucketList
    goals = [] #empty list
    goal =bucketList.find() # return all the docs present inside it currently
    for j in goal:
        j.pop('_id')
        goals.append(j)
    return jsonify(goals)
"""

@app.route('/addgoal', methods=['POST'])
def add_goal():
    #bucketList = mongo.db.bucketList
    req_data = request.get_json()
    goal = req_data["goal"]
    user = req_data["usname"]
    print(user,goal)

    if db[user].find({'name':goal}).count()>0:
        return "Goal already Exists! Try new things men!"
    else:
        db[user].insert({'name':goal,'status': 'Incomplete'})
        return "Added Goal Succesfully Bro :)"



@app.route('/update', methods=['POST'])
def update():
    req_data = request.get_json()
    user = req_data['usname']
    goal = req_data['goal']
    if db.users.find({'username': user}).count() > 0:

        if db[user].find({'name': goal}).count() > 0:

            db[user].update({'name':goal},{ '$set': {'status': 'complete'}}) #note: $ is not recognised by python so use in quotes '$'
            return "tagged successfully hehe"

        else:
            return "No goal found!"
    else:
        return "User doesnt exist !! "




@app.route('/showgoals/<name>', methods=['GET'])
def show_status(name):

    if db.users.find({'username':name}).count()>0:
        goals = []  # empty list
        goal = db[name].find()  # return all the docs present inside it currently
        for j in goal:
            j.pop('_id')
            goals.append(j)
        return jsonify(goals)

    else:
        return "User doesnt exist!!"


         #return jsonify(db[name].find())


