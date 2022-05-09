#!/usr/bin/env python
from ast import Global
import socket
import time
import random
import pika
from ports import Ports
from data.dbclass import Data
from threading import Thread, Lock
from queue import Queue

mutex = Lock()

socket.setdefaulttimeout(0.20)

scan_queue = Queue()


class DeepScan():
    def __init__(self, ports, avg_timeout_seconds=5.4, std_dev_timeout=1.0): # Gaussian distribution of timeout
        self.avg_timeout_seconds = avg_timeout_seconds
        # 1000 most common ports, gives between 90-95%
        self.ports = ports
        random.shuffle(self.ports)
        self.std_dev_timeout = std_dev_timeout
        self.db_connection = Data()

    # This is the actual deepscan...
    def scan(self, address):
        open_ports = []
        
        for port in self.ports:
            print("Scanning", address, "port:", port)   
            tm = max(random.gauss(self.avg_timeout_seconds, self.std_dev_timeout) ,0.05)
            # has deafult values in init, this can be modified to run slower or faster
            time.sleep(tm)
            try:
                s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                s.connect((address, port))
                open_ports.append(port)
                print(open_ports)
                s.close()
            except:
                 pass
        
        # We had problems with writing into DB
        # we think there might have been some trouble with the thread running 
        # the DB query. Probobly becouse the function we are calling is both
        # reading and writing. 
        if open_ports:
            with mutex:
                self.db_connection.write_to_database(open_ports, address)
                open_ports = []

    
def callback(ch, method, properties, body):
    global scan_queue
    scan_queue.put(body) 

def consume_queue():
    global scan_queue
    while True:
        worker = scan_queue.get()                               
        DEEPSCAN.scan(worker)                                            
        scan_queue.task_done()


if __name__ == "__main__":
    p = Ports(1558)
    p = p.get_common_ports()
    global DEEPSCAN
    DEEPSCAN = DeepScan(p, 1.5, 0.3)
    for _ in range(100):
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

