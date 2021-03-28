from django.urls import path
from vacancies.views import custom_500, MainView, VacanciesView, VacancyView, CompanyView

handler500 = custom_500

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("vacancies/", VacanciesView.as_view(), name="vacancies"),
    path("vacancies/<int:pk>", VacancyView.as_view(), name="vacancy"),
    path("vacancies/cat/<str:slug>", VacanciesView.as_view(), name="vacancies_by_specialty"),
    path("companies/<int:pk>", CompanyView.as_view(), name="company"),
]
