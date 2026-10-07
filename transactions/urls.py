from django.urls import path

from .views import (
    default_income_list,
    transaction_list,
    add_transaction,
    edit_transaction,
    delete_transaction,
)


urlpatterns = [

    path(
        "",
        transaction_list,
        name="transaction-list"
    ),

    path(
        "defaults/",
        default_income_list,
        name="default-income-list"
    ),

    path(
        "add/",
        add_transaction,
        name="add-transaction"
    ),

    path(
        "edit/<int:transaction_id>/",
        edit_transaction,
        name="edit-transaction"
    ),

    path(
        "delete/<int:transaction_id>/",
        delete_transaction,
        name="delete-transaction"
    ),

]