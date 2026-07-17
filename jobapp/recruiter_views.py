from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RecruiterProfile
from .forms import RecruiterProfileForm


@login_required
def recruiter_profile(request):

    try:
        recruiter = RecruiterProfile.objects.get(user=request.user)

    except RecruiterProfile.DoesNotExist:
        recruiter = None

    if request.method == "POST":

        if recruiter is None:

            recruiter = RecruiterProfile(
                user=request.user
            )

        form = RecruiterProfileForm(
            request.POST,
            request.FILES,
            instance=recruiter
        )

        if form.is_valid():

            form.save()

            return redirect("view_recruiter_profile")

    else:

        form = RecruiterProfileForm(instance=recruiter)

    return render(
        request,
        "recruiter_profile.html",
        {
            "form": form
        }
    )
@login_required
def view_recruiter_profile(request):

    try:
        recruiter = RecruiterProfile.objects.get(
            user=request.user
        )

    except RecruiterProfile.DoesNotExist:

        return redirect("recruiter_profile")

    return render(
        request,
        "view_recruiter_profile.html",
        {
            "recruiter": recruiter
        }
    )

@login_required
def edit_recruiter_profile(request):

    recruiter = get_object_or_404(
        RecruiterProfile,
        user=request.user
    )

    if request.method == "POST":

        form = RecruiterProfileForm(
            request.POST,
            request.FILES,
            instance=recruiter
        )

        if form.is_valid():

            form.save()

            return redirect("view_recruiter_profile")

    else:

        form = RecruiterProfileForm(instance=recruiter)

    return render(
        request,
        "recruiter_profile.html",
        {
            "form": form
        }
    )