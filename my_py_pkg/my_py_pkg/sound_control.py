import threading
import rclpy
from rclpy.node import Node
from custom_msg_srv.msg import String

from custom_msg_srv.srv import Control
from custom_msg_srv.srv import Command
from custom_msg_srv.srv import Direction
from custom_msg_srv.srv import Speed


import pyaudio
import speech_recognition as sr
from gtts import gTTS
import os
import gtts.lang
from mutagen.mp3 import MP3
import time
import pygame
from pathlib import Path
#print(gtts.lang.tts_langs())

NODE = None
stopfunc = False
mic = sr.Microphone()

recog = sr.Recognizer()

pygame.init()
pygame.mixer.init()

recive_effect = Path("buildMain/sound/recive.mp3")
error_effect = Path("buildMain/sound/succes.mp3")

class MyNode(Node):

    def __init__(self):
        super().__init__('Sound_Func')
        
        self.sound_pub_command = self.create_publisher(msg_type=String, topic="/sound_control_topic", qos_profile=10)
        
        self.srv_sound_direction_client = self.create_client(srv_type=Direction,srv_name="/direction/send_message")
        while not self.srv_sound_direction_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for service /direction/send_message")
            
        self.create_subscription(msg_type=String,topic="/command_topic",callback=self.close_node,qos_profile=10)
    
    def call_srv_direction_client(self,direction:str):
        request = Direction.Request()
        request.direction = direction
        self.srv_sound_direction_client.call_async(request=request)
    
    def close_node(self,msg:String):
        global data
        global NODE
        global stopfunc
        data = msg.msg
        self.get_logger().info(msg.msg)
        if data == "ALL close" or data == "Sound_Control close":
            stopfunc = True
            NODE.destroy_node()
            rclpy.shutdown()

def LoadSoundEffect(comesound):#recive.mp3  or succes.mp3
    UnLoad()
    sound = comesound
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()
    time.sleep(0.5)


    # text = text_input
    # myobj = gTTS(text=text, lang='th', slow=False)
    # myobj.save("welcome.mp3")
    # radio = MP3("welcome.mp3")
    # tdelay = radio.info.length
    # os.system("welcome.mp3")

def LoadSound(comesound):
    UnLoad()
    robot_text = comesound
    robotsay = gTTS(text=robot_text, lang='th', slow=False)
    robotsay.save("fromRobot.mp3")
    pygame.mixer.music.load("fromRobot.mp3")
    pygame.mixer.music.play()
    radio = MP3("fromRobot.mp3")
    tdelay = radio.info.length
    time.sleep(tdelay)
    

def UnLoad():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

#LoadSoundEffect(recive_effect)

def command(in_text):
    NODE = MyNode()
    UnLoad()
    global robot_loop
    global gui_run
    global quest
    global teacher
    global teacherS
    global teacherC
    global position
    global positionSucces
    global hello
    global follow
    if (("robot" in in_text) or ("โรบอท" in in_text) or ("หุ่นยนต์" in in_text)) and robot_loop == False:

        #LoadSound("ว่า")
        # LoadSoundEffect(recive_effect)
        robot_loop = True
        if (("forwards" in in_text) or ("forward" in in_text) or ("เดินหน้า" in in_text)) and robot_loop == True:
            dataSound = "Forward"
            NODE.call_srv_direction_client(direction=dataSound)
            #LoadSound("ว่า")
            #LoadSoundEffect(recive_effect)
            #LoadSound("กำลังเดินหน้า")
            robot_loop = False
        elif (("backwards" in in_text) or ("backward" in in_text) or ("ถอยหลัง" in in_text)) and robot_loop == True:
            dataSound = "Backward"
            NODE.call_srv_direction_client(direction=dataSound)
            #LoadSound("ว่า")
            #LoadSoundEffect(recive_effect)
            #LoadSound("กำลังถอยหลัง")
            robot_loop = False
        elif (("stop" in in_text) or ("stops" in in_text) or ("หยุด" in in_text)) and robot_loop == True:
            dataSound = "Stop"
            NODE.call_srv_direction_client(direction=dataSound)
            #LoadSound("ว่า")
            #LoadSoundEffect(recive_effect)
            #LoadSound("หยุดแล้ว")
            robot_loop = False
        elif ("turn" in in_text) and robot_loop == True:
            if ("left" in in_text) and robot_loop == True:
                dataSound = "TrunLeft"
                NODE.call_srv_direction_client(direction=dataSound)
                #LoadSound("ว่า")
                #LoadSoundEffect(recive_effect)
                #LoadSound("กำลังเลี้ยวซ้าย")
                robot_loop = False
            elif ("right" in in_text) and robot_loop == True:
                dataSound = "TrunRight"
                NODE.call_srv_direction_client(direction=dataSound)
                #LoadSound("ว่า")
                #LoadSoundEffect(recive_effect)
                #LoadSound("กำลังเลี้ยวขวา")
                robot_loop = False
            else:
                pass
                #LoadSoundEffect(error_effect)
        elif (("เลี้ยวซ้าย" in in_text)) and robot_loop == True:
            dataSound = "TrunLeft"
            NODE.call_srv_direction_client(direction=dataSound)
            #LoadSound("ว่า")
            #LoadSoundEffect(recive_effect)
            #LoadSound("กำลังเลี้ยวซ้าย")
            robot_loop = False
        elif (("เลี้ยวขวา" in in_text)) and robot_loop == True:
            dataSound = "TrunRight"
            NODE.call_srv_direction_client(direction=dataSound)
            #LoadSound("ว่า")
            #LoadSoundEffect(recive_effect)
            #LoadSound("กำลังเลี้ยวขวา")
            robot_loop = False
        
        else:
            pass
       #     LoadSoundEffect(error_effect)
            
            
    if (("open" in in_text) or ("เปิดหน้าต่าง" in in_text)) and gui_run == False:
        gui_run = True
        if (("home" in in_text) or ("homes" in in_text) or ("เริ่มต้น" in in_text)) and gui_run == True:
            send_pub("Open Home")
