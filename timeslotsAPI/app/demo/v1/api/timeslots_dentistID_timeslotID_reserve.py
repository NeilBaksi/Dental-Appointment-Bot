# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json,os,sys
from flask import request, g, jsonify,make_response

from . import Resource
from .. import schemas


class TimeslotsDentistidTimeslotidReserve(Resource):

    def put(self, dentistID, timeslotID):
        filename = sys.path[0]+'/v1/api/timeslots.json'
        if dentistID == 0:
            return make_response(jsonify({"message": "Dentist not found.", "id": dentistID}), 404)
        if timeslotID == 0:
            return make_response(jsonify({"message": "Timeslot not found.", "id": timeslotID}), 404)

        with open(filename) as json_data:
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
                d['timeslots'][var]['timeslots'][var2]['booked'] = True
                with open(filename, "w") as jsonFile:
                    json.dump(d, jsonFile, indent=4)
                return jsonify(d['timeslots'][var]['timeslots'][var2])
            else:
                return make_response(jsonify({"message": "Timeslot not found.", "id": timeslotID}), 404)
        else:
            return make_response(jsonify({"message": "Dentist not found.", "id": dentistID}), 404)
