# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import json,os,sys
from flask import request, g, jsonify

from . import Resource
from .. import schemas


class Dentists(Resource):

    def get(self):
        with open('/mnt/c/Users/snb19/Downloads/COMP9322-master/9322Ass1/dentistAPI/app/demo/v1/api/dentists.json') as json_data:
            d = json.load(json_data)
        #return jsonify(d), 200, None
        return jsonify({"dentists":d['dentists']})

    def post(self):
        with open('/mnt/c/Users/snb19/Downloads/COMP9322-master/9322Ass1/dentistAPI/app/demo/v1/api/dentists.json') as json_data:
            d = json.load(json_data)
        dentist = {
			'id': d['dentists'][-1]['id'] + 1,
            'name': g.json['name'],
			'location': g.json['location'],
			'spec' :g.json['specialisation']
		}
        d['dentists'].append(dentist)

        with open("/mnt/c/Users/snb19/Downloads/COMP9322-master/9322Ass1/dentistAPI/app/demo/v1/api/dentists.json", "w") as jsonFile:
            json.dump(d, jsonFile, indent=4)
    
        return jsonify({"dentists":d['dentists']})



