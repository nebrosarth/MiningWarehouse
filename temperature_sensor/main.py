import requests
import time
from random import randrange

r = requests.get('http://localhost:4041/version')

while True:
    random_temp = randrange(30, 40)
    request_temp = requests.get('http://localhost:1026/v2/entities/urn:ngsi-ld:TemperatureSensor1/attrs/current_temp',
                                headers={'fiware-service': 'openiot',
                                         'fiware-servicepath': '/'})
    print(request_temp.text)
    time.sleep(randrange(10))
    req = requests.post('http://localhost:7896/iot/d?k=4jggokgpepnvsb2uv4s40d59ov&i=temp_sensor001',
                   f'current_temp|{random_temp}', headers={'Content-Type': 'text/plain'})
    print(req)
