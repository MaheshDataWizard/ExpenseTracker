from calendar import monthrange
from datetime import date

from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):

    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("upi", "UPI"),
        ("bank", "Bank"),
        ("card", "Card"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    category = models.CharField(
        max_length=100
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

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.category} - ₹{self.amount}"


class DefaultIncome(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="default_incomes"
    )

    source_name = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    category = models.CharField(
        max_length=100,
        default="Salary"
    )

    day_of_month = models.PositiveIntegerField(
        default=1
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["day_of_month", "source_name"]

    def __str__(self):
        return f"{self.source_name} - ₹{self.amount}"

    def monthly_date_for(self, target_date=None):
        target_date = target_date or date.today()
        last_day = monthrange(target_date.year, target_date.month)[1]
        safe_day = min(int(self.day_of_month), last_day)
        return date(target_date.year, target_date.month, safe_day)

    def ensure_monthly_transaction(self, target_date=None):
        if not self.is_active:
            return None

        target_date = target_date or date.today()
        transaction_date = self.monthly_date_for(target_date)

        description = f"Recurring: {self.source_name}"
        if self.description:
            description = f"{description} - {self.description}"

        transaction = Transaction.objects.filter(
            user=self.user,
            transaction_type="income",
            category=self.category,
            amount=self.amount,
            date=transaction_date,
            description=description,
        ).first()

        if transaction:
            return transaction

        return Transaction.objects.create(
            user=self.user,
            transaction_type="income",
            category=self.category,
            amount=self.amount,
            date=transaction_date,
            payment_method="bank",
            description=description,
        )

    @classmethod
    def ensure_current_month_for_user(cls, user, target_date=None):
        target_date = target_date or date.today()

        for default_income in cls.objects.filter(user=user, is_active=True):
            default_income.ensure_monthly_transaction(target_date)

        return True