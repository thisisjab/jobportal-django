from django.contrib import admin
from . import models


@admin.register(models.JobCandidate)
class JobCandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'job_applications_count']
    list_per_page = 10

    def full_name(self, job_candidate):
        return f'{job_candidate.user.first_name} {job_candidate.user.last_name}'
    
    def job_applications_count(self, job_candidate):
        return job_candidate.job_applications.count()


@admin.register(models.Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'companies_count']
    list_per_page = 10

    def full_name(self, employer):
        return f'{employer.user.first_name} {employer.user.last_name}'
    
    def companies_count(self, employer):
        return employer.companies.count()


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    # TODO: add link to manager
    list_display = ['title', 'manager_name', 'jobs_count']
    list_per_page = 10

    def manager_name(self, company):
        return f'{company.manager.user.first_name} {company.manager.user.last_name}'
    
    def jobs_count(self, company):
        return company.jobs.count()
    

@admin.register(models.JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    # TODO: add links to related jobs
    list_display = ['name', 'jobs_count']

    def jobs_count(self, category):
        return category.jobs.count()


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    # TODO: add link to company and category, add ordering
    list_display = ['title', 'company_title', 'applications_count', 'expiry_date', 'category_name']
    list_per_page = 10
    list_select_related = ['category']

    def company_title(self, job):
        return job.company.title

    def applications_count(self, job):
        return job.applications.count()
    
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