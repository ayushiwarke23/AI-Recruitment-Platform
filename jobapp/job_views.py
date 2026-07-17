from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, RecruiterProfile
from .forms import JobForm


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