from django.urls import path

from .views import (
    receivable_list,
    add_receivable,
    receive_payment,
    receivable_detail,
)


urlpatterns = [

    path(
        "",
        receivable_list,
        name="receivable-list"
    ),

    path(
        "add/",
        add_receivable,
        name="add-receivable"
    ),

    path(
        "<int:receivable_id>/",
        receivable_detail,
        name="receivable-detail"
    ),

    path(
        "<int:receivable_id>/receive/",
        receive_payment,
        name="receive-payment"
    ),

]