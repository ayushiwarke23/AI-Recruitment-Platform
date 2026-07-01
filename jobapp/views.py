from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Education, UserRole
from django.contrib.auth.decorators import login_required
from .forms import EducationForm

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return redirect('ulogin')
    

def usignup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    elif request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:

            try:
                User.objects.get(username=username)
                return render(request, "usignup.html", {"msg": "Username already exists"})

            except User.DoesNotExist:

                if User.objects.filter(email=email).exists():
                    return render(request, "usignup.html", {"msg": "Email already exists"})

                try:
                    validate_password(password)
                except ValidationError as e:
                    return render(request, "usignup.html", {"msg": e.messages})

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                user.save()
                UserRole.objects.create(user=user, role=role)   
                return redirect("ulogin")

        else:
            return render(request, "usignup.html", {"msg": "Passwords do not match"})

    else:
        return render(request, "usignup.html")

def ulogin(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "ulogin.html", {"msg": "Invalid credentials"})
    else:
        return render(request, "ulogin.html")
    
def ulogout(request):
    logout(request)
    return redirect("ulogin")

def change_password(request):
    if not request.user.is_authenticated:
        return redirect("ulogin")
    elif request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")
        if new_password == confirm_new_password:
            user = User.objects.get(username=request.user.username)
            user.set_password(new_password)
            user.save()
            return redirect("ulogin")
        else:
            return render(request, "change_password.html", {"msg": "Passwords do not match"})
    else:   
        return render(request, "change_password.html")

from .models import CandidateProfile
@login_required
def candidate_profile(request):

    try:
        profile = CandidateProfile.objects.get(user=request.user)

    except CandidateProfile.DoesNotExist:
        profile = None

    if request.method == "POST":

        if profile is None:

            profile = CandidateProfile(
                user=request.user
            )

        profile.full_name = request.POST.get("full_name")
        profile.phone = request.POST.get("phone")
        profile.date_of_birth = request.POST.get("date_of_birth")
        profile.gender = request.POST.get("gender")
        profile.bio = request.POST.get("bio")
        profile.github = request.POST.get("github")
        profile.linkedin = request.POST.get("linkedin")

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES.get("profile_picture")

        profile.save()
        print("Profile Saved Successfully")
        return redirect("view_candidate_profile")

    return render(request, "candidate_profile.html",{"profile": profile }
    )

@login_required
def view_candidate_profile(request):

    try:
        profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return redirect("candidate_profile")

    educations = Education.objects.filter(candidate=profile)

    context = {
        "profile": profile,
        "educations": educations,
    }

    return render(
        request,
        "view_candidate_profile.html",
        context,
    )
@login_required
def add_education(request):

    profile = CandidateProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = EducationForm(request.POST)

        if form.is_valid():
            education = form.save(commit=False)
            education.candidate = profile
            education.save()

            return redirect("view_candidate_profile")

    else:
        form = EducationForm()

    educations = Education.objects.filter(candidate=profile)

    context = {
        "form": form,
        "educations": educations,
    }

    return render(request, "add_education.html", context)

@login_required
def edit_education(request,id):
    profile = CandidateProfile.objects.get(user=request.user)
    education = Education.objects.get(id=id,candidate=profile)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect("view_candidate_profile")
    else:
        form = EducationForm(instance=education)
    return render(request, "add_education.html", {"form": form})

@login_required
def delete_education(request,id):
    profile = CandidateProfile.objects.get(user=request.user)
    education = Education.objects.get(id=id,candidate=profile)
    education.delete()
    return redirect("view_candidate_profile")


