from django.urls import path
from . import views

app_name = "lk"

urlpatterns = [
    path("profile/", views.lk_profile, name="profile"),
]