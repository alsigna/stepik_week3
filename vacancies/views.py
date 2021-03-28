from django.db.models import Count
from django.http import Http404
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from .models import Company, Specialty, Vacancy


def custom_500(request):
    raise Http404


class MainView(TemplateView):
    template_name = "vacancies/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["specialties"] = Specialty.objects.all().annotate(vacancies_count=Count("vacancies"))
        context["companies"] = Company.objects.all().annotate(vacancies_count=Count("vacancies"))
        return context


class VacanciesView(ListView):
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specialty = self.kwargs.get("slug", None)
        if specialty:
            context["title"] = Specialty.objects.get(code=specialty).title
        else:
            context["title"] = "Все вакансии"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        specialty = self.kwargs.get("slug", None)
        if specialty:
            return queryset.filter(specialty__code=specialty)
        else:
            return queryset


class VacancyView(DetailView):
    model = Vacancy

    def get_queryset(self):
        return super().get_queryset().select_related("company")


class CompanyView(DetailView):
    model = Company

    def get_queryset(self):
        return super().get_queryset().prefetch_related("vacancies")
