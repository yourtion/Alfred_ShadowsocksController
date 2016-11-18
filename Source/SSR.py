#!/usr/bin/python
# -*- coding: utf-8 -*- 

import httplib
import json
import urllib

class Client:
 
  httpClient = None
  SERVER='/servers'
  STATUS='/status'
  TOGGLE='/toggle'
  MODE='/mode'
  MODES=['auto','global','manual','bypasschian']
  
  def __init__(self):
    self.httpClient = httplib.HTTPConnection('localhost', 9528, timeout=30)

  def _get(self, url):
    try:
      self.httpClient.request('GET', url)
      res = self.httpClient.getresponse()
      return res if res.status == 200 and res.reason == 'OK' else False
    except Exception, e:
      return False

  def _post(self, url, parma):
    try:
      params = urllib.urlencode(parma)
      headers = {'Content-type': 'application/x-www-form-urlencoded'
                     , 'Accept': 'text/plain'}
      self.httpClient.request('POST', url, params, headers)
      res = self.httpClient.getresponse()
      return res if res.status == 200 and res.reason == 'OK' else False
    except Exception, e:
      return False

  def _parseArgs(self, str):
    return str.split(':', 2);

  def _getServers(self):
    res = self._get(self.SERVER)
    if res:
      return json.loads(res.read())
    return []

  def _getStatus(self):
    res = self._get(self.STATUS)
    if res:
      data = json.loads(res.read())
      return data['enable']
    return False

  def _getMode(self):
    res = self._get(self.MODE)
    if res:
      data = json.loads(res.read())
      return data['mode']
    return 'unknow'

  def _setStatus(self):
    res = self._post(self.TOGGLE, {})
    if res:
      data = json.loads(res.read())
      return data['Status'] == 1
    return False

  def _setServer(self, id):
    parma = {'uuid': id}
    res = self._post(self.SERVER, parma)
    if res:
      data = json.loads(res.read())
      return data['status'] == 1
    return False

  def _setMode(self, mode):
    parma = {'value': mode}
    res = self._post(self.MODE, parma)
    if res:
      data = json.loads(res.read())
      return data['Status'] == 1
    return False

  def action(self, query):
    args = self._parseArgs(query)
    command = args[0]
    value = args[1]
    if(command == 'enable'):
      if(self._setStatus()):
        print('Set ShadowSock ' + value + ' Succeed!')
    if(command == 'server'):
      if(self._setServer(value)):
        print('Set Server ' + args[2])
    if(command == 'mode'):
      if(self._setMode(value)):
        print('Set Server Mode: ' + value + ' Succeed!')
    return ''


  def getList(self):
    list = self._getServers()
    enable = self._getStatus()
    enableStr = 'True' if enable else 'False'
    enableOptStr = 'Disable' if enable else 'Enable'
    mode = self._getMode()
    items = []
    enableItem = {
      'title':'Enable: ' + enableStr,
      'subtitle': 'Select to '+ enableOptStr,
      'arg': 'enable:'+enableOptStr,
      'icon': {'path': 'icon.png'}
    }
    if not enable:
      enableItem['icon']['path'] = 'iconb.png'
    items.append(enableItem)

    for m in self.MODES:
      modeItem = {
        'title': 'Mode: '+m,
        'arg': 'mode:'+m,
        'icon': {'path': 'iconb.png'}
      }
      if m == mode:
        modeItem['icon']['path'] = 'icon.png'
        modeItem['subtitle'] = 'Current Mode'
      else:
        modeItem['subtitle'] = 'Switch to ' + m
      items.append(modeItem)

    for item in list:
      serverItem = {
        'title': 'Server: ' + item['note'],
        'arg': 'server:' +item['id']+':'+item['note'],
      }
      items.append(serverItem)
    result = {'items': items}
    print(json.dumps(result))
    