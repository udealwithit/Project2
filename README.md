# Air Pollution Monitoring

## The IoT Devices
The folders in Thing1 - Thing4 contain the code to simulate the IoT device<br>
To start a device cd into any of the Thing folders and run:<br>
	`python3 csvreader.py`<br>
This will start sending data to the respective AWS thing associated with that device.<br>

## Discovery Node
The discovery folder has the code for the Node which stores which Peer is associated with which area.<br>
This server needs to be started before starting the webservers so that each peer can register itself at its startup.<br>
To start this server cd into discovery folder and run:
	`python3 manage.py runserver 0.0.0.0:8443`
	
## Machine learning model
In GCP_DL we provide the trained model in area1model.h5 file.<br>
To start a server which exposes REST endpoints for this model cd into mlmodel folder inside GCP_DL and run: <br>
	`python3 manage.py runserver 0.0.0.0:8000`

## The Webserver
The folder peerserver contains the webserver to be started. This code is already on the  VMs which have been created.<br>
As this is a Django Framework we can use the following command to start it, after cd into peerserver<br>
	`python3 manage.py runserver 0.0.0.0:8443`<br>
This command needs to be fired from the VM which houses the server.<br>
