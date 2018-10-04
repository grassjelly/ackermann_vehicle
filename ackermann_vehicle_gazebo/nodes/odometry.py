#! /usr/bin/env python
import rospy
import math
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from gazebo_msgs.srv import GetLinkState, GetLinkStateRequest
from geometry_msgs.msg import Twist, Pose, Point, Quaternion, Vector3
import tf

steering_angle = 0;

def cmd_callback(vel):
    steering_angle = vel.angular.z

rospy.init_node('odometry_publisher')

odom_pub = rospy.Publisher ('/raw_odom', Odometry)
cmd_sub = rospy.Subscriber('/cmd_vel', Twist, cmd_callback)

rospy.wait_for_service ('/ackermann_vehicle/gazebo/get_link_state')
get_model_srv = rospy.ServiceProxy('/ackermann_vehicle/gazebo/get_link_state', GetLinkState)

odom=Odometry()
header = Header()
header.frame_id='/odom'

left_rear_wheel = GetLinkStateRequest()
left_rear_wheel.link_name = "left_rear_wheel"
left_rear_wheel.reference_frame = "base_footprint"

right_rear_wheel = GetLinkStateRequest()
right_rear_wheel.link_name = "right_rear_wheel"
right_rear_wheel.reference_frame = "base_footprint"

r = rospy.Rate(15)
current_time = rospy.Time.now()
last_vel_time = rospy.Time.now()

x_pos = 0.0
y_pos = 0.0
heading = 0.0

while not rospy.is_shutdown():
    current_time = rospy.Time.now()

    lrw_result = get_model_srv(left_rear_wheel)
    rrw_result = get_model_srv(right_rear_wheel)
    lrw_vel = lrw_result.link_state.twist.angular.y * (0.14605 / 2)
    rrw_vel = rrw_result.link_state.twist.angular.y * (0.14605 / 2)

    linear_velocity = (lrw_vel + rrw_vel) / 2
    angular_velocity = (linear_velocity * math.tan(steering_angle)) / 0.304
    print angular_velocity

    vel_dt = (current_time - last_vel_time).to_sec()
    last_vel_time = current_time
    
    delta_heading = angular_velocity * vel_dt
    delta_x = (linear_velocity * math.cos(heading)) * vel_dt
    delta_y = (linear_velocity * math.sin(heading)) * vel_dt

    x_pos += delta_x
    y_pos += delta_y
    heading += delta_heading

    odom_quat = tf.transformations.quaternion_from_euler(0, 0, heading)

    # next, we'll publish the odometry message over ROS
    odom = Odometry()
    odom.header.stamp = current_time
    odom.header.frame_id = "odom"

    # set the position
    odom.pose.pose = Pose(Point(delta_x, delta_y, 0.), Quaternion(*odom_quat))

    # set the velocity
    odom.child_frame_id = "base_footprint"
    odom.twist.twist = Twist(Vector3(linear_velocity, 0, 0), Vector3(0, 0, angular_velocity))

    # publish the message
    odom_pub.publish(odom)

    r.sleep()