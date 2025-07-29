## <<Before Starting, Open Gazebo>>
## <<Copy and Paste the Following Commands into Terminal!!>>
## ---------------------------------------------

# cd ~/catkin_ws
#  source devel/setup.bash

#  에뮬레이터 모델 지정하기
#  docker run -it --rm \
#   --name dsr01_emulator \
#   -e ROBOT_ID=dsr01 \
#   -e ROBOT_MODEL=a0509 \
#   -p 12345:12345 \
#   doosanrobot/dsr_emulator:3.0.1

# roslaunch dsr_launcher single_robot_gazebo.launch model:=a0509
# roslaunch dsr_launcher SJ_Custom.launch model:=a0509_custom mode:=virtual
# roslaunch dsr_launcher SJ_Custom.launch model:=a0509_Calibration mode:=real host:=192.168.0.181 port:=12345
## ---------------------------------------------

## <<Connection LAN>>
# sudo ip addr add 192.168.0.100/24 dev enx00e04f82fbd0
# sudo ip link set enx00e04f82fbd0 up
# ping 192.168.0.181
## ---------------------------------------------

## <<Console Control>>
## <<Copy and Paste the Following Commands into "New" Terminal!!>>
## ---------------------------------------------
# python3 RobotController.py
## ---------------------------------------------

import rospy
import threading
import subprocess
import code
from dsr_msgs.srv import MoveLine, MoveJoint, MoveHome, MoveWait, Fkin, Ikin
from dsr_msgs.srv import GetCurrentPose, SetCurrentTcp, ConfigCreateTcp, GetCurrentTcp, ConfigDeleteTcp


class RobotController:
    def __init__(self, modelName="a0509_custom"):
        self.Running = False
        self.lock = threading.Lock()
        self.SamplingTime = 100/1000
        self.modelName = modelName
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
        self.InitJoint = [11.9, 4.15, 112.47, 0, 63.38, 11.9]
        self.InitPose = [210.5/1000, 42/1000, 358.0/1000]



    def Ready(self):
        # Model Name
        modelName = self.launch_model
        print("Preprocessing...")
        print("---------------------------")
        print("")

        # ROS
        print("Wait for ROS Service...")
        rospy.init_node('Sejun_RobotController', anonymous=True)
        rospy.wait_for_service('/dsr01' + modelName + '/motion/move_home')
        rospy.wait_for_service('/dsr01' + modelName + '/motion/move_joint')
        print("Ros Service is Ready!")
        print("")

        # Doosan API Handle
        print("Define Doosan API Messages...")
        self.Function_MoveHome = rospy.ServiceProxy('/dsr01' + modelName + '/motion/move_home', MoveHome)
        self.Function_MoveWait = rospy.ServiceProxy('/dsr01' + modelName + '/motion/move_wait', MoveWait)
        self.Function_MoveLine = rospy.ServiceProxy('/dsr01' + modelName + '/motion/move_line', MoveLine)
        self.Function_MoveJoint = rospy.ServiceProxy('/dsr01' + modelName + '/motion/move_joint', MoveJoint)
        self.Function_GetPose = rospy.ServiceProxy('/dsr01' + modelName + '/system/get_current_pose', GetCurrentPose)
        print("Doosan API Messages Defined!")
        print("")

        print("---------------------------")
        print("Preprocessing Done!")
        print("")
        print("")


    def OpenGazeboSimulation(self):
        # Open Emulator(Choose Right Robot Model DRCF!!)
        Docker_Msg = "docker run -it --rm \ --name dsr01_emulator \ -e ROBOT_ID=dsr01 \ -e ROBOT_MODEL=a0509 \ -p 12345:12345 \ doosanrobot/dsr_emulator:3.0.1"
        print("Opening Docker Emulator...")
        subprocess.Popen(['bash', '-c', Docker_Msg])
        print("Emulator Opened!")
        print("")

        Gazebo_Msg = "cd ~/catkin_ws ; source devel/setup.bash ; roslaunch dsr_launcher SJ_Custom.launch model:=" + self.modelName
        print("Opening Gazebo Simulator...")
        subprocess.Popen(['gnome-terminal','--title=Gazebo','--','bash', '-c', Gazebo_Msg + "; exec bash"])
        print("Gazebo Opened!")
        print("")
        print("")



    def ConnectIP(self, Device):
        # Find IP Device Name
        ConnectIP_Msg = "sudo ip addr add 192.168.0.100/24 dev" + Device + "\ sudo ip link set enx00e04f82fbd0 up \ ping 192.168.0.181"



    def ConnectRealRobot(self):
        # Real Robot
        RealRobot_Msg = "cd ~/catkin_ws \ source devel/setup.bash \ roslaunch dsr_launcher SJ_Custom.launch model:=" + self.modelName



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
        CreatTCP = rospy.ServiceProxy('/dsr01' + self.modelName + '/tcp/config_create_tcp', ConfigCreateTcp)
        Result1 = CreatTCP(name="SJ_TCP", pos=self.TCP_Offset)
        SetTCP = rospy.ServiceProxy('/dsr01' + self.modelName + '/tcp/set_current_tcp', SetCurrentTcp)
        Result2 = SetTCP(name="SJ_TCP")
        GetTCP = rospy.ServiceProxy('/dsr01' + self.modelName + '/tcp/get_current_tcp', GetCurrentTcp)
        Result3 = GetTCP()
        if Result1.success == True and Result2.success == True:
            print("TCP Setting Done!")
            print("Current TCP Name:" + Result3.info)
            print("")
        else:
            print("TCP Setting Failed!")
            print("")



    def DeletTCP(self):
        DeletTCP = rospy.ServiceProxy('/dsr01' + self.modelName + '/tcp/config_delete_tcp', ConfigDeleteTcp)
        Result = DeletTCP(name="SJ_TCP")
        if Result.success == True:
            print("TCP Deleting Done!")
            print("")
        else:
            print("TCP Deleting Failed!")
            print("")


    def Fkin(self, q):
        Function_Fkin = rospy.ServiceProxy('/dsr01' + self.modelName + '/motion/fkin', Fkin)
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
                   }

    code.interact(banner=banner, local=locals_dict)

    RC.EndController()
rospy.get_param_names()