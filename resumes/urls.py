from django.urls import path
from .views import candidate_dashboard, hr_dashboard, shortlisted_candidates, analytics, add_job_description
from . import views
urlpatterns = [
    path("dashboard/",candidate_dashboard, name="candidate_dashboard"),
    path('hr/', hr_dashboard, name='hr_dashboard'),     
    path("upload/", views.upload_resume, name="upload_resume"),
    path("result/<int:cid>/", views.resume_result, name="resume_result"),
    path("shortlisted/", shortlisted_candidates, name="shortlisted"),
    path("analytics/", analytics, name="analytics"),
    path("add-job/", add_job_description, name="add_job"),
    path("hr/shortlisted/", views.hr_shortlisted_candidates, name="hr_short"),
]

