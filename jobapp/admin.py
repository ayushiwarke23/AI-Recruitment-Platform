from django.contrib import admin
from .models import Certification, Company, Education, Experience, RecruiterProfile, Skill, UserRole, CandidateProfile, Project, Job, Application, SavedJob, Interview, Offer

admin.site.register(UserRole)
admin.site.register(CandidateProfile)
admin.site.register(Education)
admin.site.register(Skill) 
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Company)
admin.site.register(Certification)
admin.site.register(RecruiterProfile)
admin.site.register(Job)
admin.site.register(SavedJob)
admin.site.register(Application)
admin.site.register(Interview)
admin.site.register(Offer)