from django import forms
from django.core.exceptions import ValidationError
from .models import Book
from django.utils import timezone

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date', 'pages', 'cover_image']

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if any(char.isdigit() for char in author):
            raise ValidationError('Author name should not contain numbers.')
        return author

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if not isbn.isdigit() or len(isbn) != 13:
            raise ValidationError('ISBN must be exactly 13 digits.')
        return isbn

    def clean_publication_date(self):
        publication_date = self.cleaned_data.get('publication_date')
        if publication_date > timezone.now().date():
            raise ValidationError('Publication date cannot be in the future.')
        return publication_date

    def clean_pages(self):
        pages = self.cleaned_data.get('pages')
        if pages <= 0:
            raise ValidationError('Number of pages must be greater than 0.')
        return pages
