from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from jobapp import views
from jobapp.views import add_education, ulogin,usignup,ulogout,change_password,dashboard, candidate_profile, view_candidate_profile, edit_education, delete_education,add_skills,delete_skills,add_project,edit_project,delete_project, add_experience, edit_experience, delete_experience, add_certifications, delete_certifications   
from jobapp.company_views import company_profile, view_company_profile
from jobapp.recruiter_views import recruiter_profile, view_recruiter_profile, edit_recruiter_profile
from jobapp.job_views import add_job, view_job, edit_job, delete_job, browse_jobs, job_details, apply_job, my_applications, save_job, saved_jobs, remove_saved_job, recruiter_applications, change_application_status, schedule_interview, send_offer, update_offer_status, notifications, delete_notification



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
    path("recruiter_profile/", recruiter_profile, name="recruiter_profile"),
    path("view_recruiter_profile/", view_recruiter_profile, name="view_recruiter_profile"),
    path("edit_recruiter_profile/", edit_recruiter_profile, name="edit_recruiter_profile"),
    path("add_job/", add_job,name="add_job"),
    path("view_job/", view_job, name="view_job" ),
    path("edit_job/<int:id>/", edit_job,name="edit_job"),
    path("delete_job/<int:id>/",delete_job,name="delete_job"),
    path("browse_jobs/", browse_jobs, name="browse_jobs"),
    path("job_details/<int:id>/", job_details, name = "job_details"),
    path("apply_job/<int:id>/",apply_job,name="apply_job"),
    path("my_applications/",my_applications,name="my_applications"),
    path("save_job/<int:id>/",save_job,name="save_job"),
    path("saved_jobs/",saved_jobs,name="saved_jobs"),
    path("remove_saved_job/<int:id>/",remove_saved_job,name="remove_saved_job"),  
    path("recruiter_applications/<int:id>/", recruiter_applications, name = "recruiter_applications"),
    path("change_application_status/<int:id>/", change_application_status, name = "change_application_status"),
    path("schedule_interview/<int:id>/", schedule_interview, name="schedule_interview"),
    path("send_offer/<int:id>/", send_offer, name="send_offer"),
    path("update_offer_status/<int:id>/<str:status>/",update_offer_status, name = "update_offer_status"),
    path("notifications/",notifications, name = "notifications"),
    path("delete_notification/<int:id>/",delete_notification, name = "delete_notification"),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)