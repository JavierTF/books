import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm
from rest_framework import generics
from books.serializers import BookSerializer

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        title_query = self.request.GET.get('title')
        author_query = self.request.GET.get('author')

        if title_query:
            queryset = queryset.filter(title__icontains=title_query)
        if author_query:
            queryset = queryset.filter(author__icontains=author_query)
            
        return queryset
    
class BookListViewDRF(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AddBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('books:book_list')

class EditBookView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/edit_book.html'
    success_url = reverse_lazy('books:book_list')

    def get_object(self, queryset=None):
        # Obtiene el objeto Book basado en el ID de la URL
        return Book.objects.get(pk=self.kwargs['pk'])
    
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_object(self, queryset=None):
        # Obtiene el objeto Book basado en el ID de la URL
        return Book.objects.get(pk=self.kwargs['pk'])
    
class DeleteBookView(DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:book_list')