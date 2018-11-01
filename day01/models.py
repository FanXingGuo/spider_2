from mongoengine import connect,StringField,DateTimeField,Document


DB_HOST='ip'
DB_PORT=27017
DB_NAME='test'
username="name"
password="password"


connect(DB_NAME,host=DB_HOST,port=DB_PORT,username=username,password=password, authentication_source='admin')

class BaseModel(Document):
    create_at=DateTimeField()
    meta={
        'allow_inheritance':True,
        'abstract':True
    }
class Proxy(BaseModel):
    address=StringField(unique=True)
    meta = {'collection':'proxy'}

    @classmethod
    def get_random(cls):
        proxy=cls.objects.aggregate({'$sample':{'size':1}}).next()
        return proxy

