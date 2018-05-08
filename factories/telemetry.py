#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Factories for Telemetry events """

import abc
import models.telemetry as model

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
        return model.TelemetryHeroSelect(
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
        return model.TelemetryHeroSkin(
            time = self.time,
            type = self.type,
            hero = self.payload['Hero'],
            skin = self.payload['Skin']
        )

class HeroBan(TelemetryFactory):
    """Concrete factory for Hero Ban event."""
    def parse(self):
        return model.TelemetryHeroBan(
            time = self.time,
            type = self.type,
            hero = self.payload['Hero'],
            team = self.payload['Team']
        )

class HeroSwap(TelemetryFactory):
    """Concrete factory for Hero Ban event."""
    def parse(self):
        return model.TelemetryHeroSwap(
            time = self.time,
            type = self.type,
            swap = [model.TelemetryHeroSwapPayload(
                hero = i['Hero'],
                team = i['Team'],
                player = i['Player'],
            ) for i in self.payload]
        )

class PlayerFirstSpawn(TelemetryFactory):
    """Concrete factory for Player First Spawn event."""
    def parse(self):
        return model.TelemetryPlayerFirstSpawn(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor']
        )