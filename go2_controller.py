import time
import sys
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
from unitree_sdk2py.go2.sport.sport_client import (
    SportClient,
    PathPoint,
    SPORT_PATH_POINT_SIZE,
)
import math
from dataclasses import dataclass

class Go2Controller:
    def __init__(self):
        ChannelFactoryInitialize(0, "enx00e04c6800da")
        self.sport_client = SportClient()
        self.sport_client.SetTimeout(10.0)
        self.sport_client.Init()

    def control(self, gesture_buffer):
        gesture_id = gesture_buffer.get_gesture()
        print("GESTURE", gesture_id)

        if gesture_id == 0:  # Forward
            self.sport_client.Move(0.3,0,0)
        elif gesture_id == 1:  # STOP
            self.sport_client.StopMove()
        if gesture_id == 5:  # Back
            self.sport_client.Move(-0.3,0,0)

        elif gesture_id == 2:  # UP
            self.sport_client.RiseSit()
            self.sport_client.FreeWalk(True)
        elif gesture_id == 4:  # DOWN
            self.sport_client.Sit()

        elif gesture_id == 3:  # LEFT LAND
            self.sport_client.Dance1()
        elif gesture_id == 8:  # RIGHT LAND
            self.sport_client.Heart()

        elif gesture_id == 6: # LEFT
            self.sport_client.Move(0, 0, 0.6)
        elif gesture_id == 7: # RIGHT
            self.sport_client.Move(0, 0, -0.6)

        elif gesture_id == -1:
            ...