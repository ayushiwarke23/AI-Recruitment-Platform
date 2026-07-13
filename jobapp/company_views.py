from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Company
from .forms import CompanyForm

@login_required
def company_profile(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        company = None

    if request.method == "POST":
        if company == None:
            company = Company(user=request.user)
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect("view_company_profile")
    else:
        form = CompanyForm(instance=company)
    return render(request, "company_profile.html", {"form": form})

@login_required
def view_company_profile(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        return redirect("company_profile") 
    return render(request, "view_company_profile.html", {"company": company})