from django.db.models import Count
from django.http import HttpResponseNotFound
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from .models import Company, Specialty, Vacancy
from django.shortcuts import get_object_or_404


def custom_404(request, exception):
    return HttpResponseNotFound("Page Not Found")


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


# via DetailView
class CompanyViewVer1(DetailView):
    model = Company


# the same via View + get_object_or_404
class CompanyViewVer2(View):
    def get(self, request, *args, **kwargs):
        company_pk = self.kwargs.get("pk", None)
        if not company_pk:
            raise Http404
        company = get_object_or_404(Company, pk=company_pk)
        return render(
            request=request,
            template_name="vacancies/company_detail.html",
            context={
                "object": company,
            },
        )


# the same via View + prefetch_related
class CompanyViewVer3(View):
    def get(self, request, *args, **kwargs):
        company_pk = self.kwargs.get("pk", None)
        if not company_pk:
            raise Http404
        company = Company.objects.prefetch_related("vacancies").filter(pk=company_pk).first()
        if not (company):
            raise Http404
        return render(
            request=request,
            template_name="vacancies/company_detail.html",
            context={
                "object": company,
            },
        )


class CompanyViewVer4(DetailView):
    model = Company

    def get_queryset(self):
        return super().get_queryset().prefetch_related("vacancies")
