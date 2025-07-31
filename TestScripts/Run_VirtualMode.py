import sys
import os
import code

from geometry_msgs.msg import PoseArray

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from GazeboSimulator import GazeboSimulator
from RobotController import RobotController

# Gazebo = GazeboSimulator()
# Gazebo.launcher_name = "SJ_Custom" # or single_robot_gazebo/SJ_Custom
# Gazebo.launcher_model = "a0509_custom" # or a0509/a0509_Calibration/a0509_custom
# Gazebo.VirtualMode()

RC = RobotController()
RC.launcher_model = "a0509_custom"
RC.Ready()
rel = [[0,-25,0], [40,0,0], [0,50,0], [-80,0,0]]
RC.SplineTrajectory(rel)


