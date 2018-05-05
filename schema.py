#!/usr/bin/python
# -*- coding: utf-8 -*-
""" GraphQL wrapper for Vainglory API """

import abc
import json
import logging
import os
from collections import namedtuple

import requests

import vgapi
from graphene import (ID, Boolean, Date, Field, Int, Interface, List, ObjectType, String, Union)


def event_to_object(event_types, event):
    """Map a telemetry event to a factory based on the event type."""
    for t in event_types:
        if t.__name__ == event['type']:
            return t(event).parse()

def transform_telemetry(events):
    processed_telemetry = []
    event_types = TelemetryFactory.__subclasses__()

    for event in events:
        e = event_to_object(event_types, event)
        if e != None:
            processed_telemetry.append(e)
    return processed_telemetry

# TODO can this be mapped automatically somehow?
def transform_player(player_data):
    processed_player = Player(
        player_id = player_data['id'], 
        name = player_data['attributes']['name'],
        patchVersion = player_data['attributes']['patchVersion'],
        shardId = player_data['attributes']['shardId'],
        lifetimeGold = player_data['attributes']['stats']['lifetimeGold'],
        lossStreak = player_data['attributes']['stats']['lossStreak'],
        winStreak = player_data['attributes']['stats']['winStreak'],
        elo_earned_season_4 = player_data['attributes']['stats']['elo_earned_season_4'],
        elo_earned_season_5 = player_data['attributes']['stats']['elo_earned_season_5'],
        elo_earned_season_6 = player_data['attributes']['stats']['elo_earned_season_6'],
        elo_earned_season_7 = player_data['attributes']['stats']['elo_earned_season_7'],
        elo_earned_season_8 = player_data['attributes']['stats']['elo_earned_season_8'],
        elo_earned_season_9 = player_data['attributes']['stats']['elo_earned_season_9'],
        gamesPlayed = GamesPlayed(
            aral = player_data['attributes']['stats']['gamesPlayed']['aral'],
            blitz = player_data['attributes']['stats']['gamesPlayed']['blitz'], 
            blitz_rounds = player_data['attributes']['stats']['gamesPlayed']['blitz_rounds'],
            casual = player_data['attributes']['stats']['gamesPlayed']['casual'],
            casual_5v5 = player_data['attributes']['stats']['gamesPlayed']['casual_5v5'],
            ranked = player_data['attributes']['stats']['gamesPlayed']['ranked']
        ),
        played = player_data['attributes']['stats']['played'],
        played_ranked = player_data['attributes']['stats']['played_ranked'],
        played_aral = player_data['attributes']['stats']['played_aral'],
        played_casual = player_data['attributes']['stats']['played_casual'],
        played_blitz = player_data['attributes']['stats']['played_blitz'],
        rankPoints = RankedPoints(
            blitz=player_data['attributes']['stats']['rankPoints']['blitz'], 
            ranked=player_data['attributes']['stats']['rankPoints']['ranked']
        ),
        guildTag = player_data['attributes']['stats']['guildTag'],
        karmaLevel = player_data['attributes']['stats']['karmaLevel'],
        level = player_data['attributes']['stats']['level'],
        skillTier = player_data['attributes']['stats']['skillTier'],
        wins = player_data['attributes']['stats']['wins'],
        xp = player_data['attributes']['stats']['xp']
    )
    return processed_player

