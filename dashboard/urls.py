from django.urls import path

from .views import dashboard_page, dashboard_summary


urlpatterns = [
    path("", dashboard_page, name="dashboard"),
    path("summary/", dashboard_summary, name="dashboard-summary"),
]