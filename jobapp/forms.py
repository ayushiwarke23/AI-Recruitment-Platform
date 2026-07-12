from django import forms
from .models import Education, Experience, Skill, Project

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