from mongoengine import fields,Document


class BaseDocument(Document):
    active = fields.BooleanField(default=True)
    modified = fields.DateTimeField()

    meta = {'abstract': True}



class Movie(Document):
    name = fields.StringField(required=True)
    director = fields.StringField(required=True)
    categories = fields.ListField(fields.StringField())
    imdb_score = fields.FloatField()
    popularity_99 = fields.FloatField()

    meta = {'indexes': [
        {'fields': ['$name', "$director"],
         'default_language': 'english',
         'weights': {'name': 10, 'director': 5}
        }
    ]}



    def __str__(self):
        return f"Name - {self.name} : Director - {self.director}"
    
    def __repr__(self):
        return f"<{self.name} : {self.director}>"
