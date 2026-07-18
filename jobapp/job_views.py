from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, RecruiterProfile, CandidateProfile, Application, SavedJob, Interview, Offer
from .forms import JobForm, ApplicationForm, InterviewForm, OfferForm


@login_required
def view_job(request):

    recruiter = get_object_or_404(
    RecruiterProfile,
    user=request.user
    )

    jobs = Job.objects.filter(
    recruiter=recruiter
    )
    return render(
        request,
        "view_job.html",
        {
            "jobs": jobs
        }
    )

@login_required
def add_job(request):
    recruiter = get_object_or_404(RecruiterProfile, user=request.user)
    if request.method == "POST" :
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = recruiter
            job.company = recruiter.company
            job.save()
            return redirect("view_job")
    else:
        form = JobForm()
    return render(request, "add_job.html",{"form":form})
    
@login_required
def edit_job(request, id):
    recruiter = get_object_or_404(RecruiterProfile, user = request.user)
    job = get_object_or_404(Job, id=id, recruiter = recruiter)

    if request.method == "POST":
        form = JobForm( request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect("view_job")
        
    else:
        form = JobForm(instance=job)
        
    return render(request,"add_job.html",{"form":form})

@login_required
def delete_job(request, id):

    recruiter = get_object_or_404(
        RecruiterProfile,
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=id,
        recruiter=recruiter
    )

    job.delete()

    return redirect("view_job")

@login_required
def browse_jobs(request):
    jobs = Job.objects.filter(
        is_active=True
    )
    return render(
        request, "browse_jobs.html", {"jobs":jobs}
    )

@login_required
def job_details(request, id):
    job = get_object_or_404(Job, id=id, is_active=True)

    return render(request, "job_details.html",{"job":job})

@login_required
def apply_job(request, id):

    profile = get_object_or_404(
        CandidateProfile,
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=id,
        is_active=True
    )

    existing = Application.objects.filter(
        candidate=profile,
        job=job
    ).first()
    if existing:
        return redirect("my_applications")
    
    if request.method == "POST":

        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(commit=False)
            application.candidate = profile
            application.job = job
            application.save()
            return redirect("my_applications")

    else:
        form = ApplicationForm()

    return render(
        request,
        "apply_job.html",
        {
            "form": form,
            "job": job
        }
    )

@login_required
def my_applications(request):

    profile = get_object_or_404(
        CandidateProfile,
        user=request.user
    )

    applications = Application.objects.filter(
        candidate=profile
    )

    return render(
        request,
        "my_applications.html",
        {
            "applications": applications
        }
    )
@login_required
def save_job(request, id):

    profile = get_object_or_404(
        CandidateProfile,
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=id,
        is_active=True
    )

    SavedJob.objects.get_or_create(
        candidate=profile,
        job=job
    )

    return redirect("browse_jobs")

@login_required
def saved_jobs(request):

    profile = get_object_or_404(
        CandidateProfile,
        user=request.user
    )

    saved_jobs = SavedJob.objects.filter(
        candidate=profile
    )

    return render(
        request,
        "saved_jobs.html",
        {
            "saved_jobs": saved_jobs
        }
    )
@login_required
def remove_saved_job(request, id):

    profile = get_object_or_404(
        CandidateProfile,
        user=request.user
    )

    saved = get_object_or_404(
        SavedJob,
        id=id,
        candidate=profile
    )

    saved.delete()

    return redirect("saved_jobs")

@login_required
def recruiter_applications(request,id):
    recruiter = get_object_or_404(RecruiterProfile, user = request.user)
    job = get_object_or_404(Job, id=id, recruiter=recruiter)

    applications = Application.objects.filter(job=job)
    return render(request, "recruiter_applications.html", {"job":job, "applications":applications})

@login_required
def change_application_status(request,id):
    recruiter = get_object_or_404(RecruiterProfile, user = request.user)
    application = get_object_or_404(Application, id=id, job__recruiter = recruiter)
    if request.method == "POST":
        application.status = request.POST.get("status")
        application.save()
        return redirect("recruiter_applications", application.job.id)
    return render(request, "change_application_status.html", {"application":application})

@login_required
def schedule_interview(request, id):

    recruiter = get_object_or_404(
        RecruiterProfile,
        user=request.user
    )

    application = get_object_or_404(
        Application,
        id=id,
        job__recruiter=recruiter
    )

    if request.method == "POST":

        form = InterviewForm(
            request.POST
        )

        if form.is_valid():

            interview = form.save(commit=False)

            interview.application = application

            interview.save()

            application.status = "Interview Scheduled"

            application.save()

            return redirect(
                "recruiter_applications",
                application.job.id
            )

    else:

        form = InterviewForm()

    return render(
        request,
        "schedule_interview.html",
        {
            "form": form,
            "application": application
        }
    )    
@login_required
def send_offer(request, id):

    recruiter = get_object_or_404(
        RecruiterProfile,
        user=request.user
    )

    application = get_object_or_404(
        Application,
        id=id,
        job__recruiter=recruiter
    )

    if request.method == "POST":

        form = OfferForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            offer = form.save(commit=False)

            offer.application = application

            offer.save()

            application.status = "Selected"

            application.save()

            return redirect(
                "recruiter_applications",
                application.job.id
            )

    else:

        form = OfferForm()

    return render(
        request,
        "send_offer.html",
        {
            "form": form,
            "application": application
        }
    )

@login_required
def update_offer_status(request, id, status):

    profile = get_object_or_404(
        CandidateProfile,
        user=request.user
    )

    offer = get_object_or_404(
        Offer,
        id=id,
        application__candidate=profile
    )

    if status == "accept":
        offer.status = "Accepted"

    elif status == "decline":
        offer.status = "Declined"

    offer.save()

    return redirect("my_applications")