import pandas as pd
import time
import sys
import logging, traceback
from datasender import getMQTTClient
import paho.mqtt.client as mqtt

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

logger.info("Setting up device...")
df = pd.read_csv("NJ_Camden.csv")
df = df[1:]
df.fillna(df.mean(), inplace=True)

logger.info("Device is ready to send data")

ca = "../AmazonRootCA1.pem" 
cert = "56c9f1c68a-certificate.pem.crt"
private = "56c9f1c68a-private.pem.key"

aws_iot_endpoint = "a3an6t3dmucedq-ats.iot.us-east-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
url = "https://{}".format(aws_iot_endpoint)
topic = "thing2/data"

try:
	mqttc = getMQTTClient(ca, cert, private)
	logger.info("start connect")
	mqttc.connect(aws_iot_endpoint, port=8883)
	logger.info("connect success")
	mqttc.loop_start()
	
	for index, row in df.iterrows():
		data = row.to_json()
		logger.info("Publishing data: " + data)
		mqttc.publish(topic, data)
		time.sleep(30)
	
except Exception as e:
	logger.error("exception main()")
	logger.error("e obj:{}".format(vars(e)))
	logger.error("message:{}".format(e.message))
	traceback.print_exc(file=sys.stdout)