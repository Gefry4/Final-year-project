
from adafruit_servokit import ServoKit
import time
from math import *

#####################################################
#
#  Constants
#
####################################################
FOREARM=48
HAND=141
SHOULDER=40
YOFFSET=100

####################################################
#
#   Classes
#
####################################################


class Servo():
	def __init__(self, servo, reverse,min,max,offset):
		self.servo=servo
		self.reverse = reverse
		self.minAngle=min
		self.maxAngle=max
        self.offset=offset
		self.setAngle(90)
		self.servo.set_pulse_width_range(625,2840)
		self.servo.actuation_range = 210


	def setAngle(self, angle):
		self.angle = angle
		if angle >= self.minAngle and  angle <= self.maxAngle:
			if self.reverse:
				self.servo.angle=(180 - angle ) + offset
			else:
				self.servo.angle = angle + offset

class Leg():
	def __init__(self, Servo0,minB,maxB,offsetB Servo1,minS,maxS, Servo2,minW,maxW,  reverse):
		self.servoB = Servo(Servo0, reverse, minB,maxB,offsetB)
		self.servoS = Servo(Servo1, reverse, minS,maxS)
		self.servoW = Servo(Servo2, False, minW,maxW)
		time.sleep(0.1)
	def forward(self,angle):
		self.servoB.setAngle(angle)

	def lift(self,angle):
		self.servoS.setAngle(angle)
		time.sleep(0.1)

	def step(self, angle):
		self.lift(140)
		self.forward(angle)
		self.lift(90)
    
	def moveTo(self,x,y):
		#Calculate body_servo
		body_servo= degrees(atan(x/y))
		
		#Calculate Hypotenuse
		H = sqrt(pow(YOFFSET, 2) + pow((y - SHOULDER), 2))

		#Calculate SS2 shoulder_servo2
		SS2 = degrees(acos(YOFFSET/H))

		#Calculate SS1 shoulder_servo1
		SS1 = degrees(acos((pow(HAND, 2) - pow(H,2) - pow(FOREARM, 2))/(-2*H*FOREARM)))

		#Calculate shoulder_servo
		shoulder_servo = SS2 +SS1

		#Calculate wrist_servo
		wrist_servo = degrees(acos((pow(H, 2) - pow(HAND, 2) - pow(FOREARM, 2))/ (-2 * HAND * FOREARM)))

		#Move
		#Lift
		self.servoS.setAngle(45)
		time.sleep(0.1)
		#Body
		self.servoB.setAngle(body_servo)
		self.servoW.setAngle(wrist_servo)
		self.servoS.setAngle(shoulder_servo)
		time.sleep(0.1)
		
############################################################
#
#       Main
#
############################################################

NUM_SERVOS=16 #define the number of servos

kit = ServoKit(channels=NUM_SERVOS) #initialise the servos

legs=[]
#		    servo, min, max, offset, servo, min, max, ooffset...
legs.append( Leg(kit.servo[0],0,90,8,kit.servo[1],0,115,-12,kit.servo[2],20,180,-15,False))   #Back right leg
legs.append( Leg(kit.servo[4],90,180,-1,kit.servo[5],55,180,10,kit.servo[6],0,150,5,False))    #Front left leg
legs.append( Leg(kit.servo[8],90,180,0,kit.servo[9],55,180,-5,kit.servo[10],0,150,-5,True))    #Back left leg
legs.append( Leg(kit.servo[12],0,90,2,kit.servo[13],0,115,0,kit.servo[14],20,180,-12,True))    #Front right leg
time.sleep(2)

move=[[[50,50],[50,50],[50,50],[50,50]],[[100,100],[100,100],[100,100],[100,100]]]
while True:

	#leg_no = int(input("Leg number: "))
	#x = int(input("X: "))
	#y= int(input("Y: "))
	#legs[leg_no].moveTo(x,y)
	for steps in move:
		for  i in range(len(steps)):
            legs[i].moveTo(steps[i][0],steps[i][1])
        time.sleep(1)
    time.sleep(2)	


	
