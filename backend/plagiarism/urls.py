from django.urls import re_path
from plagiarism import views

urlpatterns = [
    re_path(r'^plagiarism/$',views.check_plagiarism)
]