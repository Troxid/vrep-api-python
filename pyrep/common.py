import math
from .vrep import vrep as v


class Vec3:

    def __init__(self, x=0, y=0, z=0):
        self._x = x
        self._y = y
        self._z = z

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def distance(self):
        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    def __str__(self):
        return "Vec3(x={0}, y={1}, z={2})"\
               .format(str(self._x), str(self._y), str(self._z))

    def __repr__(self):
        return self.__str__()


class EulerAngles:

    def __init__(self, alpha=0, beta=0, gamma=0):
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma

    def get_alpha(self):
        return self._alpha

    def get_beta(self):
        return self._beta

    def get_gamma(self):
        return self._gamma

    def __str__(self):
        return "EulerAngles(alpha={0}, beta={1}, gamma={2})"\
               .format(str(self._alpha), str(self._beta), str(self._gamma))

    def __repr__(self):
        return self.__str__()


class NotFoundComponentError(Exception):
    def __init__(self, name):
        super(NotFoundComponentError, self).__init__(
            "Not found component with name \"" + name +
            "\"")


class MatchObjTypeError(Exception):

    def __init__(self, name):
        super(MatchObjTypeError, self).__init__(
            "Component with name: \"" + name +
            "\" does not fit the parameters.")


class ReturnCommandError(Exception):

    def __init__(self, code):
        msg = ""
        if code == v.simx_return_novalue_flag:
            msg = "Input buffer doesn't contain the specified command"
        elif code == v.simx_return_timeout_flag:
            msg = "Command reply not received in time for opmode_oneshot_wait operation mode"
        elif code == v.simx_return_illegal_opmode_flag:
            msg = "Command doesn't support the specified operation mode"
        elif code == v.simx_return_remote_error_flag:
            msg = "Command caused an error on the server side"
        elif code == v.simx_return_split_progress_flag:
            msg = "Previous similar command not yet fully processed (applies to opmode_oneshot_split operation modes)"
        elif code == v.simx_return_local_error_flag:
            msg = "Command caused an error on the client side"
        elif code == v.simx_return_initialize_error_flag:
            msg = "simxStart was not yet called"
        else:
            msg = "Undefined return code: " + str(code)
        super(ReturnCommandError, self).__init__(msg)
