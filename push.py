import hashlib

import requests

password = "123"
password_hash_object = hashlib.sha256(password.encode("utf-8"))
password_hex_dig = password_hash_object.hexdigest()
print(requests.get(f"https://watersensors.herokuapp.com/check_user", params={"l": 123, "p": password_hex_dig}))
