# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json,os,sys
from flask import request, g, jsonify

from . import Resource
from .. import schemas


class Timeslots(Resource):

    def get(self):
        with open('/mnt/c/Users/snb19/Downloads/COMP9322-master/9322Ass1/timeslotsAPI/app/demo/v1/api/timeslots.json') as json_data:
            d = json.load(json_data)
        return jsonify({"timeslots":d['timeslots']})
