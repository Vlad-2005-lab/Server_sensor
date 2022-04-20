import random

import requests
import time
import datetime

domen = "a339-178-72-68-143.ngrok.io"

password = "boevojvertoletapach"
for i in range(1, 16):
#     requests.request("POST", f"https://{domen}/add_new_sensor?p={password}")
#     # ans = requests.request("POST", f"https://watersensors.herokuapp.com/are_you_alive")
# #     # print(ans.text)
    time.sleep(1)
    try:
        requests.request("POST", f"https://{domen}/set_data_sensor?i={i}&d={random.choice(['green', 'yellow', 'red'])}")
        print(i, "done")
    except Exception:
        print(i, "fail")
    # requests.request("POST", f"https://{domen}/set_data_sensor?i={i}&d=gray")
# password_hash_object = hashlib.sha256(password.encode("utf-8"))
# password_hex_dig = password_hash_object.hexdigest()
# print(password_hex_dig)
# a = "1;2;3"
# a = ";".join(a.replace(";", " ").replace("2", "").split())
# print(a)
