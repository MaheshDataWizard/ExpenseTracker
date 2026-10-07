from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Receivable,
    ReceivablePayment
)


class ReceivablePaymentInline(
    admin.TabularInline
):

    model = ReceivablePayment

    extra = 0


@admin.register(Receivable)
class ReceivableAdmin(admin.ModelAdmin):

    list_display = (
        "person_name",
        "amount",
        "received_amount",
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
        ReceivablePaymentInline
    ]

    def remaining(self, obj):

        return obj.remaining_amount

    remaining.short_description = "Remaining"

    def edit(self, obj):
        url = reverse("admin:receivables_receivable_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', url)

    edit.short_description = "Edit"


@admin.register(ReceivablePayment)
class ReceivablePaymentAdmin(admin.ModelAdmin):

    list_display = (
        "receivable",
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
        "receivable__person_name",
        "notes",
    )

    def edit(self, obj):
        url = reverse("admin:receivables_receivablepayment_change", args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', url)

    edit.short_description = "Edit"