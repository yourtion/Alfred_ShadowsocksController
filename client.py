#!/usr/bin/python
# -*- coding: utf-8 -*- 

URL_SERVER="/servers"
URL_STATUS="/status"
URL_TOGGLE="/toggle"
URL_MODE="/mode"

import httplib
import json

class Client:
 
  httpClient = None
  
  def __init__(self):
    self.httpClient = httplib.HTTPConnection('localhost', 9528, timeout=30)

  def _getServers(self):
    self.httpClient.request('GET', URL_SERVER)
    response = self.httpClient.getresponse()
    if response.status == 200 and response.reason == "OK":
      return json.loads(response.read())

  def _getStatus(self):
    self.httpClient.request('GET', URL_STATUS)
    response = self.httpClient.getresponse()
    if response.status == 200 and response.reason == "OK":
      data = json.loads(response.read())
      return data['enable']

  def _getMode(self):
    self.httpClient.request('GET', URL_MODE)
    response = self.httpClient.getresponse()
    if response.status == 200 and response.reason == "OK":
      data = json.loads(response.read())
      return data['mode']
       
  def getList(self):
    try:
      list = self._getServers()
      enable = self._getStatus()
      enableStr = "true" if enable else "false"
      mode = self._getMode()
      print('<?xml version="1.0"?>')
      print('<items>')
      print("  <item uid=\"octal\" valid=\"yes\" arg=\""+enableStr+"\">")
      print("    <title>Enable: "+enableStr+"</title>")
      print('    <icon>icon.png</icon>')
      print('  </item>')
      print("  <item uid=\"octal\" valid=\"yes\" arg=\""+mode+"\">")
      print("    <title>Mode:"+mode+"</title>")
      print('    <icon>icon.png</icon>')
      print('  </item>')
      for item in list:
        print("  <item uid=\"octal\" valid=\"yes\" arg=\""+item['id']+"\">")
        print("    <title>"+item['note']+"</title>")
        print('    <icon>icon.png</icon>')
        print('  </item>')
      print('</items>')
    except Exception, e:
      print e
    

