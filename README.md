# GatewayForMicrolabIoT
A flask project to work as the Gateway for the MicrolabIoT project

It has been tested on Ubuntu 18.04 and Raspbian and python 3.7
It is not recommended to run this script on a computer with internet access. Use a local network instead.

## Preparation

To prepare the computer install python if not already installed and run the following commands

```pip3 install mysql-connector-python==8.0.29```

```pip3 install DateTime```

```pip3 install flask```

```pip3 install pytz```

```sudo apt install mariadb-server```

```sudo mysql_secure_installation```

set password and answer yes to all
Then run 

```mysql -u root -p```

and login
then give permissions to gnostis

```CREATE USER 'gnostis'@'localhost' IDENTIFIED BY 'gnostis';```

```GRANT ALL PRIVILEGES ON *.* TO 'gnostis'@'localhost' WITH GRANT OPTION;```

Create a folder and place microlabIoT.py and the templates folder with its contents. Open a terminal in the folder you created and run microlabIoT.py

```python3 microlabIoT.py ```

## Data

The data should be posted by the IoT devices to the following path

```http://192.168.1.250:5000/data```

The payload sent from the IoT devices should be in the format

```payload: [{"name": "temperature","value": "36.0"},{"name": "pressure","value": "60.0"},{"name": "team","value": "5"},{"name": "status","value": "OK"}]```

The only header should be 

```Content-Type application/json```

## Other Settings
You should set up your Gateway to have a specific IP such as 192.168.1.250
