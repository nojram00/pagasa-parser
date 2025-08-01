from mongoengine import *

class WindAndCoastalWaters(Document):
    meta = {'db_alias': 'default'}
    date= DateField()
    place = StringField(max_length=220)
    speed = StringField(max_length=220)
    direction = StringField(max_length=220)
    coastal_water = StringField(max_length=220)