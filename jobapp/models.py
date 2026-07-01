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
        return f"{self.degree} - {self.college_name}"