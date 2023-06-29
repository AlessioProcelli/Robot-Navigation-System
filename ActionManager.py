#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 18:32:02 2023

@author: alessio
"""
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
import tf2_ros
import geometry_msgs.msg
from actionlib_msgs.msg import GoalStatusArray
import tf2_geometry_msgs
import ROSManager
import math
import Point
from geometry_msgs.msg import Twist
import random
import CriticalPoint
from actionlib_msgs.msg import GoalID
is_critical=False
current_critical=0
N_CRIT_POINT=2
GREEK_PASS=2.5
class ActionManager:
    
    def __init__(self):
        self.ros_mng=ROSManager.ROSManager()
        self.pub=self.ros_mng.publish_to_node('/jackal_velocity_controller/cmd_vel', Twist,1)
        self.ros_mng.register_subscriber('jackal_velocity_controller/cmd_vel', Twist, self.increase(Twist))
        
        self.goal_queue=[]
        self.critical_points=[]
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.ros_mng.register_subscriber('/move_base/result', MoveBaseActionResult
                                         ,self.move_base_callback_result)
        self.ros_mng.register_subscriber('/move_base/current_goal', MoveBaseActionResult
                                         ,self.move_base_callback_result)
        #self.ros_mng.register_subscriber('/move_base/status', GoalStatusArray
          #                               ,self.move_base_callback)
        self.client.wait_for_server()
        print("ActionManager Connesct")
        
    def move_base_callback_result(self,msg):
        print(msg)
        
        self._do_greek_movement()
        
        
    def go_to_goal(self,p):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.pose.position.x = p.x
        goal.target_pose.pose.position.y = p.y
        print("ok")
        #goal.target_pose.pose.position.z = 0.0
        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0
        print("okked")
        for el in self.critical_points:
            if(el.point.x==p.x and el.point.y==p.y):
                print("CPPP")
                
    
        self.client.send_goal(goal)
        print("Goal inviato aspetto il risultato")
        
    def stop_goals(self):
       self.goal_queue=[]
       cancel_goal = MoveBaseGoal()

# Send the empty goal to cancel the current `move_base` goal
       self.client.send_goal(cancel_goal)
     

    def _generate_greek_movement(self,p1,p2,p3,p4):
    # in square p1 top-left, p2,top-right,p3 bottom-right , p4 bottom-left
        result=[]
        result.append(p1)
        current_x=p1.x
        
        while current_x <p3.x:
            
            result.append(Point.Point(current_x,p4.y))
            current_x+=GREEK_PASS
            result.append(Point.Point(current_x,p4.y))
            if(current_x<p3.x):
                result.append(Point.Point(current_x,p1.y))
                current_x+=GREEK_PASS
                if(current_x<p3.x):
                    result.append(Point.Point(current_x,p1.y))
                
        if current_x==p3.x:
            result.append(Point.Point(current_x,p4.y))
        return result 
    
    def greek_movement(self,p1,p2,p3,p4):
        
        self.goal_queue=self._generate_greek_movement(p1,p2,p3,p4)
        self.generate_critical_point()
        #self.goal_queue.append(p1,p2)
        for el in self.goal_queue:
            el.print_values()
        self._do_greek_movement()
        return self.goal_queue
        
    def _do_greek_movement(self):
        if len(self.goal_queue)!=0:
            point=self.goal_queue.pop(0)
            print(point.print_values())
            
            self.go_to_goal(point)
        
    def generate_critical_point(self):
        
        # Generate a random float within a specific range
        self.critical_points=[]
        length = len(self.goal_queue)
        print("lengt List")
        print(length)
        for i in range (0,N_CRIT_POINT):
            random_int = random.randint(0, length-2)
            print(random_int)
            el1=self.goal_queue[random_int]
            el2=self.goal_queue[random_int+1]
            print("point")
            print(el1.print_values())
            print(el2.print_values())
            if(el1.x==el2.x):
                random_float = random.uniform(el1.y,el2.y)
                generatedPoint=Point.Point(el1.x,random_float)
                
            else:
                random_float = random.uniform(el1.x,el2.x)
                generatedPoint=Point.Point(random_float,el1.y)
            print("cP inserito")    
            self.goal_queue.insert(random_int+1,generatedPoint)
            print("ok1")
            self.critical_points.append(CriticalPoint.CriticalPoint(
                        generatedPoint,True)) #fix true
            print("ok2")
            
            generatedPoint.print_values()
        
    
    def move_robot(self,action):
        velo_msg = Twist()
        	
	# l = Twist.linear.x
	# print(l)
	# define the rate at which
	# we will be publishing the velocity.
    
        rate = rospy.Rate(1)

	# prompt the user for the acceleration value
        speed = 20

        if(action=="go_front"):
           
            velo_msg.linear.x=speed
        if(action=="go_back"):
            
            velo_msg.linear.x=-speed
        if(action=="rotate_right"):
            
            velo_msg.angular.z = -speed
        if(action=="rotate_left"):
            
            velo_msg.angular.z = speed
		
		# publish the increased velocity
        self.ros_mng.publish_msg(self.pub,velo_msg)
        print('Publishing was successful!')
        rate.sleep()
        clear_msg = Twist()
        self.ros_mng.publish_msg(self.pub,clear_msg)
    
        
        
    def increase(self,msg):

        print('We are in the callback function!')
        print(msg)
       
    
    
    
    
        
