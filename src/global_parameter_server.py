#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import Parameter, ParameterValue
from rcl_interfaces.srv import SetParameters

class GlobalParamServer(Node):
    def __init__(self):
        super().__init__('global_parameter_server')
        self.params = {}  # Dictionary to store global params
        
        # Create service for setting parameters
        self.srv = self.create_service(SetParameters, 'set_parameters', self.set_parameters_callback)
        
        self.get_logger().info('Global parameter server started')

    def set_parameters_callback(self, request, response):
        """Service callback to set parameters"""
        for param in request.parameters:
            self.params[param.name] = param.value
            self.get_logger().info(f'Set parameter: {param.name} = {param.value.string_value}')
        
        # Set success result for each parameter
        response.results = [True] * len(request.parameters)
        return response

def main(args=None):
    rclpy.init(args=args)
    node = GlobalParamServer()
    rclpy.spin(node)  # Keep node alive
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
