from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import include, path


class CustomLoginView(auth_views.LoginView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


urlpatterns = [
    path("", landing_page, name="home"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
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