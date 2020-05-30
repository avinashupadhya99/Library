from django.urls import path
from . import views

urlpatterns = [
    path('returnBook',views.returnBook,name='returnBook'),
]