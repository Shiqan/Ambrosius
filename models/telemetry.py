#!/usr/bin/python
# -*- coding: utf-8 -*-
""" GraphQL Telemetry (events) """

from graphene import (ID, Boolean, Date, Field, Int, Interface, List, ObjectType, String, Union)

class Position(ObjectType):
    x = Int()
    y = Int()
    z = Int()

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

class TelemetryLevelUp(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )
    
    team = String()
    actor = String()
    level = Int()
    lifetimegold = Int()

class TelemetryBuyItem(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )
    
    team = String()
    actor = String()
    item = String()
    cost = Int()
    remaininggold = Int()
    position = Field(Position)

class TelemetrySellItem(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )
    
    team = String()
    actor = String()
    item = String()
    cost = Int()

class TelemetryLearnAbility(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    ability = String()
    level = Int()

class TelemetryUseItemAbility(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    ability = String()
    position = Field(Position)
    target = String()
    target_position = Field(Position)

class TelemetryDealDamage(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    target = String()
    source = String()
    damage = Int()
    dealt = Int()
    is_hero = Boolean()
    target_is_hero = Boolean()

# TODO auto select type
class TelemetryEvent(Union):
    class Meta:
        types = (TelemetryHeroBan, TelemetryHeroSelect, TelemetryHeroSkin, TelemetryHeroSwap, TelemetryPlayerFirstSpawn, TelemetryLevelUp, TelemetryBuyItem, TelemetrySellItem, TelemetryLearnAbility, TelemetryUseItemAbility)