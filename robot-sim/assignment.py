from __future__ import print_function

import time
from sr.robot import *

R = Robot()

a_th = 2.0
""" float: Threshold for the control of the orientation"""
d_th = 0.4
""" float: Threshold for the control of the linear distance"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn_cws(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

markers_captured = []
""" Lists of markers captured by robot"""

def find_marker(marker_code = None):
    dist = 100
    
    for marker in R.see():
        if marker_code is not None:
            # we are looking for specific marker
            if marker.info.offset in markers_captured[:-1]:
                # this is the marker we are looking for, get distance
                dist = marker.dist
                rot_y = marker.rot_y
                mark = marker.info.offset
        else:
            # we are looking for the closest box which was not found yet
            if marker.info.offset in markers_captured:
                print(f"This fella no {marker.info.offset} was already touched")
                dist = 100
            else:
                print(f"looking for a new box these are already found {markers_captured}")
                if marker.dist < dist:
                    dist = marker.dist
                    rot_y = marker.rot_y  
                    mark = marker.info.offset
    if dist == 100:
        # In this case no box is seen or it doesnt see the box we are looking or
        return -1, -1, -1
    else:
        return dist, rot_y, mark
    
        

        


current_marker = None
while 1:
    
    dist, rot_y, mark = find_marker(current_marker)
    
    if not markers_captured:
        # lets choose the first box as the place we throw them all
        print("Powiedz mi ze nie jestes tutaj")
        markers_captured.append(mark)
    
    
    if dist == -1:
        # It either sees no boxes or no boxes
        print("I dont see anything interesting")
        turn_cws(-20, 0.5)
    elif dist > d_th :
        # Robot sees marker
        if rot_y > a_th:
            # Rotate right
            print("Right a bit...")
            turn_cws(2, 0.5)
        elif rot_y < -a_th:  
            # Rotate left 
            print("Left a bit...")
            turn_cws(-2, 0.5)
        else:
            # Robot is oriented on the target, drive forward.
            print("Ah, that'll do.")
            if dist > 2.5*d_th:
                drive(3*35, 0.1)
            else:
                drive(10, 0.5)
    else:
        # Robot is within threshold
        if not current_marker:
            # if current marker is empty, we are looking for  
            if R.grab(): 
                # Robot grabbed the box
                print("Gotcha!")
                # set our main goal to the first marker
                for marker in R.see():
                    if marker.dist <= d_th:
                        markers_captured.append(mark)
                print(f"This is the list {markers_captured} and this is the list without the last element {markers_captured[:-1]}")
                current_marker = markers_captured[0]
                d_th = 1.5*d_th;
                time.sleep(1)

            else:
                print("Grab failed")
        else:

            R.release()
            print("Box dumped")
            current_marker = None
            d_th = d_th / 1.5
            print(markers_captured)
            drive(-20, 3)
            turn_cws(10,2)
    

        
    
    print(print(f"Closest marker {mark} is {dist} away and {rot_y}"))
    print(R.see())

    
    
