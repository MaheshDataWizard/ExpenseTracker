from django.contrib import admin

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


@admin.register(ReceivablePayment)
class ReceivablePaymentAdmin(admin.ModelAdmin):

    list_display = (
        "receivable",
        "amount",
        "date",
        "payment_method",
    )

    list_filter = (
        "payment_method",
        "date",
    )

    search_fields = (
        "receivable__person_name",
        "notes",
    )