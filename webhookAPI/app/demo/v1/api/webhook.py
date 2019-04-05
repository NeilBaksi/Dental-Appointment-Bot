# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
from flask import make_response, jsonify

from . import Resource
from .. import schemas
import json
import os
import requests 
import urllib

## ngrok http -subdomain=dentistapi 5001
dentistUrl= "http://192.168.99.100:9999/v1/dentists"
## ngrok http -subdomain=timeslotsapi 5000
timeslotsUrl = "http://192.168.99.100:9998/v1/timeslots"


class Webhook(Resource):
    global makeGetReq
    global getChoice
    global getNameID
    global getFullName
    global getNameInfo
    global getAvail
    global getTime
    global getCancel

    def get(self):
        response = {
            "test": "This is for the Webhook only. Only used for POST methods!"
        }
        # r = make_response(response)
        # r.headers['Content-Type'] = 'application/json'
        return jsonify(response)
    
    def makeGetReq(baseurl):
        res = urllib.urlopen(baseurl)
        getReq = json.loads(res.read())
        return getReq

    def getChoice():
        url1 = dentistUrl
        dentistChoicesQuery = makeGetReq(url1)
        dents = ""
        for key in dentistChoicesQuery['dentists']:
            dents = dents + key['name'] + " ; "
        res = "Which Doctor would you like to book an appointment with? We have the following doctors available today: \n"+dents
        return res

    def getFullName(name):
        url2 = dentistUrl+"/"+name
        dentistQuery = makeGetReq(url2)
        return dentistQuery['name']

    # returns all available timeslots for a dentist
    def getNameID(name):
        #Got Dentist Details
        url2 = dentistUrl+"/"+name
        dentistQuery = makeGetReq(url2)
        #All timeslots of a dentist
        url3 = timeslotsUrl+"/"+name
        dentTimeslotsQuery = makeGetReq(url3)
        #for each timeslot, make a string
        times = ""
        for key in dentTimeslotsQuery['timeslots']:
            if (key['booked']== False):
                times = times + str(key['startTime']) + " to " + str(key['endTime']) + " ; " 
        res = "Dr "+ getFullName(name)+" is available at : \n" + times
        return res

    # returns info for a dentist
    def getNameInfo(id):
        #Got Dentist Details
        url2 = dentistUrl+"/"+id
        dentistQuery = makeGetReq(url2)
        info = "Name: "+ dentistQuery['name'] + "; Specialization: " + dentistQuery['spec'] + "; Location: " +dentistQuery['location'] 
        res = info
        return res
    
    def getAvail(name,startTime):
        time = 0  
        url3 = timeslotsUrl+"/"+name
        dentTimeslotsQuery = makeGetReq(url3)
        for key2 in dentTimeslotsQuery['timeslots']:
            if startTime == key2['startTime']:
                time = key2['id']
        #Get one specific timeslot
        url4 = timeslotsUrl+"/"+name+"/"+str(time)
        timeslotQuery = makeGetReq(url4)
        try:
            if(timeslotQuery['message'] != None):
                res = "Invalid Timeslot. Please Choose a valid Timeslot"
                resAdd = getNameID(name)
                res = res +"\n"+ "These are the available timeslots : \n"+ resAdd
                return res
        except:
            pass

        if (timeslotQuery['timeslot']['booked'] == True):
            res = "This appointment slot is unavailable."
            resAdd = getNameID(name)
            res = res +"\n"+ "These are the available timeslots : \n"+ resAdd
            return res
        else:
            res = "Yes, this timeslot is available."
            resAdd = getNameID(name)
            res = res +"\n"+ "These are all the available timeslots : \n"+ resAdd
            return res


    def getTime(name, startTime):
        time = 0  
        url3 = timeslotsUrl+"/"+name
        dentTimeslotsQuery = makeGetReq(url3)
        for key2 in dentTimeslotsQuery['timeslots']:
            if startTime == key2['startTime']:
                time = key2['id']
        #Get one specific timeslot
        url4 = timeslotsUrl+"/"+name+"/"+str(time)
        timeslotQuery = makeGetReq(url4)
        try:
            if(timeslotQuery['message'] != None):
                res = "Invalid Timeslot. Please Choose a valid Timeslot"
                resAdd = getNameID(name)
                res = res +"\n"+ "These are the available timeslots : \n"+ resAdd
                return res
        except:
            pass

        if (timeslotQuery['timeslot']['booked'] == True):
            res = "This appointment slot is unavailable. Please choose another timeslot!"
            resAdd = getNameID(name)
            res = res +"\n"+ "These are the available timeslots : \n"+ resAdd
            return res
        
        f=open("./url.txt", "w+")
        f.write(url4)
        f.close
        
        #install requests and do a put call to reserve the booking
        r = requests.put(url4+"/reserve")
        fullname = getFullName(name)
        res = "Your appointment has been made with Dr " +fullname+ " at " + str(timeslotQuery['timeslot']['startTime']) + \
                " till " + str(timeslotQuery['timeslot']['endTime']) + "  today. Would that be all for today?"
        
        return res

    def getCancel():
        f=open("./name.txt", "r")
        name =f.read()
        f=open("./url.txt", "r")
        url =f.read()
        timeslotQuery = makeGetReq(url)
        r = requests.put(url+"/cancel")
        fullname = getFullName(name)
        res = "Your appointment with Dr " +fullname+ " at " + str(timeslotQuery['timeslot']['startTime']) + \
                " till " + str(timeslotQuery['timeslot']['endTime']) + "  today has been cancelled. Would that be all for today?"
        
        return res


    def post(self):
        req = request.get_json(silent=True, force=True)

        # print("Request:")
        print(req.get("queryResult").get("action"))

        if req.get("queryResult").get("action") == "get-choice":
            res = getChoice()

        if req.get("queryResult").get("action") == "get-name":
            f=open("./name.txt", "w+")
            name = req.get("queryResult").get("parameters").get("name")
            res = getNameID(name)
            f.write(name)
            f.close

        if req.get("queryResult").get("action") == "get-info":
            name = req.get("queryResult").get("parameters").get("name")
            res = getNameInfo(name)
            
        if req.get("queryResult").get("action") == "get-avail":
            name = req.get("queryResult").get("parameters").get("name")
            startTime = req.get("queryResult").get("parameters").get("number")
            res = getAvail(name,int(startTime))
            
        if req.get("queryResult").get("action") == "get-time":
            #Got Dentist Timeslot Details
            f=open("./name.txt", "r")
            name =f.read()
            startTime = req.get("queryResult").get("parameters").get("number")
            res = getTime(name,int(startTime))

        if req.get("queryResult").get("action") == "time-pref":
            os.remove("./name.txt")
            os.remove("./url.txt")
            res = "Thank you! See you soon! :D" 
        
        # taking booking url and change the end point to cancel it. API handles the rest
        if req.get("queryResult").get("action") == "cancel":
            res = getCancel()
            os.remove("./name.txt")
            os.remove("./url.txt")

        return jsonify({"fulfillmentText": res})

    