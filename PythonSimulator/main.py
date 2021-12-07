import random, queue

from typing import Counter
from Vessel import Vessel
from QuayCrane import QuayCrane
from EventLog import EventLog

class TerminalOperator:
    def __init__(self):
        self.totalQuayLength = 400
        self.vesselQueue = queue.SimpleQueue()
        self.vessel_quayCrane = {}
        self.quayCrane = []


    def _handleMotionEvent(self, motionObject, motions):
        for m in motions:
            print(m)

    def addVessel(self, vessel):
        self.vesselQueue.put(vessel)

    def addQuayCrane(self, qc):
        self.quayCrane.append(qc)
        qc.onMotion = self._handleMotionEvent

    def unloadNextVessel(self):
        if self.vesselQueue.qsize() == 0:
            EventLog('tos', 'bye')
            return

        vessel = self.vesselQueue.get()
        idleQuayCrane = self._getIdleQuayCrane()
        if idleQuayCrane > vessel.maxQuayCrane:
            idleQuayCrane = idleQuayCrane[0: vessel.maxQuayCrane]

        # allocate quaycrane
        baysPerQc = int(vessel.bays / len(idleQuayCrane))
        for i in range(0, idleQuayCrane):
            fromBay = i*baysPerQc
            idleQuayCrane[i].idle = False
            idleQuayCrane[i].drive(fromBay)

        # while not vessel.isEmpty:
        #     for i in range(0, idleQuayCrane):
        #         fromBay = i*baysPerQc
        #         toBay = (i+1)*baysPerQc
        #         if i == len(idleQuayCrane)-1:
        #             toBay = len(idleQuayCrane)-1
        #         bay, row, tier = vessel.findFirstContainerInBay(fromBay, toBay)
        #         if bay is not None:
        #             container = vessel.removeContainer(bay, row, tier)

        #         # free the quaycrane
        #         else:
        #             idleQuayCrane[i].idle = True

    def _getIdleQuayCrane(self):
        idleQuayCrane = []
        for qc in self.quayCrane:
            if qc.idle:
                idleQuayCrane.append(qc)
        return idleQuayCrane


class Simulator:

    def __init__(self):
        to = TerminalOperator()
        qc = QuayCrane()
        to.addQuayCrane(qc)
        qc.unload(0,1,1,1,0)
        # qc.drive(0, -1)

        # vessel = Vessel()
        # vessel.randomCargos(0.5)
       
        # terminalOperator.addVessel(vessel)
        # terminalOperator.addQuayCrane(quayCrane)


if __name__ == "__main__":
    # v = Vessel()
    # v.randomCargos(0.5)
    # print(str(v))

    Simulator()
