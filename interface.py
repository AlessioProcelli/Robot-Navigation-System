#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 18:24:33 2023

@author: alessio
"""

from flask import Flask, jsonify,send_file,render_template, request,send_from_directory
from flask_cors import CORS
import PositionManager
import ActionManager
import ROSManager
import Point
import rospy
import CriticalPoint
import FileManager
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
# enable CORS
#CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/get_yaw_angle')
def get_yaw_angle_route():
    yaw_angle = pos_manager.current_rotation
    #print(yaw_angle)
    return jsonify(yaw_angle=yaw_angle)


@app.route('/coordinates', methods=['POST'])
def receive_coordinates():
    data = request.get_json()
    lat = data['lat']
    lng = data['lng']
    print(lat)
    print(lng)
    print(pos_manager.find_map_coords(lat, lng))

@app.route('/move_robot', methods=['POST'])
def move_robot():
    # Get the direction from the request data
    direction = request.json['direction']
    print(direction)
    # Publish the movement command to the robot
    # Perform the necessary action based on the direction

    # Return a response if needed
    return 'Command received'
@app.route('/get_robot_position')
def get_robot_position():
    # Logic to retrieve the robot's current position
    robot_latitude,robot_longitude = pos_manager.find_lat_lon(
            pos_manager.current_pos.x, pos_manager.current_pos.y)# Example value
    
   

    # Return the robot's position as JSON
    return jsonify(latitude=robot_latitude, longitude=robot_longitude)

@app.route('/move_action', methods=['POST'])
def handle_action():
    data = request.json
    action = data['action']
    print(action)
    act_manager.move_robot(action)
    # Perform the corresponding action on the robot based on the received action

    return "ok"
    
@app.route('/i')
def index():
    
    current_lat = pos_manager.initial_pos.latitudine # Initial latitude
    current_lng = pos_manager.initial_pos.longitudine  # Initial longitude
    return render_template('index.html',initial_latitude=current_lat,
                           initial_longitude=current_lng)
    #return render_template('scan.html')

@app.route('/process_rectangle', methods=['POST'])
def process_rectangle():
    data = request.get_json()
    # Access the vertex coordinates
    north_east = data['northEast']
    south_west = data['southWest']
    north_west = data['northWest']
    south_east = data['southEast']
    print(data)
    #print(pos_manager.find_map_coords)
    print("lat e long")
    latitude,longitude=pos_manager.find_map_coords(north_west["lat"],north_west["lng"])
    nordW=Point.Point(latitude,longitude)
    latitude,longitude=pos_manager.find_map_coords(north_east["lat"],north_east["lng"])
    nordE=Point.Point(latitude,longitude)
    latitude,longitude=pos_manager.find_map_coords(south_east["lat"],south_east["lng"])
    sudE=Point.Point(latitude,longitude)
    latitude,longitude=pos_manager.find_map_coords(south_west["lat"],south_west["lng"])
    sudW=Point.Point(latitude,longitude)
    print(nordW.print_values())
    print(pos_manager.find_lat_lon(nordW.x,nordW.y))
    #print(nordE.print_values())
    #print(sudE.print_values())
    #print(sudW.print_values())
    res=act_manager.greek_movement(nordW,nordE,sudE,sudW)
    resUtm=[]
    for el in res:
        x,y=pos_manager.find_lat_lon(el.x,el.y)
        point=Point.Point(x,y)
        resUtm.append(point.to_dict())
        
    #print(resUtm)
    #act_manager.go_to_goal(x,y)
    #print(north_west)
    #print(south_west)
    # Perform any necessary processing with the vertex coordinates
    # ...

    # Return a response if needed
    #response = {'message': 'Rectangle coordinates processed successfully'}
    return jsonify(vector=resUtm)

@app.route('/take_critical_point', methods=['POST'])
def take_critical_point():
    
    print("provo")
    cp=act_manager.critical_points
    res=[]
    for el in cp:
        print("ok")
        x,y=pos_manager.find_lat_lon(el.point.x,el.point.y)
        point=Point.Point(x,y)
        critP=CriticalPoint.CriticalPoint(point,False,el.unique_id)
        print(critP.to_dict())
        res.append(critP.to_dict())
    print("fatto")
    for el in res:
        print(el)   
    #print(resUtm)
    #act_manager.go_to_goal(x,y)
    #print(north_west)
    #print(south_west)
    # Perform any necessary processing with the vertex coordinates
    # ...

    return jsonify(res)

@app.route('/del-action-goal', methods=['POST'])
def button_action():
    # Ferma tutti i goals
    print("stop_clikked")
    act_manager.stop_goals()
    return 'Button clicked!'

@app.route('/process_critical_point', methods=['POST'])
def process_critical_point():
    # Retrieve the ID from the request payload
    id = request.json['id']
    print(id)
    # Process the ID as needed
    points=act_manager.critical_points
    for el in points:
        if id== el.unique_id:
            print("trovato")
            res=el
    
    
    # Return the result as JSON
    return jsonify(res.to_dict())

#return scan Page
@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/get_3d_scans', methods=['GET'])
def get_3d_image():
    # Create a simple 3D image
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    # Convert the image data to a list for JSON serialization
    image_data = Z.tolist()

    # Return the image data as JSON
    return jsonify(image_data=image_data)


if __name__ == '__main__':
    #inizializzo Nodo RosManager signleton
    
    ros_manager = ROSManager.ROSManager()
    pos_manager = PositionManager.PositionManager()
    act_manager = ActionManager.ActionManager()
    fil_manager=FileManager.FileManager()
    
    """
    #image_data = np.random.rand(60, 60, 40)

    # Generate a random filename
    #filename = "random_image.npy"
    x = np.random.rand(100)
    y = np.random.rand(100)
    z = np.random.rand(100)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    plt.savefig('static/images/scans/3d_image.png')

    # Save the image
    #fil_manager.save_3d_image(image_data, filename)
    
    #act_manager.greek_movement(Point.Point(1,1),
    #Point.Point(3,1),Point.Point(3,0),Point.Point(1,0))
    #rospy.spin()
    #for el in res:
       # print(el.print_values())
    """    
  
    app.run()
    
    
    