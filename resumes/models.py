from django.db import models

class JobDescription(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    
class CandidateResult(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume_text = models.TextField()
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name="candidates")
    job_title = models.CharField(max_length=200)  # 👈 ADD THIS
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    extracted_skills = models.TextField(blank=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    

