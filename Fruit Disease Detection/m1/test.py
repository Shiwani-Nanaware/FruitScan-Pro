import requests

BASE = "http://127.0.0.1:5000/"

get = input("Enter the path: ")

# file = input("Image File: ")

response = requests.post(BASE + get, files={"file":open("224.jpeg", "rb")})
print(response.json())

response = requests.get(BASE + get, json={"disease": str(response.json()['disease'])})
print(response.json())