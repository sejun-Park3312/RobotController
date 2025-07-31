#!/usr/bin/env python3
import rospy

ROBOT_ID     = "dsr01"
ROBOT_MODEL  = "a0509_custom"
import DR_init
DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL
from DSR_ROBOT import *

rospy.Subscriber('/' + ROBOT_ID + ROBOT_MODEL + '/state', RobotState, msgRobotState_cb)
rospy.spin()
# rospy.spinner(2)

X1 = posx(370, 670, 650, 0, 180, 0)
X1a = posx(370, 670, 400, 0, 180, 0)
X1a2 = posx(370, 545, 400, 0, 180, 0)
X1b = posx(370, 595, 400, 0, 180, 0)
X1b2 = posx(370, 670, 400, 0, 180, 0)
X1c = posx(370, 420, 150, 0, 180, 0)
X1c2 = posx(370, 545, 150, 0, 180, 0)
X1d = posx(370, 670, 275, 0, 180, 0)
X1d2 = posx(370, 795, 150, 0, 180, 0)


seg11 = posb(DR_LINE, X1, radius=20)
seg12 = posb(DR_CIRCLE, X1a, X1a2, radius=21)
seg14 = posb(DR_LINE, X1b2, radius=20)
seg15 = posb(DR_CIRCLE, X1c, X1c2, radius=22)
seg16 = posb(DR_CIRCLE, X1d, X1d2, radius=23)
b_list1 = [seg11, seg12, seg14, seg15, seg16]

moveb(b_list1, vel=150, acc=250, ref=DR_BASE, mod=DR_MV_MOD_ABS)