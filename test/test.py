import json
import os
import requests 
import urllib

dentistUrl= "http://1b0422bb.ngrok.io/v1/dentists"
timeslotsUrl = "http://e179e675.ngrok.io/v1/timeslots"
name = 1
time = 8
startTime = 8
dentistChoicesQuery = ""
dentistQuery = ""
dentTimeslotsQuery = ""
timeslotQuery = ""


with open('./test.txt') as json_file:  
    data = json.load(json_file)

def makeGetReq(baseurl):
    res = urllib.urlopen(baseurl)
    data = json.loads(res.read())
    return data
    
def processRequest(req):

    # with open('./test.txt') as json_file:  
    #     req = json.load(json_file)
    # psuedo code
    # if params = Name then get dentist
    #  ---show available timeslots
    # --- ask what timeslot they want
    # if params = Number then get timeslot
    if req.get("queryResult").get("action") == "get-choice":
        url1 = dentistUrl
        dentistChoicesQuery = makeGetReq(url1)
        dents = ""
        for key in dentistChoicesQuery['dentists']:
            dents = dents + key['name'] + " ; "
        res = dents

    if req.get("queryResult").get("action") == "get-name":
        name = req.get("queryResult").get("parameters").get("Name")
        #Got Dentist Details
        url2 = dentistUrl+"/"+name
        dentistQuery = makeGetReq(url2)
        #All timeslots of a dentist
        url3 = timeslotsUrl+"/"+name
        dentTimeslotsQuery = makeGetReq(url3)
        #for each timeslot, make a string
        times = ""
        for key in dentTimeslotsQuery['timeslots']:
            times = times + str(key['startTime']) + " to " + str(key['endTime']) + " ; " 
        res = times
    
    if req.get("queryResult").get("action") == "get-time":
        #Got Dentist Timeslot Details
        name = "1"
        time = 1
        url3 = timeslotsUrl+"/"+name
        dentTimeslotsQuery = makeGetReq(url3)
        startTime = req.get("queryResult").get("parameters").get("Number")
        for key2 in dentTimeslotsQuery['timeslots']:
            if startTime is key2['startTime']:
                time = key2['id']
                print time
        #Get one specific timeslot
        url4 = timeslotsUrl+"/"+name+"/"+str(time)
        print url4
        timeslotQuery = makeGetReq(url4)
        print timeslotQuery
        #install requests and do a put call to reserve the booking
        r = requests.put(url4+"/reserve")
        res = "Your appointment has been made with Dr " +name+ " at " + str(timeslotQuery['timeslot']['startTime']) + \
             " till " + str(timeslotQuery['timeslot']['endTime']) + "  today."

    ## check everywhere , if there is anothing booked, store its name and id and make url
    if req.get("queryResult").get("action") == "cancel":
        r = requests.put(url4+"/cancel")
        res = "Your appointment with Dr " +dentistQuery.name+ " at " + str(timeslotQuery['timeslot']['startTime']) + \
             " till " + str(timeslotQuery['timeslot']['endTime']) + "  today has been cancelled. Have a nice day!"

    return res

response = processRequest(data)

print("Response: \t")
print(response)
# return {
# "fulfillmentText": res
# }