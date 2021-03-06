#!/usr/bin/env python
import socket
from sre_constants import SUCCESS
import time
import os
from threading import Thread, Lock
from queue import Queue
from ports import Ports
from generator import Generator
import pika
import sys

cwd = os.getcwd()
threads = 512
queue = Queue()
scanned_count = 0
neighbour_queue = Queue()                                                        
#open_ip =  []
ip_count = 0                                                        
print_lock = Lock()                                                  
socket.setdefaulttimeout(0.15)     

def scan_ports(host, port):
    """scans a list of addresses to one port"""
    global neighbour_queue
    global ip_count
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)           
        s.connect((host, port))                                         
        with print_lock:                                                
            channel.basic_publish(exchange='',
                routing_key='deepscan',
                body=host,
                properties=pika.BasicProperties(
                         delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
                ))  
            #For show only
            ip_count += 1
            #open_ip.append(host)
        s.close()
    except Exception as err:
        #print("closed")                    
        pass

def scan_thread():
    global queue
    while True:
        worker = queue.get()                               
        scan_ports(worker[0], worker[1])                                             
        queue.task_done()

def main(ip_list, port):
    global queue
    global ip_count
    global scanned_count
    startTime = time.time()
    for ip in ip_list:                                               
        queue.put((ip, port))                                                   

    queue.join()    
                                          
    runtime = float("%0.2f" % (time.time() - startTime))             
    print("Run time: " + str(runtime), "seconds")
    #print("Open hosts: ", str(open_ip))
    print("total open: ", str(ip_count))
    print(f"Scanned port: {str(port)}")
    #print(f"Remaining ips: {len(ips)}")
    
    
if __name__ == "__main__":
    try:
        country_code = sys.argv[1]
        id = int(sys.argv[2])
        pool_size = int(sys.argv[3])
        scan_target_count = int(sys.argv[4])
        if not os.path.exists(f'{cwd}/addresses/ipv6{country_code.upper()}.csv'):
            quit()
        #while True:
        #    country_code = input("Please select a valid country you want to scan: ")
        #    if os.path.exists(f'{cwd}/addresses/ipv6{country_code.upper()}.csv'):
        #        break
            
        #connecting to rabbitmq
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='deepscan')
        

        #Generating ports
        p = Ports(10)
        ports = p.get_common_ports()
        ports = [22, 80, 8080] 
        
        # starting an instance of Generotor so we can genarate the ipv6 addresses
        gene = Generator(f'addresses/ipv6{country_code.upper()}.csv', id, pool_size, 0)

        
        for i in range(threads):
            t = Thread(target=scan_thread)
            t.daemon = False
            t.start()

        # We have no plans of stopping the scan..
        # As of now the proscess must be killed, no ips will be lost though
        # if the deepscanner is up and running
        while scanned_count < scan_target_count:
            # To be more stealthy you can put this line in the for loop
            # before the call to main is made
            #ips = gene.get_list(16384)
            if scanned_count > 0:
                print(f"Hits {ip_count} of {scanned_count}, {(ip_count / scanned_count) * 100}% Hit rate")
            
            for port in ports:
                scanned_count += 16384
                ips = gene.get_list(16384)
                main(ips, port)

    except KeyboardInterrupt:
        print("Closed By key interrupt..")   