#            LoadSoundEffect(recive_effect)
            gui_run = False
        if (("setting" in in_text) or ("settings" in in_text) or ("ตั้งค่า" in in_text)) and gui_run == True:
            send_pub("Open Setting")
#            LoadSoundEffect(recive_effect)
            gui_run = False
        if (("hello" in in_text) or ("ทักทาย" in in_text) ) and gui_run == True:
            hello = True
            follow = False
            positionSucces = False
            send_pub("Open Hello")
            
 #           LoadSoundEffect(recive_effect)
            gui_run = False
        if (("follow" in in_text) or ("เดินตาม" in in_text) ) and gui_run == True:
            hello = False
            follow = True
            positionSucces = False
            send_pub("Open Follow")
   #         LoadSoundEffect(recive_effect)
            gui_run = False
        if ((("teacher" in in_text)and(("position" in in_text))) or ("ตำแหน่งครู" in in_text) ) and gui_run == True:
            send_pub("Open Teacher")
#            LoadSoundEffect(recive_effect)
            teacher = True
            gui_run = False
        if (("position" in in_text) or ("เดินนำทาง" in in_text) ) and gui_run == True:
            position = True
            
            send_pub("Open Position")
 #           LoadSoundEffect(recive_effect)
            gui_run = False
        if (("ask" in in_text) or ("question" in in_text) or ("ตอบคำถาม" in in_text) ) and gui_run == True:
            send_pub("Open Ask")
  #          LoadSoundEffect(recive_effect)
            quest = True
            gui_run = False
        else:
            pass    
        
            
        
    if (("question is" in in_text) or ("ถามว่า" in in_text)) and quest == True:
        #--send data without question is or ถามว่า to gui_node and run func gpt
        #/print("Tesss")
        if "question is" in in_text:
            send_text = in_text.split("question is")
            print(str(send_text[1]))
            question = str("question is"+send_text[1])
            send_pub(question)
     #       LoadSoundEffect(recive_effect)

            
        if "ถามว่า" in in_text:
            send_text = in_text.split("ถามว่า")
            print(str(send_text[1]))
            question = str("question is"+send_text[1])
            send_pub(question)
      #      LoadSoundEffect(recive_effect)
            
    if (("computer category" in in_text) or ("หมวดคอมพิวเตอร์" in in_text) or ("หมวดคอม" in in_text) or ("คอมพิวเตอร์" in in_text) or ("คอม" in in_text) or ("computer" in in_text)) and teacher == True:
        NODE.get_logger().info("RUN Computer")
        send_pub("Open TeacherC")
  #      LoadSoundEffect(recive_effect)
        teacherC = True
        teacherS = False
        print("Computer")
        
    if (("stem category" in in_text) or ("หมวดสเต็ม" in in_text) or ("stem" in in_text)) and teacher == True:
        send_pub("Open TeacherS")
        #LoadSoundEffect(recive_effect)
        teacherS = True
        teacherC = False
        print("Stem")
        
    if (("ครูคนที่" in in_text) or ("teacher number" in in_text)) and teacher == True and ((teacherS == True) or (teacherC == True)):
        if teacherC == True and teacherS == False:
            if (("1" in in_text) or ("หนึ่ง" in in_text) or ("one" in in_text)):
         #       LoadSoundEffect(recive_effect)
                print("First")
                send_pub("TeacherC 1")
                pass
            
            if (("2" in in_text) or ("สอง" in in_text) or ("two" in in_text)):
          #      LoadSoundEffect(recive_effect)
                send_pub("TeacherC 2")
                print("2")
                pass
            
            if (("3" in in_text) or ("สาม" in in_text) or ("three" in in_text)):
           #     LoadSoundEffect(recive_effect)
                send_pub("TeacherC 3")
                print("3")
                pass

        if teacherS == True and teacherC == False:
            if (("1" in in_text) or ("หนึ่ง" in in_text) or ("one" in in_text)):
            #    LoadSoundEffect(recive_effect)
                send_pub("TeacherS 1")
                #pass
            
            if (("2" in in_text) or ("สอง" in in_text) or ("two" in in_text)):
             #   LoadSoundEffect(recive_effect)
                send_pub("TeacherS 2")
                #pass
           
            if (("3" in in_text) or ("สาม" in in_text) or ("three" in in_text)):
              #  LoadSoundEffect(recive_effect)
                send_pub("TeacherS 3")
                #pass
        
    

    if (("go to" in in_text) or ("ไปที่" in in_text)) and position == True:

        if (("หอประชุม" in in_text) or ("main hall" in in_text))and position == True:
           # LoadSoundEffect(recive_effect)
            send_pub("Position MainHall")
            hello = False
            follow = False
            positionSucces = True
            #pass
        if (("ห้องน้ำชาย" in in_text) or ("man toilet" in in_text)) and position == True:
            send_pub("Position ManToilet")
            #LoadSoundEffect(recive_effect)
            hello = False
            follow = False
            positionSucces = True
            #pass
        if (("ห้องน้ำหญิง" in in_text) or ("woman toilet" in in_text)) and position == True:
            send_pub("Position WomanToilet")
            hello = False
            follow = False
            positionSucces = True
            #LoadSoundEffect(recive_effect)
            #pass
            
    if ("start" in in_text) or ("เริ่มทำงาน" in in_text) or ("เริ่ม" in in_text) and ((hello == True) or (follow == True) or (positionSucces == True)):
        #NODE.get_logger().info("KKKKK")
        #   send_pub("Hello Start")
        if hello == True and follow == False and positionSucces == False:
            send_pub("Hello Start")
            
        if follow == True and hello == False and positionSucces == False:
            send_pub("Follow Start")
        
        if positionSucces == True and hello == False and follow == False:
            send_pub("Position Start")
        #LoadSoundEffect(recive_effect)
        
    if (("stop" in in_text) or ("หยุดทำงาน" in in_text) or ("หยุด" in in_text)) and ((hello == True) or (follow == True) or (positionSucces == True)):
        if hello == True:
            send_pub("Hello Stop")
        if follow == True:
            send_pub("Follow Stop")
        if positionSucces == True:
            send_pub("Position Stop")
        #LoadSoundEffect(recive_effect)
        
    if (("exit" in in_text) or ("back" in in_text) or ("ย้อนกลับ" in in_text) or ("ออก" in in_text)):
        send_pub("Back")
        quest = False
        gui_run = False
        teacher = False
        teacherC = False
        teacherS = False
        position = False
        hello = False
        follow = False
        positionSucces = False

    else:
        LoadSoundEffect(error_effect)
