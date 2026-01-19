from django.shortcuts import render, redirect, get_object_or_404
from .models import CandidateResult, JobDescription
from .utils import extract_jd_skills, extract_text_from_pdf, calculate_score
from django.conf import settings
import os
from django.db.models import Max
from collections import Counter

def upload_resume(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        pdf = request.FILES.get("resume")

        # ✅ SAFE JobDescription fetch
        job = JobDescription.objects.last()
        if not job:
            return render(request, "candidate_dashboard.html", {
                "error": "No job posted by HR yet"
            })

        jd_skills = extract_jd_skills(job.description)

        # ✅ Ensure media folder exists
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf.name)

        with open(pdf_path, "wb+") as f:
            for chunk in pdf.chunks():
                f.write(chunk)

        resume_text = extract_text_from_pdf(pdf_path)

        score, matched_skills = calculate_score(jd_skills, resume_text)
        status = "Shortlisted" if score >= 60 else "Rejected"

        candidate = CandidateResult.objects.create(
            name=name,
            email=email,
            job=job,
            score=score,
            extracted_skills=", ".join(matched_skills),
            status=status,
            resume_text=resume_text
        )

        # ✅ STORE SESSION
        request.session["candidate_id"] = candidate.id

        # ✅ REDIRECT
        return redirect("candidate_dashboard")
    return render(request, "candidate_result.html")

    
def candidate_dashboard(request):
    cid = request.session.get("candidate_id")
    candidate = None

    if cid:
        candidate = CandidateResult.objects.filter(id=cid).first()
    
    jobs = JobDescription.objects.all()
    return render(request, "candidate_dashboard.html", {
        "candidate": candidate,
        "candidate_id": cid,
        "jobs":jobs
    })

def resume_result(request, cid):
    candidate = get_object_or_404(CandidateResult, id=cid)

    jobs = JobDescription.objects.all()
    selected_job = None
    skills = []
    score = None
    status = None

    job_id = request.GET.get("job_id")

    if job_id:
        selected_job = JobDescription.objects.filter(id=job_id).first()

        if selected_job:
            jd_skills = extract_jd_skills(selected_job.description)
            score, matched_skills = calculate_score(
                jd_skills, candidate.resume_text
            )
            skills = matched_skills
            status = "Shortlisted" if score >= 60 else "Rejected"

    return render(request, "candidate_result.html", {
        "candidate": candidate,
        "jobs": jobs,
        "selected_job": selected_job,
        "skills": skills,
        "score": score,
        "status": status
    })

def candidate_result(request):
    return render(request, "candidate_result.html")

def hr_dashboard(request):
    return render(request, "hr_dashboard.html")

def hr_shortlisted_candidates(request):
    selected_job_id = request.GET.get("job_id")
    jobs = JobDescription.objects.all()

    candidates = CandidateResult.objects.all()

    if selected_job_id:
        candidates = candidates.filter(job_id=selected_job_id)

    # ✅ Deduplicate: latest / highest score per candidate per job
    candidates = (
        candidates
        .values("name", "job__title", "status")
        .annotate(score=Max("score"))
        .order_by("-score")
    )

    return render(request, "hr_shortlisted.html", {
        "candidates": candidates,
        "jobs": jobs,
        "selected_job_id": selected_job_id
    })


def shortlisted_candidates(request):
    candidates = CandidateResult.objects.all()

    processed = []
    for c in candidates:
        processed.append({
            "name": c.name,
            "score": c.score,
            "skills": c.extracted_skills.split(",") if c.extracted_skills else [],
            "result": c.status
        })

    return render(request, "shortlisted.html", {"candidates": processed})


def analytics(request):
    selected_job_id = request.GET.get("job_id")

    jobs = JobDescription.objects.all()

    # ==========================
    # JOB → CANDIDATE COUNT
    # ==========================
    job_counts = Counter()
    all_results = CandidateResult.objects.select_related( "job")

    for r in all_results:
        key = (r.job.title, r.email)
        job_counts[key] += 1
    
    job_wise_final = Counter()
    for (r.job_title, r.email) in job_counts:
        job_wise_final[r.job_title] += 1
        
    job_labels = list(job_wise_final.keys())
    job_values = list(job_wise_final.values())
    
    if selected_job_id:
        filtered_results = all_results.filter(job_id=selected_job_id)
    else:
        filtered_results = all_results

    # ---------------- UNIQUE CANDIDATES (EMAIL BASED) ----------------
    candidate_map = {}

    for r in filtered_results:
        email = r.email

        if email not in candidate_map or r.score > candidate_map[email]["score"]:
            candidate_map[email] = {
                "name": r.name,
                "email": email,
                "score": max(0,r.score),
                "skills": r.extracted_skills,
                "status": r.status,
                "job": r.job.title,
            }
    candidates = []
    skill_counter = Counter()

    for c in candidate_map.values():
        skills_list = []

        if c["skills"]:
            skills_list = [s.strip().lower() for s in c["skills"].split(",")]

        # Count skills ONLY for shortlisted
        if c["status"] == "Shortlisted":
            for skill in skills_list:
                skill_counter[skill] += 1

        candidates.append({
            "name": c["name"],
            "score": c["score"],
            "job": c["job"],
            "skills_list": skills_list,
        })
    skill_labels = list(skill_counter.keys())
    skill_values = list(skill_counter.values())

    context = {
        "jobs": jobs,
        "selected_job_id": selected_job_id,
        "job_labels": job_labels,
        "job_values": job_values,
        "skill_labels": skill_labels,
        "skill_values": skill_values,
        "candidates": candidates,
    }

    return render(request, "analytics.html", context)

def add_job_description(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        JobDescription.objects.create(
            title=title,
            description=description
        )

        return redirect("hr_dashboard")

    return redirect("hr_dashboard")








