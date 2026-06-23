# scrape the data from the website and collect the data and then clean it 
# using html parsing and beautiful soap 

import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.giva.co/collections/mens-silver-jewellery"

HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(
    URL,
    headers=HEADERS
)

response.raise_for_status()

soup = BeautifulSoup(
    response.text,
    "lxml"
)

products = soup.select(
    "ul#product-grid li.grid__item"
)

results = []

for product in products:

    title = product.select_one(
        'input[id="hidden_title"]'
    )

    sku = product.select_one(
        'input[id="hidden_sku"]'
    )

    price = product.select_one(
        'input[id="hidden_price"]'
    )

    category = product.select_one(
        'input[id="hidden_type"]'
    )

    product_data = {
        "title":
            title["value"] if title else None,

        "sku":
            sku["value"] if sku else None,

        "price":
            price["value"] if price else None,

        "category":
            category["value"] if category else None
    }

    results.append(product_data)

with open(
    "products.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        results,
        file,
        indent=4,
        ensure_ascii=False
    )

print(f"Saved {len(results)} products")

# data is scraped and now will be inserted in the mongodb database using pymongo


from pymongo import MongoClient
import json

uri = "mongodb+srv://akashjangid:<PASSWORD>@cluster0.ejifxf9.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)




# --------------------------------
# Connect to MongoDB Atlas
# --------------------------------

uri = "mongo url"

client = MongoClient(uri)

# --------------------------------
# Create / Select Database
# --------------------------------

db = client["giva"]

# Create / Select Collection
products_collection = db["products"]

# --------------------------------
# Read JSON File
# --------------------------------

with open(
    "products.json",
    "r",
    encoding="utf-8"
) as file:

    products = json.load(file)

# --------------------------------
# Insert Data
# --------------------------------

result = products_collection.insert_many(products)

print(
    f"{len(result.inserted_ids)} products inserted."
)