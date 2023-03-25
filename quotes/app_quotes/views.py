from collections import Counter

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import AuthorForm, QuoteForm, TagForm
from .models import Author, Quote, Tag


def main(request):
    all_tags = []
    most_popular_tag = []

    quotes = Quote.objects.all()

    for quote in quotes:
        for tag in quote.get_quote_tags():
            all_tags.append(tag)

    for top in Counter(all_tags).most_common(10):
        most_popular_tag.append(top[0])

    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "app_quotes/index.html",
                  context={"quotes": quotes, "most_popular_tag": most_popular_tag, 'page_obj': page_obj})


@login_required
def add_author(request):
    form = AuthorForm(instance=Author())
    authors = Author.objects.all()
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=Author())
        if form.is_valid():
            form.save(commit=True)
            return redirect(to='app_quotes:main')
    return render(request, 'app_quotes/add_author.html',
                  context={'title': 'Quotes: Add author', 'authors': authors, 'form': form})


@login_required
def add_quote(request):
    form = QuoteForm(instance=Quote())
    if request.method == 'POST':
        form = QuoteForm(request.POST, request.FILES, instance=Quote())
        if form.is_valid():
            quote = form.save(commit=True)

            selected_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in selected_tags.iterator():
                quote.tags.add(tag)

            quote.save()
            return redirect(to='app_quotes:main')
    return render(request, 'app_quotes/add_quote.html', context={'title': 'Quotes: Add quote', 'form': form})


@login_required
def add_tag(request):
    form = TagForm(instance=Tag())
    if request.method == 'POST':
        form = TagForm(request.POST, request.FILES, instance=Tag())
        if form.is_valid():
            form.save(commit=True)
            return redirect(to='app_quotes:main')
    return render(request, 'app_quotes/add_tag.html', context={'title': 'Quotes: Add tag', 'form': form})


def tag(request, tag):
    tag_object = get_object_or_404(Tag, name=tag)

    quotes = Tag.objects.get(name=tag)
    quotes = quotes.quote_set.all()  # Returns all Entry objects for this Author.

    # quotes = Quote.objects.all()
    # # quotes.tags.all()  # Returns all Author objects for this Entry.
    # # e.authors.count()
    # quotes.tags.filter(tag__name=tag)

    # quotes = Tag.objects.filter(name=tag)
    # quotes.quote_set.all()
    # tag_object.quote.all()
    # e = Tag.objects.get(T)
    # e.authors.all()
    # quotes = tag_object.quote.all();
    # quotes = Quote.objects.all().filter(tags=tag)
    return render(request, 'app_quotes/tag.html', context={'title': 'Quotes: Tag', 'tag': tag_object, 'quotes': quotes})


def author(request, fullname):
    author = get_object_or_404(Author, fullname=fullname)
    return render(request, 'app_quotes/author.html', context={'title': 'Quotes: author', 'author': author})


# def quote(request):
#     return render(request, 'app_quotes/quote.html', context={'title': 'Quotes: quote'})
