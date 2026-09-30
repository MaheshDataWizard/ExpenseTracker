from django.urls import path

from .views import (
    debt_list,
    add_debt,
    repay_debt,
    debt_detail,
)


urlpatterns = [

    path(
        "",
        debt_list,
        name="debt-list"
    ),

    path(
        "add/",
        add_debt,
        name="add-debt"
    ),

    path(
        "<int:debt_id>/",
        debt_detail,
        name="debt-detail"
    ),

    path(
        "<int:debt_id>/repay/",
        repay_debt,
        name="repay-debt"
    ),

]