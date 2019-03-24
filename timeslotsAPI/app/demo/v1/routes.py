# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.timeslots_dentistID import TimeslotsDentistid
from .api.timeslots import Timeslots
from .api.timeslots_dentistID_timeslotID import TimeslotsDentistidTimeslotid
from .api.timeslots_dentistID_timeslotID_cancel import TimeslotsDentistidTimeslotidCancel
from .api.timeslots_dentistID_timeslotID_reserve import TimeslotsDentistidTimeslotidReserve


routes = [
    dict(resource=TimeslotsDentistid, urls=['/timeslots/<int:dentistID>'], endpoint='timeslots_dentistID'),
    dict(resource=Timeslots, urls=['/timeslots'], endpoint='timeslots'),
    dict(resource=TimeslotsDentistidTimeslotid, urls=['/timeslots/<int:dentistID>/<int:timeslotID>'], endpoint='timeslots_dentistID_timeslotID'),
    dict(resource=TimeslotsDentistidTimeslotidCancel, urls=['/timeslots/<int:dentistID>/<int:timeslotID>/cancel'], endpoint='timeslots_dentistID_timeslotID_cancel'),
    dict(resource=TimeslotsDentistidTimeslotidReserve, urls=['/timeslots/<int:dentistID>/<int:timeslotID>/reserve'], endpoint='timeslots_dentistID_timeslotID_reserve'),
]