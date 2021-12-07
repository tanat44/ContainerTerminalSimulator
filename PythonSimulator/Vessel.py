import random
from EventLog import EventLog
from Container import Container

class Vessel:
    count = 0

    class Job:
        LOAD = "LOAD"
        UNLOAD = "UNLOAD"

    def __init__(self, rows=3, tiers=1, bays=6, type=Job.UNLOAD, maxQuayCrane=2, length=200):
        self.rows = rows
        self.tiers = tiers
        self.bays = bays
        self.stowagePlan = [[[None for k in range(self.tiers)] for j in range(self.rows)] for i in range(self.bays)]
        self.type = type
        self.maxQuayCrane = maxQuayCrane
        self.length=length
        self.mooringPos = None
        self.isEmpty = True
        self.id = Vessel.count
        Vessel.count += 1

    def moore(self, pos):
        self.mooringPos = pos
        e = EventLog(f'vessel{str(self.id)}', f'mooreAt={pos}')

    def randomCargos(self, loadPercentage):
        maxBox = int(self.rows * self.tiers * self.bays * loadPercentage)
        stowCount = 0
        for i in range(maxBox):
            c = Container()
            bay, row = self._randomGridPosition()
            if self.stowContainer(c, bay, row):
                stowCount += 1
        self.isEmpty = False

    def stowContainer(self, container, bay, row):
        foundSlot = False
        for tier in range(self.tiers):
            if self.stowagePlan[bay][row][tier] is None:
                self.stowagePlan[bay][row][tier] = container
                foundSlot = True
                break
        return foundSlot

    def removeContainer(self, bay, row, tier):
        # check if there is a container on top
        for k in range(self.tiers-1, tier, -1):
            if self.stowagePlan[bay][row][k] is not None:
                print(f'Cannot remove container ({bay}, {row}, {tier})')
                return None

        aContainer = self.stowagePlan[bay][row][tier] 
        if self.stowagePlan[bay][row][tier] is not None:
            self.stowagePlan[bay][row][tier] = None
            aContainer = self.stowagePlan[bay][row][tier] 

        # if actaully removing conntainer > update isEmpty
        isEmpty = True
        for i in range(self.bays):
            for j in range(self.rows):
                for k in range(self.tiers):
                    if self.stowagePlan[i][j][k] is not None:
                        isEmpty = False
                        break
                if not isEmpty:
                    break
            if not isEmpty:
                break
        self.isEmpty = isEmpty
        
        return aContainer

    def findFirstContainerInBay(self, fromBay, toBay):
        for i in range(fromBay, toBay):
            for j in range(self.rows):
                for k in range(self.tiers-1, -1, -1):
                    if self.stowagePlan[i][j][k] is not None:
                        return i, j, k
        return None

    def _randomGridPosition(self):
        bay = random.randint(0, self.bays-1)
        row = random.randint(0, self.rows-1)
        return bay, row

    def __str__(self):
        out = f'vessel{str(self.id)}\n'
        for k in range(self.tiers-1, -1, -1):
            out += f'[ tier={str(k)} ]\n'
            for j in range(self.rows-1, -1, -1):
                for i in range(self.bays):
                    container = self.stowagePlan[i][j][k]
                    if container is not None:
                        out += str(container) + ' '
                    else:
                        out += '- '
                out += '\n'
        return out