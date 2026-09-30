from django.db import models
from django.contrib.auth.models import User


class Receivable(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("partially_received", "Partially Received"),
        ("received", "Received"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    person_name = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    received_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    date = models.DateField()

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="pending"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def update_status(self):

        if self.received_amount <= 0:

            self.status = "pending"

        elif self.received_amount >= self.amount:

            self.status = "received"

            self.received_amount = self.amount

        else:

            self.status = "partially_received"

        self.save(
            update_fields=[
                "received_amount",
                "status"
            ]
        )

    @property
    def remaining_amount(self):

        remaining = (
            self.amount
            - self.received_amount
        )

        return max(remaining, 0)

    def __str__(self):

        return (
            f"{self.person_name} - "
            f"₹{self.amount}"
        )


class ReceivablePayment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("upi", "UPI"),
        ("bank", "Bank"),
        ("card", "Card"),
    ]

    receivable = models.ForeignKey(
        Receivable,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    date = models.DateField()

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.receivable.person_name} - "
            f"₹{self.amount}"
        )