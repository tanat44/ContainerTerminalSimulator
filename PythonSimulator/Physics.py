import math

class Physics:
    BOX_HEIGHT = 2.4
    BOX_WIDTH = 2.4
    BOX_LENGTH = 12.2

    # BANG-BANG acceleration
    def PlanMotion(startTime, x0, x1, v0, v1, vMax, accel):
        motion=[]
        totalTime = 0
        distance = x1-x0

        if distance == 0:
            return motion

        if x1 < x0:
            accel *= -1
        sAccel = (vMax*vMax - v0*v0) / 2 / accel
        sDecel = (v1*v1 - vMax*vMax) / 2 / -accel

        # not enough distance to accel to maxV: accel > decel
        if abs(sAccel + sDecel) > abs(distance):
            # start accel
            motion.append(MotionState(startTime, x0, v0, accel))
            s1 = (v1*v1 - v0*v0 + 2*accel*distance)/4/accel
            vMid = math.sqrt(v0*v0 + 2*accel*s1)
            if x1 < x0:
                vMid *= -1
            t1 = (vMid-v0) / accel
            # start decel
            motion.append(MotionState(startTime + t1, x0+s1, vMid, -accel))
            # end
            t2 = (v1-vMid) / -accel
            totalTime = t1 + t2
            motion.append(MotionState(startTime + totalTime, x1, v1, 0))           

        # accel -> maxV -> decel
        else:
            if x1 < x0:
                vMax *= -1
            # start accel
            motion.append(MotionState(startTime, x0, v0, accel))
            tAccel = (vMax - v0) / accel
            # start cruise
            motion.append(MotionState(startTime + tAccel, x0+sAccel, vMax, 0))
            tDecel = (vMax - v1) / accel
            sCruise = distance - sAccel - sDecel
            tCruise = sCruise / vMax
            # start decel
            motion.append(MotionState(startTime + tAccel + tCruise, x0 + sAccel + sCruise, vMax, -accel))
            # end
            totalTime = tAccel + tDecel + tCruise
            motion.append(MotionState(startTime + totalTime, x1, v1, 0))
        
        return motion

    def isClose(a, b):
        #2 precision close
        return math.isclose(a, b, abs_tol=0.005)

class MotionState:
    def __init__(self, time=0, pos=0, vel=0, acc=0):
        self.time = time
        self.pos = pos
        self.vel = vel
        self.acc = acc

    def __str__(self):
        return f't={"{:.2f}".format(self.time)}\t{"{:.2f}".format(self.pos)}\t{"{:.2f}".format(self.vel)}\t{"{:.2f}".format(self.acc)}\t '

class MotionState3D:
    def __init__(self, time, pos=[0,0,0], vel=[0,0,0], acc=[0,0,0]):
        self.time = time
        self.pos = pos
        self.vel = vel
        self.acc = acc

    @staticmethod
    def from1D (time, motionX=MotionState(), motionY=MotionState(), motionZ=MotionState()):
        out = MotionState3D(time)
        out.pos = [motionX.pos, motionY.pos, motionZ.pos]
        out.vel = [motionX.vel, motionY.vel, motionZ.vel]
        out.acc = [motionX.acc, motionY.acc, motionZ.acc]
        return out

    def getX(self):
        return self._getElementIndex(0)
    
    def getY(self):
        return self._getElementIndex(1)

    def getZ(self):
        return self._getElementIndex(2)

    def _getElementIndex(self, index):
        return MotionState(self.time, self.pos[index], self.vel[index], self.acc[index])

    def toDict(self):
        return {
            "time": self.time,
            "pos": self.pos,
            "vel": self.vel,
            "acc": self.acc,
        }

    def __str__(self):
        return f't={Utils.floatToString(self.time)}\npos={Utils.floatToString(self.pos)}\tvel={Utils.floatToString(self.vel)}\tacc={Utils.floatToString(self.acc)}'

class Utils:
    @staticmethod
    def floatToString(input, format='{:.2f}'):
        if isinstance(input, list):
            out = []
            for i in input:
                out.append(format.format(i))
            return out
        else:   
            return format.format(input)