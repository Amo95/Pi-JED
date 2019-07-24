import paho.mqtt.client as mqtt
import time
import datetime
import myapp

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")
Connected = False  # global variable for the state of the connection


client = mqtt.Client()
client.on_connect = on_connect
#client.connect("104.248.163.70", 1883, 60)
client.connect("127.0.0.1",1883,60)
client.loop_start()  # start the loop


while Connected != True:  # Wait for connection
    time.sleep(0.1)


try:
    while True:
        no_of_students = 0
        while no_of_students >= 0:
            print(datetime.datetime.now())    
            no_of_students = attendance.countdown(no_of_students)
            message = "Student Number:" + str(no_of_students) #"Number of Students:" {no_of_students}
            client.publish("glblcd/sam", message)
            
    #can be.. message = input('Your message:')
    #     client.publish("glbcd/sam", "Bright: " + message)


except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
