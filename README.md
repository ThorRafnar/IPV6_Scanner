# IPV6_Scanner
An ipv6 scanning tool.

<h2>First: Set up the Master API on the node you plan to run the database on.</h2>
Install MongoDB<br>
$ apt install mongodb<br>
Set up data/db directory for MongoDB<br>
$ cd /<br>
$ mkdir data<br>
$ mkdir data/db<br>
Run MongoDB<br>
$ mongod --fork --logpath /var/log/mongod.log<br>
Note: This will run mongodb in the background, logging to /var/log/mongod.log<br>
cd to the /API directory<br>
install required pip3 modules<br>
$ pip3 install -r requirements.txt<br>
Run the API<br>
$ python3 app2.py<br>
<h2>Then: Set up the Nodes</h2>
install nmap<br>
$ apt install nmap<br>
Change the variable DB_HOST (Line 9 in run.py) to the API ip address and port<br>
Install rabbitmq (Follow these up to step 6)<br>
https://www.hackerxone.com/2021/08/24/steps-to-install-rabbitmq-on-ubuntu-20-04/<br>
cd to the /src directory<br>
install required pip3 modules<br>
$ pip3 install -r requirements.txt<br>

Run the node<br>
$ python3 run.py

This will send a signal to the control API that the node is ready.<br>
We tested with up to 8 nodes.<br>
<h2>To run a scan</h2>
Send a post request to the control API with settings as JSON body. We tested using postman.<br>
URL: http://API_IP:5000/start_scan<br>
example JSON:<br>
{<br>
    "country_code": "dk",<br>
    "processes_per_ip": 4,<br>
    "ips_to_scan": 4000000<br>
}<br>
country_code is the country you want to scan.<br>
processes per ip is how many instances of scanner and deepscan to run per node. On our test setup 4 was the maximum.<br>
ips to scan is the total amount of IP addresses to scan, this will be distributed between nodes and processes evenly.<br>
NOTE: sending a post request to /start_scan will kill other scans that are going on. Keeping an eye on the Master API and making sure the processes are done is a good idea to prevent lost data. The processes are done when new POST requests stop appearing.<br>






