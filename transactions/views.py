from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TransactionForm
from .models import Transaction


@login_required
def transaction_list(request):

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
def add_transaction(request):

    if request.method == "POST":

        form = TransactionForm(request.POST)

        if form.is_valid():

            transaction = form.save(commit=False)

            transaction.user = request.user

            transaction.save()

            return redirect("transaction-list")

    else:

        form = TransactionForm()

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