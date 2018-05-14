#!/usr/bin/python
# -*- coding: utf-8 -*-
""" GraphQL Relay Nodes """

from graphene import ObjectType
from graphene.relay import Node

from models.match import Match

class MatchNode(ObjectType):
    class Meta:
        interfaces = (Node, )

    @classmethod
    def get_node(cls, info, id):
        return id