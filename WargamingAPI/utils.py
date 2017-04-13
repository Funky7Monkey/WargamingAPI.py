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

import urllib.request, json

class stats:
    def __init__(self):
        with urllib.request.urlopen("http://www.wnefficiency.net/exp/expected_tank_values_latest.json") as url:
            self.expected = json.loads(url.read().decode())


    def calcWN8(self, exp, act):
        """http://wiki.wnefficiency.net/pages/WN8#The_Steps_of_WN8_-_The_Formula"""

        # Step 1
        rWIN     = act['avgWins'] / exp['expWins']
        rDAMAGE  = act['avgDmg']  / exp['expDmg']
        rSPOT    = act['avgSpot'] / exp['expSpot']
        rFRAG    = act['avgFrag'] / exp['expFrag']
        rDEF     = act['avgDef']  / exp['expDef']

        # Step 2
        rWINc    = max(0,                     (rWIN    - 0.71) / (1 - 0.71) )
        rDAMAGEc = max(0,                     (rDAMAGE - 0.22) / (1 - 0.22) )
        rFRAGc   = max(0, min(rDAMAGEc + 0.2, (rFRAG   - 0.12) / (1 - 0.12)))
        rSPOTc   = max(0, min(rDAMAGEc + 0.1, (rSPOT   - 0.38) / (1 - 0.38)))
        rDEFc    = max(0, min(rDAMAGEc + 0.1, (rDEF    - 0.10) / (1 - 0.10)))

        # Step 3
        rat = (980*rDAMAGEc) + (210*rDAMAGEc*rFRAGc) + (155*rFRAGc*rSPOTc) + (75*rDEFc*rFRAGc) + (145*min(1.8,rWINc))
        WN8 = {'rating':rat, 'win':rWINc, 'dmg':rDAMAGEc, 'frag':rFRAGc, 'spot':rSPOTc, 'def':rDEFc}
        return WN8

    def WN8(self, player):

        vehAll = {}
        vehAll['battles'] = 0
        vehAll['avgWins'] = player['statistics']['all']['wins']
        vehAll['avgDmg']  = player['statistics']['all']['damage_dealt']
        vehAll['avgSpot'] = player['statistics']['all']['spotted']
        vehAll['avgFrag'] = player['statistics']['all']['frags']
        vehAll['avgDef']  = player['statistics']['all']['dropped_capture_points']

        expAll = {'expWins' : 0 ,'expDmg' : 0 ,'expSpot' : 0 ,'expFrag' : 0 ,'expDef' : 0}

        for i, vehicle in enumerate(player['vehicles']):
            vehAll['battles'] += vehicle['all']['battles']

            # Prep per-vehicle
            veh = {}
            veh['avgWins'] = vehicle['all']['wins']
            veh['avgDmg']  = vehicle['all']['damage_dealt']
            veh['avgSpot'] = vehicle['all']['spotted']
            veh['avgFrag'] = vehicle['all']['frags']
            veh['avgDef']  = vehicle['all']['dropped_capture_points']

            exp = None
            for j, v in enumerate(self.expected):
                if v['IDNum'] == vehicle['tank_id']:
                    exp = v

            # Prep expected per-vehicle
            expVeh = {}
            try:
                expVeh['expWins']  = (exp['expWinRate'] / 100) * vehicle['all']['battles']
                expVeh['expDmg']   =  exp['expDamage']         * vehicle['all']['battles']
                expVeh['expSpot']  =  exp['expSpot']           * vehicle['all']['battles']
                expVeh['expFrag']  =  exp['expFrag']           * vehicle['all']['battles']
                expVeh['expDef']   =  exp['expDef']            * vehicle['all']['battles']

                vehicle['WN8']     = self.calcWN8(expVeh, veh)
                # Prep expected total
                expAll['expWins'] += expVeh['expWins']
                expAll['expDmg']  += expVeh['expDmg']
                expAll['expSpot'] += expVeh['expSpot']
                expAll['expFrag'] += expVeh['expFrag']
                expAll['expDef']  += expVeh['expDef']
            except (ZeroDivisionError, TypeError) as e:
                pass

        player['WN8']   = self.calcWN8(expAll, vehAll)
        return player