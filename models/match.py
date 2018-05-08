#!/usr/bin/python
# -*- coding: utf-8 -*-
""" GraphQL Match """

from graphene import ID, Date, Field, Int, List, ObjectType, String
from models.roster import Roster
from models.telemetry import TelemetryData, TelemetryEvent


class Match(ObjectType):
    match_id = ID()
    createdAt = Date()
    duration = Int()
    gameMode  = String()
    shardId = String()
    patchVersion = String()
    endGameReason = String()
    queue = String()
    rosters = List(Roster)
    telemetry_data = Field(TelemetryData)
    telemetry = List(TelemetryEvent)