def transform(data):
    response = []
    matches = data['data']
    for match in matches:
        telemetry_id = match['relationships']['assets']['data'][0]['id']
        telemetry_data = [i for i in data['included'] if i['id'] == telemetry_id][0]
        processed_telemetry_data = TelemetryData(
            telemetry_id = telemetry_data['id'],
            name = telemetry_data['attributes']['name'],
            url = telemetry_data['attributes']['URL'], 
            createdAt = telemetry_data['attributes']['createdAt']
        )
        logging.error(telemetry_data)
        
        # TODO use api wrapper
        events = requests.get(processed_telemetry_data.url).json()
        processed_telemetry = transform_telemetry(events)
        # logging.error(processed_telemetry)

        processed_match = Match(
            match_id = match['id'],
            createdAt = match['attributes']['createdAt'],
            duration = match['attributes']['duration'],
            gameMode = match['attributes']['gameMode'],
            shardId = match['attributes']['shardId'],
            patchVersion = match['attributes']['patchVersion'],
            endGameReason = match['attributes']['stats']['endGameReason'],
            queue = match['attributes']['stats']['queue'],
            rosters = [],
            telemetry_data = processed_telemetry_data,
            telemetry = processed_telemetry
        )

        rosters = []
        for roster in match['relationships']['rosters']['data']:
            roster_data = [i for i in data['included'] if i['id'] == roster['id']][0]
            processed_roster = Roster(
                roster_id = roster_data['id'],
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
                player_data = [i for i in data['included'] if i['id'] == participant_data['relationships']['player']['data']['id']][0]
                processed_player = transform_player(player_data)
        
                processed_participant = Participant(
                    participant_id = participant_data['id'],
                    player = processed_player,
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
                    itemGrants = [Item(name=i, uses=j) for i, j in participant_data['attributes']['stats']['itemGrants'].items()],
                    itemSells = [Item(name=i, uses=j) for i, j in participant_data['attributes']['stats']['itemSells'].items()],
                    itemUses = [Item(name=i, uses=j) for i, j in participant_data['attributes']['stats']['itemUses'].items()],
                    items= [Item(name=i) for i in participant_data['attributes']['stats']['items']],
                )               
                participants.append(processed_participant)
            
            processed_roster.participants = participants
            rosters.append(processed_roster)
        
        processed_match.rosters = rosters
        response.append(processed_match)
    return response

# TODO Move to seprate folders
class TelemetryFactory():
    """Abstract factory interface for Telemetry events."""
    __metaclass__ = abc.ABCMeta
    def __init__(self, data):
        self.payload = data['payload']
        self.time = data['time']
        self.type = data['type']

    @abc.abstractmethod
    def parse(self):
        pass

class HeroSelect(TelemetryFactory):
    """Concrete factory for Hero Select event."""  
    def parse(self):
        return TelemetryHeroSelect(
            time = self.time,
            type = self.type,
            hero = self.payload['Hero'],
            team = self.payload['Team'],
            player = self.payload['Player'],
            handle = self.payload['Handle']
        )

class HeroSkinSelect(TelemetryFactory):
    """Concrete factory for Hero Skin Select event."""
    def parse(self):
        return TelemetryHeroSkin(
            time = self.time,
            type = self.type,
            hero = self.payload['Hero'],
            skin = self.payload['Skin']
        )

class HeroBan(TelemetryFactory):
    """Concrete factory for Hero Ban event."""
    def parse(self):
        return TelemetryHeroBan(
            time = self.time,
            type = self.type,
            hero = self.payload['Hero'],
            team = self.payload['Team']
        )

class HeroSwap(TelemetryFactory):
    """Concrete factory for Hero Ban event."""
    def parse(self):
        return TelemetryHeroSwap(
            time = self.time,
            type = self.type,
            swap = [TelemetryHeroSwapPayload(
                hero = i['Hero'],
                team = i['Team'],
                player = i['Player'],
            ) for i in self.payload]
        )

class PlayerFirstSpawn(TelemetryFactory):
    """Concrete factory for Player First Spawn event."""
    def parse(self):
        return TelemetryPlayerFirstSpawn(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor']
        )

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

class GamesPlayed(ObjectType):
    aral = Int()
    blitz = Int()
    blitz_rounds = Int()
    casual = Int()
    casual_5v5 = Int()
    ranked = Int()


class RankedPoints(ObjectType):
    blitz = Int()
    ranked = Int()


class Player(ObjectType):
    player_id = ID()
    name = String()
    patchVersion = String()
    shardId = String()
    lifetimeGold = Int()
    lossStreak = Int()
    winStreak = Int()
    elo_earned_season_4 = Int()
    elo_earned_season_5 = Int()
    elo_earned_season_6 = Int()
    elo_earned_season_7 = Int()
    elo_earned_season_8 = Int()
    elo_earned_season_9 = Int()
    gamesPlayed = Field(GamesPlayed)
    played = Int()
    played_ranked = Int()
    played_aral = Int()
    played_casual = Int()
    played_blitz = Int()
    rankPoints = Field(RankedPoints)
    guildTag = String()
    karmaLevel = Int()
    level = Int()
    skillTier = Int()
    wins = Int()
    xp = Int()

class Item(ObjectType):
    name = String()
    uses = Int()

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


class Query(ObjectType):
    matches = List(Match, player_id=ID())
    player = Field(Player, player_id=ID())

    def resolve_matches(self, info, player_id):
        # "2537169e-2619-11e5-91a4-06eb725f8a76"
        api = vgapi.VaingloryApi(os.environ.get('API_KEY', "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJkNzYzYTkyMC1kYzMyLTAxMzQtYTc1NC0wMjQyYWMxMTAwMDMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNDg3ODgwOTcwLCJwdWIiOiJzZW1jIiwidGl0bGUiOiJ2YWluZ2xvcnkiLCJhcHAiOiJkNzYxY2Q1MC1kYzMyLTAxMzQtYTc1My0wMjQyYWMxMTAwMDMiLCJzY29wZSI6ImNvbW11bml0eSIsImxpbWl0IjoxfQ.GzkEYeb8r3x6z6_vj5E7IICYy_RvsOp4gnfTlthbEJs"))
        m = api.matches("eu", limit=5, playerId=[player_id])

        # logging.error(m)
        transformed = transform(m)
        return transformed

    def resolve_player(self, info, player_id):
        api = vgapi.VaingloryApi(os.environ.get('API_KEY', None))
        p = api.player(player_id, "eu")
        # logging.error(p)
        transformed = transform_player(p['data'])
        return transformed
