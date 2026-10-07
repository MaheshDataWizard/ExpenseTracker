from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Debt, DebtPayment


class DebtPaymentInline(admin.TabularInline):

    model = DebtPayment

    extra = 0


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):

    list_display = (
        "person_name",
        "borrowed_amount",
        "repaid_amount",
        "remaining",
        "status",
        "date",
        "user",
        "edit",
    )

    list_filter = (
        "status",
        "date",
    )

    search_fields = (
        "person_name",
        "notes",
    )

    ordering = ("-date",)

    inlines = [
        DebtPaymentInline
    ]

    def remaining(self, obj):

        return obj.remaining_amount

    remaining.short_description = "Remaining"

    def edit(self, obj):
        url = reverse("admin:debts_debt_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', url)

    edit.short_description = "Edit"


@admin.register(DebtPayment)
class DebtPaymentAdmin(admin.ModelAdmin):

    list_display = (
        "debt",
        "amount",
        "date",
        "payment_method",
        "edit",
    )

    list_filter = (
        "payment_method",
        "date",
    )

    search_fields = (
        "debt__person_name",
        "notes",
    )

    def edit(self, obj):
        url = reverse("admin:debts_debtpayment_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', url)

    edit.short_description = "Edit"