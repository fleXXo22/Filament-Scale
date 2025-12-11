import requests as rq
import json

URL = "http://192.168.100.45:7912/api/v1"#/spool?lot_nr=043bcf6bbe2a81?fields=id"
Argument = "/spool?lot_nr=043bcf6bbe2a81"

def do_API_get_call(argument):
    response = rq.get(f"{URL}{argument}")
    print(response)
    print(type(response))
    response = response.json()
    print(response[0]["id"])
    print(type(response))

do_API_get_call(Argument)