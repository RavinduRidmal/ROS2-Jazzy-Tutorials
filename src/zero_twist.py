#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class ZeroTwist(Node):
    def __init__(self):
        super().__init__('zero_twist')
        
        # Create subscription to is_stopped topic
        self.subscription = self.create_subscription(
            String,
            'is_stopped',
            self.is_stopped_callback,
            10
        )
        
        # Create publisher for twist topic
        self.publisher = self.create_publisher(Twist, 'twist', 10)
        
        self.get_logger().info('zero_twist node started')

    def is_stopped_callback(self, msg):
        # Check if the message contains "true"
        if msg.data.lower() == "true":
            self.publish_zero_twist()
            self.get_logger().info('Received stop signal, publishing zero twist')

    def publish_zero_twist(self):
        # Create zero twist message
        zero_twist = Twist()
        zero_twist.linear.x = 0.0
        zero_twist.linear.y = 0.0
        zero_twist.linear.z = 0.0
        zero_twist.angular.x = 0.0
        zero_twist.angular.y = 0.0
        zero_twist.angular.z = 0.0
        
        # Publish the zero twist message
        self.publisher.publish(zero_twist)
        self.get_logger().debug('Published zero twist message')

def main(args=None):
    rclpy.init(args=args)
    zero_twist = ZeroTwist()
    rclpy.spin(zero_twist)
    zero_twist.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
