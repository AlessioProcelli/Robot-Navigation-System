import utm
import Coordinates
from sensor_msgs.msg import NavSatFix
import ROSManager
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import Imu
import math
import Point
from nav_msgs.msg import Odometry
import ConstantManager


class PositionManager:
    
    
    def __init__(self):  
        self.ros_mng=ROSManager.ROSManager()
        self.current_rotation=0
        self.cost_mng=ConstantManager.ConstantManager()
        self.ros_mng.register_subscriber(self.cost_mng.get_constant("POS_NODE"),
                                         NavSatFix, self.take_pos)
        self.ros_mng.register_subscriber(self.cost_mng.get_constant("ROTATION_NODE"),
                                         Imu,self.rotation_callback)
        self.ros_mng.register_subscriber(self.cost_mng.get_constant("LOC_POS_NODE"), Odometry,
                                         self.odometry_callback)
        
        print("PositionManager Connect")
        
    # take first robot position    
    def take_pos(self,msg):
        print("Current NavSatFix position:")
        print("Latitude:", msg.latitude," Longitude:", msg.longitude)
        
        initial_cord=Coordinates.Coordinates(msg.latitude,msg.longitude,msg.altitude)
        self.initial_pos=initial_cord
        self.ros_mng.unsubscribe(self.cost_mng.get_constant("POS_NODE"))
        
        
    #update current robot pos    
    def update_pos(self,msg):
        current_cord=Coordinates.Coordinates(msg.latitude,msg.longitude,msg.altitude)
        self.current_pos=current_cord

    def find_utm_coords(self,lat, lon):
        u = utm.from_latlon(float(lat), float(lon))
        east = float(u[0])
        north = float(u[1])
        return north, east
    
    def find_map_coords(self,point_lat, point_lon):
        #find utm coordinate of the datum
        datum_north, datum_east = self.find_utm_coords(
                self.initial_pos.latitudine,
                self.initial_pos.longitudine)
        #find utm coordinate of the desired point
        point_north, point_east = self.find_utm_coords(point_lat, point_lon)
        X = point_east - datum_east
        Y = point_north - datum_north
        
        return X, Y
    
    def find_lat_lon(self, x, y):
        # Calculate the UTM coordinates of the datum point
        datum_utm = utm.from_latlon(self.initial_pos.latitudine,
                    self.initial_pos.longitudine)
        datum_easting =datum_utm[0]
        datum_northing = datum_utm[1]
        datum_zone_number = datum_utm[2]
        datum_zone_letter = datum_utm[3]
    
        # Calculate the UTM coordinates of the desired point
        point_easting = datum_easting+x
        point_northing = datum_northing+y
    
        # Convert UTM coordinates back to latitude and longitude
        point_latlon = utm.to_latlon(float(point_easting),
                                     float(point_northing), datum_zone_number, datum_zone_letter)
    
        return point_latlon
        
    def rotation_callback(self,msg):
         # Retrieve orientation from the IMU message
        orientation = msg.orientation
        quaternion = [orientation.x, orientation.y, orientation.z, orientation.w]
        euler = euler_from_quaternion(quaternion)
        roll, pitch, yaw = euler
    
        # Convert yaw angle to degrees and wrap it within the range of 0 to 360
        #per farlo tornare con cordinate
        
        yaw_degrees = math.degrees(yaw)
        if yaw_degrees < 0:
            yaw_degrees=(yaw_degrees+360)%360
            
        
        
        self.current_rotation=yaw
        
    # Set Current Position over local map
    def odometry_callback(self,msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.current_pos=Point.Point(x,y)
        
        






        