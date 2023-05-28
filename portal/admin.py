from typing import Any
from django.contrib import admin
from django.db.models import Count, Value
from django.db.models.functions import Concat
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


@admin.register(models.JobCandidate)
class JobCandidateAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'last_name', 'first_name', 'job_applications_count']
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            Count('job_applications'),
        )
    
    # TODO: add ordering for user_id
    def user_id(self, job_candidate):
        return job_candidate.user.id

    @admin.display(ordering='user__username')
    def username(self, job_candidate):
        url = reverse('admin:core_user_change', kwargs={
            'object_id': job_candidate.user.pk
        })
        return format_html('<a href="{}">{}</a>', url, job_candidate.user.username)

    @admin.display(ordering='user__last_name')
    def last_name(self, job_candidate):
        return job_candidate.user.last_name
    
    @admin.display(ordering='user__first_name')
    def first_name(self, job_candidate):
        return job_candidate.user.first_name
    
    def job_applications_count(self, job_candidate):
        return job_candidate.job_applications__count
    
    job_applications_count.admin_order_field = 'job_applications__count'


@admin.register(models.Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'last_name', 'first_name', 'companies_count']
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            Count('companies')
        )
    
    def user_id(self, employer):
        return employer.user.id
    
    @admin.display(ordering='user__username')
    def username(self, employer):
        url = reverse('admin:core_user_change', kwargs={
            'object_id': employer.user.pk
        })
        return format_html('<a href="{}">{}</a>', url, employer.user.username)

    @admin.display(ordering='user__last_name')
    def last_name(self, employer):
        return employer.user.last_name
    
    @admin.display(ordering='user__first_name')
    def first_name(self, employer):
        return employer.user.first_name
    
    def companies_count(self, employer):
        return employer.companies__count
    
    companies_count.admin_order_field = 'companies__count'


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['title', 'manager_username', 'manager_full_name', 'jobs_count']
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            Count('jobs'),
            manager_full_name = Concat('manager__user__last_name' , 'manager__user__first_name'),
            manager_username = Value('manager__user__username')
        )
    
    def manager_username(self, company):
        url = reverse('admin:portal_employer_change', kwargs={
            'object_id': company.manager.user.pk
        })
        text = f'@{company.manager.user.username}'
        return format_html('<a href="{}">{}</a>', url, text)
    
    manager_username.admin_order_field = 'manager_username'

    def manager_full_name(self, company):
        return f'{company.manager.user.first_name} {company.manager.user.last_name}'
    
    manager_full_name.admin_order_field = 'manager_full_name'
    
    def jobs_count(self, company):
        url = (reverse('admin:portal_job_changelist')
        + '?'
        + urlencode({
            'company__id': str(company.id)
        }))
        text = company.jobs__count
        return format_html('<a href="{}">{}</a>', url, text)
    
    jobs_count.admin_order_field = 'jobs__count'

    
@admin.register(models.JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'jobs_count']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            Count('jobs')
        )

    def jobs_count(self, category):
        url = (reverse('admin:portal_job_changelist')
        + '?'
        + urlencode({
            'category__id': str(category.id)
        }))
        text = category.jobs__count
        return format_html('<a href="{}">{}</a>', url, text)
    
    jobs_count.admin_order_field = 'jobs__count'


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company_title', 'applications_count', 'expiry_date', 'category_name']
    list_per_page = 10
    list_select_related = ['category']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            Count('applications')
        )
    
    @admin.display(ordering='title')
    def job_title(self, job):
        return job.title

    @admin.display(ordering='company__title')
    def company_title(self, job):
        url = reverse('admin:portal_company_change', kwargs={
            'object_id': job.company.pk
        })
        return format_html('<a href="{}">{}</a>', url, job.company.title)

    def applications_count(self, job):
        url = (reverse('admin:portal_jobapplication_changelist')
        + '?'
        + urlencode({
            'job__id': str(job.id)
        }))
        text = job.applications__count
        return format_html('<a href="{}">{}</a>', url, text)
    
    applications_count.admin_order_field = 'applications__count'
    
    @admin.display(ordering='category__name')
    def category_name(self, job):
        url = (reverse('admin:portal_job_changelist')
        + '?'
        + urlencode({
            'category__id': str(job.category.id)
        }))
        text = job.category.name
        return format_html('<a href="{}">{}</a>', url, text)


@admin.register(models.JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    # TODO: add related links and orderings
    list_display = ['candidate_username', 'candidate_name', 'job_title', 'job_link', 'job_category', 'job_company_title', 'submition_date', 'status']
    list_per_page = 10
    list_select_related = ['job', 'candidate']

    @admin.display(ordering='job__title')
    def job_title(self, application):
        return application.job.title
    
    def job_link(self, application):
        url = reverse('admin:portal_job_change', kwargs={
            'object_id': application.job.pk
        })
        text = 'Link'
        return format_html('<a href="{}">{}</a>', url, text)
    
    def candidate_username(self, application):
        return application.candidate.user.username

    @admin.display(ordering='candidate__user')
    def candidate_name(self, application):
        return f'{application.candidate.user.first_name} {application.candidate.user.last_name}'
    
    @admin.display(ordering='job__category__name')
    def job_category(self, application):
        return application.job.category
    
    @admin.display(ordering='job__company__title')
    def job_company_title(self, application):
        url = reverse('admin:portal_company_change', kwargs={
            'object_id': application.job.company.pk
        })
        text = application.job.company.title
        return format_html('<a href="{}">{}</a>', url, text)