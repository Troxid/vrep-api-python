from vrepapi import VRepApi
import time


class PioneerP3DX:

    def __init__(self, api: VRepApi):
        self._api = api
        self._left_motor = api.joint.with_velocity_control("Pioneer_p3dx_leftMotor")
        self._right_motor = api.joint.with_velocity_control("Pioneer_p3dx_rightMotor")
        self._left_sensor = api.sensor.proximity("Pioneer_p3dx_ultrasonicSensor3")
        self._right_sensor = api.sensor.proximity("Pioneer_p3dx_ultrasonicSensor6")

    def rotate_right(self, speed=2.0):
        self._set_two_motor(speed, -speed)

    def rotate_left(self, speed=2.0):
        self._set_two_motor(-speed, speed)

    def move_forward(self, speed=2.0):
        self._set_two_motor(speed, speed)

    def move_backward(self, speed=2.0):
        self._set_two_motor(-speed, -speed)

    def _set_two_motor(self, left: float, right: float):
        self._left_motor.set_target_velocity(left)
        self._right_motor.set_target_velocity(right)

    def right_length(self):
        return self._right_sensor.read()[1].distance()

    def left_length(self):
        return self._left_sensor.read()[1].distance()

api = VRepApi.connect("127.0.0.1", 19997)

api.simulation.start()

r = PioneerP3DX(api)
for _ in range(100):
    rl = r.right_length()
    ll = r.left_length()
    if rl != 0 and rl < 10:
        r.rotate_left()
    elif ll != 0 and ll < 10:
        r.rotate_right()
    else:
        r.move_forward()
    time.sleep(0.1)

api.simulation.stop()



