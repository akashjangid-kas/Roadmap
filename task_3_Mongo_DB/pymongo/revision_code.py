"""
====================================================
MONGODB + PYMONGO COMPLETE REVISION FILE
====================================================

Topics Covered:
1. Connect to MongoDB Atlas
2. List Databases
3. Access Database
4. Access Collection
5. Read Documents
6. Find One Document
7. Insert One
8. Insert Many
9. Filter Documents
10. Count Documents
11. Sort Documents
12. Update One
13. Update Many
14. Delete One
15. Delete Many
16. Student Database Example

====================================================
"""

from pymongo import MongoClient
from pprint import pprint

# ====================================================
# STEP 1: CONNECT TO ATLAS
# ====================================================

URI = "mongodb+srv://akashjangid:<PASSWORD>@cluster0.ejifxf9.mongodb.net/?appName=Cluster0"

client = MongoClient(URI)

print("\n✅ Connected to MongoDB Atlas Successfully!")

# ====================================================
# STEP 2: LIST ALL DATABASES
# ====================================================

print("\n==============================")
print("ALL DATABASES")
print("==============================")

databases = client.list_database_names()

for db_name in databases:
    print(db_name)

# ====================================================
# STEP 3: ACCESS DATABASE
# ====================================================

db = client["store"]

print("\n==============================")
print("CURRENT DATABASE")
print("==============================")

print(db)

# ====================================================
# STEP 4: ACCESS COLLECTION
# ====================================================

products = db["products"]

print("\n==============================")
print("CURRENT COLLECTION")
print("==============================")

print(products)

# ====================================================
# STEP 5: READ ALL DOCUMENTS
# ====================================================

print("\n==============================")
print("ALL PRODUCTS")
print("==============================")

for product in products.find().limit(5):
    pprint(product)

# ====================================================
# STEP 6: FIND ONE DOCUMENT
# ====================================================

print("\n==============================")
print("FIND ONE PRODUCT")
print("==============================")

product = products.find_one({"id": 1})

if product:
    pprint(product)
else:
    print("Product not found")

# ====================================================
# STEP 7: INSERT ONE DOCUMENT
# ====================================================

print("\n==============================")
print("INSERT ONE PRODUCT")
print("==============================")

new_product = {
    "id": 100,
    "name": "Python Mug",
    "price": 25,
    "category": "Accessories"
}

# Uncomment to run
# products.insert_one(new_product)
# print("Inserted successfully")

# ====================================================
# STEP 8: INSERT MANY DOCUMENTS
# ====================================================

print("\n==============================")
print("INSERT MANY PRODUCTS")
print("==============================")

many_products = [
    {
        "id": 101,
        "name": "Flask Mug",
        "price": 20,
        "category": "Accessories"
    },
    {
        "id": 102,
        "name": "Django T-Shirt",
        "price": 30,
        "category": "Clothing"
    },
    {
        "id": 103,
        "name": "FastAPI Notebook",
        "price": 15,
        "category": "Stationery"
    }
]

# Uncomment to run
# products.insert_many(many_products)
# print("Multiple products inserted")

# ====================================================
# STEP 9: FILTER DOCUMENTS
# ====================================================

print("\n==============================")
print("HOODIE PRODUCTS")
print("==============================")

for product in products.find({"category": "Hoodie"}):
    pprint(product)

# ====================================================
# STEP 10: PRICE > 40
# ====================================================

print("\n==============================")
print("PRICE GREATER THAN 40")
print("==============================")

for product in products.find({"price": {"$gt": 40}}):
    pprint(product)

# ====================================================
# STEP 11: PRICE < 50
# ====================================================

print("\n==============================")
print("PRICE LESS THAN 50")
print("==============================")

for product in products.find({"price": {"$lt": 50}}):
    pprint(product)

# ====================================================
# STEP 12: COUNT DOCUMENTS
# ====================================================

print("\n==============================")
print("COUNT PRODUCTS")
print("==============================")

count = products.count_documents({})

print("Total Products =", count)

# ====================================================
# STEP 13: SORT ASCENDING
# ====================================================