stopfunc = False

def send_pub(x):
    NODE = MyNode()
    msg = String()
    data = str(x)
    NODE.get_logger().info(x)
    msg.msg = data
    NODE.sound_pub_command.publish(msg=msg)

def speech():
    
    NODE = MyNode()
    global stopfunc
    global gui_run
    global robot_loop
    robot_loop = False
    gui_run = False
    send_pub("Open")
    with mic as source:
        while stopfunc == False:
            
            print("listening")
            audio = recog.listen(source)
            NODE.get_logger().info("listening")
            try:
                UnLoad()
                comming_text = recog.recognize_google(audio, language='th')
                comming_text = comming_text.lower()
                text = comming_text#.split()
                #print("waiting")
                print(text)
                NODE.get_logger().info(text)
                command(text)
                
            except:
                print('try again please')
                robot_loop = False
                gui_run = False
                
                continue
            
def main():
    global NODE
    rclpy.init()
    
    NODE = MyNode()
    thread_spin = threading.Thread(target=rclpy.spin,args=(NODE, ))
    thread_spin.start()

    #AIpos(input("Location you want /ManToilet/WomanToilet/MainHall: "))
    speech()
    NODE.destroy_node()
    rclpy.shutdown()
    thread_spin.join()
    
if __name__ == '__main__':
	main()
