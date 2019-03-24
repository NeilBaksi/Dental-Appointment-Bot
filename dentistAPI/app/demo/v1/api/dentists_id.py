# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import json
from flask import request, g, jsonify, make_response

from . import Resource
from .. import schemas


class DentistsId(Resource):

    def get(self, id):
        if id == 0:
            return make_response(jsonify({"message": "Dentist not found.", "id": id}), 404)
        with open('/mnt/c/Users/snb19/Downloads/COMP9322-master/9322Ass1/dentistAPI/app/demo/v1/api/dentists.json') as json_data:
            d = json.load(json_data)
            var = id-1
            try:
                dentist = jsonify(d['dentists'][var]['id'])
            except IndexError:
                dentist = ""
        if dentist != "":
            return jsonify(d['dentists'][var])
        else:
            return make_response(jsonify({"message": "Dentist not found.", "id": id}), 404)


    def delete(self, id):

        return None, 200, None