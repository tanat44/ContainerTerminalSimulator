import queue
from Physics import Utils
from EventLog import EventLog

class TerminalOperator:
    DEBUG_MOTION_EVENT = False

    def __init__(self):
        self.totalQuayLength = 400
        self.vesselQueue = queue.SimpleQueue()
        self.vessel_quayCrane = {}
        self.quayCrane = []

    def _handleMotionEvent(self, motionObject, motions):
        if TerminalOperator.DEBUG_MOTION_EVENT:
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
        if len(idleQuayCrane) > vessel.maxQuayCrane:
            idleQuayCrane = idleQuayCrane[0: vessel.maxQuayCrane]

        # allocate quaycrane to vessel
        baysPerQc = int(vessel.bays / len(idleQuayCrane))

        startTime = 0
        for i in range(0, len(idleQuayCrane)):
            fromBay = i*baysPerQc
            idleQuayCrane[i].idle = False
            motions = idleQuayCrane[i].drive(startTime, fromBay)
            if len(motions) > 0:
                t = motions[-1].time
                if t > startTime:
                    startTime = t
        qcTime = [startTime for i in range(len(idleQuayCrane))]

        while not vessel.isEmpty:
            for i in range(0, len(idleQuayCrane)):
                fromBay = i*baysPerQc
                toBay = (i+1)*baysPerQc
                if i == len(idleQuayCrane):
                    toBay = vessel.bays
                bay, row, tier = vessel.findFirstContainerInBay(fromBay, toBay)

                # unload the container, qc[i] unload to i_th lane
                if bay is not None:
                    container = vessel.removeContainer(bay, row, tier)
                    motions = idleQuayCrane[i].unload(qcTime[i], bay, row, tier, i)
                    qcTime[i] += motions[-1].time
                    print(f'QC#{str(i)}\t Unload #{str(container)}\t from({str(bay)} {str(row)} {str(tier)}) Finish at {Utils.floatToString(qcTime[i])}')

                # free the quaycrane
                else:
                    idleQuayCrane[i].idle = True

    def _getIdleQuayCrane(self):
        idleQuayCrane = []
        for qc in self.quayCrane:
            if qc.idle:
                idleQuayCrane.append(qc)
        return idleQuayCrane
