#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import csv
import os

class TwistFromDatabase(Node):
    def __init__(self):
        super().__init__('twist_from_database')
        
        # Create publisher for twist messages
        self.publisher = self.create_publisher(Twist, 'twist_from_database', 20)
        
        # Create timer for 10Hz publishing rate
        self.timer = self.create_timer(0.1, self.publish_twist)  # 10Hz = 0.1 seconds
        
        # Load CSV data
        self.twist_data = []
        self.current_index = 0
        self.load_csv_data()
        
        self.get_logger().info('twist_from_database node started')

    def load_csv_data(self):
        csv_file_path = 'values.csv'
        try:
            if os.path.exists(csv_file_path):
                with open(csv_file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if not row or (len(row) == 1 and not row[0].strip()):  # check for empty lines
                            continue
                        if len(row) == 6:  # Ensure we have at least 6 values
                            try:
                                # Parse linear x, y, z and angular x, y, z
                                linear_x = float(row[0].strip())
                                linear_y = float(row[1].strip())
                                linear_z = float(row[2].strip())
                                angular_x = float(row[3].strip())
                                angular_y = float(row[4].strip())
                                angular_z = float(row[5].strip())
                                
                                twist_values = {
                                    'linear': [linear_x, linear_y, linear_z],
                                    'angular': [angular_x, angular_y, angular_z]
                                }
                                self.twist_data.append(twist_values)
                            except ValueError as e:
                                self.get_logger().warn(f'Error parsing row {row}: {e}')
                        else:
                            self.get_logger().warn(f'Row has insufficient values: {row}')
                self.get_logger().info(f'Loaded {len(self.twist_data)} twist commands from CSV')
            else:
                self.get_logger().error(f'CSV file {csv_file_path} not found')
        except Exception as e:
            self.get_logger().error(f'Error reading CSV file: {e}')

    def publish_twist(self):
        if not self.twist_data:
            self.get_logger().warn('No twist data available')
            return
        
        # Get current twist data
        current_twist = self.twist_data[self.current_index]
        
        # Create Twist message
        twist_msg = Twist()
        twist_msg.linear.x = current_twist['linear'][0]
        twist_msg.linear.y = current_twist['linear'][1]
        twist_msg.linear.z = current_twist['linear'][2]
        twist_msg.angular.x = current_twist['angular'][0]
        twist_msg.angular.y = current_twist['angular'][1]
        twist_msg.angular.z = current_twist['angular'][2]
        
        # Publish the message
        self.publisher.publish(twist_msg)
        self.get_logger().debug(f'Published twist: linear=({twist_msg.linear.x}, {twist_msg.linear.y}, {twist_msg.linear.z}), angular=({twist_msg.angular.x}, {twist_msg.angular.y}, {twist_msg.angular.z})')
        
        # Move to next twist data (cycle through)
        self.current_index = (self.current_index + 1) % len(self.twist_data)

def main(args=None):
    rclpy.init(args=args)
    twist_from_database = TwistFromDatabase()
    rclpy.spin(twist_from_database)
    twist_from_database.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
