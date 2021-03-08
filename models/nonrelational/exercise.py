from mongoengine import Document, ListField, StringField, URLField

class Exercise(Document):
     title = StringField(required=True, max_length=70)
     author = StringField(required=True, max_length=20)
     contributors = ListField(StringField(max_length=20))
     exercises = StringField(required=True, max_length=70)     
     url = URLField(required=True)
