from pymongo import MongoClient

uri = "mongodb+srv://akashjangid:mongo@cluster0.ejifxf9.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

print(client.list_database_names())

# Access Your Database
db = client["store"]
print(db)



# Access Collection
products = db["products"]
print(products)



# Read Documents
for product in products.find():
    print(product)



# Find one product with a specific id
product = products.find_one({"id": 1})
print(product)


# Insert a new product
new_product = {
    "id": 100,
    "name": "Python Mug",
    "price": 25,
    "category": "Accessories"
}

products.insert_one(new_product)