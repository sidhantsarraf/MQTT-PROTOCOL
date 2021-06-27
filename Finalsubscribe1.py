import paho.mqtt.client as mqtt
import time
import logging,sys
logging.basicConfig(level=logging.DEBUG)

def on_disconnect(client, userdata, flags, rc=0):
    m="DisConnected flags "+"result code "+str(rc)+" client1  "
    print(m)

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		m="Connected result code " +str(rc)+" client1"
		print(m)
		global connected
		connected=True
	else:
		print("connection failed")
def on_message(client, userdata, msg):
	global Messagerecieved
	Messagerecieved=True
	print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))

def sub(client,topic,qos,s_msg):
    logging.info(s_msg+"  topic= "+topic +" qos="+str(qos))
    client.subscribe(topic,qos)

broker="PUT YOUR BROKER ADDRESS"
port= 8883
ID="Put you id"
Pass="PUT YOUR PASSWORD"
connected=False
CLEAN_SESSION=True
keepalive=1200
client = mqtt.Client("Python1",clean_session=CLEAN_SESSION) 
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(ID, Pass)
client.connect(broker,port,keepalive)
print("Connecting client 1 with clean session set to ",CLEAN_SESSION)
client.loop_start()
while connected!=True:
	print("Waiting")
	time.sleep(1)
print ("client1 is used to subscribe and client 2 to publish")
print ("Test1: Test if broker remembers subcription with non clean session ")
print ("Test1: Test that Messages with QOS of 0 are not stored for client ")
msg1="message0"
qos_s=0
topic1="my/test/topic"
sub(client,topic1,qos_s,"client1 subscribed")
inp=input("Press Something to Disconnect from server and reconnect with clean_session false:")
print("disconnecting client1")
client.disconnect()
client.loop_stop()



print("connecting client1 but not subscribing")
connected=False
client = mqtt.Client("Python1",clean_session=CLEAN_SESSION)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(ID, Pass)
client.connect(broker,port,keepalive)
client.loop_start() 
while connected!=True:
	print("Waiting")
	time.sleep(1)
inp=input("Waiting for publisher to publish something:")
client.disconnect()
client.loop_stop()
print("Test1 Passed that as broker donot remembers subcription with non clean session")



CLEAN_SESSION=False
print("Connecting client 1 with clean session set to ",CLEAN_SESSION)
client = mqtt.Client("Python1",clean_session=CLEAN_SESSION)    #create new instance
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(ID, Pass)
client.connect(broker,port,keepalive)
client.loop_start()
while connected!=True:
	print("Waiting")
	time.sleep(1)
qos_s=0
topic1="my/test/topic"
sub(client,topic1,qos_s,"client1 subscribed")
inp=input("Waiting for Publisher to Publish Something")
print("disconnecting client1")
client.disconnect()
logging.info("client1 disconected ")
inp=input("Waiting for Publisher to Publish Something while Client1 is Disconnected")
client.loop_stop()


print ("client1 reconnected but not subscribing ")
client = mqtt.Client("Python1",clean_session=CLEAN_SESSION)    #create new instance
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(ID, Pass)
client.connect(broker,port,keepalive)
client.loop_start()
while connected!=True:
	print("Waiting")
	time.sleep(1)
inp=input("Waiting for Publisher to Publish Something while Client1 is connected to check whether it rembers it subscription")
print("Test1 Passed that Test that Messages with QOS of 0 are not stored for client but Remebers Subscription when connected with Clean session False")



topic2="house/bulbs/bulb3"
print ("Test2: Now test if broker stores messages with qos 1 \
and above for disconnected client first subscribe with qos of \
1 to new topic ",topic2)
qos_s=1
sub(client,topic2,qos_s,"Subscribed to")
time.sleep(2)
print("disonnecting client1")
client.disconnect()
logging.info("client1 disconected")
client.loop_stop()
inp=input("Waiting for Publisher to Publish Something while Client1 is Disconnected to check whether it receive message or not")
client = mqtt.Client("Python1",clean_session=CLEAN_SESSION)    #create new instance
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(ID, Pass)
client.connect(broker,port,keepalive)
client.loop_start()
while connected!=True:
	print("Waiting")
	time.sleep(1)
print ("client1 reconnected but not subscribing to topics")
time.sleep(10)
print("Message Msg5 Received-Test2 Passed")
print("ending")
client.loop_stop()
