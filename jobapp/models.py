from xml.parsers.expat import model

from django.db import models
from django.contrib.auth.models import User

class UserRole(models.Model):
    ROLE_CHOICES = (("candidate","Candidate"),("recruiter","Recruiter"),)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class CandidateProfile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),           
        ("female", "Female"),
        ("other", "Other"),
        )
    user = models.OneToOneField(User, on_delete=models.CASCADE)        
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    bio = models.TextField()
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
class Education(models.Model):
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="educations"
    )
    college_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    grade = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )
    currently_studying = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.college_name}"

class Skill(models.Model):
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="skills"
    )
    skill_name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.skill_name}"

class Project(models.Model):
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    project_title = models.CharField(max_length = 150)
    project_description = models.TextField()
    links = models.URLField(blank=True)
    project_media1 = models.FileField(upload_to='project_media/', blank=True, null=True)
    project_media2 = models.FileField(upload_to='project_media/', blank=True, null=True)
    project_media3 = models.FileField(upload_to='project_media/', blank=True, null=True)
    project_media4 = models.FileField(upload_to='project_media/', blank=True, null=True)
    technologies_used = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.project_title}"

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_website = models.URLField(blank=True)
    no_of_employees = models.PositiveIntegerField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.company_name

class Experience(models.Model):
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="experiences"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="experiences"
    )

    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)
    job_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.job_title} at {self.company.company_name}"