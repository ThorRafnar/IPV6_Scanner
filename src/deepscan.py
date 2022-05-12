#!/usr/bin/env python

######################################
#   CREATED BY Arnjee & ThorRafnar   #
######################################

from ast import Global
import socket
import time
import random
import requests as req
import pika
from ports import Ports
from data.dbclass import Data
from threading import Thread, Lock
from queue import Queue

mutex = Lock()

socket.setdefaulttimeout(0.20)

VARIATIONS = 0 #Amount of different last_hextet values to try, increase for more coverage
scan_queue = Queue()
SCANS_RUNNING = 0
THREAD_COUNT = 512

class DeepScan():
    def __init__(self, ports, avg_timeout_seconds=5.4, std_dev_timeout=1.0): # Gaussian distribution of timeout
        self.avg_timeout_seconds = avg_timeout_seconds
        # 1000 most common ports, gives between 90-95%
        self.ports = ports
        random.shuffle(self.ports)
        self.std_dev_timeout = std_dev_timeout
        self.url = 'http://64.227.64.75:5000'
        
                
    # This is the actual deepscan...
    def scan(self, address):
        address = address.decode()
        addresses = [address]
        address_as_list = address.split(':')[:7]
        last_hextet = 0
        for i in range(VARIATIONS):
            last_hextet += random.randint(1, 0x1F000 // VARIATIONS) 
            addresses.append(":".join(address_as_list + [format(last_hextet % 0x10000, 'x')]))
        #print(addresses)
        open_ports = [ [] for _ in range(len(addresses)) ]
        start = time.time()        
        for port in self.ports:
            #print("Scanning", address, "port:", port)   
            tm = max(random.gauss(self.avg_timeout_seconds, self.std_dev_timeout) ,0.05)
            # has deafult values in init, this can be modified to run slower or faster
            time.sleep(tm)
            for index,add in enumerate(addresses):
                try:
                    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                    s.connect((add, port))
                    open_ports[index].append(port)
                    #print(open_ports)
                    s.close()
                except:
                    pass
        
        for i,a in enumerate(addresses):
            if len(open_ports[i]) != 0:
                data = {
                    "address": a,
                    "ports" : open_ports[i]
                }
                res = req.post( self.url + '/address', json=data)
        found_addresses = 0
        for p in open_ports:
            if len(p) > 0:
                found_addresses += 1
        print(f'Found {found_addresses} using {VARIATIONS} variations, time: {time.time() - start} seconds')

    
def callback(ch, method, properties, body):
    global scan_queue
    scan_queue.put(body) 

def consume_queue():
    global scan_queue
    global SCANS_RUNNING
    while True:
        worker = scan_queue.get()
        with mutex:
            SCANS_RUNNING += 1
            print(f'Running {SCANS_RUNNING} scans')
        DEEPSCAN.scan(worker)
        with mutex:
            SCANS_RUNNING -= 1
        scan_queue.task_done()


if __name__ == "__main__":
    p = Ports(10)
    p = p.get_common_ports()
    global DEEPSCAN
    DEEPSCAN = DeepScan(p, 1.5, 0.3)
    for _ in range(THREAD_COUNT):
        t = Thread(target=consume_queue)
        t.daemon = False
        t.start()
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue='deepscan')
    channel.basic_consume(queue='deepscan',
        auto_ack=True,
        on_message_callback=callback)
    channel.start_consuming()
    channel.close()

