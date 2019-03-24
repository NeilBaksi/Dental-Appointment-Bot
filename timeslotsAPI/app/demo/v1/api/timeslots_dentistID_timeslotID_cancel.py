# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import json,os,sys
from flask import request, g, jsonify,make_response
from . import Resource
from .. import schemas


class TimeslotsDentistidTimeslotidCancel(Resource):

    def put(self, dentistID, timeslotID):
        if dentistID == 0:
            return make_response(jsonify({"message": "Dentist not found.", "id": dentistID}), 404)
        if timeslotID == 0:
            return make_response(jsonify({"message": "Timeslot not found.", "id": timeslotID}), 404)

        with open('/mnt/c/Users/snb19/Downloads/COMP9322-master/9322Ass1/timeslotsAPI/app/demo/v1/api/timeslots.json') as json_data:
            d = json.load(json_data)
            var = dentistID - 1
            var2 = timeslotID -1        
        try:
            dentist = jsonify(d['timeslots'][var])
        except IndexError:
            dentist = ""
        if dentist != "":
            try:
                timeslot = jsonify(d['timeslots'][var]['timeslots'][var2])
            except IndexError:
                timeslot = ""
            if timeslot != "":
                d['timeslots'][var]['timeslots'][var2]['booked'] = False
                with open("/mnt/c/Users/snb19/Downloads/COMP9322-master/9322Ass1/timeslotsAPI/app/demo/v1/api/timeslots.json", "w") as jsonFile:
                    json.dump(d, jsonFile, indent=4)
                return jsonify(d['timeslots'][var]['timeslots'][var2])
            else:
                return make_response(jsonify({"message": "Timeslot not found.", "id": timeslotID}), 404)
        else:
            return make_response(jsonify({"message": "Dentist not found.", "id": dentistID}), 404)