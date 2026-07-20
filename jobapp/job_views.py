from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, RecruiterProfile, CandidateProfile, Application, SavedJob, Interview, Offer, Notification
from .forms import JobForm, ApplicationForm, InterviewForm, OfferForm
from jobapp.ai.index import build_and_save_index
from jobapp.ai.engine import engine
from jobapp.ai.search import semantic_search
from django.db.models import Q
from urllib.parse import urlencode

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
            build_and_save_index()
            engine.index = None
            engine.job_ids = None
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
            build_and_save_index()
            engine.index = None
            engine.job_ids = None
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
    build_and_save_index()
    engine.index = None
    engine.job_ids = None

    return redirect("view_job")

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Job, Company
from jobapp.ai.search import semantic_search


@login_required
def browse_jobs(request):

    query = request.GET.get("q", "").strip()

    company_id = request.GET.get("company")

    location = request.GET.get("location")

    job_type = request.GET.get("job_type")

    workplace_type = request.GET.get("workplace_type")

    experience = request.GET.get("experience")

    salary = request.GET.get("salary")

    sort = request.GET.get("sort")



    companies = Company.objects.order_by(
        "company_name"
    )

    locations = (
        Job.objects.filter(
            is_active=True
        )
        .values_list(
            "location",
            flat=True
        )
        .distinct()
        .order_by("location")
    )



    if query:

        semantic_results = semantic_search(
            query,
            top_k=100
        )

        ids = [
            result["job_id"]
            for result in semantic_results
        ]

        jobs_dict = {
            job.id: job
            for job in Job.objects.filter(
                id__in=ids,
                is_active=True
            ).select_related(
                "company",
                "recruiter"
            )
        }

        ranked_jobs = []

        query_words = query.lower().split()

        for result in semantic_results:

            job = jobs_dict.get(
                result["job_id"]
            )

            if not job:
                continue

            score = result[
                "semantic_score"
            ]

            title = job.title.lower()

            company = (
                job.company.company_name.lower()
            )

            skills = (
                job.skills_required.lower()
            )

            job_location = (
                job.location.lower()
            )

            for word in query_words:

                if word == company:

                    score += 0.60

                elif word in company:

                    score += 0.40

                if word in title:

                    score += 0.35

                if word in skills:

                    score += 0.25

                if word == job_location:

                    score += 0.20

                elif word in job_location:

                    score += 0.10

            ranked_jobs.append(
                (score, job)
            )

        ranked_jobs.sort(
            key=lambda x: x[0],
            reverse=True
        )

        jobs = [
            job
            for score, job
            in ranked_jobs
        ]

    else:

        jobs = list(

            Job.objects.filter(
                is_active=True
            ).select_related(
                "company",
                "recruiter"
            )

        )



    # -----------------------
    # Company Filter
    # -----------------------

    if company_id:

        jobs = [

            job

            for job in jobs

            if str(job.company.id) == company_id

        ]



    # -----------------------
    # Location Filter
    # -----------------------

    if location:

        jobs = [

            job

            for job in jobs

            if job.location == location

        ]



    # -----------------------
    # Job Type
    # -----------------------

    if job_type:

        jobs = [

            job

            for job in jobs

            if job.job_type == job_type

        ]



    # -----------------------
    # Workplace Type
    # -----------------------

    if workplace_type:

        jobs = [

            job

            for job in jobs

            if job.workplace_type == workplace_type

        ]



    # -----------------------
    # Experience
    # -----------------------

    if experience:

        exp = int(experience)

        jobs = [

            job

            for job in jobs

            if job.experience_required <= exp

        ]



    # -----------------------
    # Sorting
    # -----------------------

    if sort == "latest":

        jobs.sort(

            key=lambda x: x.created_at,

            reverse=True

        )


    # -----------------------
    # Pagination
    # -----------------------

    paginator = Paginator(

        jobs,

        10

    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(

        page_number

    )

    query_params = request.GET.copy()

    if "page" in query_params:
        query_params.pop("page")

    query_string = query_params.urlencode()

    return render(

        request,

        "browse_jobs.html",

        {

            "page_obj": page_obj,

            "jobs": page_obj,

            "query": query,

            "companies": companies,

            "locations": locations,

            "selected_company": company_id,

            "selected_location": location,

            "selected_job_type": job_type,

            "selected_workplace_type": workplace_type,

            "selected_experience": experience,

            "selected_sort": sort,
            "query_string":query_string,

        }

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
            Notification.objects.create(user = job.recruiter.user, title = "New Job Application", message = f"{profile.full_name} applied for {job.title}")
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
    ).select_related(
    "job",
    "job__company"
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
    ).select_related(
    "job",
    "job__company"
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

    applications = Application.objects.filter(job=job).select_related("candidate","job")
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
            Notification.objects.create( user = application.candidate.user, title = "Interview Scheduled", message = f"Your interview for {application.job.title} has been scheduled.")

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
            Notification.objects.create( user=application.candidate.user, title="Offer Received", message=f"You have received an offer for {application.job.title}.")

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
        Notification.objects.create(
        user=offer.application.job.recruiter.user,
        title="Offer Accepted",
        message=f"{offer.application.candidate.full_name} accepted the offer.")

    elif status == "rejected":
        offer.status = "Rejected"
        Notification.objects.create(
        user=offer.application.job.recruiter.user,
        title="Offer Rejected",
        message=f"{offer.application.candidate.full_name} declined the offer.")

    offer.save()
    

    return redirect("my_applications")

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user = request.user).order_by("-created_at")
    notification_count = notifications.count()
    return render(request, "notifications.html", {"notifications":notifications, "notification_count":notification_count})

@login_required
def delete_notification(request, id):
    notification = get_object_or_404(
        Notification, id=id, user = request.user
    )
    notification.delete()
    return redirect("notifications")