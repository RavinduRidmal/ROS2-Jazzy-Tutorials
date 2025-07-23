#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class ParamReader(Node):
    def __init__(self):
        super().__init__('param_reader')
        
        # Check or Declare with default (optional but recommended)
        self.declare_parameter('robot_name', 'robot')
        
        # Get the parameter value
        robot_name = self.get_parameter('robot_name').value
        
        # Print to terminal
        self.get_logger().info(f"Robot name: {robot_name}")

def main(args=None):
    rclpy.init(args=args)
    node = ParamReader()
    try:
        rclpy.spin(node)  # Keep node alive briefly
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
