import os
from datetime import datetime

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()

import data  # noqa: E402
from vacancies.models import Company, Specialty, Vacancy  # noqa: E402


def fill_specialties(specialties):
    """Populate speciality database

    Args:
        specialties (dict): 'specialties' dict from moc-file

    Returns:
        bool: True at the end
    """
    for specialty in data.specialties:
        Specialty.objects.create(**specialty)
    return True


def fill_companies(companies):
    """Populate company database

    Args:
        companies (dict): 'companies' dict from moc-file

    Returns:
        dict: mapping dictionary for saving job->company relations
    """
    mapping = {}
    for company in companies:
        moc_id = company.pop("id")
        company["name"] = company["title"]
        _ = company.pop("title")
        new_company = Company(**company)
        new_company.save()
        mapping.setdefault(moc_id, new_company.pk)
    return mapping


def fill_vacancies(vacancies, mapping):
    """Populate vacancy database

    Args:
        vacancies (dict): 'job' dict from moc-file
        mapping (dict): dict which is saved relations between moc-company-id and company in database

    Returns:
        [type]: [description]
    """
    for vacancy in vacancies:
        Vacancy.objects.create(
            title=vacancy["title"],
            salary_min=vacancy["salary_from"],
            salary_max=vacancy["salary_to"],
            skills=vacancy["skills"],
            description=vacancy["description"],
            published_at=datetime.strptime(vacancy["posted"], "%Y-%m-%d").date(),
            specialty=Specialty.objects.get(code=vacancy["specialty"]),
            company=Company.objects.get(pk=mapping[vacancy["company"]]),
        )
    return True


if __name__ == "__main__":
    fill_specialties(data.specialties)
    mapping = fill_companies(data.companies)
    fill_vacancies(data.jobs, mapping)
