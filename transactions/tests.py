from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from .forms import TransactionForm
from .models import DefaultIncome


class DefaultIncomeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="monthlyuser",
            email="monthly@example.com",
            password="StrongPass123!",
        )

    def test_transaction_form_defaults_to_today(self):
        form = TransactionForm()

        self.assertEqual(form.initial.get("date"), date.today())

    def test_default_income_creates_current_month_transaction(self):
        default_income = DefaultIncome.objects.create(
            user=self.user,
            source_name="Salary",
            amount="1500.00",
            category="Salary",
            day_of_month=date.today().day,
        )

        created = default_income.ensure_monthly_transaction(date.today())

        self.assertIsNotNone(created)
        self.assertEqual(created.user, self.user)
        self.assertEqual(created.transaction_type, "income")
        self.assertEqual(created.date, date.today())
