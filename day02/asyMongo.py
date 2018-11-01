import motor.motor_asyncio
import asyncio
import time

client=motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db=client.test_database

start=time.time()
async def do_insert():
    for i in range(1000):
        result=await db.test_collection.insert_one({"e":"4"})
        print("result%s"%repr(result.inserted_id))

loop=asyncio.get_event_loop()
loop.run_until_complete(do_insert())
end=time.time()
print("Cost time:%f"%(end-start))
# Cost time:0.091702 100inserts
# Cost time:1.626462 1000 inserts


