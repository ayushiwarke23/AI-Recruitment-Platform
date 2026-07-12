from django.contrib import admin
from .models import Company, Education, Experience, Skill, UserRole, CandidateProfile, Project

admin.site.register(UserRole)
admin.site.register(CandidateProfile)
admin.site.register(Education)
admin.site.register(Skill) 
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Company)