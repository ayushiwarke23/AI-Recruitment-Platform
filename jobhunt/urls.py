from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from jobapp import views
from jobapp.views import add_education, ulogin,usignup,ulogout,change_password,dashboard, candidate_profile, view_candidate_profile, edit_education, delete_education,add_skills,delete_skills,add_project,edit_project,delete_project, add_experience, edit_experience, delete_experience, add_certifications, delete_certifications   
from jobapp.company_views import company_profile, view_company_profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("ulogin/", ulogin, name="ulogin"),
    path("usignup/", usignup, name="usignup"),
    path("ulogout/", ulogout, name="ulogout"),
    path("change_password/", change_password, name="change_password"),
    path("candidate_profile/", candidate_profile, name="candidate_profile"),  
    path("view_candidate_profile/",view_candidate_profile, name="view_candidate_profile"),
    path("add_skills/", add_skills, name="add_skills"),
    path("delete_skills/<int:id>/", delete_skills, name="delete_skills"),
    path("add_certifications/", add_certifications, name="add_certifications"),
    path("delete_certifications/<int:id>/", delete_certifications, name="delete_certifications"),
    path("add_education/", add_education, name="add_education"),
    path("edit_education/<int:id>/", edit_education, name="edit_education"),
    path("delete_education/<int:id>/", delete_education, name="delete_education"),
    path("add_project/", add_project, name="add_project"),
    path("edit_project/<int:id>/", edit_project, name="edit_project"),
    path("delete_project/<int:id>/", delete_project, name="delete_project"),
    path("add_experience/", add_experience, name="add_experience"),
    path("edit_experience/<int:id>/", edit_experience, name="edit_experience"),
    path("delete_experience/<int:id>/", delete_experience, name="delete_experience"),
    path("company_profile/", company_profile, name="company_profile"),
    path("view_company_profile/", view_company_profile, name="view_company_profile"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)