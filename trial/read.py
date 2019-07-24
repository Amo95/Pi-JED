import paho.mqtt.client as mqtt

def on_connect(client,userdata,flag,rc): #when subscriber connects,
                    #rc-result code should be printed as 
                    #str-string
    print("Connected with result code"+str(rc))

    #Here you can subscribe to whatever topics you like
    #use '#' for a 'wildcard'-subscribe to any messages
    #
    client.subscribe("#") #client should subscribe to topic glbcd/sam.


def on_message(client,userdata,msg): #this calls message from publisher/sender

    print(msg.topic + " \n " + msg.payload.decode("utf-8") + "\n")
        #msg.topic- message topic
        #msg.payload.decode- decoded message with content(payload)


#Initiating MQTT client and setting up callbacks(for message)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#connecting to the server to host both publisher and sender
#the server and the topic connects all the people connected to the server
#i.e you will receive messages from all those connected on the server
#client.connect("104.248.163.70",1883,60)
client.connect("127.0.0.1",1883,60)

#prevent program from exiting by calling a loop
client.loop_forever()
