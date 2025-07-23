#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import Parameter, ParameterValue
from rcl_interfaces.srv import SetParameters
from rclpy.parameter import ParameterType

class ParamSetter(Node):
    def __init__(self):
        super().__init__('param_setter')
        
        # Get input parameters (passed via CLI or launch file)
        self.declare_parameter('param_name', 'robot_name')
        self.declare_parameter('param_value', 'default_robot')
        
        param_name = self.get_parameter('param_name').value
        param_value = self.get_parameter('param_value').value
        
        self.get_logger().info(f'Setting parameter: {param_name} = {param_value}')
        
        # Set parameter globally
        self.set_parameter_globally(param_name, param_value)

    def set_parameter_globally(self, name, value):
        # Create client for global parameter service
        client = self.create_client(SetParameters, '/global_parameter_server/set_parameters')
        
        if not client.wait_for_service(timeout_sec=2.0):
            self.get_logger().error("Global parameter service not available!")
            return
        
        # Prepare request
        request = SetParameters.Request()
        param = Parameter()
        param.name = name
        param.value = ParameterValue(string_value=value, type=ParameterType.PARAMETER_STRING)
        request.parameters = [param]
        
        # Send request
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        
        if future.result() is not None:
            self.get_logger().info(f"Successfully set global parameter: {name} = {value}")
        else:
            self.get_logger().error("Failed to set global parameter")

def main(args=None):
    rclpy.init(args=args)
    node = ParamSetter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
