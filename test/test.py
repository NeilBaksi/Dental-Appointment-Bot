import json
import os
import requests 
import urllib

## ngrok http -subdomain=dentistapi 5001
dentistUrl= "http://26be13ab.ngrok.io/v1/dentists"
## ngrok http -subdomain=timeslotsapi 5000
timeslotsUrl = "http://e22a00b2.ngrok.io/v1/timeslots"

with open('./test.txt') as json_file:  
    data = json.load(json_file)

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
    res = dents
    return res

# returns all available timeslots for a dentist
def getName(name):
    #Got Dentist Details
    url2 = dentistUrl+"/"+name
    dentistQuery = makeGetReq(url2)
    # print dentistQuery['name']
    #All timeslots of a dentist
    url3 = timeslotsUrl+"/"+name
    dentTimeslotsQuery = makeGetReq(url3)
    #for each timeslot, make a string
    times = ""
    for key in dentTimeslotsQuery['timeslots']:
        if (key['booked']== False):
            times = times + str(key['startTime']) + " to " + str(key['endTime']) + " ; " 
    res = times
    return res

def getTime(name, startTime):
    time = 0  
    url3 = timeslotsUrl+"/"+name
    dentTimeslotsQuery = makeGetReq(url3)
    for key2 in dentTimeslotsQuery['timeslots']:
        if startTime == str(key2['startTime']):
            time = key2['id']
    #Get one specific timeslot
    url4 = timeslotsUrl+"/"+name+"/"+str(time)
    timeslotQuery = makeGetReq(url4)
    if (timeslotQuery['timeslot']['booked'] == True):
        res = "This appointment slot is unavailable. Please choose another timeslot!"
        resAdd = getName(name)
        res = res +"\n"+ "These are the available timeslots : \n"+ resAdd
        return res
    
    f=open("./url.txt", "w+")
    f.write(url4)
    f.close
    
    #install requests and do a put call to reserve the booking
    r = requests.put(url4+"/reserve")
    res = "Your appointment has been made with Dr " +name+ " at " + str(timeslotQuery['timeslot']['startTime']) + \
            " till " + str(timeslotQuery['timeslot']['endTime']) + "  today."
    
    return res

def getCancel():
    f=open("./name.txt", "r")
    name =f.read()
    f=open("./url.txt", "r")
    url =f.read()
    timeslotQuery = makeGetReq(url)
    r = requests.put(url+"/cancel")
    res = "Your appointment with Dr " +name+ " at " + str(timeslotQuery['timeslot']['startTime']) + \
            " till " + str(timeslotQuery['timeslot']['endTime']) + "  today has been cancelled. Have a nice day!"

def processRequest(req):

    if req.get("queryResult").get("action") == "get-choice":
        res = getChoice()

    if req.get("queryResult").get("action") == "get-name":
        f=open("./name.txt", "w+")
        name = req.get("queryResult").get("parameters").get("Name")
        res = getName(name)
        f.write(name)
        f.close
    
    if req.get("queryResult").get("action") == "get-time":
        #Got Dentist Timeslot Details
        f=open("./name.txt", "r")
        contents =f.read()
        name = contents
        startTime = req.get("queryResult").get("parameters").get("Number")
        res = getTime(name,startTime)
        
    ## check everywhere , if there is anothing booked, store its name and id and make url
    if req.get("queryResult").get("action") == "cancel":
        res = getCancel()

    return {
    "fulfillmentText": res
    }

response = processRequest(data)

response = json.dumps(response, indent=4)
print(response)
# return {
# "fulfillmentText": response
# }