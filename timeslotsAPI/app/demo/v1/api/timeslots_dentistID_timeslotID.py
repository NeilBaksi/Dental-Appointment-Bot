# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import json,os,sys
from flask import request, g, jsonify,make_response

from . import Resource
from .. import schemas


class TimeslotsDentistidTimeslotid(Resource):

    def get(self, dentistID, timeslotID):
        if dentistID == 0:
            return make_response(jsonify({"message": "Dentist not found.", "id": dentistID}), 404)
        if timeslotID == 0:
            return make_response(jsonify({"message": "Timeslot not found.", "id": timeslotID}), 404)

        with open(sys.path[0]+'/v1/api/timeslots.json') as json_data:
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
                return jsonify({"timeslot":d['timeslots'][var]['timeslots'][var2]})
            else:
                return make_response(jsonify({"message": "Timeslot not found.", "id": timeslotID}), 404)
        else:
            return make_response(jsonify({"message": "Dentist not found.", "id": dentistID}), 404)
        