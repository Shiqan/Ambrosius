#!/usr/bin/python
# -*- coding: utf-8 -*-
""" GraphQL Telemetry (events) """

from graphene import (ID, Boolean, Date, Field, Int, Interface, List, ObjectType, String, Union)


class TelemetryData(ObjectType):
    telemetry_id = ID()
    name = String()
    url = String()
    createdAt = Date()

class TelemetryBaseEvent(Interface):
    time = Date()
    type = String()

class TelemetryHeroSelect(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent,)

    hero = String()
    team = String()
    player = String()
    handle = String()

class TelemetryHeroBan(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent,)

    hero = String()
    team = String()

class TelemetryHeroSkin(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent,)
    hero = String()
    skin = String()

class TelemetryHeroSwapPayload(ObjectType):
    hero = String()
    team = String()
    player = String()

class TelemetryHeroSwap(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent,)

    swap = List(TelemetryHeroSwapPayload)

class TelemetryPlayerFirstSpawn(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )
    
    team = String()
    actor = String()

class TelemetryEvent(Union):
    class Meta:
        types = (TelemetryHeroBan, TelemetryHeroSelect, TelemetryHeroSkin, TelemetryHeroSwap, TelemetryPlayerFirstSpawn)