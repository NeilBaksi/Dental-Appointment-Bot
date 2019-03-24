# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import json
from flask import request, g, jsonify, make_response

from . import Resource
from .. import schemas


class TimeslotsDentistid(Resource):

    def get(self, dentistID):
        if dentistID == 0:
            return make_response(jsonify({"message": "Dentist not found.", "id": dentistID}), 404)
        with open('/mnt/c/Users/snb19/Downloads/COMP9322-master/9322Ass1/timeslotsAPI/app/demo/v1/api/timeslots.json') as json_data:
            d = json.load(json_data)
            var = dentistID-1
            try:
                timeslot = jsonify(d['timeslots'][var])
            except IndexError:
                timeslot = ""
        if timeslot != "":
            return jsonify(d['timeslots'][var])
        else:
            return make_response(jsonify({"message": "Dentist not found.", "id": dentistID}), 404)


    def post(self, dentistID):
        if dentistID == 0:
            return make_response(jsonify({"message": "Dentist not found.", "id": dentistID}), 404)
        with open('/mnt/c/Users/snb19/Downloads/COMP9322-master/9322Ass1/timeslotsAPI/app/demo/v1/api/timeslots.json') as json_data:
            d = json.load(json_data)
            var = dentistID-1
            try:
                timeslot = {
                    'id': d['timeslots'][var]['timeslots'][-1]['id'] + 1,
                    'startTime': g.json['startTime'],
                    'endTime': g.json['startTime'] + 1,
                    'booked' : False
                }
                d['timeslots'][var]['timeslots'].append(timeslot)
                with open("/mnt/c/Users/snb19/Downloads/COMP9322-master/9322Ass1/timeslotsAPI/app/demo/v1/api/timeslots.json", "w") as jsonFile:
                    json.dump(d, jsonFile, indent=4)
            except IndexError:
                timeslot = ""
        if timeslot != "":
            return jsonify(d['timeslots'][var])
        else:
            return make_response(jsonify({"message": "Dentist not found.", "id": dentistID}), 404)
