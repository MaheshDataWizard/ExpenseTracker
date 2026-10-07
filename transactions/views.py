from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import DefaultIncomeForm, TransactionForm
from .models import DefaultIncome, Transaction


@login_required
def transaction_list(request):
    DefaultIncome.ensure_current_month_for_user(request.user, date.today())

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by("-date", "-created_at")

    transaction_type = request.GET.get("type")
    category = request.GET.get("category")
    search = request.GET.get("search")

    if transaction_type:
        transactions = transactions.filter(
            transaction_type=transaction_type
        )

    if category:
        transactions = transactions.filter(
            category=category
        )

    if search:
        transactions = transactions.filter(
            description__icontains=search
        )

    return render(
        request,
        "transactions/transaction_list.html",
        {
            "transactions": transactions,
            "selected_type": transaction_type,
            "selected_category": category,
            "search": search,
        }
    )


@login_required
def default_income_list(request):
    default_incomes = DefaultIncome.objects.filter(user=request.user).order_by("day_of_month")

    if request.method == "POST":
        form = DefaultIncomeForm(request.POST)
        if form.is_valid():
            default_income = form.save(commit=False)
            default_income.user = request.user
            default_income.save()
            default_income.ensure_monthly_transaction(date.today())
            return redirect("default-income-list")
    else:
        form = DefaultIncomeForm()

    return render(
        request,
        "transactions/default_income_list.html",
        {
            "form": form,
            "default_incomes": default_incomes,
        },
    )


@login_required
def add_transaction(request):

    if request.method == "POST":

        form = TransactionForm(request.POST)

        if form.is_valid():

            transaction = form.save(commit=False)

            transaction.user = request.user

            transaction.save()

            return redirect("transaction-list")

    else:

        form = TransactionForm(initial={"date": date.today()})

    return render(
        request,
        "transactions/add_transaction.html",
        {
            "form": form
        }
    )


@login_required
def edit_transaction(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user
    )

    if request.method == "POST":

        form = TransactionForm(
            request.POST,
            instance=transaction
        )

        if form.is_valid():

            form.save()

            return redirect("transaction-list")

    else:

        form = TransactionForm(
            instance=transaction
        )

    return render(
        request,
        "transactions/add_transaction.html",
        {
            "form": form,
            "edit_mode": True
        }
    )


@login_required
def delete_transaction(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user
    )

    if request.method == "POST":

        transaction.delete()

        return redirect("transaction-list")

    return render(
        request,
        "transactions/delete_transaction.html",
        {
            "transaction": transaction
        }
    )