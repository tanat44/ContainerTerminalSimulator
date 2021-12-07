from Physics import Physics, MotionState3D, MotionState


def motionEvent(func):
    def wrapper(self, *args, **kwargs):
        motions = func(self, *args, **kwargs)
        if self.onMotion is not None:
            self.onMotion(self, motions)
        return motions

    return wrapper

class QuayCrane:
    count = 0
    MAX_V = 3
    ACCEL = 1
    MAX_HEIGHT = 5             # multiple of BOX_HEIGHT
    BOOM_REACH = 5              # multiple of BOX_WIDTH      
    BOOM_LANE_GAP = 2           # ROW_4 ROW_3 ROW_2 ROW_1 ROW_0 QUAY QUAY LANE_0 LANE_1 LANE_2 LANE_3 LANE_4
    LANE = 5                    # ------------------------------------------ 0 +++++++++++++++++++++++++++++
    DEBUG_MOVE_LOGIC = False

    def __init__(self):
        self.state = MotionState3D(0)           # x = translate along the quay
                                                # y = speader height    
                                                # z = reach equal zero at back stay
        self.idle = True
        self.id = QuayCrane.count
        self.onReady = None
        self.onMotion = None

        QuayCrane.count += 1

    def unload(self, startTime, bay, row, tier, lane):
        time = startTime
        motions = []

        if QuayCrane.DEBUG_MOVE_LOGIC:
            print('moveToship')

        # pickup box
        motions += self.moveToShip(time, bay, row, tier)
        if len(motions) > 0:
            time = motions[-1].time

        if QuayCrane.DEBUG_MOVE_LOGIC:
            print('moveToLand')
            
        # drop off box
        motions += self.moveToLand(time, lane)
        if len(motions) > 0:
            time = motions[-1].time
        return motions

    def moveToLand(self, startTime, lane):
        time = startTime
        motions = []

        # Spreader to Top Most
        motions += self.moveSpreaderVertical(time, QuayCrane.MAX_HEIGHT + 1)
        if len(motions) > 0:
            time = motions[-1].time
        
        # Spreader Backward to land
        row = self._laneToRow(lane)
        motions += self.moveSpreaderFront(time, row)
        if len(motions) > 0:
            time = motions[-1].time

        # Spreader down
        motions += self.moveSpreaderVertical(time, 1)
        if len(motions) > 0:
            time = motions[-1].time
        return motions

    def moveToShip(self, startTime, bay, row, tier):
        time = startTime
        motions = []
        # X
        motions += self.drive(time, bay)
        if len(motions) > 0:
            time = motions[-1].time

        # Spreader to Top Most
        motions += self.moveSpreaderVertical(time, QuayCrane.MAX_HEIGHT + 1)
        if len(motions) > 0:
            time = motions[-1].time
        
        # Spreader front/Back
        motions += self.moveSpreaderFront(time, row)
        if len(motions) > 0:
            time = motions[-1].time

        # Spreader down
        motions += self.moveSpreaderVertical(time, tier)
        if len(motions) > 0:
            time = motions[-1].time
        return motions

    @motionEvent
    def moveSpreaderVertical(self, startTime, toTier):
        toY = self._tierToZ(toTier)
        motions = Physics.PlanMotion(startTime, self.state.pos[1], toY, 0, 0, QuayCrane.MAX_V, QuayCrane.ACCEL)
        motions = [MotionState3D.from1D(m.time, motionY=m, motionX=self.state.getX(), motionZ=self.state.getZ()) for m in motions]
        self.state.pos[1] = toY
        return motions
    
    @motionEvent
    def moveSpreaderFront(self, startTime, toRow):
        toZ = self._rowToY(toRow)
        motions = Physics.PlanMotion(startTime, self.state.pos[2], toZ, 0, 0, QuayCrane.MAX_V, QuayCrane.ACCEL)
        motions = [MotionState3D.from1D(m.time, motionZ=m, motionY=self.state.getY(), motionX=self.state.getX()) for m in motions]
        self.state.pos[2] = toZ
        return motions

    @motionEvent
    def drive(self, startTime, toBay):
        toX = self._bayToX(toBay)
        motions = Physics.PlanMotion(startTime, self.state.pos[0], toX, 0, 0, QuayCrane.MAX_V, QuayCrane.ACCEL)
        motions = [MotionState3D.from1D(m.time, motionX=m, motionY=self.state.getY(), motionZ=self.state.getZ()) for m in motions]
        self.state.pos[0] = toX
        return motions

    def _bayToX(self, bay):
        return bay*Physics.BOX_LENGTH

    def _laneToRow(self, lane):
        return -lane-QuayCrane.BOOM_LANE_GAP-1

    def _rowToY(self, row):
        return (-QuayCrane.BOOM_LANE_GAP-row-1)*Physics.BOX_WIDTH

    def _tierToZ(self, tier):
        return tier*Physics.BOX_HEIGHT

    def __str__(self):
        return f'QuayCrane id={str(self.id)} idle={str(self.idle)}'

