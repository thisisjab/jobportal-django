from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
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
    # TODO: add link to manager
    list_display = ['title', 'manager_name', 'jobs_count']
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            Count('jobs')
        )

    def manager_name(self, company):
        return f'{company.manager.user.first_name} {company.manager.user.last_name}'
    
    def jobs_count(self, company):
        return company.jobs__count
    
    jobs_count.admin_order_field = 'jobs__count'

    
@admin.register(models.JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    # TODO: add links to related jobs
    list_display = ['name', 'jobs_count']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            Count('jobs')
        )

    def jobs_count(self, category):
        return category.jobs__count
    
    jobs_count.admin_order_field = 'jobs__count'


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    # TODO: add link to company and category, add ordering
    list_display = ['title', 'company_title', 'applications_count', 'expiry_date', 'category_name']
    list_per_page = 10
    list_select_related = ['category']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            Count('applications')
        )

    def company_title(self, job):
        return job.company.title

    def applications_count(self, job):
        return job.applications__count
    
    applications_count.admin_order_field = 'applications__count'
    
    def category_name(self, job):
        return job.category.name


@admin.register(models.JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    # TODO: add related links and orderings
    list_display = ['job_title', 'candidate_name', 'job_category', 'job_company_title', 'submition_date', 'status']
    list_per_page = 10
    list_select_related = ['job', 'candidate']

    def job_title(self, application):
        return application.job.title
    
    def candidate_name(self, application):
        return application.candidate
    
    def job_category(self, application):
        return application.job.category
    
    def job_company_title(self, application):
        return application.job.company.title