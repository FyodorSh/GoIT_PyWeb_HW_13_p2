from django.forms import ModelForm, CharField, TextInput, Textarea, ModelChoiceField, Select, SelectMultiple, \
    MultipleChoiceField

from .models import Author, Quote, Tag


class AuthorForm(ModelForm):
    fullname = CharField(max_length=150, widget=TextInput(attrs={'class': 'form-control'}))
    born_date = CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control'}))
    born_location = CharField(max_length=150, widget=TextInput(attrs={'class': 'form-control'}))
    description = CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': 6}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    text = CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': 6}))
    tags = MultipleChoiceField(widget=SelectMultiple(attrs={'class': 'form-control', 'rows': 9}),
                               choices=((tag.id, tag.name) for tag in Tag.objects.all()))

    class Meta:
        model = Quote
        fields = ['text', 'author', 'tags']


class TagForm(ModelForm):
    name = CharField(max_length=50, required=True, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Tag
        fields = ['name']
