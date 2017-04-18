"""
The MIT License (MIT)

Copyright (c) 2017 Funky7Monkey

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import urllib.request
import urllib.parse
import json
import time
from .errors import *
from .enums import *
from . import utils
import os.path
import os


def getData(API, method, params, scheme='https'):
    q = []
    for k, v in params.items():
        if isinstance(v, list):
            v = ','.join(v)
        if not v == '':
            q.append(k + '=' + v)
    fieldstr = '&'.join(q)
    url = urllib.parse.quote(urllib.parse.urlunsplit(
        (scheme, API, method, fieldstr, '')), safe='/=&:?%')
    with urllib.request.urlopen(url) as f:
        response = json.loads(f.read().decode('utf-8'))

    if response['status'] == "error":
        request = {
            'scheme': scheme,
            'API': API,
            'method': method,
            'fields': params}
        print(response)
        print(request)
        print(url)
        raise HTTPException(
            response=response,
            request=request,
            **response['error'])

    return response


class Client:
    def __init__(self, application_ID, language='en'):
        self.application_ID = application_ID
        self.language = language

    def searchPlayer(self):
        raise NotImplementedError

    def searchExactPlayer(self):
        raise NotImplementedError

    def getPlayerData(self):
        raise NotImplementedError

    def getPlayerVehicles(self):
        raise NotImplementedError

    def searchClan(self):
        raise NotImplementedError

    def getClanData(self):
        raise NotImplementedError

    def getRatingTypes(self):
        raise NotImplementedError

    def getPlayerRatings(self):
        raise NotImplementedError


class WoT_Client(Client):
    def __init__(self, application_ID, language='en'):
        super().__init__(application_ID, language)


class WoT_PC_Client(WoT_Client):
    def __init__(self, application_ID, region, language='en'):
        super().__init__(application_ID, language)
        self.region = region
        self.API = 'api.worldoftanks.' + self.region.domain()

    def searchPlayer(
            self,
            search,
            stype='startswith',
            limit=100,
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'search': search,
            'type': stype,
            'limit': limit,
            'fields': fields,
            'language': language}
        data = getData(
            API=self.API,
            method='/wot/account/list/',
            params=params)
        return data['data']

    def searchExactPlayer(self, search, limit=100, fields=[], *language):
        if all(language):
            language = self.language
        return searchPlayer(search, limit, fields, language, stype='exact')

    def getPlayerData(
            self,
            account_id,
            access_token='',
            extra=[],
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'account_id': account_id,
            'access_token': access_token,
            'extra': extra,
            'fields': fields,
            'fields': fields,
            'language': language}
        data = getData(
            API=self.API,
            method='/wot/account/info/',
            params=params)
        return data['data']

    def getPlayerVehicles(
            self,
            account_id,
            access_token='',
            extra=[],
            fields=[],
            *language,
            in_garage='',
            tank_id=''):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'account_id': account_id,
            'access_token': access_token,
            'extra': extra,
            'fields': fields,
            'fields': fields,
            'language': language,
            'in_garage': in_garage,
            'tank_id': tank_id}
        data = getData(API=self.API, method='/wot/tanks/stats/', params=params)
        return data['data']

    def searchClan(self, search, limit=100, fields=[], *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'search': search,
            'limit': limit,
            'fields': fields,
            'language': language}
        data = getData(API=self.API, method='/wgn/clans/list/', params=params)
        return data['data']

    def getClanData(
            self,
            clan_id,
            access_token='',
            extra=[],
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'clan_id': str(clan_id),
            'access_token': access_token,
            'extra': extra,
            'fields': fields,
            'fields': fields,
            'language': language}
        data = getData(API=self.API, method='/wgn/clans/info/', params=params)
        return data['data']

    def getRatingTypes(self, battle_type='default', fields=[], *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'battle_type': battle_type,
            'fields': fields,
            'language': language}
        data = getData(
            API=self.API,
            method='/wot/ratings/types/',
            params=params)
        return data['data']

    def getPlayerRatings(
            self,
            account_id,
            period,
            battle_type='default',
            date='',
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'account_id': account_id,
            'type': period,
            'battle_type': battle_type,
            'date': date,
            'fields': fields,
            'language': language}
        data = getData(
            API=self.API,
            method='/wot/ratings/accounts/',
            params=params)
        return data['data']

    def buildPlayerStats(self, account_id):
        playerFields = [
            '-statistics.team',
            '-statistics.clan',
            '-statistics.company',
            '-statistics.historical',
            '-statistics.stronghold_defense',
            '-statistics.stronghold_skirmish',
            '-statistics.regular_team']
        player = self.getPlayerData(
            account_id, fields=playerFields)[account_id]
        vehFields = [
            '-clan',
            '-company',
            '-globalmap',
            '-regular_team',
            '-stronghold_defense',
            '-stronghold_skirmish',
            '-team']
        player['vehicles'] = self.getPlayerVehicles(
            account_id, fields=vehFields)[account_id]
        player['region'] = self.region.name
        stats = utils.stats()
        stats.WN8(player)
        if player['clan_id'] is None:
            player['clan'] = None
        else:
            player['clan'] = self.getClanData(player['clan_id'])
        return player


class WoT_Console_Client(WoT_Client):
    def __init__(self, application_ID, platform, language='en'):
        super().__init__(application_ID, language)
        self.platform = platform
        self.API = 'api-' + self.platform.name.lower() + \
            '-console.worldoftanks.com'

    def searchPlayer(
            self,
            search,
            stype='startswith',
            limit=100,
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'search': search,
            'type': stype,
            'limit': limit,
            'fields': fields,
            'language': language}
        data = getData(
            API=self.API,
            method='/wotx/account/list/',
            params=params)
        return data['data']

    def searchExactPlayer(self, search, limit=100, fields=[], *language):
        if all(language):
            language = self.language
        return searchPlayer(search, limit, fields, language, stype='exact')

    def getPlayerData(
            self,
            account_id,
            access_token='',
            extra=[],
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'account_id': account_id,
            'access_token': access_token,
            'extra': extra,
            'fields': fields,
            'fields': fields,
            'language': language}
        data = getData(
            API=self.API,
            method='/wotx/account/info/',
            params=params)
        return data['data']

    def getPlayerVehicles(
            self,
            account_id,
            access_token='',
            extra=[],
            fields=[],
            *language,
            in_garage='',
            tank_id=''):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'account_id': account_id,
            'access_token': access_token,
            'extra': extra,
            'fields': fields,
            'fields': fields,
            'language': language,
            'in_garage': in_garage,
            'tank_id': tank_id}
        data = getData(
            API=self.API,
            method='/wotx/tanks/stats/',
            params=params)
        return data['data']

    def searchClan(self, search, limit=100, fields=[], *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'search': search,
            'limit': limit,
            'fields': fields,
            'language': language}
        data = getData(API=self.API, method='/wotx/clans/list/', params=params)
        return data['data']

    def getClanData(
            self,
            clan_id,
            access_token='',
            extra=[],
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'clan_id': clan_id,
            'access_token': access_token,
            'extra': extra,
            'fields': fields,
            'fields': fields,
            'language': language}
        data = getData(API=self.API, method='/wotx/clans/info/', params=params)
        return data['data']

    def getRatingTypes(self, fields=[], *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'platform': self.platform.name.lower(),
            'fields': fields,
            'language': language}
        data = getData(
            API=self.API,
            method='/wotx/ratings/types/',
            params=params)
        return data['data']

    def getPlayerRatings(
            self,
            account_id,
            period,
            date='',
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'account_id': account_id,
            'type': period,
            'platform': self.platform.name.lower(),
            'date': date,
            'fields': fields,
            'language': language}
        data = getData(
            API=self.API,
            method='/wotx/ratings/accounts/',
            params=params)
        return data['data']

    def buildPlayerStats(self, account_id):
        playerFields = ['-statistics.company']
        player = self.getPlayerData(
            account_id, fields=playerFields)[account_id]
        vehFields = ['-company']
        player['vehicles'] = self.getPlayerVehicles(
            account_id, fields=vehFields)[account_id]
        player['region'] = self.region.name
        stats = utils.stats()
        stats.WN8(player)
        if player['clan_id'] is None:
            player['clan'] = None
        else:
            player['clan'] = self.getClanData(player['clan_id'])
        return player


class WoT_Blitz_Client(WoT_Client):
    def __init__(self, application_ID, region, language='en'):
        super().__init__(application_ID, language)
        self.region = region
        self.API = 'api.wotblitz.' + self.region.domain()

    def searchPlayer(
            self,
            search,
            stype='startswith',
            limit=100,
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'search': search,
            'type': stype,
            'limit': limit,
            'fields': fields,
            'language': language}
        data = getData(
            API=self.API,
            method='/wotb/account/list/',
            params=params)
        return data['data']

    def searchExactPlayer(self, search, limit=100, fields=[], *language):
        if all(language):
            language = self.language
        return searchPlayer(search, limit, fields, language, stype='exact')

    def getPlayerData(
            self,
            account_id,
            access_token='',
            extra=[],
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'account_id': account_id,
            'access_token': access_token,
            'extra': extra,
            'fields': fields,
            'fields': fields,
            'language': language}
        data = getData(
            API=self.API,
            method='/wotb/account/info/',
            params=params)
        return data['data']

    def getPlayerVehicles(
            self,
            account_id,
            access_token='',
            extra=[],
            fields=[],
            *language,
            in_garage='',
            tank_id=''):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'account_id': account_id,
            'access_token': access_token,
            'extra': extra,
            'fields': fields,
            'fields': fields,
            'language': language,
            'in_garage': in_garage,
            'tank_id': tank_id}
        data = getData(
            API=self.API,
            method='/wotb/tanks/stats/',
            params=params)
        return data['data']

    def searchClan(self, search, limit=100, fields=[], *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'search': search,
            'limit': limit,
            'fields': fields,
            'language': language}
        data = getData(API=self.API, method='/wotb/clans/list/', params=params)
        return data['data']

    def getClanData(
            self,
            clan_id,
            access_token='',
            extra=[],
            fields=[],
            *language):
        if all(language):
            language = self.language
        params = {
            'application_id': self.application_ID,
            'clan_id': clan_id,
            'access_token': access_token,
            'extra': extra,
            'fields': fields,
            'fields': fields,
            'language': language}
        data = getData(API=self.API, method='/wotb/clans/info/', params=params)
        return data['data']
