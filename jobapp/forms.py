from django import forms
from .models import Certification, Education, Experience, RecruiterProfile, Skill, Project, Company, Job, Application, Interview, Offer

class EducationForm(forms.ModelForm):

    class Meta:
        model = Education

        fields = [
            "college_name",
            "degree",
            "field_of_study",
            "start_year",
            "end_year",
            "grade",
            "currently_studying",
        ]
class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill

        fields = [
            "skill_name",
        ]
class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            "project_title",
            "project_description",
            "links",
            "project_media1",
            "project_media2",
            "project_media3",
            "project_media4",
            "technologies_used",
        ]

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience

        fields = [
            "company",
            "job_title",
            "start_date",
            "end_date",
            "currently_working",
            "job_description",
        ]
        widgets = { 
            "start_date":forms.DateInput(
                attrs={"type":"date"}), 
            "end_date":forms.DateInput(
                attrs={"type":"date"})
            }
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company

        fields = [
            "company_name",
            "company_logo",
            "website",
            "email",
            "phone",
            "description",
            "industry",
            "headquarters",
            "founded_year",
            "company_size",
            "linkedin",
        ]
class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification

        fields = [
            "certification_name",
            "issuing_organization",
            "issue_date",
            "expiration_date",
            "credential_id",
            "credential_url",
        ]
        widgets = {
        "issue_date": forms.DateInput(
            attrs={"type": "date"}),
        "expiration_date": forms.DateInput(
            attrs={"type": "date"}),
        }
class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile

        fields = [
            "full_name",
            "profile_picture",
            "phone",
            "email",
            "designation",
            "department",
            "experience_years",
            "linkedin",
            "office_location",
            "bio",
            "company",
        ]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "skills_required",
            "location",
            "job_type",
            "workplace_type",
            "experience_required",
            "salary_min",
            "salary_max",
            "skills_required",
            "vacancies",
            "application_deadline",
            "is_active",
        ]
        widgets = {
        "application_deadline": forms.DateInput(
            attrs={"type": "date"}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "resume",
            "cover_letter",
        ]

class InterviewForm(forms.ModelForm):

    class Meta:

        model = Interview

        fields = "__all__"

        widgets = {

            "interview_date": forms.DateInput(
                attrs={"type":"date"}
            ),

            "interview_time": forms.TimeInput(
                attrs={"type":"time"}
            ),
        }
class OfferForm(forms.ModelForm):

    class Meta:

        model = Offer

        fields = "__all__"

        widgets = {

            "joining_date": forms.DateInput(
                attrs={"type":"date"}
            ),
        }
