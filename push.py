import time

import requests
import hashlib

text = "Adminam privet"
hash_object = hashlib.sha256(text.encode("utf-8"))
hex_dig = hash_object.hexdigest()

# request = requests.request(method="POST", url="http://192.168.1.2:8080/add_new_sensor?p=Adminam privet")
# for i in range(10):
#     requests.request(method="POST", url=f"http://192.168.1.2:8080/add_new_data?id=2&data={i}")
#     time.sleep(1)
requests.request(method="POST", url=f"http://192.168.1.2:8080/add_new_data?id=2&data={99}")
