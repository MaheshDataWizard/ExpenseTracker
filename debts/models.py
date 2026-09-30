from django.db import models
from django.contrib.auth.models import User


class Debt(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("partially_paid", "Partially Paid"),
        ("paid", "Paid"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    person_name = models.CharField(
        max_length=100
    )

    borrowed_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    repaid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    date = models.DateField()

    status = models.CharField(
        max_length=20,
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

        if self.repaid_amount <= 0:
            self.status = "pending"

        elif self.repaid_amount >= self.borrowed_amount:
            self.status = "paid"
            self.repaid_amount = self.borrowed_amount

        else:
            self.status = "partially_paid"

        self.save(
            update_fields=[
                "repaid_amount",
                "status"
            ]
        )

    @property
    def remaining_amount(self):

        remaining = (
            self.borrowed_amount
            - self.repaid_amount
        )

        return max(remaining, 0)

    def __str__(self):

        return (
            f"{self.person_name} - "
            f"₹{self.borrowed_amount}"
        )


class DebtPayment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("upi", "UPI"),
        ("bank", "Bank"),
        ("card", "Card"),
    ]

    debt = models.ForeignKey(
        Debt,
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
            f"{self.debt.person_name} - "
            f"₹{self.amount}"
        )