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

class TelemetryUseAbility(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    ability = String()
    position = Field(Position)
    target = String()
    target_position = Field(Position)

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

class TelemetryHealTarget(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    target = String()
    target_team = String()
    source = String()
    heal = Int()
    healed = Int()
    is_hero = Boolean()
    target_is_hero = Boolean()

class TelemetryVampirism(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    target = String()
    target_team = String()
    source = String()
    vamp = Int()
    is_hero = Boolean()
    target_is_hero = Boolean()

class TelemetryKillActor(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    killed = String()
    killed_team = String()
    gold = Int()
    is_hero = Boolean()
    target_is_hero = Boolean()
    position = Field(Position)

class TelemetryEarnXP(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    source = String()
    amount = Int()
    shared_with = Int()

class TelemetryNPCkillNPC(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    killed = String()
    killed_team = Int()
    gold = Int()
    is_hero = Boolean()
    target_is_hero = Boolean()
    position = Field(Position)

class TelemetryGoldFromTowerKill(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    amount = Int()

class TelemetryGoldFromGoldMine(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    amount = Int()

class TelemetryGoldFromKrakenKill(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    amount = Int()

class TelemetryGoldFromExecution(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    amount = Int()

class TelemetryExecuted(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    killed = String()
    killed_team = Int()
    gold = Int()
    is_hero = Boolean()
    target_is_hero = Boolean()
    position = Field(Position)

class TelemetryTalentEquipped(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    team = String()
    actor = String()
    talent = String()
    level = Int()

class TelemetryDraftLobby_Role_Bumped(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    mode = String()
    elo_5v5 = Int()
    elo_3v3 = Int()
    turn = Int()
    role_bumped = Int()


class TelemetryDraftLobby_AutoLocked(ObjectType):
    class Meta:
        interfaces = (TelemetryBaseEvent, )

    mode = String()
    elo_5v5 = Int()
    elo_3v3 = Int()


# TODO auto select type
class TelemetryEvent(Union):
    class Meta:
        types = (TelemetryHeroBan, TelemetryHeroSelect, TelemetryHeroSkin, TelemetryHeroSwap, TelemetryPlayerFirstSpawn, TelemetryLevelUp, TelemetryBuyItem, TelemetrySellItem, TelemetryLearnAbility, TelemetryUseAbility, TelemetryUseItemAbility,
            TelemetryDealDamage, TelemetryHealTarget, TelemetryVampirism, TelemetryKillActor, TelemetryEarnXP, TelemetryGoldFromTowerKill, TelemetryGoldFromGoldMine, TelemetryGoldFromKrakenKill, TelemetryGoldFromExecution, TelemetryExecuted,
            TelemetryNPCkillNPC, TelemetryTalentEquipped)