print("\n==============================")
print("CHEAPEST PRODUCTS FIRST")
print("==============================")

for product in products.find().sort("price", 1).limit(5):
    pprint(product)

# ====================================================
# STEP 14: SORT DESCENDING
# ====================================================

print("\n==============================")
print("MOST EXPENSIVE PRODUCTS FIRST")
print("==============================")

for product in products.find().sort("price", -1).limit(5):
    pprint(product)

# ====================================================
# STEP 15: CHEAPEST PRODUCT
# ====================================================

print("\n==============================")
print("CHEAPEST PRODUCT")
print("==============================")

cheapest = products.find().sort("price", 1).limit(1)

for item in cheapest:
    pprint(item)

# ====================================================
# STEP 16: UPDATE ONE
# ====================================================

print("\n==============================")
print("UPDATE ONE PRODUCT")
print("==============================")

# Uncomment to run
"""
result = products.update_one(
    {"id": 100},
    {
        "$set": {
            "price": 30
        }
    }
)

print("Modified Count:", result.modified_count)
"""

# ====================================================
# STEP 17: UPDATE MANY
# ====================================================

print("\n==============================")
print("UPDATE MANY PRODUCTS")
print("==============================")

# Uncomment to run
"""
result = products.update_many(
    {"category": "Hoodie"},
    {
        "$set": {
            "discount": 10
        }
    }
)

print("Modified Count:", result.modified_count)
"""

# ====================================================
# STEP 18: DELETE ONE
# ====================================================

print("\n==============================")
print("DELETE ONE PRODUCT")
print("==============================")

# Uncomment to run
"""
result = products.delete_one(
    {"id": 100}
)

print("Deleted Count:", result.deleted_count)
"""

# ====================================================
# STEP 19: DELETE MANY
# ====================================================

print("\n==============================")
print("DELETE MANY PRODUCTS")
print("==============================")

# Uncomment to run
"""
result = products.delete_many(
    {"category": "Accessories"}
)

print("Deleted Count:", result.deleted_count)
"""

# ====================================================
# STEP 20: CREATE STUDENT DATABASE
# ====================================================

print("\n==============================")
print("STUDENT DATABASE")
print("==============================")

student_db = client["student_db"]

students = student_db["students"]

# Uncomment to insert
"""
students.insert_one(
    {
        "name": "Akash",
        "age": 21,
        "course": "MCA"
    }
)
"""

# Read students

print("\nSTUDENTS:")

for student in students.find():
    pprint(student)

# ====================================================
# TASK 1
# PRINT ALL PRODUCT NAMES
# ====================================================

print("\n==============================")
print("TASK 1: PRODUCT NAMES")
print("==============================")

for product in products.find():
    print(product.get("name"))

# ====================================================
# TASK 2
# PRODUCTS ABOVE ₹40
# ====================================================

print("\n==============================")
print("TASK 2: PRICE > 40")
print("==============================")

for product in products.find({"price": {"$gt": 40}}):
    pprint(product)

# ====================================================
# TASK 3
# COUNT PRODUCTS
# ====================================================

print("\n==============================")
print("TASK 3: COUNT PRODUCTS")
print("==============================")

print(products.count_documents({}))

# ====================================================
# TASK 4
# CHEAPEST PRODUCT
# ====================================================

print("\n==============================")
print("TASK 4: CHEAPEST PRODUCT")
print("==============================")

for product in products.find().sort("price", 1).limit(1):
    pprint(product)

# ====================================================
# TASK 5
# INSERT CUSTOM PRODUCTS
# ====================================================

custom_products = [
    {
        "id": 200,
        "name": "Python Hoodie",
        "price": 50
    },
    {
        "id": 201,
        "name": "MongoDB Mug",
        "price": 20
    },
    {
        "id": 202,
        "name": "Docker T-Shirt",
        "price": 35
    },
    {
        "id": 203,
        "name": "FastAPI Sticker",
        "price": 5
    },
    {
        "id": 204,
        "name": "VS Code Notebook",
        "price": 12
    }
]

# Uncomment to run
# products.insert_many(custom_products)

print("\n✅ MongoDB Revision Script Completed")