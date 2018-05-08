#!/usr/bin/python
# -*- coding: utf-8 -*-
""" GraphQL Roster """

from graphene import ID, Field, Int, List, ObjectType, String
from models.participant import Participant


class Roster(ObjectType):
    roster_id = ID() 
    aces_earned = Int()
    gold = Int()
    heroKills = Int()
    krakenCaptures = Int()
    side = String()
    turretKills = Int()
    turretsRemaining = Int()
    participants = List(Participant)
