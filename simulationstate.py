import vrep as v
import vrepConst as vc


class SimulationState:

    def __init__(self, id):
        self._id = id
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def start(self):
        v.simxStartSimulation(self._id, self._def_op_mode)

    def pause(self):
        v.simxPauseSimulation(self._id, self._def_op_mode)

    def stop(self):
        v.simxStopSimulation(self._id, self._def_op_mode)
