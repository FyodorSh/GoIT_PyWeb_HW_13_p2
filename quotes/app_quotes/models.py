from django.db.models import Model, CharField, TextField, ManyToManyField, ForeignKey, CASCADE


class Tag(Model):
    name = CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f'{self.name}'


class Author(Model):
    fullname = CharField(max_length=150, unique=True)
    born_date = CharField(max_length=100, null=False)
    born_location = CharField(max_length=150, null=False)
    description = TextField(null=True)

    def __str__(self):
        return f'{self.fullname}'


class Quote(Model):
    tags = ManyToManyField(Tag)
    text = TextField(max_length=1000, null=False)
    author = ForeignKey(Author, on_delete=CASCADE)

    def __str__(self):
        return f'{self.text}'

    def get_quote_text(self):
        return self.text

    def get_quote_author(self):
        return self.author

    def get_quote_tags(self):
        tags = self.tags.all()
        return tags
