from django.db import models

class book_details(models.Model):
    book_id = models.CharField(max_length=8)
    book_name = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    publication = models.CharField(max_length=20)
    book_type = models.CharField(max_length=20)
    availability = models.BooleanField(default=True)
    edition = models.CharField(max_length=20, null=True)

    def __str__(self):  
        return self.book_name + '(' + self.book_id + ')'