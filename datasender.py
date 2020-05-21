import hmac
import hashlib
import datetime
import base64
import uuid
import functools

from paho.mqtt.client import Client


def get_amazon_auth_headers(access_key, secret_key, region, host, port, headers=None):
    """ Get the amazon auth headers for working with the amazon websockets
    protocol
    Requires a lot of extra stuff:
    http://docs.aws.amazon.com/general/latest/gr//sigv4-create-canonical-request.html
    http://docs.aws.amazon.com/general/latest/gr//signature-v4-examples.html#signature-v4-examples-pythonw
    http://docs.aws.amazon.com/general/latest/gr//sigv4-signed-request-examples.html#sig-v4-examples-get-auth-header
    Args:
        access_key (str): Amazon access key (AWS_ACCESS_KEY_ID)
        secret_key (str): Amazon secret access key (AWS_SECRET_ACCESS_KEY)
        region (str): aws region
        host (str): iot endpoint (xxxxxxxxxxxxxx.iot.<region>.amazonaws.com)
        headers (dict): a dictionary of the original headers- normally websocket headers
    Returns:
        dict: A string containing the headers that amazon expects in the auth
            request for the iot websocket service
    """

    # pylint: disable=unused-variable,unused-argument

    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def getSignatureKey(key, dateStamp, regionName, serviceName):
        kDate = sign(("AWS4" + key).encode("utf-8"), dateStamp)
        kRegion = sign(kDate, regionName)
        kService = sign(kRegion, serviceName)
        kSigning = sign(kService, "aws4_request")
        return kSigning

    service = "iotdevicegateway"
    algorithm = "AWS4-HMAC-SHA256"

    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime("%Y%m%d") # Date w/o time, used in credential scope

    if headers is None:
        headers = {
            "Host": "{0:s}:443".format(host),
            "Upgrade": "websocket",
            "Connection": "Upgrade",
            "Origin": "https://{0:s}:443".format(host),
            "Sec-WebSocket-Key": base64.b64encode(uuid.uuid4().bytes),
            "Sec-Websocket-Version": "13",
            "Sec-Websocket-Protocol": "mqtt",
        }

    headers.update({
        "X-Amz-Date": amzdate,
    })

    # get into 'canonical' form - lowercase, sorted alphabetically
    canonical_headers = "\n".join(sorted("{}:{}".format(i.lower(), j).strip() for i, j in headers.items()))
    # Headers to sign - alphabetical order
    signed_headers = ";".join(sorted(i.lower().strip() for i in headers.keys()))

    # No payload
    payload_hash = hashlib.sha256("".encode("utf-8")).hexdigest().lower()

    request_parts = [
        "GET",
        "/mqtt",
        # no query parameters
        "",
        canonical_headers + "\n",
        signed_headers,
        payload_hash,
    ]

    canonical_request = "\n".join(request_parts).encode("utf-8")

    # now actually hash request and sign
    hashed_request = hashlib.sha256(canonical_request).hexdigest()

    credential_scope = "{datestamp:s}/{region:s}/{service:s}/aws4_request".format(**locals())
    string_to_sign = "{algorithm:s}\n{amzdate:s}\n{credential_scope:s}\n{hashed_request:s}".format(**locals())

    signing_key = getSignatureKey(secret_key, datestamp, region, service)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    # create auth header
    authorization_header = "{algorithm:s} Credential={access_key:s}/{credential_scope:s}, SignedHeaders={signed_headers:s}, Signature={signature:s}".format(**locals())

    # get final header string
    headers["Authorization"] = authorization_header

    return headers


def example_use():
    access_key = "ASIA23TQKTNW3HZQRIVM"
    secret_key = "XzFXZpIRCOJrXG0qIuXSjwpbf50B1c39jJt6pWYf"
    port = 8883

    region = "us-east-1"

    # This is specific to your AWS account
    host = "a3an6t3dmucedq-ats.iot.{0:s}.amazonaws.com".format(region)

    extra_headers = functools.partial(
        get_amazon_auth_headers,
        access_key,
        secret_key,
        region,
        host,
        port,
    )

    client = Client(transport="websockets")

    client.ws_set_options(headers=extra_headers)

    # Use client as normal from here
    client.tls_set(ca_certs="AmazonRootCA1.pem", certfile="9fe37e8b85-certificate.pem.crt", keyfile="9fe37e8b85-private.pem.key")
    client.connect(host, port)
    client.publish("demo/topic1", payload="Hello World", qos=0, retain=False)

example_use()