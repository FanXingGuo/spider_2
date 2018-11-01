from pymongo import MongoClient
import time

client=MongoClient("mongodb://localhost:27017/")

db=client.test_database;

test_collection=db.test_collection

start=time.time()

for i in range(1000):
    post_id=test_collection.insert_one({"f":"5"}).inserted_id
    print(post_id)

end=time.time()

print("Cost time:%f"%(end-start))
# Cost time:0.070694  100
# Cost time:0.722102  1000