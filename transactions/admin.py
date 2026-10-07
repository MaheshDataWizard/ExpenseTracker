from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import DefaultIncome, Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "transaction_type",
        "category",
        "amount",
        "payment_method",
        "user",
        "edit",
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

    def edit(self, obj):
        url = reverse("admin:transactions_transaction_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', url)

    edit.short_description = "Edit"


@admin.register(DefaultIncome)
class DefaultIncomeAdmin(admin.ModelAdmin):
    list_display = (
        "source_name",
        "category",
        "amount",
        "day_of_month",
        "is_active",
        "user",
        "edit",
    )

    list_filter = (
        "category",
        "is_active",
        "day_of_month",
    )

    search_fields = (
        "source_name",
        "description",
    )

    ordering = ("day_of_month", "source_name")

    def edit(self, obj):
        url = reverse("admin:transactions_defaultincome_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', url)

    edit.short_description = "Edit"