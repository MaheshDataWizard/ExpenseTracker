from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import DebtForm
from .models import Debt
from .payment_forms import DebtPaymentForm


@login_required
def debt_list(request):

    debts = Debt.objects.filter(
        user=request.user
    ).order_by("-date", "-created_at")

    total_remaining = sum(
        debt.remaining_amount
        for debt in debts
    )

    return render(
        request,
        "debts/debt_list.html",
        {
            "debts": debts,
            "total_remaining": total_remaining,
        }
    )


@login_required
def add_debt(request):

    if request.method == "POST":

        form = DebtForm(request.POST)

        if form.is_valid():

            debt = form.save(commit=False)

            debt.user = request.user

            debt.repaid_amount = 0

            debt.status = "pending"

            debt.save()

            messages.success(
                request,
                "Borrowed money added successfully."
            )

            return redirect("debt-list")

    else:

        form = DebtForm()

    return render(
        request,
        "debts/add_debt.html",
        {
            "form": form
        }
    )


@login_required
def repay_debt(request, debt_id):

    debt = get_object_or_404(
        Debt,
        id=debt_id,
        user=request.user
    )

    if debt.remaining_amount <= 0:

        messages.info(
            request,
            "This debt is already fully paid."
        )

        return redirect("debt-list")

    if request.method == "POST":

        form = DebtPaymentForm(request.POST)

        if form.is_valid():

            payment = form.save(
                commit=False
            )

            if payment.amount > debt.remaining_amount:

                form.add_error(
                    "amount",
                    "Repayment cannot be greater than the remaining debt."
                )

            else:

                payment.debt = debt

                payment.save()

                debt.repaid_amount += (
                    payment.amount
                )

                debt.update_status()

                messages.success(
                    request,
                    "Repayment recorded successfully."
                )

                return redirect(
                    "debt-detail",
                    debt_id=debt.id
                )

    else:

        form = DebtPaymentForm()

    return render(
        request,
        "debts/repay_debt.html",
        {
            "form": form,
            "debt": debt
        }
    )


@login_required
def debt_detail(request, debt_id):

    debt = get_object_or_404(
        Debt,
        id=debt_id,
        user=request.user
    )

    payments = debt.payments.all().order_by(
        "-date",
        "-created_at"
    )

    return render(
        request,
        "debts/debt_detail.html",
        {
            "debt": debt,
            "payments": payments
        }
    )