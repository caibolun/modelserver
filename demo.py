#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-28 21:58:15
LastEditTime: 2022-02-28 23:07:05
'''
from ModelServer import Client
client = Client()
ret, resp = client.call('/home/qspace/data/mmbizimggeneralclassify/poemclassify_unix', 'hello world')
print (ret, resp)
