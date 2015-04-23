# -*- coding: utf-8 -*-
from django.db import models
from django.forms.models import model_to_dict

from datetime import datetime
import time


# Create your models here.
class Node(models.Model):
    #node_id = models.CharField(max_length=30, unique=True, db_index=True)
    node_name = models.CharField(max_length=30, unique=True)
    category = models.CharField(max_length=20, default='switch')
    loc = models.CharField(max_length=20, default="0 0")

    class Meta:
        db_table = 'node'

    def get_dict(self):
        dic = model_to_dict(self)
        #dic.pop('id')
        return dic


class Link(models.Model):
    link_id = models.CharField(max_length=70, unique=True, db_index=True)
    source_node = models.ForeignKey(Node, related_name='+')
    dest_node = models.ForeignKey(Node, related_name='+')
    load_s2d = models.FloatField(default=0.0)
    load_d2s = models.FloatField(default=0.0)
    curve = models.FloatField(default=0.0)

    class Meta:
        db_table = 'link'

    def get_dict(self):
        dic = model_to_dict(self)
        dic['source_node_id'] = self.source_node_id
        dic['dest_node_id'] = self.dest_node_id
        dic['source_node_name'] = self.source_node.node_name
        dic['dest_node_name'] = self.dest_node.node_name
        dic.pop('source_node')
        dic.pop('dest_node')
        dic['load_s2d'] = str(round(self.load_s2d,2)) + ' Mbps'
        dic['load_d2s'] = str(round(self.load_s2d,2)) + ' Mbps'
        return dic


class LinkLoad(models.Model):
    link = models.ForeignKey(Link, related_name='link_load')
    bytes_s2d = models.FloatField(default=0.0)
    bytes_d2s = models.FloatField(default=0.0)
    update_time = models.BigIntegerField(blank=True, null=True)


class MiniNode(models.Model):
    node_id = models.CharField(max_length=30, unique=True, db_index=True)
    node_name = models.CharField(max_length=30, unique=True)
    category = models.CharField(max_length=20, default='switch')
    loc = models.CharField(max_length=20, default="0 0")

    class Meta:
        db_table = 'mini_node'

    def get_dict(self):
        dic = model_to_dict(self)
        #dic.pop('id')
        return dic


class MiniLink(models.Model):
    link_id = models.CharField(max_length=70, unique=True, db_index=True)
    source_node = models.ForeignKey(MiniNode, related_name='+')
    dest_node = models.ForeignKey(MiniNode, related_name='+')
    curve = models.FloatField(default=0.0)

    class Meta:
        db_table = 'mini_link'

    def get_dict(self):
        dic = model_to_dict(self)
        dic['source_node_id'] = self.source_node_id
        dic['dest_node_id'] = self.dest_node_id
        dic['source_node_name'] = self.source_node.node_name
        dic['dest_node_name'] = self.dest_node.node_name

        return dic
