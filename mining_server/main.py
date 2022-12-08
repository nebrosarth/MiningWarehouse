import re
from typing import Union

from fastapi import FastAPI, Request, Body
import uvicorn
import requests
import json
from random import uniform

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root(request: Request,
                    ):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/xxx")
async def read_root(request: Request,
                    ):
    data = requests.get('http://localhost:8666/STH/v2/entities/urn:ngsi-ld:TemperatureSensor1/attrs/current_temp?type=temp_sensor&lastN=1',
                                headers={'fiware-service': 'openiot',
                                         'fiware-servicepath': '/'})
    data2 = data.json()
    lst = []
    # for a in data2['value'][-1]['attrValue']:
    #     lst.append(int(a['attrValue']))
    return int(data2['value'][-1]['attrValue'])


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/items")
def kaef():
    return {"wqe": 'asd'}


@app.post("/items")
def jest(request=Body()):
    current_temp = int(request['data'][0]['current_temp'])
    adjustFans(current_temp)
    return {'sads': 'asd'}


def formulaCoolerSpeed(temp):
    return 0.17 * temp ** 2.12


def adjustFans(temp: int):
    r = requests.get('http://localhost:1026/v2/entities?type=GPU', headers={'fiware-service': 'openiot',
                                                                            'fiware-servicepath': '/'}, )
    data = json.loads(r.text)
    array_items_reqs = []
    for item in data:
        id = item['id']
        # speed_scale = item['cooler_speed']['value']
        speed_scale = uniform(2.5, 3.0)
        cooler_speed = formulaCoolerSpeed(temp) * speed_scale
        req_item = f'''{{
          "id":"{id}", "type":"GPU",
          "cooler_speed":{{"type":"Integer", "value": {cooler_speed}}}
        }}'''
        array_items_reqs += [req_item]
    url = f'''
    {{
  "actionType":"update",
  "entities":[
    {','.join(set(array_items_reqs))}
  ]
}}
    '''
    result = requests.post('http://localhost:1026/v2/op/update',
                           url,
                           headers={'fiware-service': 'openiot',
                                    'fiware-servicepath': '/',
                                    'Content-Type': 'application/json'})

    print(12)
    # requests.post('')


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
