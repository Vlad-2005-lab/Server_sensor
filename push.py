import random

import requests
import time
import datetime
import hashlib

domen = "127.0.0.1:54321"

password = "boevojvertoletapach"
for i in range(1, 16):
    ans = requests.request("POST", f"http://{domen}/add_new_sensor?p={password}")
    # ans = requests.request("POST", f"https://watersensors.herokuapp.com/are_you_alive")
    print(i, ans)
    # time.sleep(1)
    color = random.choice(['green', 'yellow', 'red'])
    requests.request("POST", f"http://{domen}/set_data_sensor?i={i}&d={color}")
    print(i, color, "done")
    time.sleep(1)
