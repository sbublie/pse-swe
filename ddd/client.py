import requests
import json

if __name__ == "__main__":
    
    url = "http://127.0.0.1:8000/allocate"

    for i in range(11):    
        data = {"orderid": f"test{i}", "sku": "AAA", "qty": 10}

        response = requests.post(url=url, json=data)
        print(response)
        print(response.content)
