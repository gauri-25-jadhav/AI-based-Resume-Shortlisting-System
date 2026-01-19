from django.contrib import admin
from .models import JobDescription, CandidateResult

@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ("title", "description","created_at")

@admin.register(CandidateResult)
class CandidateResultAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "resume_text", "job", "job_title", "created_at", "score", "extracted_skills", "status")
