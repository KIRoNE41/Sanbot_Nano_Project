#!/usr/bin/env python3
import threading
import rclpy
from rclpy.node import Node
from custom_msg_srv.msg import String

from custom_msg_srv.srv import Control
from custom_msg_srv.srv import Direction

import cv2
import time
import serial 

NODE = None
GUI = None

send = ""
last_send = ""
data = ""
class MyNode(Node):
    
    def __init__(self):
        super().__init__('AI_Pos')
#        self.srv_gui_client = self.create_client(srv_type=Control,srv_name="/control/send_message")
#        while not self.srv_gui_client.wait_for_service(timeout_sec=1.0):
#            self.get_logger().info("Waiting for service /control/send_message")
            
        self.srv_ai_pos_direction_client = self.create_client(srv_type=Direction,srv_name="/direction/send_message")
        while not self.srv_ai_pos_direction_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for service /direction/send_message")
        
        self.create_subscription(msg_type=String,topic="/control_topic",callback=self.callback_command,qos_profile=10)
    
        self.create_subscription(msg_type=String,topic="/command_topic",callback=self.close_node,qos_profile=10)
    
    def close_node(self,msg:String):
        global data
        data = msg.msg
        self.get_logger().info(msg.msg)
        
    def call_srv_direction_client(self,direction:str):
        global last_send
        global send
        send = str(direction)
        if send != last_send:
            request = Direction.Request()
            request.direction = direction
            self.srv_ai_pos_direction_client.call_async(request=request)
            last_send = send

        elif send == last_send:
            pass
    def callback_command(self,msg:String):
       	self.get_logger().info(msg.msg)

######
# cap2 = cv2.VideoCapture(cameraNo2)#####
#arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1) 
last_x = None
#def write_read(x): #def write_read(x): 
#    global last_x
#    if x != last_x:
#        arduino.write(bytes(x, 'utf-8') )#
#        time.sleep(0.05) 
#        data = arduino.readline() 
#        print(x)
#        last_x = x
#        return data 
#    elif x == last_x:
#        pass

T = ""    

def AIpos():
    frameWidth = 256  # DISPLAY WIDTH
    frameHeight = 192  # DISPLAY HEIGHT
    cameraNo = '/dev/video0'#   0||'/dev/video0'  # CAMERA NUMBER
    cameraNo2 = 1
    color = (255, 0, 0)  # Blue
    color2 = (0, 255, 0)  # Green
    color3 = (0, 0, 255)  # Red
    cap = cv2.VideoCapture(cameraNo)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,frameWidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,frameHeight)
    cap.set(cv2.CAP_PROP_FPS,30)
    #global NODE
    NODE = MyNode()
    global stopfunc
    global data
    global T
    stopfunc = False
    if data == "MainHall" or data == "ManToilet" or data == "WomanToilet":
        T = data
    qcd = cv2.QRCodeDetector()
    window_name = 'OpenCV QR Code'
    dataAIP = ""
    # last_dataAIP = ""
    while stopfunc == False:
        ret, frame = cap.read()
        #frame = cv2.resize(frame, (frameWidth, frameHeight))
        frameWidth2 = frameWidth
        frameHeight2 = frameHeight
        Big_zone = int(frameWidth2*(1/3))#outside Big_zone is Out_zone // Outzone == pos > Big_zone 
        Small_zone1 = int(Big_zone*(1/2))#Small_zone1 == MaximumLeft // Small_zone2 == Between Small_zone1 and Big_zone  --> pos > Small_zone1 and pos < Big_zone
        if ret:
            ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
            if ret_qr:
                for s, p in zip(decoded_info, points):
                    pos0 = p[0].astype(int)
                    pos1 = p[1].astype(int)
                    pos2 = p[2].astype(int)
                    pos3 = p[3].astype(int)
                    frame = cv2.circle(frame,pos0, 5, (255, 0, 0), -1)
                    frame = cv2.circle(frame,pos1, 5, (255, 0, 0), -1)
                    frame = cv2.circle(frame,pos2, 5, (255, 0, 0), -1)
                    frame = cv2.circle(frame,pos3, 5, (255, 0, 0), -1)
                    if s:
                        x = s.split(" ")   
                        print(x)
                        for target in x: 
                            direction = target.split(":")
                            print(target+"\n-------")
                            
                            print(direction)
                            #target = direction[0]
                            
                            #if ":" in T:
                             #   direc = direction[1]
                            
                            #else :
                              #  direc = ""
                            NODE.get_logger().info(str(target))      
                            NODE.get_logger().info(str(direction))

                        if T in target and ((":L") in target) and (not (":R") in target)and (not(":S") in target):
                            print('yes')
                            print("Go")
                            dataAIP = "TrunLeft"
                            #NODE.call_srv_direction_client(direction=dataAIP)

                        elif T in target and (not(":L") in target) and ((":R") in target)and (not(":S") in target):
                            print('yes')
                            print("Go")
                            dataAIP = "TrunRight"
                            #NODE.call_srv_direction_client(direction=dataAIP)

                        elif T in target and (not(":L") in target) and (not(":R") in target)and ((":S") in target):
                            print('yes')
                            print("Succes")
                            dataAIP = "Stop"
                            #NODE.call_srv_direction_client(direction=dataAIP)

                        elif T in target and (not (":L") in target) and (not (":R") in target and (not(":S") in target)):
                            print('yes')
                            print("Go")
                            dataAIP = "Forward"
                            #NODE.call_srv_direction_client(direction=dataAIP)


                        else:
                            pass

                        color = (0, 255, 0)

                    else:   
                        pass
                        #if last_x == "Forward":
                        #    dataAIP = "TrunRight"
                            #NODE.call_srv_direction_client(direction=dataAIP)
            
                        color = (0, 0, 255)
                    frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
            else:
                pass
                #if last_x == "Forward":
                #    dataAIP = "TrunLeft"
                    #NODE.call_srv_direction_client(direction=dataAIP)
        cv2.imshow(window_name, frame)
        NODE.call_srv_direction_client(direction=dataAIP)
        time.sleep(0.1)


        if cv2.waitKey(1) & 0xFF == ord('s'):
            dataAIP="Stop"
            NODE.call_srv_direction_client(direction=dataAIP)

        if cv2.waitKey(1) & 0xFF == ord('q')  or stopfunc == True or data =="AI_Pos close":
            stopfunc = True
            dataAIP="Stop"
            NODE.call_srv_direction_client(direction=dataAIP)
            break
    cap.release()
    cv2.destroyWindow(window_name)
    pass
    
def main():
    rclpy.init()
    
    NODE = MyNode()
    thread_spin = threading.Thread(target=rclpy.spin,args=(NODE, ))
    thread_spin.start()

    #AIpos(input("Location you want /ManToilet/WomanToilet/MainHall: "))
    AIpos()
    NODE.destroy_node()
    rclpy.shutdown()
    thread_spin.join()
    
if __name__ == '__main__':
	main()
