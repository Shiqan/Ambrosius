#!/usr/bin/python
# -*- coding: utf-8 -*-
""" GraphQL Participant """

from graphene import ID, Boolean, Field, Int, List, ObjectType, String
from models.player import Player
from models.item import Item


class Participant(ObjectType):
    participant_id = ID()
    player = Field(Player)
    actor = String()
    kills = Int()
    assists = Int()
    deaths = Int()
    crystalMineCaptures = Int()
    goldMindCaptures = Int()
    krakenCaptures = Int()
    turretCaptures = Int()
    winner = Boolean()
    farm = Int()
    minionKills = Int()
    nonJungleMinionKills = Int()
    jungleKills = Int()
    firstAfkTime = Int()
    wentAfk = Boolean()
    skinKey = String()
    karmaLevel = String()
    level = Int()
    skillTier = Int()
    itemGrants = List(Item)
    itemSells = List(Item)
    itemUses = List(Item)
    items = List(Item)
