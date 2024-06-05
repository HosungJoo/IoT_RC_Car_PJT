import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from mainUI import Ui_MainWindow
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error


width = 800
height = 480

# forward:0, backward:1 parking:99
state = 99
# steering mid:0, R:1, L:-1
steering = 0

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main()

        # init setValue
        self.vellocity_bar.setValue(self.vellocity_bar.maximum())
        self.handle.setValue(50)

        self.forward_btn.clicked.connect(self.click_forward_btn)
        self.backward_btn.clicked.connect(self.click_backward_btn)
        self.vellocity_bar.valueChanged.connect(self.display_velocity)
        self.handle.valueChanged.connect(self.control_handle)

        # MQTT Client 설정
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect("192.168.137.212", 1883, 60)  # MQTT 브로커 주소로 변경
        self.client.loop_start()

        #MySQL 연결 설정
        self.db = mysql.connector.connect(host='13.125.156.170',
                                          user='mincoding',
                                          password='1234',
                                          database='minDB',
                                          auth_plugin='mysql_native_password')
        self.cur = self.db.cursor()

        #timer 셋팅
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.pollingQuery)
        self.timer.timeout.connect(self.sensingQuery)
        self.timer.start()

    def pollingQuery(self):
        self.cur.execute("select * from command")
        self.log_data.clear()
        for (id, time, cmd_string, arg_string, is_finish) in self.cur:
            str = "%d | %s | %6s | %6s | %4d" % (
            id, time.strftime("%Y%m%d %H:%M:%S"), cmd_string, arg_string, is_finish)
            self.log_data.appendPlainText(str)

    def sensingQuery(self):
        self.cur.execute("select * from sensing")
        self.sensing_data.clear()
        for (id, time, num1, num2, num3, meta_string, is_finish) in self.cur:
            str = "%d | %s | %6s | %6s | %6s | %4s | %4d" % (
            id, time.strftime("%Y%m%d %H:%M:%S"), num1, num2, num3, meta_string, is_finish)
            self.sensing_data.appendPlainText(str)


    def insertCommand(self, cmd_string, arg_string):
        # 현재 시간 가져오기
        time = QDateTime().currentDateTime().toPython()
        is_finish = 0

        query = "insert into command(time, cmd_string, arg_string, is_finish) values (%s, %s, %s, %s)"
        value = (time, cmd_string, arg_string, is_finish)

        self.cur.execute(query, value)
        self.db.commit()

    def main(self):
        # -60은 화면 상단 작업표시줄 높이
        self.setGeometry(0, 60, width, height - 60)

    def click_forward_btn(self):
        global state
        print("forward")
        state = 0
        print(state)
        self.client.publish("RcCar/gear/state", state)
        self.insertCommand("go", "0")

    def click_backward_btn(self):
        global state
        print("backward")
        state = 1
        print(state)
        self.client.publish("RcCar/gear/state", state)
        self.insertCommand("back", "0")

    def display_velocity(self, value):
        value = (230 - value)
        self.client.publish("RcCar/motor/velocity", value)

    def control_handle(self, value):
        global steering
        if value > 70:
            steering = 1
            print("Right")
            self.client.publish("RcCar/servo/handle", "Right")
            self.insertCommand("right", "0")
        elif value < 30:
            steering = -1
            print("Left")
            self.client.publish("RcCar/servo/handle", "Left")
            self.insertCommand("left", "0")
        else:
            steering = 0
            print("Mid")
            self.client.publish("RcCar/servo/handle", "Mid")
            self.insertCommand("mid", "0")
        print(steering)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.publish("RcCar/servo/handle", steering)

    def closeEvent(self, event):
        event.accept()
        # 접속 종료
        self.cur.close()
        self.db.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    win.show()
    app.exec_()
