#!/usr/bin/env python3

import rospy
import threading
import numpy as np
import code
from std_msgs.msg import Float64MultiArray, MultiArrayDimension
from dsr_msgs.srv import MoveLine, MoveJoint, MoveHome, MoveWait, Fkin, Ikin
from dsr_msgs.srv import MoveSplineTask, MoveSplineTaskRequest
from dsr_msgs.srv import GetCurrentPose, SetCurrentTcp, ConfigCreateTcp, GetCurrentTcp, ConfigDeleteTcp
from SplineTrajectory import SplineTrajectory


class RobotController:
    def __init__(self):
        self.Running = False
        self.lock = threading.Lock()
        self.SamplingTime = 100/1000
        self.launcher_model = "a0509_custom"
        self.TCP_Offset = [0,-34.5,-397.5,0,0,0]

        self.Function_MoveWait = None
        self.Function_MoveHome = None
        self.Function_MoveLine = None
        self.Function_MoveJoint = None
        self.Function_GetPose = None

        self.EE_Position = None
        self.EE_Rotation = None

        self.Velocity = [50, 20]
        self.Acceleration = [30, 20]
        self.InitJoint = [11.859779357910156, -0.6888203024864197, 99.6191177368164, -1.7431619358347097e-15, 81.0697021484375, 11.859779357910159]
        self.InitPose = [350/1000, 73.5/1000, 383.5/1000, 0]


    def Ready(self):
        # Model Name
        modelName = self.launcher_model

        # Preprocessing
        rospy.init_node('Sejun_RobotController', anonymous=True)
        rospy.wait_for_service('/dsr01' + modelName + '/motion/move_home')
        rospy.wait_for_service('/dsr01' + modelName + '/motion/move_joint')

        # Functions
        self.Function_MoveHome = rospy.ServiceProxy('/dsr01' + modelName + '/motion/move_home', MoveHome)
        self.Function_MoveWait = rospy.ServiceProxy('/dsr01' + modelName + '/motion/move_wait', MoveWait)
        self.Function_MoveLine = rospy.ServiceProxy('/dsr01' + modelName + '/motion/move_line', MoveLine)
        self.Function_MoveJoint = rospy.ServiceProxy('/dsr01' + modelName + '/motion/move_joint', MoveJoint)
        self.Function_MoveSpline = rospy.ServiceProxy('/dsr01' + modelName + '/motion/move_spline_task', MoveSplineTask)
        self.Function_GetPose = rospy.ServiceProxy('/dsr01' + modelName + '/system/get_current_pose', GetCurrentPose)


        self.Running = True
        print("Ready!")
        print("")


    def Move_Home(self):

        results = self.Function_MoveHome()
        if results.success == True:
            print("Homing...")
            self.Function_MoveWait()
            print("Done!")
            print("")
        else:
            print("Failed...")
            print("")



    def Move_Abs(self, X, Y, Z, Phi):
        pose = [X, Y, Z, 0, 180, Phi]
        vel = self.Velocity
        acc = self.Acceleration
        time = 0
        radius = 0
        ref = 0
        mode = 0
        blendType = 0
        syncType = 0

        if self.Running:
            print("Moving...")
            results = self.Function_MoveLine(pose, vel, acc, time, radius, ref, mode, blendType, syncType)
            if results.success == True:

                self.Function_MoveWait()
                print("Done!")
                print("")
            else:
                print("Failed...")
                print("")



    def Move_Rel(self, X, Y, Z, Phi):
        pose = [X, Y, Z, 0, 0, Phi]
        vel = self.Velocity
        acc = self.Acceleration
        time = 0
        radius = 0
        ref = 0
        mode = 1
        blendType = 0
        syncType = 0

        if self.Running:
            print("Moving...")
            results = self.Function_MoveLine(pose, vel, acc, time, radius, ref, mode, blendType, syncType)
            if results.success == True:

                self.Function_MoveWait()
                print("Done!")
                print("")
            else:
                print("Failed...")
                print("")



    def Move_Joint(self, q):
        vel = 20
        acc = 20
        time = 0
        radius = 0
        mode = 0
        blendType = 0
        syncType = 0

        if self.Running:
            print("Moving...")
            results = self.Function_MoveJoint(q, vel, acc, time, radius, mode, blendType, syncType)
            if results.success == True:

                self.Function_MoveWait()
                print("Done!")
                print("")
            else:
                print("Failed...")
                print("")


    def MoveSpline(self, X_Y_Z_Phi_ListArray, mode=1):

        req = MoveSplineTaskRequest()
        req.pos = []
        for XYZPhi in X_Y_Z_Phi_ListArray:
            fma = Float64MultiArray()
            dim = MultiArrayDimension()
            dim.label = "pose"
            dim.size = 6
            dim.stride = 6
            fma.layout.dim = [dim]
            fma.layout.data_offset = 0
            x,y,z,phi = XYZPhi
            fma.data = [x, y, z, 0, 0, phi]
            req.pos.append(fma)

        req.posCnt = len(req.pos)
        req.acc = [50.0, 50.0]
        req.vel = [50.0, 50.0]
        req.time = 0.0
        req.ref = 0
        req.mode = mode # Abs:0, Rel:1
        req.opt = 0
        req.syncType = 0

        if self.Running:
            print("Moving...")
            results = self.Function_MoveSpline(req)
            if results.success == True:
                self.Function_MoveWait()
                print("Done!")
                print("")
            else:
                print("Failed...")
                print("")



    def SplineTrajectory(self, Rel_Move):
        Pose = self.Function_GetPose(1)
        pos_abs = Pose.pos[:3]
        Points = np.zeros([len(Rel_Move)+1,3], float)
        Points[0] = pos_abs

        for i in range(len(Rel_Move)):
            Points[i+1] = Points[i] + Rel_Move[i]

        X_Y_Z_Phi_ListArray = SplineTrajectory(Points)

        self.MoveSpline(X_Y_Z_Phi_ListArray, mode=0)




    def Init_Pose(self):
        if self.Running:
            self.Move_Joint(self.InitJoint)



    def Get_Joint(self):
        with self.lock:
            Pose = self.Function_GetPose(0)
        print("")
        return Pose.pos



    def Get_Pose(self):
        with self.lock:
            Pose = self.Function_GetPose(1)
        print("")
        return Pose.pos



    def Track_EE(self):
        print("Tracking...")
        while self.Running:
            Pose = self.Function_GetPose(1)
            with self.lock:
                self.EE_Position = Pose.pos[:3]
                self.EE_Rotation = Pose.pos[3:]
            print(f"Pose: {self.EE_Position}")
            rospy.sleep(1)
        print("Done!")
        print("")



    def SetTCP(self):
        CreatTCP = rospy.ServiceProxy('/dsr01' + self.launcher_model + '/tcp/config_create_tcp', ConfigCreateTcp)
        Result1 = CreatTCP(name="SJ_TCP", pos=self.TCP_Offset)
        SetTCP = rospy.ServiceProxy('/dsr01' + self.launcher_model + '/tcp/set_current_tcp', SetCurrentTcp)
        Result2 = SetTCP(name="SJ_TCP")
        GetTCP = rospy.ServiceProxy('/dsr01' + self.launcher_model + '/tcp/get_current_tcp', GetCurrentTcp)
        Result3 = GetTCP()
        if Result1.success == True and Result2.success == True:
            print("TCP Setting Done!")
            print("Current TCP Name:" + Result3.info)
            print("")
        else:
            print("TCP Setting Failed!")
            print("")



    def DeletTCP(self):
        DeletTCP = rospy.ServiceProxy('/dsr01' + self.launcher_model + '/tcp/config_delete_tcp', ConfigDeleteTcp)
        Result = DeletTCP(name="SJ_TCP")
        if Result.success == True:
            print("TCP Deleting Done!")
            print("")
        else:
            print("TCP Deleting Failed!")
            print("")


    def Fkin(self, q):
        Function_Fkin = rospy.ServiceProxy('/dsr01' + self.launcher_model + '/motion/fkin', Fkin)
        Result = Function_Fkin(pos=q, ref=2)
        Pose = Result.conv_posx
        return Pose


    def EndController(self):
        self.Running = False


if __name__ == "__main__":
    RC = RobotController()
    RC.Ready()

    # EE_Tracker = threading.Thread(target=RC.Track_EE, daemon=True)
    # EE_Tracker.start()

    # RC.Move_Home()

    banner = "\n Waiting Your Order..."
    locals_dict = {"RC":RC,
                   'MoveJoint':RC.Move_Joint,
                   'MoveRel':RC.Move_Rel,
                   'MoveAbs':RC.Move_Abs,
                   'GetPose':RC.Get_Pose,
                   'GetJoint':RC.Get_Joint,
                   'HomePose':RC.Move_Home,
                   'InitPose':RC.Init_Pose,
                   'SetTcp':RC.SetTCP,
                   'MoveSpline':RC.MoveSpline
                   }

    code.interact(banner=banner, local=locals_dict)

    RC.EndController()
