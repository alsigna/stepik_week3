from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.http import Http404

from .models import Company, Specialty, Vacancy


def custom_404(request, exception):
    return HttpResponseNotFound("Page Not Found")


def custom_500(request):
    raise Http404

    # return HttpResponseServerError("Internal Server Error")


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
        specialty = self.kwargs.get("specialty_code", None)
        if specialty:
            context["title"] = Specialty.objects.get(code=specialty).title
        else:
            context["title"] = "Все вакансии"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        specialty = self.kwargs.get("specialty_code", None)
        if specialty:
            return queryset.filter(specialty__code=specialty)
        else:
            return queryset


class VacancyView(DetailView):
    model = Vacancy


class CompanyView(DetailView):
    model = Company


# class CompanyView(TemplateView):
#     template_name = "vacancies/company.html"

#     def get_context_data(self, company_id, **kwargs):
#         context = super().get_context_data(**kwargs)
#         company = get_object_or_404(Company, id=company_id)
#         vacancies = Vacancy.objects.filter(company=company)
#         context["company"] = company
#         context["vacancies"] = vacancies
#         return context
