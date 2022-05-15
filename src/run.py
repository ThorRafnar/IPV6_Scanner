#!/usr/bin/env python
# encoding: utf-8
import json
import subprocess
import os
import requests as req
from flask import Flask, request, jsonify, Response

DB_HOST = "64.227.64.75:5000"
app = Flask(__name__)


@app.route('/start_working_bitch', methods=['POST'])
def start_working():
    data = request.get_json()
    print(data)
    process_count = data['processes_to_run']
    base_id = data['id']
    pool_size = data['pool_size']
    country_code = data['country_code']
    ips_to_scan = data['scan_count']
    # Shut down previous processes
    os.system('kill -9 $(pgrep -f scannernmap.py)')
    os.system('kill -9 $(pgrep -f deepscan.py)')
    #Start Deepscan consumers
    for _ in range(process_count):
        subprocess.Popen(['python3', 'deepscan.py', DB_HOST], stdout=subprocess.DEVNULL)
    #Start Masscan Producers
    for i in range(process_count):
        subprocess.Popen(['python3', 'scannernmap.py', country_code, str(base_id + i), str(pool_size), str(ips_to_scan)])
        
    return Response(status=201)


if __name__ == "__main__":
    req.post(f'http://{DB_HOST}/ready')
    app.run('0.0.0.0', port=5001, debug=True)
