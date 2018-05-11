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
        
class LevelUp(TelemetryFactory):
    """Concrete factory for Level Up event."""
    def parse(self):
        return model.TelemetryLevelUp(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor'],
            level = self.payload['Level'],
            lifetimegold = self.payload['LifetimeGold']
        )

class BuyItem(TelemetryFactory):
    """Concrete factory for Buy Item event."""
    def parse(self):
        x, y, z = self.payload['Position']
        return model.TelemetryBuyItem(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor'],
            item = self.payload['Item'],
            cost = self.payload['Cost'],
            remaininggold = self.payload['RemainingGold'],
            position =  model.Position(
                x = x,
                y = y,
                z = z
            )
        )

class SellItem(TelemetryFactory):
    """Concrete factory for Sell Item event."""
    def parse(self):
        return model.TelemetrySellItem(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor'],
            item = self.payload['Item'],
            cost = self.payload['Cost']
        )

class LearnAbility(TelemetryFactory):
    """Concrete factory for LearnAbility event."""
    def parse(self):
        return model.TelemetryLearnAbility(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor'],
            ability = self.payload['Ability'],
            level = self.payload['Level']
        )

class UseAbility(TelemetryFactory):
    """Concrete factory for Use Ability event."""
    def parse(self):
        x, y, z = self.payload['Position']
        tx, ty, tz =  self.payload['TargetPosition']
        return model.TelemetryUseAbility(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor'],
            ability = self.payload['Ability'],
            position =  model.Position(
                x = x,
                y = y,
                z = z
            ),
            target = self.payload['TargetActor'],            
            target_position =  model.Position(
                x = tx,
                y = ty,
                z = tz
            )
        )

class UseItemAbility(TelemetryFactory):
    """Concrete factory for Use Item Ability event."""
    def parse(self):
        x, y, z = self.payload['Position']
        tx, ty, tz =  self.payload['TargetPosition']
        return model.TelemetryUseItemAbility(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor'],
            ability = self.payload['Ability'],
            position =  model.Position(
                x = x,
                y = y,
                z = z
            ),
            target = self.payload['TargetActor'],            
            target_position =  model.Position(
                x = tx,
                y = ty,
                z = tz
            )
        )

class DealDamage(TelemetryFactory):
    """Concrete factory for Deal Damage event."""
    def parse(self):
        return model.TelemetryDealDamage(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor'],
            target = self.payload['Target'],
            source = self.payload['Source'],
            damage = self.payload['Damage'],
            dealt = self.payload['Dealt'],
            is_hero = self.payload['IsHero'],
            target_is_hero = self.payload['TargetIsHero']
        )

class HealTarget(TelemetryFactory):
    """Concrete factory for Heal Target event."""
    def parse(self):
        return model.TelemetryHealTarget(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor'],
            target = self.payload['TargetActor'],
            target_team = self.payload['TargetTeam'],
            source = self.payload['Source'],
            heal = self.payload['Heal'],
            healed = self.payload['Healed'],
            is_hero = self.payload['IsHero'],
            target_is_hero = self.payload['TargetIsHero']
        )

class Vampirism(TelemetryFactory):
    """Concrete factory for Vampirism event."""
    def parse(self):
        return model.TelemetryVampirism(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor'],
            target = self.payload['TargetActor'],
            target_team = self.payload['TargetTeam'],
            source = self.payload['Source'],
            vamp = self.payload['Vamp'],
            is_hero = self.payload['IsHero'],
            target_is_hero = self.payload['TargetIsHero']
        )

class KillActor(TelemetryFactory):
    """Concrete factory for Kill Actor event."""
    def parse(self):
        x, y, z = self.payload['Position']
        return model.TelemetryKillActor(
            time = self.time,
            type = self.type,
            team = self.payload['Team'],
            actor = self.payload['Actor'],
            killed = self.payload['Killed'],
            killed_team = self.payload['KilledTeam'],
            gold = self.payload['Gold'],
            is_hero = self.payload['IsHero'],
            target_is_hero = self.payload['TargetIsHero'],
            position = model.Position(
                x = x,
                y = y,
                z = z
            )
        )