from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "transaction_type",
        "category",
        "amount",
        "payment_method",
        "user",
    )

    list_filter = (
        "transaction_type",
        "category",
        "payment_method",
        "date",
    )

    search_fields = (
        "category",
        "description",
    )

    ordering = ("-date",)