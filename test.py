import requests

r = requests.get("http://192.168.0.10:8000/docs")
print(r.status_code)
