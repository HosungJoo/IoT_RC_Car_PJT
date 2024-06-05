import paho.mqtt.client as mqtt
from time import sleep
from picamera2 import Picamera2
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
from sense_hat import SenseHat

import mysql.connector
import signal
import sys
from threading import Timer, Lock
import atexit
import datetime
import pytz

sense = SenseHat()
db = mysql.connector.connect(host='13.125.156.170', user='mincoding', password='1234', database='minDB', auth_plugin='mysql_native_password')
cur = db.cursor()

# RC Car의 상태 및 제어를 관리하는 클래스
class RCCarController:
    def __init__(self):
        # MotorHAT 및 PWM 초기화
        self.mh = Raspi_MotorHAT(addr=0x6f)
        self.pwm = PWM(0x6F)
        self.pwm.setPWMFreq(60)

        # RC Car 속도 및 스티어링 기본값 설정
        self.velocity = 0
        self.steering_mid = 370
        self.steering_right = 450
        self.steering_left = 250
        self.pwm.setPWM(0, 0, 370)

        # 모터 초기화
        self.motor = self.mh.getMotor(2)
        self.motor.setSpeed(150)
        self.motor.run(Raspi_MotorHAT.FORWARD)
        self.motor.run(Raspi_MotorHAT.RELEASE)

        # 예외 발생 시 모터 종료
        atexit.register(self.turnOffMotors)
    
    def get_speed(self):
        return self.velocity

    def handleGearState(self, gear_state):
        print(f"Gear State: {gear_state}")
        if gear_state == "0":
            self.motor.run(Raspi_MotorHAT.FORWARD)
        elif gear_state == "1":
            self.motor.run(Raspi_MotorHAT.BACKWARD)

    def handleMotorVelocity(self, velocity):
        print(f"Motor Velocity: {velocity}")
        self.velocity = int(velocity)
        self.motor.setSpeed(self.velocity)

    def handleServoHandle(self, steering):
        print(f"Servo Handle: {steering}")
        if steering == "Mid":
            self.pwm.setPWM(0, 0, self.steering_mid)
        elif steering == "Right":
            self.pwm.setPWM(0, 0, self.steering_right)
        elif steering == "Left":
            self.pwm.setPWM(0, 0, self.steering_left)

    def turnOffMotors(self):
        self.mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)



# MQTT 브로커 설정
broker_address = "192.168.137.212"
broker_port = 1883

# MQTT 클라이언트 설정 및 콜백 함수 정의
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("RcCar/gear/state")
    client.subscribe("RcCar/motor/velocity")
    client.subscribe("RcCar/servo/handle")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(f"Received message on topic {topic}: {payload}")

    # RCCarController 인스턴스를 통해 메시지 처리
    if topic == "RcCar/gear/state":
        car_controller.handleGearState(payload)
    elif topic == "RcCar/motor/velocity":
        car_controller.handleMotorVelocity(payload)
    elif topic == "RcCar/servo/handle":
        car_controller.handleServoHandle(payload)

def sensing():
    pressure = sense.get_pressure()
    temp = sense.get_temperature()
    humidity = sense.get_humidity()

    time = datetime.datetime.now()
    num1 = round(pressure, 3)
    num2 = round(temp, 2)
    num3 = round(humidity, 2)
    meta_string = car_controller.get_speed() 
    is_finish = 0

    print(num1, num2, num3)
    query = "insert into sensing(time, num1, num2, num3, meta_string, is_finish) values (%s, %s, %s, %s, %s, %s)"
    value = (time, num1, num2, num3, meta_string, is_finish)

    cur.execute(query, value)
    db.commit()

    timer = Timer(2, sensing)
    timer.start()

# RCCarController 인스턴스 생성
car_controller = RCCarController()

# MQTT 클라이언트 설정 및 연결
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)
client.loop_start()
sensing()


try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
