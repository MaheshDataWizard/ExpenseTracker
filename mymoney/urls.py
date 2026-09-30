from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "dashboard/",
        include("dashboard.urls")
    ),

    path(
        "transactions/",
        include("transactions.urls")
    ),
    path(
    "debts/",
    include("debts.urls")
    ),
    path(
    "receivables/",
    include("receivables.urls")
),
]