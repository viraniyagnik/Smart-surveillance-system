#import smtplib, email and os for sending email for administration view
import smtplib, email, os

#for temperature and humidity
import time
import board
import adafruit_dht

#import PiCamera for camara module
from picamera import PiCamera

#import sleep for wait
from time import sleep

#import MIMEBase, provide base class
from email.mime.base import MIMEBase

#import MIMEMultipart, to add the message object
from email.mime.multipart import MIMEMultipart

#import MIMEText, use to create MIME objects
from email.mime.text import MIMEText

#import encoders module from email package to encode the message object
from email import encoders

# to import data and time
from datetime import datetime

#for raspberry pi GPIO pins
import RPi.GPIO as GPIO

dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

#To desable warnings, GPIO pins is already in use
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# to set 11 number pin of raspberry pi
GPIO.setup(11, GPIO.IN)
temperature_c = dhtDevice.temperature
humidity = dhtDevice.humidity

#A motion has been detected.
subject='Motion detected in surveillance area'
bodyText="""\
Surveillance System,

Motion has been detected.

Temp:  {:.1f} C    Humidity: {}%
Please check the attachement of that.

Note: If Temperature above 57 C, heat detected(Fire).
And also, Humidilty level will decrease.

""".format(temperature_c, humidity)

#for gmail smtp server
SMTP_SERVER='smtp.gmail.com'
#use 587 port
SMTP_PORT=587
#sender email
Sender_email='****************************'
#sender password
Password='****************************'
#reciever email
Receiver_email='****************************'

# for file name and file extention with date and time
file_name="CPIN_project"
file_ext=".mp4"
now = datetime.now()
current_time = now.strftime("%d-%m-%Y_%H:%M")
filename=file_name+"_"+current_time+file_ext
filepath="/home/pi/python_code/capture/"

#send method to send email
def send():
 message=MIMEMultipart()
 message["From"]=Sender_email
 message["To"]=Receiver_email
 message["Subject"]=subject

 message.attach(MIMEText(bodyText, 'plain'))
 attachment=open(filepath+filename, "rb")

 mimeBase=MIMEBase('application','octet-stream')
 mimeBase.set_payload((attachment).read())

 encoders.encode_base64(mimeBase)
 mimeBase.add_header('Content-Disposition', "attachment; filename= " +filename)

 message.attach(mimeBase)
 text=message.as_string()

 session=smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
 session.ehlo()
 session.starttls()
 session.ehlo()

 session.login(Sender_email, Password)
 session.sendmail(Sender_email, Receiver_email, text)
 session.quit
 print("Email has been sent to the registered email.")

#video() to capture video
def video():
 camera.start_preview()
 camera.start_recording('/home/pi/python_code/capture/CPIN_Project_Motionvideo.h264')
 camera.wait_recording(15)
 camera.stop_recording()
 camera.stop_preview()

#remove file after sending email
def remove():
 if os.path.exists("/home/pi/python_code/capture/CPIN_Project_Motionvideo.h264"):
  os.remove("/home/pi/python_code/capture/CPIN_Project_Motionvideo.h264")
 else:
  print("file not founded.")

 if os.path.exists(filepath+filename):
  os.remove(filepath+filename)
 else:
  print("file not founded.")


#to active camera
camera=PiCamera()


while True:
 i = GPIO.input(11)
 if temperature_c>=57 or if i==1::
  print(' Motion Detected Temp:  {:.1f} C Humidity: {}% '.format(temperature_c, humidity))
  video()
  res=os.system("MP4Box -add /home/pi/python_code/capture/CPIN_Project_Motionvideo.h264 /home/pi/python_code/capture/CPIN_Project_Motionvideo.mp4")
  os.system("mv /home/pi/python_code/capture/CPIN_Project_Motionvideo.mp4 "+filepath+filename)
  send()
  sleep(10)
  remove()
