# IPV6_Scanner
An ipv6 scanning tool.

First make sure you have all the required python modules:
$ pip3 install -r requirements.txt

To run open 3 terminals and navigate to /src
Execute these commands, one per terminal:
$ rabbitmq-server
$ python3 scannernmap.py
$ python3 deepscan.py

To start with a fresh database, first navigate to /src/data
Delete the file scan.sqlite3
and execute:
$ python3 create_database.py
