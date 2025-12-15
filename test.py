import requests as rq
import json

import requests as rq


URL = "http://192.168.100.45:7912"#/spool?lot_nr=043bcf6bbe2a81?fields=id"
#Argument = "/spool?lot_nr=04bfd96bbe2a80"
Argument = "/spool?sort=id:desc&limit=1"

def do_API_get_call2(argument):
    response = rq.get(f"{URL}{argument}")
    print(response)
    print(type(response))
    try:
        #print(response.json()[0]["id"])
        print(response.json())
    except: 
        print("that didnt work")

def do_API_get_call(argument):
    api_call = f"{URL}/api/v1{argument}"
    response = rq.get(api_call)
    try:
        response.json()[0]["id"]
        return response.json()
    except: 
        return False
    
spool_id = do_API_get_call(Argument)[0]["id"]
print(spool_id)

