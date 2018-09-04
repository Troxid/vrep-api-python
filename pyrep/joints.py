from .vrep import vrep as v
from .vrep import vrepConst as vc
from .common import NotFoundComponentError, MatchObjTypeError

class AnyJoint:
    def __init__(self, id, handle):
        self._id = id
        self._handle = handle
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def set_target_velocity(self, target):
        v.simxSetJointTargetVelocity(
            self._id, self._handle, target, self._def_op_mode)

    def set_target_position(self, target):
        v.simxSetJointTargetPosition(
            self._id, self._handle, target, self._def_op_mode)

    def get_force(self):
        code, force = v.simxGetJointForce(
            self._id, self._handle, self._def_op_mode)
        return force

    def set_maximum_force(self, force):
        v.simxSetJointForce(
            self._id, self._handle, force, self._def_op_mode)

    def set_position(self, position):
        v.simxSetJointPosition(
            self._id, self._handle, position, self._def_op_mode)

    def get_position(self):
        code, position = v.simxGetJointPosition(
            self._id, self._handle, self._def_op_mode)
        return position

    def get_matrix(self):
        code, matrix = v.simxGetJointMatrix(
            self._id, self._handle, self._def_op_mode)
        return matrix

    def set_matrix(self, matrix):
        assert len(matrix) == 12
        v.simxSetSphericalJointMatrix(
            self._id, self._handle, matrix, self._def_op_mode)


class JointWithVelocityControl:

    def __init__(self, any_joint: AnyJoint):
        self._any_joint = any_joint

    def set_target_velocity(self, target: float):
        self._any_joint.set_target_velocity(target)

    def set_maximum_force(self, force: float):
        self._any_joint.set_maximum_force(force)

    def get_position(self):
        return self._any_joint.get_position()

    def get_force(self):
        return self._any_joint.get_force()


class JointWithPositionControl:

    def __init__(self, any_joint: AnyJoint):
        self._any_joint = any_joint

    def set_target_position(self, target: float):
        self._any_joint.set_target_position(target)

    def set_maximum_force(self, force: float):
        self._any_joint.set_maximum_force(force)

    def get_position(self):
        return self._any_joint.get_position()

    def get_force(self):
        return self._any_joint.get_force()


class PassiveJoint:

    def __init__(self, any_joint: AnyJoint):
        self._any_joint = any_joint

    def get_position(self):
        return self._any_joint.get_position()

    def set_position(self, pos: float):
        self._any_joint.set_position(pos)


class SphericalJoint:

    def __init__(self, any_joint: AnyJoint):
        self._any_joint = any_joint

    def set_matrix(self, matrix):
        self._any_joint.set_matrix(matrix)

    def get_matrix(self):
        return self._any_joint.get_matrix()


class SpringJoint:

    def __init__(self, any_joint: AnyJoint):
        self._any_joint = any_joint

    def set_target_position(self, target: float):
        self._any_joint.set_target_position(target)

    def set_maximum_force(self, force: float):
        self._any_joint.set_maximum_force(force)

    def get_position(self):
        return self._any_joint.get_position()

    def get_force(self):
        return self._any_joint.get_force()

    def set_target_velocity(self, target: float):
        self._any_joint.set_target_velocity(target)

class Joints:

    def __init__(self, id):
        self._id = id
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def spherical(self, name: str) -> SphericalJoint:
        """
        Retrieves the joint with next parameters:
            * Joint type: Spherical
            * Joint mode: Passive
        """
        joint = self._get_joint_with_param(
            name,
            [vc.sim_joint_spherical_subtype],
            vc.sim_jointmode_passive)
        return SphericalJoint(joint)

    def spring(self, name: str) -> SpringJoint:
        """
        Retrieves the joint with next parameters:
            * Joint type: Revolute or Prismatic
            * Joint mode: Force
            * Motor enabled: True
            * Control loop enabled: True
            * Spring-damper mode
        """
        joint = self._get_joint_with_param(
            name, [vc.sim_joint_revolute_subtype, vc.sim_joint_prismatic_subtype],
            vc.sim_jointmode_force)
        return SpringJoint(joint)

    def passive(self, name: str) -> PassiveJoint:
        """
        Retrieves the joint (kinematic mode)with next parameters:
            * Joint type: Revolute or Prismatic
            * Joint mode: Passive
        """
        joint = self._get_joint_with_param(
            name, [vc.sim_joint_revolute_subtype, vc.sim_joint_prismatic_subtype],
            vc.sim_jointmode_passive)
        return PassiveJoint(joint)

    def with_position_control(self, name: str) -> JointWithPositionControl:
        """
        Retrieves the joint (like servo) with next parameters:
            * Joint type: Revolute or Prismatic
            * Joint mode: Force
            * Motor Enabled: True
            * Control loop enabled: True
            * Position control (PID)
        """
        joint = self._get_joint_with_param(
            name, [vc.sim_joint_revolute_subtype, vc.sim_joint_prismatic_subtype],
            vc.sim_jointmode_force)
        return JointWithPositionControl(joint)

    def with_velocity_control(self, name: str) -> JointWithVelocityControl:
        """
        Retrieves the joint (like DC motor) with next parameters:
            * Joint type: Revolute or Prismatic
            * Joint mode: Force
            * Motor Enabled: True
        """
        joint = self._get_joint_with_param(
            name, [vc.sim_joint_revolute_subtype, vc.sim_joint_prismatic_subtype],
            vc.sim_jointmode_force)
        return JointWithVelocityControl(joint)

    def _get_joint_with_param(self, name, types, mode) -> AnyJoint:
        handle = self._get_object_handle(name)
        if handle is not None:
            type, curr_mode, limit, range = self._get_info_about_joint(handle)
            if type in types and curr_mode == mode:
                return AnyJoint(self._id, handle)
            else:
                raise MatchObjTypeError("Joint with name: \"" + name +
                                        "\" does not fit the parameters. ")
        else:
            raise NotFoundComponentError("Handle not found")

    def _get_info_about_joint(self, handle):
        obj_type_code = vc.sim_object_joint_type
        data_type_code = 16
        code, handles, types_and_mode, limits_and_ranges, string_data = v.simxGetObjectGroupData(
            self._id, obj_type_code, data_type_code, self._def_op_mode)
        if code == v.simx_return_ok:
            index = handles.index(handle)
            index = index * 2
            return types_and_mode[index], types_and_mode[index+1], limits_and_ranges[index], limits_and_ranges[index+1]
        else:
            return None

    def _get_object_handle(self, name):
        code, handle = v.simxGetObjectHandle(self._id, name, self._def_op_mode)
        if code == v.simx_return_ok:
            return handle
        else:
            return None

