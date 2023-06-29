import utm
import Coordinates
import rospy
from sensor_msgs.msg import NavSatFix
import ROSManager
from tf import transformations
from tf.transformations import euler_from_quaternion
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import Imu
import tf2_ros
import math
import Point
from nav_msgs.msg import Odometry
POS_NODE='/navsat/fix'
class PositionManager:
    
    
    def __init__(self):  
        print("initPositionM")
        self.ros_mng=ROSManager.ROSManager()
        self.current_rotation=0
        self.ros_mng.register_subscriber(POS_NODE, NavSatFix, self.take_pos)
        self.ros_mng.register_subscriber('/imu/data',
                                         Imu,self.rotation_callback)
        self.ros_mng.register_subscriber('/odometry/filtered', Odometry,
                                         self.odometry_callback)
        rospy.sleep(0.3)
        print("finePositionM")
        
    def take_pos(self,msg):
        # Process the received NavSatFix message
        print("Received NavSatFix message:")
        print("Latitude:", msg.latitude)
        print("Longitude:", msg.longitude)
        print("Altitude:", msg.altitude)
        print("---------------------------")
        initial_cord=Coordinates.Coordinates(msg.latitude,msg.longitude,msg.altitude)
        # Unsubscribe from the topic
        self.initial_pos=initial_cord
        self.ros_mng.unsubscribe(POS_NODE)
        
        
    def update_pos(self,msg):
        current_cord=Coordinates.Coordinates(msg.latitude,msg.longitude,msg.altitude)
        self.current_pos=current_cord

    def find_utm_coords(self,lat, lon):
        u = utm.from_latlon(lat, lon)
        east = u[0]
        north = u[1]
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
        #print("X and Y coordinates of poin is %f and %f" %(X, Y))
        return X, Y
    def find_lat_lon(self, x, y):
        # Calculate the UTM coordinates of the datum point
        datum_utm = utm.from_latlon(self.initial_pos.latitudine,
                    self.initial_pos.longitudine)
        datum_easting = datum_utm[0]
        datum_northing = datum_utm[1]
        datum_zone_number = datum_utm[2]
        datum_zone_letter = datum_utm[3]
    
        # Calculate the UTM coordinates of the desired point
        point_easting = x + datum_easting
        point_northing = y + datum_northing
    
        # Convert UTM coordinates back to latitude and longitude
        point_latlon = utm.to_latlon(point_easting, point_northing, datum_zone_number, datum_zone_letter)
    
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
    
    def odometry_callback(self,msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.current_pos=Point.Point(x,y)
        #self.current_pos.print_values()
        # Use the extracted x and y values as required