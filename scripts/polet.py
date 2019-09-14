import rospy
import cv2
from clever import srv
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from red import linii
#from polet import polet
import time

rospy.init_node('computer_vision_sample')
bridge = CvBridge()


get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
z0=int(input())





def polet(yaw, yaw_2, z0):
    if yaw!=yaw_2:
        z = z0-get_telemetry().z
        navigate(yaw=yaw, z=z, yaw_rate=0.5, frame_id='body')
        time.sleep(1)
        z = z0 - get_telemetry().z
        navigate(x=0.3, z=z, speed=1, frame_id='body')
        time.sleep(1)
    else:
        z = z0 - get_telemetry().z
        navigate(x=0.3, z=z, speed=1, frame_id='body')
        time.sleep(1)
    #if yaw==0:
        #rospy.sleep(1)
        #land()


navigate(x=0, y=0, z=z0, speed=0.5, frame_id='body', auto_arm=True)

time.sleep(3)
yaw_2=0
def image_callback(data):

    global yaw_2
    cv_image = bridge.imgmsg_to_cv2(data, 'bgr8')  # OpenCV image
    # Do any image processing with cv2...
    cv_image= linii(cv_image)
    from red import arctg
    yaw_i=arctg
    polet(yaw_i, yaw_2)
    print('2')
    yaw_2=yaw_i
    image_pub.publish(bridge.cv2_to_imgmsg(cv_image, 'bgr8'))


image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)
image_pub = rospy.Publisher('~debug', Image, queue_size=10)

rospy.spin()
