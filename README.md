# IPV6_Scanner
An ipv6 scanning tool.

First make sure you have all the required python modules:
$ pip3 install -r requirements.txt

To run open 3 terminals and navigate to /src
Execute these commands, one per terminal:<br>
rabbitmq-server<br>
python3 scannernmap.py<br>
python3 deepscan.py<br>

To start with a fresh database, first navigate to /src/data<br>
Delete the file scan.sqlite3<br>
and execute:<br>
$ python3 create_database.py
