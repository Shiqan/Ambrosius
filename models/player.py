#!/usr/bin/python
# -*- coding: utf-8 -*-
""" GraphQL Player """

from graphene import ID, Field, Int, ObjectType, String


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
