from decimal import Decimal
from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse

from transactions.models import Transaction
from debts.models import Debt
from receivables.models import Receivable

from django.shortcuts import render



@login_required
def dashboard_summary(request):

    user = request.user

    # Get month and year from URL
    today = date.today()

    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))

        if month < 1 or month > 12:
            raise ValueError

    except ValueError:
        return JsonResponse(
            {"error": "Invalid month or year"},
            status=400
        )

    # -------------------------
    # Income
    # -------------------------

    total_income = (
        Transaction.objects
        .filter(
            user=user,
            transaction_type="income",
            date__year=year,
            date__month=month
        )
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0")
    )

    # -------------------------
    # Expenses
    # -------------------------

    total_expenses = (
        Transaction.objects
        .filter(
            user=user,
            transaction_type="expense",
            date__year=year,
            date__month=month
        )
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0")
    )

    # -------------------------
    # Borrowed Money
    # -------------------------

    total_borrowed = (
        Debt.objects
        .filter(
            user=user,
            date__year=year,
            date__month=month
        )
        .aggregate(total=Sum("borrowed_amount"))["total"]
        or Decimal("0")
    )

    total_repaid = (
        Debt.objects
        .filter(
            user=user,
            date__year=year,
            date__month=month
        )
        .aggregate(total=Sum("repaid_amount"))["total"]
        or Decimal("0")
    )

    # -------------------------
    # Money to Receive
    # -------------------------

    total_receivable = (
        Receivable.objects
        .filter(
            user=user,
            date__year=year,
            date__month=month
        )
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0")
    )

    total_received = (
        Receivable.objects
        .filter(
            user=user,
            date__year=year,
            date__month=month
        )
        .aggregate(total=Sum("received_amount"))["total"]
        or Decimal("0")
    )

    # -------------------------
    # Calculations
    # -------------------------

    cash_balance = (
        total_income
        + total_borrowed
        - total_expenses
        - total_repaid
        + total_received
    )

    debt_remaining = total_borrowed - total_repaid

    receivable_remaining = (
        total_receivable - total_received
    )

    return JsonResponse({

        "month": month,
        "year": year,

        "income": float(total_income),
        "expenses": float(total_expenses),

        "borrowed": float(total_borrowed),
        "repaid": float(total_repaid),
        "debt_remaining": float(debt_remaining),

        "receivable": float(total_receivable),
        "received": float(total_received),
        "receivable_remaining": float(
            receivable_remaining
        ),

        "cash_balance": float(cash_balance),
    })


@login_required
def dashboard_page(request):
    return render(request, "dashboard/dashboard.html")