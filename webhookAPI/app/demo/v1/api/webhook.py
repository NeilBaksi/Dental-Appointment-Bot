# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class Webhook(Resource):

    def post(self):
        req = request.get_json(silent=True, force=True)

        print("Request:")
        print(json.dumps(req, indent=4))

        res = processRequest(req)

        res = json.dumps(res, indent=4)
        #print(res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r


    def processRequest(req):
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = makeDentistGetReq(req)
        if yql_query is None:
            return {}
        yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
        print (yql_url)
        result = urlopen(yql_url).read()
        data = json.loads(result)
        print (data)
        res = makeWebhookResult(data)
        return res


    def makeDentistGetReq(req):
        testurl= "http://1b0422bb.ngrok.io/v1/dentists"
        fs = wget.download(url=testurl)
        with open(fs, 'r') as f:
            content = f.read()
        print(content)
        # result = req.get("queryResult")
        # parameters = result.get("parameters")
        # city = parameters.get("geo-city")
        # if city is None:
        #     return None
        # return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


    def makeWebhookResult(data):
        print ("starting makeWebhookResult...")
        query = data.get('query')
        if query is None:
            return {}

        result = query.get('results')
        if result is None:
            return {}

        channel = result.get('channel')
        if channel is None:
            return {}

        item = channel.get('item')
        location = channel.get('location')
        units = channel.get('units')
        if (location is None) or (item is None) or (units is None):
            return {}

        condition = item.get('condition')
        if condition is None:
            return {}

        # print(json.dumps(item, indent=4))

        speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
                ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

        print("Response:")
        print(speech)
        return {

        "fulfillmentText": speech,
        "source": "Yahoo Weather"
        }