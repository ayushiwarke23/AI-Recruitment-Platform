from django import forms
from .models import Certification, Education, Experience, Skill, Project, Company

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