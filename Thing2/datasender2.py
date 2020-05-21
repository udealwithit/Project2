from __future__ import print_function
import sys
import ssl
import time
import json
import datetime
import logging, traceback
import paho.mqtt.client as mqtt

IoT_protocol_name = "x-amzn-mqtt-ca"

aws_iot_endpoint = "a3an6t3dmucedq-ats.iot.us-east-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
url = "https://{}".format(aws_iot_endpoint)

ca = "../AmazonRootCA1.pem" 
cert = "56c9f1c68a-certificate.pem.crt"
private = "56c9f1c68a-private.pem.key"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

def ssl_alpn():
    try:
        #debug print opnessl version
        logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

if __name__ == '__main__':
    topic = "thing2/data"
    try:
        mqttc = mqtt.Client()
        ssl_context= ssl_alpn()
        mqttc.tls_set_context(context=ssl_context)
        logger.info("start connect")
        mqttc.connect(aws_iot_endpoint, port=8883)
        logger.info("connect success")
        mqttc.loop_start()

        data = {
                    "country": "USA",
                    "State": "NJ",
                    "City": "New Jersey",
                    "air-quality": 4.3
                }
        data_out = json.dumps(data)
        count = 0
        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            count += 1
            logger.info("try to publish:{}".format(count))
            mqttc.publish(topic, data_out)
            time.sleep(1)

    except Exception as e:
        logger.error("exception main()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
