#!/usr/bin/python
# -*- coding: utf-8 -*- 

URL_SERVER="/servers"
URL_STATUS="/status"
URL_TOGGLE="/toggle"
URL_MODE="/mode"

import httplib
import json
import urllib

class Client:
 
  httpClient = None
  
  def __init__(self):
    self.httpClient = httplib.HTTPConnection('localhost', 9528, timeout=30)

  def _post(self, url, parma):
    params = urllib.urlencode(parma)
    headers = {"Content-type": "application/x-www-form-urlencoded"
                   , "Accept": "text/plain"}
    self.httpClient.request('POST', url, params, headers)
    return self.httpClient.getresponse()

  def _parseArgs(self, str):
    return str.split(':', 1);

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

  def _setStatus(self, enable):
    parma = {enable: enable}
    res = self._post(URL_TOGGLE, parma)

  def _setStatusString(self, enable):
    if(enable == 'Enable'):
      self._setStatus(True)
    if(enable == 'Disable'):
      self._setStatus(False)

  def action(self, query):
    args = self._parseArgs(query)
    command = args[0]
    value = args[1]
    if(command == 'enable'):
      self._setStatusString(value)
      print("Set ShadowSock " + value)

  def getList(self):
    try:
      list = self._getServers()
      enable = self._getStatus()
      enableStr = "True" if enable else "False"
      enableOptStr = "Disable" if enable else "Enable"
      mode = self._getMode()
      print('<?xml version="1.0"?>')
      print('<items>')
      print("  <item uid=\"octal\" valid=\"yes\" arg=\"enable:"+enableOptStr+"\">")
      print("    <title>Enable: "+enableStr+"</title>")
      print("    <subtitle>Select to "+ enableOptStr +"</subtitle>")
      print('    <icon>icon.png</icon>')
      print('  </item>')
      print("  <item uid=\"octal\" valid=\"yes\" arg=\"mode:"+mode+"\">")
      print("    <title>Mode:"+mode+"</title>")
      print('    <icon>icon.png</icon>')
      print('  </item>')
      for item in list:
        print("  <item uid=\"octal\" valid=\"yes\" arg=\""+ "server:" +item['id']+"\">")
        print("    <title>"+item['note']+"</title>")
        print('    <icon>icon.png</icon>')
        print('  </item>')
      print('</items>')
    except Exception, e:
      print e
    

