#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.dev/sumo
# Copyright (C) 2008-2024 German Aerospace Center (DLR) and others.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0/
# This Source Code may also be made available under the following Secondary
# Licenses when the conditions for such availability set forth in the Eclipse
# Public License 2.0 are satisfied: GNU General Public License, version 2
# or later which is available at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later

# @file    runner.py
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @author  Daniel Krajzewicz
# @date    2011-03-04


from __future__ import print_function
from __future__ import absolute_import
import os
import sys
if "SUMO_HOME" in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci  # noqa
import sumolib  # noqa
import simpla  # noqa
from simpla import SimplaException  # noqa

binary = 'sumo-gui'
if 'nogui' in sys.argv:
    binary = 'sumo'

traci.start([sumolib.checkBinary(binary),
             '-c', 'sumo.sumocfg',
             '--step-length', '0.5',
             '--fcd-output', 'fcd.xml',
             '--fcd-output.max-leader-distance', '100'])

simpla.load("simpla.cfg.xml")

step = 0
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    step += 1
    
    avgLength = simpla.getAveragePlatoonLength()
    avgSpeed = simpla.getAveragePlatoonSpeed()
    currentLeaderIDs = simpla.getPlatoonLeaderIDList()
    print("\n\n-------------\ncurrent step: ", step)
    print("platoon avgLength: ", avgLength)
    print("platoon avgSpeed: ", avgSpeed)
    print("platoon currentLeaderIDs: ", currentLeaderIDs)
    print()
    
    allEdgeIDs = ["A0left0", "A0right0", "left0A0", "right0A0"]
    for edgeID in allEdgeIDs:
        platoonIDs = simpla.getPlatoonIDList(edgeID)
        print("current edgeID: ", edgeID)
        print("platoonIDs in this edgeID: ", platoonIDs)
        if len(platoonIDs) > 0:
            platoonInfo = simpla.getPlatoonInfo(platoonIDs[0])
            print("platoonInfo: ", platoonInfo)
            platoonSize = len(platoonInfo["members"])
            print("platoonSize: ", platoonSize)
        print()
            
    allVehIDs_inThisSUMOStep = traci.vehicle.getIDList()
    for vehID in allVehIDs_inThisSUMOStep:
        platoonID = simpla.getPlatoonID(vehID)
        print("current vehID: ", vehID)
        print("platoonID which controls this vehID: ", platoonID)
        print("-1 means no platoon controls this veh.")


traci.close()
