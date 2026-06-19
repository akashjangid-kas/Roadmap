import requests
import json

# set up the request parameters
params = {
'api_key': '4A5A99828DDB45F38A520929EA492906',
  'amazon_domain': 'amazon.com',
  'asin': 'B073JYC4XM',
  'type': 'product'
}

# make the http GET request to Rainforest API
api_result = requests.get('https://api.rainforestapi.com/request', params=params)
api_result.raise_for_status()
with open("api_result.json", "w", encoding="utf-8") as file:
  json.dump(api_result.json(), file, indent=2)
# print the JSON response from Rainforest API
print(json.dumps(api_result.json(), indent=2))