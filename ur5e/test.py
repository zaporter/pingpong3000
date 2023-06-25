import urx
import time

rob = urx.Robot("10.1.10.82")
time.sleep(1)  #leave some time to robot to process the setup commands
rob.set_tcp((0, 0, 0.1, 0, 0, 0))
time.sleep(1)  #leave some time to robot to process the setup commands
rob.set_payload(0.01, (0, 0, 0.1))
time.sleep(1)  #leave some time to robot to process the setup commands
print("started")
print(rob.is_running())
a=10.0
v=20.0
rob.movej((0.1, 0, 0, 0, 0, 0), a, v, wait=True)
# rob.movej((3, -0.75, 0, 1, 0, 0), a, v, wait=True)
rob.close()
print("finished")
# rob.movel((x, y, z, rx, ry, rz), a, v)
# print "Current tool pose is: ",  rob.getl()
# rob.movel((0.1, 0, 0, 0, 0, 0), a, v, relative=true)  # move relative to current pose
# rob.translate((0.1, 0, 0), a, v)  #move tool and keep orientation
#rob.stopj(0.1)
print("stopped")

# rob.movel(x, y, z, rx, ry, rz), wait=False)

# rob.movel(x, y, z, rx, ry, rz), wait=False)
# while rob.getForce() < 50:
#     sleep(0.01)
#     if not rob.is_program_running():
#         break
# rob.stopl()

# try:
#     rob.movel((0,0,0.1,0,0,0), relative=True)
# except RobotError, ex:
#     print("Robot could not execute move (emergency stop for example), do something", ex)
