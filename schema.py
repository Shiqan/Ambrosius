#!/usr/bin/env python
"""Simple draft client with websockets for Vainglory, but more or less usable for whatever draft you want..."""

import json
import logging
import os
from collections import namedtuple

from graphene import ID, Boolean, Date, Field, Int, List, ObjectType, String

import vgapi


def transform(data):
    response = []
    matches = data['data']
    for match in matches:
        processed_match = Match(
            id = match['id'],
            createdAt = match['attributes']['createdAt'],
            duration = match['attributes']['duration'],
            gameMode = match['attributes']['gameMode'],
            shardId = match['attributes']['shardId'],
            patchVersion = match['attributes']['patchVersion'],
            endGameReason = match['attributes']['stats']['endGameReason'],
            queue = match['attributes']['stats']['queue'],
            rosters = []
        )

        rosters = []
        for roster in match['relationships']['rosters']['data']:
            roster_data = [i for i in data['included'] if i['id'] == roster['id']][0]
            processed_roster = Roster(
                id = roster_data['id'],
                aces_earned = roster_data['attributes']['stats']['acesEarned'],
                gold = roster_data['attributes']['stats']['gold'],
                heroKills = roster_data['attributes']['stats']['heroKills'],
                krakenCaptures =roster_data['attributes']['stats']['krakenCaptures'],
                side = roster_data['attributes']['stats']['side'],
                turretKills = roster_data['attributes']['stats']['turretKills'],
                turretsRemaining = roster_data['attributes']['stats']['turretsRemaining'],
                participants = [] 
            )
            
            participants = []
            for participant in roster_data['relationships']['participants']['data']:
                participant_data = [i for i in data['included'] if i['id'] == participant['id']][0]
        
                processed_participant = Participant(
                    id = participant_data['id'],
                    player_id = participant_data['relationships']['player']['data']['id'],
                    actor = participant_data['attributes']['actor'],
                    kills = participant_data['attributes']['stats']['kills'],
                    assists = participant_data['attributes']['stats']['assists'],
                    deaths = participant_data['attributes']['stats']['deaths'],
                    crystalMineCaptures = participant_data['attributes']['stats']['crystalMineCaptures'],
                    goldMindCaptures = participant_data['attributes']['stats']['crystalMineCaptures'],
                    krakenCaptures = participant_data['attributes']['stats']['krakenCaptures'],
                    turretCaptures = participant_data['attributes']['stats']['turretCaptures'],
                    winner = participant_data['attributes']['stats']['winner'],
                    farm = participant_data['attributes']['stats']['farm'],
                    minionKills = participant_data['attributes']['stats']['minionKills'],
                    nonJungleMinionKills = participant_data['attributes']['stats']['nonJungleMinionKills'],
                    jungleKills = participant_data['attributes']['stats']['jungleKills'],
                    firstAfkTime = participant_data['attributes']['stats']['firstAfkTime'],
                    wentAfk = participant_data['attributes']['stats']['wentAfk'],
                    skinKey= participant_data['attributes']['stats']['skinKey'],
                    karmaLevel = participant_data['attributes']['stats']['karmaLevel'],
                    level = participant_data['attributes']['stats']['level'],
                    skillTier = participant_data['attributes']['stats']['skillTier'],
                    itemGrants = participant_data['attributes']['stats']['itemGrants'],
                    itemSells = participant_data['attributes']['stats']['itemSells'],
                    itemUses = participant_data['attributes']['stats']['itemUses'],
                    items= participant_data['attributes']['stats']['items'],
                )
                participants.append(processed_participant)
            
            processed_roster.participants = participants
            rosters.append(processed_roster)
        
        processed_match.rosters = rosters
        response.append(processed_match)
    return response


def _json_object_hook(d):
    return namedtuple('X', d.keys(), rename=True)(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

class Participant(ObjectType):
    id = ID()
    player_id = ID()
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
    
    itemGrants = String()
    itemSells = String()
    itemUses = String()
    items = String()

class Roster(ObjectType):
    id = ID() 
    aces_earned = Int()
    gold = Int()
    heroKills = Int()
    krakenCaptures = Int()
    side = String()
    turretKills = Int()
    turretsRemaining = Int()
    participants = List(Participant)

class Match(ObjectType):
    id = ID()
    createdAt = Date()
    duration = Int()
    gameMode  = String()
    shardId = String()
    patchVersion = String()
    endGameReason = String()
    queue = String()
    rosters = List(Roster)


class Player(ObjectType):
    id = ID()
    shardId = String()
    name = String()
    lifetimeGold = Int()
    lossStreak = Int()
    winStreak = Int()
    played = Int()
    played_ranked = Int()
    wins = Int()
    xp = Int()


class Query(ObjectType):
    matches = List(Match)

    def resolve_matches(self, args):
        # 2537169e-2619-11e5-91a4-06eb725f8a76

        api = vgapi.VaingloryApi(os.environ.get('API_KEY', None))
        m = api.matches("eu", limit=5, playerId=["2537169e-2619-11e5-91a4-06eb725f8a76"])
        transformed_match = transform(m)
        
        # x = json2obj(json.dumps(transformed_match))
        # logging.error(x)
        return transformed_match
