from mongoengine import *

class ForecastConditions(Document):
    meta = {'db_alias': 'default'}
    date= DateField()
    caused_by = StringField(max_length=220)
    impacts = StringField(max_length=220)
    place = StringField(max_length=220)
    weather_condition = StringField(max_length=220)