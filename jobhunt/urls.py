"""
URL configuration for jobhunt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from jobapp import views
from jobapp.views import add_education, ulogin,usignup,ulogout,change_password,dashboard, candidate_profile, view_candidate_profile, edit_education, delete_education

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("ulogin/", ulogin, name="ulogin"),
    path("usignup/", usignup, name="usignup"),
    path("ulogout/", ulogout, name="ulogout"),
    path("change_password/", change_password, name="change_password"),
    path("candidate_profile/", candidate_profile, name="candidate_profile"),  
    path("view_candidate_profile/",view_candidate_profile, name="view_candidate_profile"),
    path("add_education/", add_education, name="add_education"),
    path("edit_education/<int:id>/", edit_education, name="edit_education"),
    path("delete_education/<int:id>/", delete_education, name="delete_education"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)