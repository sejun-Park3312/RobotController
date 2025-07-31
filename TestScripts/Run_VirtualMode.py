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

banner = "\n Waiting Your Order..."
locals_dict = {"RC": RC,
               'MoveJoint': RC.Move_Joint,
               'MoveRel': RC.Move_Rel,
               'MoveAbs': RC.Move_Abs,
               'GetPose': RC.Get_Pose,
               'GetJoint': RC.Get_Joint,
               'HomePose': RC.Move_Home,
               'InitPose': RC.Init_Pose,
               'SetTcp': RC.SetTCP,
               'MoveSpline': RC.MoveSpline
               }

code.interact(banner=banner, local=locals_dict)

# rel = [[0,-25,0], [40,0,0], [0,50,0], [-80,0,0]]
# RC.SplineTrajectory(rel)


