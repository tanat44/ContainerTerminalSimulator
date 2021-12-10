from Vessel import Vessel
from QuayCrane import QuayCrane
from TerminalOperator import TerminalOperator


class Simulator:

    def __init__(self):
        to = TerminalOperator()
        to.addQuayCrane(QuayCrane())
        to.addQuayCrane(QuayCrane())

        vessel = Vessel()
        vessel.randomCargos(0.5)
        vessel.printStowagePlan()
        to.addVessel(vessel)
        to.unloadNextVessel()

if __name__ == "__main__":
    Simulator()
