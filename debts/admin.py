from django.contrib import admin

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


@admin.register(DebtPayment)
class DebtPaymentAdmin(admin.ModelAdmin):

    list_display = (
        "debt",
        "amount",
        "date",
        "payment_method",
    )

    list_filter = (
        "payment_method",
        "date",
    )

    search_fields = (
        "debt__person_name",
        "notes",
    )