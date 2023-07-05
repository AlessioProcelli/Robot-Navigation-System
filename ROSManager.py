#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 18:58:36 2023

@author: Alessio
"""

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import ConstantManager

class ROSManager(object):
    
    _node = None
    _subscribers = {}
    _instance = None
   
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ROSManager, cls).__new__(cls)
            cost_mng=ConstantManager.ConstantManager()
            rospy.init_node(cost_mng.get_constant("NODE_NAME"),anonymous=True)
            cls._instance._node=True
            print("RosManager Created")
        return cls._instance
        
     
    @staticmethod
    def get_node():
        return ROSManager._node

   
    def register_subscriber(self,topic, message_type, callback):
        if ROSManager._instance._node is not None:
            ROSManager._subscribers[topic]=rospy.Subscriber(topic, message_type,callback)
            
        else:
            rospy.logwarn("ROS node is not initialized.")
    
    
    def unsubscribe(self,topic):
        if topic in ROSManager._subscribers:
            
            subscriber = ROSManager._subscribers[topic]
            subscriber.unregister()
            
            del ROSManager._subscribers[topic]
            
        else:
            rospy.logwarn("Subscriber for topic {} not found.".format(topic))


    
    def publish_to_node(self,topic, message_type, queue_size):
        if ROSManager._instance._node is not None:
           pub = rospy.Publisher(topic, message_type, queue_size=queue_size)
           return pub
        else:
            rospy.logwarn("ROS node is not initialized.")
            
    def publish_msg(self,pub,msg):
            pub.publish(msg)
            rospy.sleep(1)
           