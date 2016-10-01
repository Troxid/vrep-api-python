import vrep as v
import vrepConst as vc
from common import MatchObjTypeError, NotFoundComponentError
from common import Vec3, EulerAngles

class ProximitySensor:

    def __init__(self, id, handle):
        self._id = id
        self._handle = handle
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def read(self) -> (bool, Vec3):
        """
        Reads the state of a proximity sensor.
        @return detection state and detected point
        @rtype (bool, Vec3)
        """
        code, state, point, handle, snv = v.simxReadProximitySensor(
            self._id, self._handle, self._def_op_mode)
        return state, Vec3(point[0], point[1], point[2])


class VisionSensor:

    def __init__(self, id, handle):
        self._id = id
        self._handle = handle
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def read(self):
        code, state, aux_packets = v.simxReadVisionSensor(
            self._id, self._handle, self._def_op_mode)
        return state, state, aux_packets

    def raw_image(self, is_grey_scale=False):
        """
        Retrieves the image of a vision sensor.
        @return the image data
        """
        num_of_clr = 3
        if is_grey_scale:
            num_of_clr = 1

        code, resolution, image = v.simxGetVisionSensorImage(
            self._id, self._handle, int(is_grey_scale), self._def_op_mode)
        return image

    def depth_buffer(self):
        """
        Retrieves the depth buffer of a vision sensor.
        """
        code, resolution, buffer = v.simxGetVisionSensorDepthBuffer(
            self._id, self._handle, self._def_op_mode)
        return buffer


class ForceSensor:

    def __init__(self, id, handle):
        self._id = id
        self._handle = handle
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def read(self) -> (bool, Vec3, Vec3):
        """
        Reads the force and torque applied to a force sensor
        (filtered values are read), and its current state ('unbroken' or 'broken').
        """
        code, state, force, torque, snv = v.simxReadForceSensor(
            self._id, self._handle, self._def_op_mode)
        force_vector = Vec3(force[0], force[1], force[2])
        torque_vector = Vec3(torque[0], torque[1], torque[2])
        return state, force_vector, torque_vector


class PositionSensor:

    def __init__(self, id, handle):
        self._id = id
        self._handle = handle
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def get_position(self) -> Vec3:
        """Retrieves the orientation.
        @rtype: Vec3
        """
        code, pos = v.simxGetObjectPosition(self._id, self._handle, -1, self._def_op_mode)
        return Vec3(pos[0], pos[1], pos[2])

    def get_orientation(self) -> EulerAngles:
        """
        Retrieves the linear and angular velocity.
        @rtype EulerAngles
        """
        code, orient = v.simxGetObjectOrientation(self._id, self._handle, -1, self._def_op_mode)
        return EulerAngles(orient[0], orient[1], orient[2])

    def get_velocity(self) -> (Vec3, EulerAngles):
        """
        Retrieves the linear and angular velocity.
        @rtype (Vec3, EulerAngles)
        """
        code, lin_vel, ang_vel = v.simxGetObjectVelocity(self._id, self._handle, self._def_op_mode)
        linear_velocity = Vec3(lin_vel[0], lin_vel[1], lin_vel[2])
        angular_velocity = EulerAngles(ang_vel[0], ang_vel[1], ang_vel[2])
        return linear_velocity, angular_velocity


class Sensors:

    def __init__(self, id):
        self._id = id
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def proximity(self, name: str) -> ProximitySensor:
        handle = self._get_object_handle(name)
        if handle is not None:
            if self._check_object_type(handle, vc.sim_object_proximitysensor_type):
                return ProximitySensor(self._id, handle)
            else:
                raise MatchObjTypeError(name)
        else:
            raise NotFoundComponentError(name)

    def position(self, name: str) -> PositionSensor:
        handle = self._get_object_handle(name)
        if handle is not None:
            return PositionSensor(self._id, handle)
        else:
            raise NotFoundComponentError(name)

    def vision(self, name: str) -> VisionSensor:
        handle = self._get_object_handle(name)
        if handle is not None:
            if self._check_object_type(handle, vc.sim_object_visionsensor_type):
                return VisionSensor(self._id, handle)
            else:
                raise MatchObjTypeError(name)
        else:
            raise NotFoundComponentError(name)

    def force(self, name: str) -> ForceSensor:
        handle = self._get_object_handle(name)
        if handle is not None:
            if self._check_object_type(handle, vc.sim_object_forcesensor_type):
                return ForceSensor(self._id, handle)
            else:
                raise MatchObjTypeError(name)
        else:
            raise NotFoundComponentError(name)

    def _get_sensor(self, name, sensor_type, ctr):
        handle = self._get_object_handle(name)
        if handle is not None:
            if self._check_object_type(handle, sensor_type):
                return ctr(self._id, handle)
            else:
                raise MatchObjTypeError(name)
        else:
            raise NotFoundComponentError(name)

    def _check_object_type(self, handle, obj_type):
        code, handles, _, _, _ = v.simxGetObjectGroupData(
            self._id, obj_type, 0, self._def_op_mode)
        return handles.__contains__(handle)

    def _get_object_handle(self, name):
        code, handle = v.simxGetObjectHandle(self._id, name, self._def_op_mode)
        if code == v.simx_return_ok:
            return handle
        else:
            return None


