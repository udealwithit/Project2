import googleapiclient.discovery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="CloudProject2-c842dbb8c740.json"

instances = [[42.5,60,57,0.018417,0.036,31,8.8,15,21,0.866667,2.3,9.007212]]

PROJECT_ID="cloudproject2-278208"
MODEL_NAME="area1model"
VERSION_NAME="v1"

service = googleapiclient.discovery.build('ml', 'v1')
name = 'projects/{}/models/{}/versions/{}'.format(PROJECT_ID, MODEL_NAME, VERSION_NAME)

response = service.projects().predict(
    name=name,
    body={'instances': instances}
).execute()
print(response)

if 'error' in response:
    raise RuntimeError(response['error'])
else:
  print(response['predictions'])
