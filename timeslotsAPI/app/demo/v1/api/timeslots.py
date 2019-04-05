# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json,os,sys
from flask import request, g, jsonify

from . import Resource
from .. import schemas


class Timeslots(Resource):
    def get(self):
        filename = sys.path[0]+'/v1/api/timeslots.json'
        with open(filename) as json_data:
            d = json.load(json_data)
        return jsonify({"timeslots":d['timeslots']})

    def post(self):
        with open(filename) as json_data:
            d = json.load(json_data)
        newDentist = {
            "dentistID": g.json['dentistID'],
            "timeslots": [
                {
                    "id": 1,
                    "startTime": 8,
                    "endTime": 9,
                    "booked": False
                },
                {
                    "id": 2,
                    "startTime": 9,
                    "endTime": 10,
                    "booked": False
                },
                {
                    "id": 3,
                    "startTime": 10,
                    "endTime": 11,
                    "booked": False
                },
                {
                    "id": 4,
                    "startTime": 11,
                    "endTime": 12,
                    "booked": False
                },
                {
                    "id": 5,
                    "startTime": 12,
                    "endTime": 1,
                    "booked": False
                },
                {
                    "id": 6,
                    "startTime": 1,
                    "endTime": 2,
                    "booked": False
                },
                {
                    "id": 7,
                    "startTime": 2,
                    "endTime": 3,
                    "booked": False
                },
                {
                    "id": 8,
                    "startTime": 3,
                    "endTime": 4,
                    "booked": False
                },
                {
                    "id": 9,
                    "startTime": 4,
                    "endTime": 5,
                    "booked": False
                }
            ]
        }
        d['timeslots'].append(newDentist)
        filename = sys.path[0]+'/v1/api/timeslots.json'
        with open(filename, "w") as jsonFile:
            json.dump(d, jsonFile, indent=4)
    
        return jsonify({"timeslots":d['timeslots']})