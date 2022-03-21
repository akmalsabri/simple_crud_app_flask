from flask import Flask , redirect, url_for , render_template , session
from flask import request,jsonify
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime , timedelta
from bson import ObjectId
import os 

app = Flask(__name__)

# Get time today
start_myt = datetime.utcnow() + timedelta(hours=+8)

# Setup Pymongo
try:

    myclient = MongoClient(
       'mongodb://localhost:27017/',
        ServerSelectionTimeoutMS= 100,
    )
        
    mydb = myclient["add_event_02"]
    mycol = mydb["collection"]

except:
    print("Error - cannot access db")

############################################################3
# home page
@app.route("/",methods=["GET"])
def home():
    # for i in cursor_:
    #     print(i)
    myclient = MongoClient('mongodb://localhost:27017/')
    mydb = myclient["add_event_02"]
    mycol = mydb["collection"]

    # Upcoming
    cursor_ = mycol.find({"Event_date":{ "$gte":start_myt}})
    data = list(cursor_)
    
    # past event
    cursor_1 = mycol.find({"Event_date":{ "$lte":start_myt}})
    data1 = list(cursor_1)

    return render_template("home.html",db_list = data, db_list1 =data1)


###########################################################
# add event
@app.route("/add_event",methods=["POST","GET"])
def add_event():
    if request.method =="POST":
        event_name = request.form['event_name']
        event_date_str = request.form['event_date']
        event_date = datetime.strptime(event_date_str,'%d-%b-%Y %H:%M')
        event_note = request.form['notes']
        item_ ={
            "Event": event_name,
            "Event_date" :event_date,
            "Description" :event_note
        }
        print(item_)

        myclient = MongoClient('mongodb://localhost:27017/')
        mydb = myclient["add_event_02"]
        mycol = mydb["collection"]
        mycol.insert_one(item_)
        return redirect(url_for("event_name", cat_=item_))
    else:
        return render_template("add_event.html")



##########################
# admin page
@app.route("/admin",methods=["POST","GET"])
def admin_view():
    if request.method =="POST":
        myclient = MongoClient('mongodb://localhost:27017/')
        mydb = myclient["add_event_02"]
        mycol = mydb["collection"]
        cursor_ = mycol.find()

        data = list(cursor_)

        return redirect(url_for("add_event"))

    else: 

        myclient = MongoClient('mongodb://localhost:27017/')
        mydb = myclient["add_event_02"]
        mycol = mydb["collection"]
        cursor_ = mycol.find()

        data = list(cursor_)


        return render_template("admin.html",db_list = data)




###################################################
# update event
@app.route("/update_event/<id>",methods=["POST","GET"])
def update_event(id):
    if request.method =="POST":

        myclient = MongoClient('mongodb://localhost:27017/')
        mydb = myclient["add_event_02"]
        mycol = mydb["collection"]

        event_name = request.form['event_name']
        event_date_str = request.form['event_date']
        event_date = datetime.strptime(event_date_str,'%d-%b-%Y %H:%M')
        event_note = request.form['notes']
        mycol.find_one_and_update({"_id":ObjectId(id)},
        {'$set':{
            "Event": event_name,
            "Event_date" :event_date,
            "Description" :event_note }})
        
        return redirect(url_for("home"))
    else:

        return render_template("update_event.html")


@app.route("/<cat_>")
def event_name(cat_):
    return f"<h1>{cat_}</h1>"

##################################
# delete item
@app.route("/<id>/delete",methods=["DELETE","GET"])
def delete(id):
    # for i in cursor_:
    #     print(i)
    myclient = MongoClient('mongodb://localhost:27017/')
    mydb = myclient["add_event_02"]
    mycol = mydb["collection"]
    cursor_ = mycol.find_one_and_delete({"_id":ObjectId(id)})

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
    app.run(use_reloader=True)




# list gambar
# https://isaham.sgp1.digitaloceanspaces.com/pages/pricing/iSaham_Gear_One.jpg
# https://isaham.sgp1.digitaloceanspaces.com/pages/pricing/iSaham_Playback.jpg
# src="https://isaham.sgp1.digitaloceanspaces.com/pages/pricing/iSaham_Accelerator.jpg"
# https://isaham.sgp1.digitaloceanspaces.com/pages/pricing/iSaham_Max_2022.jpg
# https://isaham.sgp1.digitaloceanspaces.com/pages/pricing/iSaham_Pro.png


