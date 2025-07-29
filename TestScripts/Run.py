import sys
import os
import code
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from GazeboSimulator import GazeboSimulator
from RobotController import RobotController

Gazebo = GazeboSimulator(RealMode=False)
Gazebo.launcher_name = "SJ_Custom" # or single_robot_gazebo
Gazebo.launcher_model = "a0509_custom" # or a0509/a0509_Calibration
Gazebo.VirtualMode()

RC = RobotController()
RC.launcher_name = Gazebo.launcher_name
RC.launcher_model = Gazebo.launcher_model
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
               }

code.interact(banner=banner, local=locals_dict)

RC.EndController()