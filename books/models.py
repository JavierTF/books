from django.db import models

# el campo authors debería ser un modelo aparte y establecerse una relación ManyToMany
class Book(models.Model):
    title = models.CharField(max_length=200) #title
    author = models.CharField(max_length=200) #author_name
    isbn = models.CharField(max_length=13) #isbn []
    publication_date = models.DateField() #first_publish_year
    pages = models.PositiveIntegerField() #number_of_pages_median
    cover_image = models.URLField() #cover_i

    def __str__(self):
        return self.title
