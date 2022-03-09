import requests
import time
import datetime


# password = "boevojvertoletapach"
# for _ in range(15):
#     requests.request("POST", f"https://watersensors.herokuapp.com/add_new_sensor?p={password}")
#     # ans = requests.request("POST", f"https://watersensors.herokuapp.com/are_you_alive")
#     # print(ans.text)
#     time.sleep(1)
# time1 = datetime.datetime.now()
# time.sleep(5)
# time2 = datetime.datetime.now()
# print(time2 - time1)
requests.request("POST", f"https://watersensors.herokuapp.com/set_data_sensor?i=6&d=red")
# password_hash_object = hashlib.sha256(password.encode("utf-8"))
# password_hex_dig = password_hash_object.hexdigest()
# print(password_hex_dig)
# a = "1;2;3"
# a = ";".join(a.replace(";", " ").replace("2", "").split())
# print(a)

