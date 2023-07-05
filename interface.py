
"""
Created on Mon Jun 12 18:24:33 2023

@author: Alessio Procelli
"""

from flask import Flask, jsonify,render_template, request
import PositionManager
import ActionManager
import ROSManager
import Point
import CriticalPoint
import ScanManager

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

#get angle for navigation orientation
@app.route('/get_yaw_angle')
def get_yaw_angle_route():
    yaw_angle = pos_manager.current_rotation
    return jsonify(yaw_angle=yaw_angle)

#update robot Position  
@app.route('/get_robot_position')
def get_robot_position():  
    robot_latitude,robot_longitude = pos_manager.find_lat_lon(
            pos_manager.current_pos.x, pos_manager.current_pos.y)
    # Return the robot's position as JSON
    return jsonify(latitude=robot_latitude, longitude=robot_longitude)


#use to send manual commands
@app.route('/move_action', methods=['POST'])
def handle_action():
    # Get the direction from the request data
    data = request.json
    action = data['action']
    act_manager.move_robot(action)
    return "Command received"
  
#index Page 
@app.route('/')
def index():
    
    current_lat = pos_manager.initial_pos.latitudine # Initial latitude
    current_lng = pos_manager.initial_pos.longitudine  # Initial longitude
    return render_template('index.html',initial_latitude=current_lat,
                           initial_longitude=current_lng)
     
    
#used to extract the coordinates of the rectangle drawn
# by the user and establish greek points
@app.route('/process_rectangle', methods=['POST'])
def process_rectangle():
    data = request.get_json()
    # Access the vertex coordinates
    north_east = data['northEast']
    south_west = data['southWest']
    north_west = data['northWest']
    south_east = data['southEast']
    #convert in point in simulation
    latitude,longitude=pos_manager.find_map_coords(north_west["lat"],north_west["lng"])
    nordW=Point.Point(latitude,longitude)
    latitude,longitude=pos_manager.find_map_coords(north_east["lat"],north_east["lng"])
    nordE=Point.Point(latitude,longitude)
    latitude,longitude=pos_manager.find_map_coords(south_east["lat"],south_east["lng"])
    sudE=Point.Point(latitude,longitude)
    latitude,longitude=pos_manager.find_map_coords(south_west["lat"],south_west["lng"])
    sudW=Point.Point(latitude,longitude)
    #create greek point
    res=act_manager.greek_movement(nordW,nordE,sudE,sudW)
    resUtm=[]
    #reconvert point in UTM coordinates
    for el in res:
        x,y=pos_manager.find_lat_lon(el.x,el.y)
        point=Point.Point(x,y)
        resUtm.append(point.to_dict())    
    return jsonify(vector=resUtm)

#used to receive critical points to scan
@app.route('/take_critical_point', methods=['POST'])
def take_critical_point():
    cp=act_manager.critical_points
    res=[]
    #find UTM coordinates of critical point , Convert to json
    for el in cp:
        x,y=pos_manager.find_lat_lon(el.point.x,el.point.y)
        point=Point.Point(x,y)
        critP=CriticalPoint.CriticalPoint(point,False,el.unique_id)
        res.append(critP.to_dict())

    return jsonify(res)

#stop all current goals
@app.route('/del-action-goal', methods=['POST'])
def button_action():
    act_manager.stop_goals()
    return 'Goal Stopped'

#used to evaluate if the critical point has been scanned
@app.route('/process_critical_point', methods=['POST'])
def process_critical_point():
    # Retrieve the ID from the request payload
    id = request.json['id']
    points=act_manager.critical_points
    for el in points:
        if id== el.unique_id:
            res=el

    return jsonify(res.to_dict())

#return scan Page
@app.route('/scan')
def scan():
    id_cp_point = request.args.get('param')
    s=ScanManager.ScanManager() 
    scan=s.findScan(id_cp_point) 
    #extract scan image
    img3d=scan.load_3d_image()
    img2d1=scan.load_2d1_image()
    img2d2=scan.load_2d2_image()                 
    return render_template('scan.html', json_3d_image=img3d.tolist() ,
                           json_2d1_image=img2d1.tolist(),
                           json_2d2_image=img2d2.tolist())
    



if __name__ == '__main__':
    #I initialize the managers
    ros_manager = ROSManager.ROSManager()
    pos_manager = PositionManager.PositionManager()
    act_manager = ActionManager.ActionManager()
    
  
    app.run()
    
    
    