#!/usr/bin/env python3

import os
import numpy as np
import rospy
from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage
from duckietown_msgs.msg import WheelsCmdStamped
import cv2
from cv_bridge import CvBridge

class ImagePublishers(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(ImagePublishers, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # static parameters
        self._bridge = CvBridge()
        self._vehicle_name = os.environ['VEHICLE_NAME']

        self._red_detection_topic = f"/{self._vehicle_name}/camera_node/red_image_mask/compressed"
        self._red_publisher = rospy.Publisher(self._red_detection_topic, CompressedImage)

        self._blue_detection_topic = f"/{self._vehicle_name}/camera_node/blue_image_mask/compressed"
        self._blue_publisher = rospy.Publisher(self._blue_detection_topic, CompressedImage)

        self._green_detection_topic = f"/{self._vehicle_name}/camera_node/green_image_mask/compressed"
        self._green_publisher = rospy.Publisher(self._green_detection_topic, CompressedImage)

        self._yellow_detection_topic = f"/{self._vehicle_name}/camera_node/yellow_image_mask/compressed"
        self._yellow_publisher = rospy.Publisher(self._yellow_detection_topic, CompressedImage)

        self._undistort_topic = f"/{self._vehicle_name}/camera_node/undistorted_image/compressed"
        self._publisher = rospy.Publisher(self._undistort_topic, CompressedImage)

        self._homography_topic = f"/{self._vehicle_name}/camera_node/homography/compressed"
        self._homography_publisher = rospy.Publisher(self._homography_topic, CompressedImage)

        self._homography_yellow_detection_topic = f"/{self._vehicle_name}/camera_node/homography_yellow_mask/compressed"
        self._homography_yellow_detection_publisher = rospy.Publisher(self._homography_yellow_detection_topic, CompressedImage)

        self._homography_blue_detection_topic = f"/{self._vehicle_name}/camera_node/homography_blue_mask/compressed"
        self._homography_blue_detection_publisher = rospy.Publisher(self._homography_blue_detection_topic, CompressedImage)

        self._homography_red_detection_topic = f"/{self._vehicle_name}/camera_node/homography_red_mask/compressed"
        self._homography_red_detection_publisher = rospy.Publisher(self._homography_red_detection_topic, CompressedImage)

        self._undistort_gray_topic = f"/{self._vehicle_name}/camera_node/undistort_gray/compressed"
        self._undistort_gray_publisher = rospy.Publisher(self._undistort_gray_topic, CompressedImage)

        # Publishers need to be set first 
        self._camera_topic = f"/{self._vehicle_name}/camera_node/image/compressed"
        self._camera_sub = rospy.Subscriber(self._camera_topic, CompressedImage, self.callback)

    def callback(self, msg):
        # Convert JPEG bytes to CV image
        image = self._bridge.compressed_imgmsg_to_cv2(msg)

        # Convert warped image to HSV for color detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 100, 100], dtype=np.uint8)  # Lower bound for red
        upper_red = np.array([10, 255, 255], dtype=np.uint8)  # Upper bound for red
        mask_red = cv2.inRange(hsv, lower_red, upper_red)

        lower_blue = np.array([100, 150, 0], dtype=np.uint8)  # Lower bound for blue
        upper_blue = np.array([140, 255, 255], dtype=np.uint8)  # Upper bound for blue
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        lower_green = np.array([40, 40, 150], dtype=np.uint8)  # Lower bound for green (close to #56B49C)
        upper_green = np.array([90, 255, 255], dtype=np.uint8)  # Upper bound for green (close to #56B49C)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        # Define HSV range for detecting **yellow color**
        lower_yellow = np.array([15, 100, 100], dtype=np.uint8)
        upper_yellow = np.array([35, 255, 255], dtype=np.uint8)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Publish the masks
        self._blue_publisher.publish(self._bridge.cv2_to_compressed_imgmsg(mask_blue))
        self._red_publisher.publish(self._bridge.cv2_to_compressed_imgmsg(mask_red))
        self._green_publisher.publish(self._bridge.cv2_to_compressed_imgmsg(mask_green))
        self._yellow_publisher.publish(self._bridge.cv2_to_compressed_imgmsg(mask_yellow))

        undistorted = self.publish_undistorted_image(image)
        homography = self.publish_homography(undistorted)
        self.publish_homography_yellow_mask(homography)
        self.publish_homography_blue_mask(homography)
        self.publish_undistort_grayscale(undistorted)
        self.publish_homography_red_mask(homography)

    def publish_undistort_grayscale(self, undistort):
        image = undistort
        # Convert to grayscale and store it in grayscale_image
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Get image dimensions
        height, width = grayscale_image.shape

        # Crop the right half of grayscale_image
        grayscale_image = grayscale_image[:, width // 2:]

        # Publish the cropped grayscale image
        self._undistort_gray_publisher.publish(self._bridge.cv2_to_compressed_imgmsg(grayscale_image))


    def publish_homography_blue_mask(self, homography):
        # Convert warped image to HSV for color detection
        hsv = cv2.cvtColor(homography, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 150, 0], dtype=np.uint8)  # Lower bound for blue
        upper_blue = np.array([140, 255, 255], dtype=np.uint8)  # Upper bound for blue
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        self._homography_blue_detection_publisher.publish(self._bridge.cv2_to_compressed_imgmsg(mask_blue))

        return mask_blue
    
    def publish_homography_red_mask(self, homography):
        hsv = cv2.cvtColor(homography, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 100, 100], dtype=np.uint8)  # Lower bound for red
        upper_red = np.array([10, 255, 255], dtype=np.uint8)  # Upper bound for red
        mask_red = cv2.inRange(hsv, lower_red, upper_red)

        self._homography_red_detection_publisher.publish(self._bridge.cv2_to_compressed_imgmsg(mask_red))

        return mask_red
    
    def publish_homography_yellow_mask(self, homography):
        # Convert warped image to HSV for color detection
        hsv = cv2.cvtColor(homography, cv2.COLOR_BGR2HSV)
        # Define HSV range for detecting **yellow color**
        lower_yellow = np.array([15, 100, 100], dtype=np.uint8)
        upper_yellow = np.array([35, 255, 255], dtype=np.uint8)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        self._homography_yellow_detection_publisher.publish(self._bridge.cv2_to_compressed_imgmsg(mask_yellow))

        return mask_yellow

    def publish_homography(self, image):
        h, w, _ = image.shape

        img_size = (w, h)
        
        src = np.float32([
            [0,382],
            [224, 191],  # Bottom left (near where left lane line is)
            [589, 382],  # Bottom right (near where right lane line is)
            [364, 191],  # Top left (near vanishing point for left lane)
        ])

        dst = np.float32([
            [100, 382],
            [100, 0],  # Bottom left (destination for left lane)
            [489, 382],  # Bottom right (destination for right lane)
            [489, 0],    # Top left (destination after warping)
        ])

        # cv2.circle(image, tuple(point), 5, (0, 0, 255), -1)  # Red dots

        M = cv2.getPerspectiveTransform(src, dst)
        
        warped = cv2.warpPerspective(image, M, img_size)

        self._homography_publisher.publish(self._bridge.cv2_to_compressed_imgmsg(warped))

        return warped
    
    def publish_undistorted_image(self, image):
        # Camera intrinsics
        K = np.array([[310.0149584021843, 0.0, 307.7177249518777],
                    [0.0, 309.29643750324607, 229.191787718834],
                    [0.0, 0.0, 1.0]], dtype=np.float32)

        D = np.array([-0.2683225140828933, 0.049595473114203516,
                    0.0003617920649662741, 0.006030049583437601, 0.0], dtype=np.float32)

        img_width, img_height = 640, 480

        # Compute optimal camera matrix to minimize black areas after undistortion
        new_K, roi = cv2.getOptimalNewCameraMatrix(K, D, (img_width, img_height), 1, (img_width, img_height))

        # Undistort image
        undistorted = cv2.undistort(image, K, D, None, new_K)

        # Crop the image based on ROI (Region of Interest)
        x, y, w, h = roi
        undistorted = undistorted[y:y+h, x:x+w]

        h, w, _ = undistorted.shape

        # point = [224, 191]
        # print(point)
        # cv2.circle(undistorted, tuple(point), 5, (0, 0, 255), -1)  # Red dots

        self._publisher.publish(self._bridge.cv2_to_compressed_imgmsg(undistorted))

        return undistorted


if __name__ == '__main__':
    # create the node
    node = ImagePublishers(node_name="color_detection_node")
    # keep spinning
    rospy.spin()