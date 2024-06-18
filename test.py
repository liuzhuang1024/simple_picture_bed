import requests

print(requests.post("http://127.0.0.1:5000/upload", files={"file": ("1.jpg", open("1.jpg", "rb"))}).content)