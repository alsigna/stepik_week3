from django.conf import settings
from django.urls import include, path, re_path
from vacancies.views import CompanyView, MainView, VacanciesView, VacancyView, custom_500

handler500 = custom_500

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    re_path(r"^vacancies/(?:cat/(?P<slug>\w+))?$", VacanciesView.as_view(), name="vacancies"),
    path("vacancies/<int:pk>", VacancyView.as_view(), name="vacancy"),
    path("companies/<int:pk>", CompanyView.as_view(), name="company"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
