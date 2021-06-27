import paho.mqtt.client as mqtt
import time
import logging,sys
broker="PUT YOUR BROKER ADDRESS"
port= 8883
ID="Put you id"
Pass="PUT YOUR PASSWORD"
connected=False
CLEAN_SESSION=True
keepalive=1200
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
def pub(client,topic,msg,qos,p_msg):
    logging.info(p_msg + msg+ "  topic= "+topic +" qos="+str(qos))
    client.publish(topic,msg,qos)

connected=False
client = mqtt.Client("MQTT")
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

client.username_pw_set(ID, Pass)

client.connect(broker, port)
client.loop_start()
while connected!=True:
	print("Waiting")
	time.sleep(1)
inp=input("Press Something to publish in channel my/test/topic to check whether client1 able to receive message")
msg1="Message0"
topic1="my/test/topic"
qos_p=0
pub(client,topic1,msg1,qos_p,"published message ")
inp=input("Press Something to publish in channel my/test/topic to check whether he is able to receive message without subscrition")
msg1="Message1"
pub(client,topic1,msg1,qos_p,"published message ")
inp=input("Press Something to publish in channel my/test/topic to check whether client1 able to receive message")
msg2="Message2"
pub(client,topic1,msg2,qos_p,"published message ")
inp=input("Press Something to publish in channel my/test/topic when client1 is not present")
msg3="message3"
pub(client,topic1,msg3,qos_p,"client2 publishing while client1 disconnected ")
inp=input("Press Something to publish in channel my/test/topic when client1 is present but not Subscribed")
msg4="message4"
pub(client,topic1,msg4,qos_p,"published message msg4 ")
qos_p=1
inp=input("Press Something to publish in channel when client is not available with qos =1")
msg5="message5"
topic2="house/bulbs/bulb3"
lwm="Bulb1 Gone Offline" # Last will message
print("Setting Last will message=",lwm,"topic is",topic2 )
client.will_set(topic2,lwm,qos_p,retain=True)
pub(client,topic2,msg5,qos_p,"publish msg5 while client1 disconnected ")
client.loop_stop()
