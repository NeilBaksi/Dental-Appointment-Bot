# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.dentists_id import DentistsId
from .api.dentists import Dentists


routes = [
    dict(resource=DentistsId, urls=['/dentists/<int:id>'], endpoint='dentists_id'),
    dict(resource=Dentists, urls=['/dentists'], endpoint='dentists'),
]