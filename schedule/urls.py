from django.urls import path

from . import views


app_name = "schedule"

urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),
    path(
        "weekly/",
        views.weekly_schedule,
        name="weekly_schedule",
    ),
]