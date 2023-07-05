#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 18:32:02 2023

@author: alessio
"""
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
import ROSManager
import Point
from geometry_msgs.msg import Twist
import random
import CriticalPoint
import ScanManager
import ConstantManager


class ActionManager:
    
    def __init__(self):
        self.ros_mng=ROSManager.ROSManager()
        self.cost_mng=ConstantManager.ConstantManager()
        self.pub=self.ros_mng.publish_to_node(self.cost_mng.get_constant("VEL_NODE")
                                              , Twist,1)
        self.scan_manager=ScanManager.ScanManager()
        self.goal_queue=[]
        self.critical_points=[]
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.ros_mng.register_subscriber('/move_base/result', MoveBaseActionResult
                                         ,self.move_base_callback_result)
        self.ros_mng.register_subscriber('/move_base/current_goal', MoveBaseActionResult
                                         ,self.move_base_callback_result)
        self.client.wait_for_server()
        print("ActionManager Connect")
        
     
    def move_base_callback_result(self,msg):
        print(msg)
        if len(self.goal_queue)!=0:
            point=self.goal_queue.pop(0)
            for el in self.critical_points:
                if(el.point.x==point.x and el.point.y==point.y):
                    print("CriticalPointcansionato")
                    el.is_visited=True
                    index_to_replace = self.critical_points.index(el)
                    self.critical_points[index_to_replace] = el
                    self.scan_manager.scanPoint(el.unique_id)
        self._do_greek_movement()
        
        
    def go_to_goal(self,p):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.pose.position.x = p.x
        goal.target_pose.pose.position.y = p.y
        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0
        self.client.send_goal(goal)
        print("Goal inviato aspetto il risultato")
        
    def stop_goals(self):
       self.goal_queue=[]
       cancel_goal = MoveBaseGoal()
# Send the empty goal to cancel the current `move_base` goal
       self.client.send_goal(cancel_goal)
       
    def _generate_y_pass(self,y1,y2):
        if y1>=0 and y2>=0:
            res=y1-y2
            return res
        if y1>=0 and y2<=0:
            return (y1-y2)
        if y1<=0 and y2<0:
            return (abs(y2)-abs(y1))
        

    def _generate_greek_movement(self,p1,p2,p3,p4):
    # in square p1 top-left, p2,top-right,p3 bottom-right , p4 bottom-left
        result=[]
        result.append(p1)
        current_x=p1.x
        GREEK_PASS=self.cost_mng.get_constant("GREEK_PASS")
        GREEK_DENSITY=self.cost_mng.get_constant("GREEK_DENSITY")
        pass_y=self._generate_y_pass(p1.y,p4.y)/GREEK_DENSITY

        while current_x <p3.x:
            current_y=p1.y
            while current_y-pass_y>p4.y:
                current_y-=pass_y
                result.append(Point.Point(current_x,current_y))
            result.append(Point.Point(current_x,p4.y))
            current_x+=GREEK_PASS    
            result.append(Point.Point(current_x,p4.y))
            
            if(current_x<p3.x):
                current_y=p4.y
                while current_y+pass_y<p1.y:
                    current_y+=pass_y
                    result.append(Point.Point(current_x,current_y))
                result.append(Point.Point(current_x,p1.y))
                current_x+=GREEK_PASS
                if(current_x<=p3.x):
                    result.append(Point.Point(current_x,p1.y))
        return result     
        
    
    def greek_movement(self,p1,p2,p3,p4):
        self.goal_queue=self._generate_greek_movement(p1,p2,p3,p4)
        self.generate_critical_point()
        print("Point:")
        for el in self.goal_queue:
            el.print_values()
        self._do_greek_movement()
        return self.goal_queue
        
    def _do_greek_movement(self):
        if len(self.goal_queue)!=0:
            point=self.goal_queue[0]
            
            self.go_to_goal(point)
        
    def generate_critical_point(self):
        # Generate a random float within a specific range
        self.critical_points=[]
        length = len(self.goal_queue)
        N_CRIT_POINT=self.cost_mng.get_constant("N_CRIT_POINT")
        for i in range (0,N_CRIT_POINT):
            random_int = random.randint(0, length-2)
            el1=self.goal_queue[random_int]
            el2=self.goal_queue[random_int+1]
            if(el1.x==el2.x):
                random_float = random.uniform(el1.y,el2.y)
                generatedPoint=Point.Point(el1.x,random_float)
                
            else:
                random_float = random.uniform(el1.x,el2.x)
                generatedPoint=Point.Point(random_float,el1.y)
               
            self.goal_queue.insert(random_int+1,generatedPoint)
            self.critical_points.append(CriticalPoint.CriticalPoint(
                        generatedPoint,False)) 
            
            
        
    
    def move_robot(self,action):
        velo_msg = Twist()
    
        rate = rospy.Rate(1)

	# prompt the user for the acceleration value
        SPEED=self.cost_mng.get_constant("SPEED")
        SPEED_ANGULAR=self.cost_mng.get_constant("SPEEDANGULAR")

        if(action=="go_front"):
           
            velo_msg.linear.x=SPEED
        if(action=="go_back"):
            
            velo_msg.linear.x=-SPEED
        if(action=="rotate_right"):
            
            velo_msg.angular.z = -SPEED_ANGULAR
        if(action=="rotate_left"):
            
            velo_msg.angular.z = SPEED_ANGULAR
		
		# publish the increased velocity
        self.ros_mng.publish_msg(self.pub,velo_msg)
        print('Action Published')
        rate.sleep()
        clear_msg = Twist()
        self.ros_mng.publish_msg(self.pub,clear_msg)
    
        
    
        
