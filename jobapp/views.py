from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from httpcore import request
from .models import Certification, Education, Experience, Project, Skill,UserRole
from .forms import CertificationForm, EducationForm, ProjectForm, SkillForm, ExperienceForm

@login_required
def dashboard(request):

    role = UserRole.objects.filter(user = request.user).first()

    if role is None:
            return redirect("ulogout")

    return render(
        request,
        "dashboard.html",
        {
            "role": role.role
        }
    )

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
    
    educations = Education.objects.filter(candidate=profile).order_by("-end_year")
    skills = Skill.objects.filter(candidate=profile).order_by("-skill_name")
    projects = Project.objects.filter(candidate=profile).order_by("-id")
    experiences = Experience.objects.filter(candidate=profile).order_by("-start_date")
    certifications = Certification.objects.filter(candidate=profile).order_by("-issue_date")
    context = {
        "profile": profile,
        "educations": educations,
        "skills": skills,
        "projects":projects,
        "experiences": experiences,
        "certifications": certifications,
    }

    return render(
        request,
        "view_candidate_profile.html",
        context,
    )
@login_required
def add_education(request):

    profile = get_object_or_404(
    CandidateProfile,
    user=request.user
)
    if request.method == "POST":
        form = EducationForm(request.POST)

        if form.is_valid():
            education = form.save(commit=False)
            education.candidate = profile
            education.save()

            return redirect("view_candidate_profile")

    else:
        form = EducationForm()

    return render(
    request,
    "add_education.html",
    {
        "form": form
    }
)
@login_required
def edit_education(request,id):
    profile = get_object_or_404(CandidateProfile, user=request.user)
    education = get_object_or_404(Education, id=id, candidate=profile)
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
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user)   
    education = get_object_or_404(Education, id=id, candidate=profile)
    education.delete()
    return redirect("view_candidate_profile")

@login_required
def add_skills(request):
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user)    
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.candidate = profile
            skill.save()
            return redirect("view_candidate_profile")
    else:
        form = SkillForm()

    return render(
    request,
    "add_skills.html",
    {
        "form": form
    }
)

@login_required
def delete_skills(request,id):
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user
)
    skill = get_object_or_404(Skill, id=id, candidate=profile)
    skill.delete()
    return redirect("view_candidate_profile")

@login_required
def add_certifications(request):
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user)    
    if request.method == "POST":
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.candidate = profile
            certification.save()
            return redirect("view_candidate_profile")
    else:
        form = CertificationForm()

    return render(
    request,
    "add_certifications.html",
    {
        "form": form
    }
)
@login_required
def delete_certifications(request,id):
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user
)
    certification = get_object_or_404(Certification, id=id, candidate=profile)
    certification.delete()
    return redirect("view_candidate_profile")


@login_required
def add_project(request):
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user
)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.candidate = profile
            project.save()
            return redirect("view_candidate_profile")
    else:
        form = ProjectForm()

    return render(
    request,
    "add_project.html",
    {
        "form": form
    }
)
@login_required
def edit_project(request,id):
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user
)
    project = get_object_or_404(Project, id=id, candidate=profile)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("view_candidate_profile")
    else:
        form = ProjectForm(instance=project)    
    return render(request, "add_project.html", {"form": form})

@login_required
def delete_project(request,id):
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user
)
    project = get_object_or_404(Project, id=id, candidate=profile)
    project.delete()
    return redirect("view_candidate_profile")



@login_required
def add_experience(request):
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user
    )
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.candidate = profile
            experience.save()
            return redirect("view_candidate_profile")
    else:
        form = ExperienceForm()
    return render(
    request,
    "add_experience.html",
    {
        "form": form
    }
)
@login_required
def edit_experience(request,id):
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user
)
    experience = get_object_or_404(Experience, id=id, candidate=profile)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect("view_candidate_profile")
    else:
        form = ExperienceForm(instance=experience)
    return render(request, "add_experience.html", {"form": form})

@login_required
def delete_experience(request,id):
    profile = get_object_or_404(
    CandidateProfile,
    user=request.user
)
    experience = get_object_or_404(Experience, id=id, candidate=profile)
    experience.delete()
    return redirect("view_candidate_profile")