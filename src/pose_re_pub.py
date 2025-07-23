#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose

class PoseRepub(Node):
    def __init__(self):
        super().__init__('pose_re_pub')
        
        # Create subscription to pose_with_covariance_stamped topic
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            'pose_with_covariance_stamped',
            self.pose_callback,
            10
        )
        
        # Create publisher for pose topic
        self.publisher = self.create_publisher(Pose, 'pose', 10)
        
        self.get_logger().info('pose_re_pub node started')

    def pose_callback(self, msg):
        # Extract pose from PoseWithCovarianceStamped message
        pose_msg = Pose()
        pose_msg.position = msg.pose.pose.position
        pose_msg.orientation = msg.pose.pose.orientation
        
        # Publish the pose message
        self.publisher.publish(pose_msg)
        self.get_logger().debug('Republished pose message')

def main(args=None):
    rclpy.init(args=args)
    pose_re_pub = PoseRepub()
    rclpy.spin(pose_re_pub)
    pose_re_pub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
