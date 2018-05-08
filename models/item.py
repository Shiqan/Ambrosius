#!/usr/bin/python
# -*- coding: utf-8 -*-
""" GraphQL Item """

from graphene import Int, ObjectType, String


class Item(ObjectType):
    name = String()
    uses = Int()
