import time
from vrepapi import VRepApi
from math import *
# contextlib
# simpy
# multiprocessing cpu


vrep = VRepApi.connect("127.0.0.1", 19997)
vrep.simulation.stop()
time.sleep(2)
vrep.simulation.start()

j_vel = vrep.joint.with_velocity_control("joint_force")
j_pos = vrep.joint.with_position_control("joint_position")
j_pas = vrep.joint.passive("joint_passive")
j_sph = vrep.joint.spherical("sp_joint")
j_spr = vrep.joint.spring("joint_spring")

s = vrep.sensor.proximity("sensor")
v = vrep.sensor.vision("vision")

j_vel.set_target_velocity(2)
j_spr.set_target_position(2)

for i in range(5):
    b = pi / 9
    j_pos.set_target_position(b * i + 0.2)
    time.sleep(1)

for i in range(50):
    v = sin(i / 10)
    j_pas.set_position(v)
    time.sleep(0.1)

for i in range(1000):
    v = sin(i / 100) * (i / 1000)
    j_sph.set_matrix(
        [0, 0, 0, 0,
         0, 0, 0, 0,
         v, 0, 0, 0])
    time.sleep(0.01)


vrep.simulation.stop()

