#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_msg_srv.msg import String

from custom_msg_srv.srv import Control
from custom_msg_srv.srv import Direction
from custom_msg_srv.srv import Speed
import serial
import time
speed1=20
speed2=20
arduino = serial.Serial(port='/dev/ttyACM0',   baudrate=115200, timeout=.1)
data = ""
server = ""
class Server(Node):
    
    
        
    def __init__(self):
        super().__init__(node_name="control")
        self.get_logger().info(message="server start")
        self.pub_gui = self.create_publisher(msg_type=String, topic="/control_topic", qos_profile=10)
        
#        self.create_service(srv_type=Control, srv_name=f"{self.get_name()}/send_message", callback=self._service_callback)
        
        self.create_service(srv_type=Direction, srv_name="/direction/send_message", callback=self._service_direction_callback)
        
        self.create_service(srv_type=Speed, srv_name="/speed/send_message", callback=self._service_speed_callback)
        
        self.create_subscription(msg_type=String,topic="/command_topic",callback=self.close_node,qos_profile=10)
    
    def close_node(self,msg:String):
        global data
        global server
        data = msg.msg
        self.get_logger().info(msg.msg)
        if data == "ALL close":
            server.destroy_node()
            rclpy.shutdown()
            

#    def _service_callback(self, request, response):
#        
#        msg = String()
#        msg.msg = f"#{request.direction}:{request.speed};"
#        arduino.write(bytes(msg.msg,   'utf-8'))
#        time.sleep(0.05)
#        data = arduino.readline()
#        self.get_logger().info(message=str("Send"+msg.msg))
#        self.get_logger().info(message=("Recive"+str(data)))
#        self.pub_gui.publish(msg=data)
#
#        return response
                
    def _service_direction_callback(self, request, response):
        
        global speed1
        global speed2
        speed = 0
        
        if request.direction == "Forward" or request.direction == "Backward":
            speed = speed1
        if request.direction == "TrunLeft" or request.direction == "TrunRight":
            speed = speed2
        if request.direction == "Stop":
            speed = 0
        msg = String()
        msg.msg = f"#{request.direction}:{speed};"
        arduino.write(bytes(msg.msg,   'utf-8'))
        time.sleep(0.05)
        data = arduino.readline()
        self.get_logger().info(message=str("Send"+msg.msg))
        self.get_logger().info(message=("Recive"+str(data)))
        self.pub_gui.publish(msg=data)

        return response
 
    def _service_speed_callback(self, request, response):
        msg = String()
        global speed1
        global speed2
        speed1 = request.firstspeed
        speed2 = request.secondspeed
        msg.msg = f"NormalSpeed is :{speed1},TrunSpeed is :{speed2}"
        self.get_logger().info(message=str("Send"+msg.msg))

        return response    


def main():
    global server
    try:
        rclpy.init(args=None)
        server = Server()
        rclpy.spin(node=server)
    except KeyboardInterrupt:
        server.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
