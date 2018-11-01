from pymongo import MongoClient

client=MongoClient('ip',port)
db_auth = client.admin
db_auth.authenticate("username", "password")

db=client.myRun


# db.students.update({'_id',1},{'$addToSet':{'grades':120}})
# db.students.insert({ "_id" : 7, "semester" : 2, "grades" : [ 99, 90, 96 ] })  ok
# db.students.update({"_id":7},{"$set":{"grades":[99,90,96,100]}})

data={
    "_id":1,
    "username":"xingguo",
    "title":"关于爬虫代理池的想法",
    "class":"爬虫",
    "createDate":"2018年10月31日",
    "conts":[
        {"date":'2018年10月31日','cont':'ip代理池,可以防止一个ip过多访问引起的封杀'},
        {"date":"20181031","cont":"可以尝试爬去免费代理网页上的ip\n插入数据库,用时再去取"},
    ],
    "remarks":[
        {"date":"2018年10月31日","username":"xingguo","remark":"这个观点不错,可以尝试"},
        {"date":"2018年10月31日","username":"office2012.rain@gmail.com",'remark':"ip代理池里面ip很多不可用的,应该定期检查更新"},

    ]

}
#
# db.myIdea.insert(data)

#list all idea title



# result=db.myIdea.find_one({"_id":3})
# cont=result['conts']
# print(cont)
# cont.append({"date":"2018年10月31日","cont":"测试类"})
# db.myIdea.update({"_id":3},{"$set":{"conts":cont}})

data=db.myIdea.find_one({"_id":1})
print(data)
