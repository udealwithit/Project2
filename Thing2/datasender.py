import ssl
import paho.mqtt.client as mqtt


def ssl_alpn(ca, cert, private):
    try:
        #debug print opnessl version
        IoT_protocol_name = "x-amzn-mqtt-ca"
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

def getMQTTClient(ca, cert, private):
    mqttc = mqtt.Client()
    ssl_context = ssl_alpn(ca, cert, private)
    mqttc.tls_set_context(context=ssl_context)
    return mqttc