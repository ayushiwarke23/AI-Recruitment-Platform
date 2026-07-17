from xml.parsers.expat import model

from django.db import models
from django.contrib.auth.models import User

class UserRole(models.Model):
    ROLE_CHOICES = (("candidate","Candidate"),("recruiter","Recruiter"),("company","Company"))
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
class Certification(models.Model):
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="certifications"
    )
    certification_name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.certification_name}"

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
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="company_profile", blank=True, null=True)
    company_name = models.CharField(max_length=100)
    COMPANY_SIZE = [
        ("1-10", "1-10"),
        ("11-50", "11-50"),
        ("51-200", "51-200"),
        ("201-500", "201-500"),
        ("501-1000", "501-1000"),
        ("1001-5000", "1001-5000"),
        ("5001-10000", "5001-10000"),
        ("10001+", "10001+"),
    ]
    INDUSTRIES= [
        ("Information Technology", "Information Technology"),
        ("Healthcare", "Healthcare"),       
        ("Finance", "Finance"),
        ("Education", "Education"),
        ("Retail", "Retail"),
        ("Manufacturing", "Manufacturing"),
        ("Transportation and Logistics", "Transportation and Logistics"),
        ("Hospitality and Tourism", "Hospitality and Tourism"),
        ("Construction", "Construction"),
        ("Energy and Utilities", "Energy and Utilities"),
        ("Telecommunications", "Telecommunications"),
        ("Media and Entertainment", "Media and Entertainment"),
        ("Government and Public Sector", "Government and Public Sector"),
        ("Nonprofit and Social Services", "Nonprofit and Social Services"),
        ("Real Estate", "Real Estate"),
        ("Legal Services", "Legal Services"),
        ("Consulting", "Consulting"),
        ("Agriculture", "Agriculture"),
        ("Aerospace and Defense", "Aerospace and Defense"),
        ("Pharmaceuticals and Biotechnology", "Pharmaceuticals and Biotechnology"),
        ("Other", "Other"),
    ]


    company_logo = models.ImageField(upload_to = "company_logos/",blank=True, null=True )
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True)
    industry = models.CharField(max_length=100, choices=INDUSTRIES)
    headquarters = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    company_size = models.CharField(max_length=50, choices=COMPANY_SIZE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    linkedin = models.URLField(blank=True)

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
    
class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="recruiter_profile")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="recruiters")
    full_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="recruiter_profiles/", blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    linkedin = models.URLField(blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.company.company_name}"

class Job(models.Model):
    recruiter = models.ForeignKey(
        RecruiterProfile,
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    JOB_TYPE = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("contract", "Contract"),
        ("internship", "Internship"),
        ("temporary", "Temporary"),
    ]
    WORKPLACE_TYPES = [
        ("onsite", "On-site"),
        ("hybrid", "Hybrid"),
        ("remote", "Remote"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.TextField()
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE)
    workplace_type = models.CharField(max_length=20, choices=WORKPLACE_TYPES)
    experience_required = models.PositiveIntegerField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    vacancies = models.PositiveIntegerField()
    application_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"