# Air Pollution Monitoring

## The IoT Devices
The folders in Thing1 - Thing4 contain the code to simulate the IoT device<br>
To start a device cd into any of the Thing folders and run:<br>
	`python3 csvreader.py`<br>
This will start sending data to the respective AWS thing associated with that device.

## Discovery Node

## The webserver
The folder peerserver contains the webserver to be started. This code is already on the  VMs which have been created.<br>
As this is a Django Framework we can use the following command to start it, after cd into peerserver<br>
	`python3 manage.py runserver 0.0.0.0:8443`<br>
This command needs to be fired from the VM which houses the server.
