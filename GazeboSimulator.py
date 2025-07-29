import rospy
import subprocess
import code
from dsr_msgs.srv import MoveLine, MoveJoint, MoveHome, MoveWait, Fkin, Ikin
from dsr_msgs.srv import GetCurrentPose, SetCurrentTcp, ConfigCreateTcp, GetCurrentTcp, ConfigDeleteTcp


class GazeboSimulator:
    def __init__(self, RealMode = False):
        self.RealMode = RealMode
        self.launch_model = "a0509_custom"
        self.launch_name = "SJ_Custom"

        # Virtual Mode
        self.EmulatorModel = "a0509"

        # Real Mode
        self.host = "192.168.0.181" # 실제 로봇의 IP주소
        self.port = "12345"
        self.IP_Device = None



    def VirtualMode(self):
        print("Opening Simulator...")
        print("---------------------------")
        print("")

        print("Opening Docker Emulator...")
        # Close and Remove Existing Docker
        subprocess.run("docker ps -q | xargs -r docker stop", shell=True, executable="/bin/bash")
        subprocess.run("docker ps -aq | xargs -r docker rm", shell=True, executable="/bin/bash")

        # Open Emulator(Choose Right Robot Model DRCF!!)
        Docker_Msg = (
            "docker run -it --rm "
            "--name dsr01_emulator "
            "-e ROBOT_ID=dsr01 "
            "-e ROBOT_MODEL=a0509 "
            "-p 12345:12345 "
            "doosanrobot/dsr_emulator:3.0.1"
        )
        subprocess.Popen(['gnome-terminal', '--title=Docker Emulator', '--', 'bash', '-c', Docker_Msg + '; exec bash'])
        print("Emulator Opened!")
        print("")

        # Open Gazebo
        print("Opening Gazebo...")
        Gazebo_Msg = ("cd ~/catkin_ws; "
                      " source devel/setup.bash; "
                      " roslaunch dsr_launcher " + self.launch_name + ".launch model:=" + self.launch_model)
        subprocess.Popen(['gnome-terminal','--','bash', '-c', Gazebo_Msg])
        print("Gazebo Opened!")
        print("")

        print("---------------------------")
        print("Simulator Opened!")
        print("")
        print("")













## <<Before Starting, Open Gazebo>>
## <<Copy and Paste the Following Commands into Terminal!!>>


    ### <<< Virtual Mode>>>
    ## ---------------------------------------------

        ## <<Open Emulator>>
            #  docker ps -q | xargs -r docker stop
            #  docker ps -aq | xargs -r docker rm
            #  docker run -it --rm \
            #   --name dsr01_emulator \
            #   -e ROBOT_ID=dsr01 \
            #   -e ROBOT_MODEL=a0509 \
            #   -p 12345:12345 \
            #   doosanrobot/dsr_emulator:3.0.1

        ## <<Open Gazebo>>
            # cd ~/catkin_ws
            #  source devel/setup.bash
            # roslaunch dsr_launcher single_robot_gazebo.launch model:=a0509
            # roslaunch dsr_launcher SJ_Custom.launch model:=a0509_custom

    ## ---------------------------------------------




    ### <<<Real Mode>>>
    ## ---------------------------------------------

        ## <<Connect LAN>>
            # ip addr show
            # sudo ip addr add 192.168.0.100/24 dev enx00e04f82fbd0
            # sudo ip link set enx00e04f82fbd0 up
            # ping 192.168.0.181

        ## <<Open Gazebo>>
            # cd ~/catkin_ws
            #  source devel/setup.bash
            # roslaunch dsr_launcher single_robot_gazebo.launch model:=a0509 mode:=real host:=192.168.0.181 port:=12345
            # roslaunch dsr_launcher SJ_Custom.launch model:=a0509_Calibration mode:=real host:=192.168.0.181 port:=12345

    ## ---------------------------------------------
