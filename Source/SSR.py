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
    return str.split(':');

  def _getServers(self):
    self.httpClient.request('GET', URL_SERVER)
    res = self.httpClient.getresponse()
    if res.status == 200 and res.reason == "OK":
      return json.loads(res.read())

  def _getStatus(self):
    self.httpClient.request('GET', URL_STATUS)
    res = self.httpClient.getresponse()
    if res.status == 200 and res.reason == "OK":
      data = json.loads(res.read())
      return data['enable']

  def _getMode(self):
    self.httpClient.request('GET', URL_MODE)
    res = self.httpClient.getresponse()
    if res.status == 200 and res.reason == "OK":
      data = json.loads(res.read())
      return data['mode']

  def _setStatus(self):
    res = self._post(URL_TOGGLE, {})
    if res.status == 200 and res.reason == "OK":
      data = json.loads(res.read())
      return data['Status'] == 1
    return False

  def _setServer(self, id):
    parma = {'uuid': id}
    res = self._post(URL_SERVER, parma)
    if res.status == 200 and res.reason == "OK":
      data = json.loads(res.read())
      return data['Status'] == 1
    return False

  def _setMode(self, mode):
    parma = {'vaule': mode}
    res = self._post(URL_MODE, parma)
    if res.status == 200 and res.reason == "OK":
      data = json.loads(res.read())
      return data['Status'] == 1
    return False

  def action(self, query):
    args = self._parseArgs(query)
    command = args[0]
    value = args[1]
    if(command == 'enable'):
      if(self._setStatus()):
        print("Set ShadowSock " + value + ' Succeed!')
    if(command == 'server'):
      if(self._setServer(value)):
        print("Set Server " + args[2])
    if(command == 'mode'):
      if(self._setMode(value)):
        print("Set Server Mode: " + value + ' Succeed!')
    return ''


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
        print("  <item uid=\"octal\" valid=\"yes\" arg=\""+ "server:" +item['id']+":"+item['note']+"\">")
        print("    <title>"+item['note']+"</title>")
        print('    <icon>icon.png</icon>')
        print('  </item>')
      print('</items>')
    except Exception, e:
      print e
    

