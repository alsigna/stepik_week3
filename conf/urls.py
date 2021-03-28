from django.urls import path
from vacancies.views import custom_500, MainView, VacanciesView, VacancyView, CompanyViewVer4

handler500 = custom_500

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("vacancies/", VacanciesView.as_view(), name="vacancies"),
    path("vacancies/<int:pk>", VacancyView.as_view(), name="vacancy"),
    path("vacancies/cat/<str:specialty_code>", VacanciesView.as_view(), name="vacancies_by_specialty"),
    path("companies/<int:pk>", CompanyViewVer4.as_view(), name="company"),
]
