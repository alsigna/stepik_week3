from django.urls import path
from vacancies.views import custom_500, MainView, VacanciesView, VacancyView, CompanyView
from django.urls import re_path

handler500 = custom_500

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    re_path(r"^vacancies/(?:cat/(?P<slug>\w+))?$", VacanciesView.as_view(), name="vacancies"),
    path("vacancies/<int:pk>", VacancyView.as_view(), name="vacancy"),
    path("companies/<int:pk>", CompanyView.as_view(), name="company"),
]
