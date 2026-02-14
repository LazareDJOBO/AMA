import requests
import json
import sys

url = "http://127.0.0.1:8000/predict"
data = {
    "age": 45,
    "sexe": "M",
    "creatinine": 12.5,
    "uree": 0.35,
    "temperature": 37.0,
    "cholesterol_ldl": "Normal",
    "cholesterol_total": "Normal"
}

print(f"Testing URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("\nSuccess! API responded with:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\nError: Status Code {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"\nFailed to connect: {e}")
    sys.exit(1)
