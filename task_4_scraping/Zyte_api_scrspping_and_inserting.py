"""
=========================================================
ZYTE API -> JSON FILE -> MONGODB ATLAS PIPELINE
=========================================================

Flow:

GIVA Website
      ↓
Zyte API
      ↓
Structured Product Data
      ↓
products.json
      ↓
MongoDB Atlas

=========================================================
"""

import json
from datetime import datetime
from pymongo import MongoClient
import requests

# =====================================================
# CONFIGURATION
# =====================================================

ZYTE_API_KEY = "YOUR_ZYTE_API"

TARGET_URL = (
    "https://www.giva.co/collections/mens-silver-jewellery"
)

MONGO_URI = (
    "mongodb+srv://akashjangid:<PASSWORD>@cluster0.ejifxf9.mongodb.net/"
)

DATABASE_NAME = "giva_db"
COLLECTION_NAME = "giva_products"

# =====================================================
# STEP 1 : FETCH DATA FROM ZYTE
# =====================================================

print("\nFetching data from Zyte API...")

response = requests.post(
    "https://api.zyte.com/v1/extract",
    auth=(ZYTE_API_KEY, ""),
    json={
        "url": TARGET_URL,
        "productList": True
    }
)

response.raise_for_status()

data = response.json()

# =====================================================
# STEP 2 : EXTRACT PRODUCTS
# =====================================================

product_list = data.get("productList", {})

products = product_list.get("products", [])

print(f"\nFound {len(products)} products")

if not products:
    print("No products returned.")
    exit()

# =====================================================
# STEP 3 : CLEAN / ENRICH DATA
# =====================================================

for product in products:

    product["scraped_at"] = datetime.utcnow().isoformat()

    if "price" in product:
        try:
            product["price"] = float(product["price"])
        except:
            pass

    if "regularPrice" in product:
        try:
            product["regularPrice"] = float(
                product["regularPrice"]
            )
        except:
            pass

# =====================================================
# STEP 4 : SAVE TO JSON
# =====================================================

json_filename = "products.json"

with open(
    json_filename,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        products,
        file,
        indent=4,
        ensure_ascii=False
    )

print(f"\nSaved {len(products)} products to {json_filename}")

# =====================================================
# STEP 5 : CONNECT TO MONGODB
# =====================================================

print("\nConnecting to MongoDB Atlas...")

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

collection = db[COLLECTION_NAME]

print("Connected successfully")

# =====================================================
# STEP 6 : UPSERT PRODUCTS
# =====================================================

print("\nUploading products to MongoDB...")

inserted_count = 0

for product in products:

    if "url" not in product:
        continue

    collection.update_one(
        {
            "url": product["url"]
        },
        {
            "$set": product
        },
        upsert=True
    )

    inserted_count += 1

print(
    f"{inserted_count} products inserted/updated successfully"
)

# =====================================================
# STEP 7 : VERIFY INSERTION
# =====================================================

total_docs = collection.count_documents({})

print(
    f"\nTotal documents in MongoDB: {total_docs}"
)

# =====================================================
# STEP 8 : SHOW SAMPLE DOCUMENT
# =====================================================

sample = collection.find_one()

print("\nSample Document:\n")

print(
    json.dumps(
        sample,
        indent=4,
        default=str
    )
)

# =====================================================
# STEP 9 : SIMPLE ANALYTICS
# =====================================================

print("\nAnalytics")

most_expensive = collection.find_one(
    sort=[("price", -1)]
)

if most_expensive:

    print(
        f"\nMost Expensive Product:"
    )

    print(
        most_expensive.get("name")
    )

    print(
        f"₹{most_expensive.get('price')}"
    )

# =====================================================
# DONE
# =====================================================

print("\nPipeline completed successfully.")