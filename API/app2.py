#!/usr/bin/env python
# encoding: utf-8
import json
import requests as req
from flask import Flask, request, jsonify, Response
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'HPC_IPV6_SECRET_DB',
    'host': '0.0.0.0',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
READY_SLAVES = set()



class Address(db.Document):
    address = db.StringField()
    ports = db.ListField(db.IntField())
    def to_json(self):
        return {"address": self.address,
                "ports": self.ports}

@app.route('/address', methods=['POST'])
def add_record():
    record = json.loads(request.data)
    address = Address(address=record['address'],
                ports=record['ports'])
    address.save()
    return Response(status=201)

@app.route('/address', methods=['GET'])
def get_all():
    #Address.create_index('address', unique=True)
    ls = list(Address.objects.all())
    return jsonify(ls)

@app.route('/remove_all', methods=['DELETE'])
def remove_all():
    ls = list(Address.objects.all())
    for a in ls:
        a.delete()
    return jsonify([])

@app.route('/start_scan', methods=['POST'])
def start_scan():
    '''
    JSON EXAMPLE
    {
        'country_code': 'ru',
        'processes_per_ip': 4,
        'ips_to_scan': 1000000000
    }
    '''
    data = json.loads(request.data)
    print(data)
    pool_size = data['processes_per_ip'] * len(READY_SLAVES)
    ips_per_process = data['ips_to_scan'] // pool_size
    country_code = data['country_code']
    response_data = {}
    for index, ip in enumerate(READY_SLAVES):
        outgoing_data = {
            'id': index * data['processes_per_ip'],
            'pool_size': pool_size,
            'processes_to_run': data['processes_per_ip'],
            'country_code': country_code,
            'scan_count': ips_per_process}

        print(f'Slave ID: {index} -- IP: {ip}')
        try:
            res = req.post(f'http://{ip}:5001/start_working_bitch', json=outgoing_data, timeout=1.5)
            response_data[ip] = res.status_code
        except:
            response_data[ip] = 400 
    return jsonify(response_data)

@app.route('/ready', methods=['POST'])
def ready():
    ip = request.remote_addr
    READY_SLAVES.add(ip)
    print(READY_SLAVES)
    return Response(status=201)





if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
