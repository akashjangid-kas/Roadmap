import json
import requests

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
with open("C:\\Users\\HP\\OneDrive\\Desktop\\prep_folder\\task_1\\api_result.json", "w", encoding="utf-8") as file:
  json.dump(api_result.json(), file, indent=2)
# print the JSON response from Rainforest API
print(json.dumps(api_result.json(), indent=2))
with open("C:\\Users\\HP\\OneDrive\\Desktop\\prep_folder\\task_1\\api_result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

product = data["product"]

summary_text = f"""
Title: {product.get('title', '')}

Brand: {product.get('brand', '')}

Rating: {product.get('rating', '')}

Total Reviews: {product.get('ratings_total', '')}

Description:
{product.get('description', '')}

Top Features:
"""

for feature in product.get("feature_bullets", [])[:5]:
    summary_text += f"- {feature}\n"

with open("C:\\Users\\HP\\OneDrive\\Desktop\\prep_folder\\task_1\\product_summary.txt", "w", encoding="utf-8") as f:
    f.write(summary_text)

print("Created product_summary.txt")