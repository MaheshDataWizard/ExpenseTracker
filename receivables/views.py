from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import ReceivableForm
from .models import Receivable
from .payment_forms import ReceivablePaymentForm


@login_required
def receivable_list(request):

    receivables = Receivable.objects.filter(
        user=request.user
    ).order_by(
        "-date",
        "-created_at"
    )

    total_remaining = sum(
        item.remaining_amount
        for item in receivables
    )

    return render(
        request,
        "receivables/receivable_list.html",
        {
            "receivables": receivables,
            "total_remaining": total_remaining,
        }
    )


@login_required
def add_receivable(request):

    if request.method == "POST":

        form = ReceivableForm(request.POST)

        if form.is_valid():

            receivable = form.save(
                commit=False
            )

            receivable.user = request.user

            receivable.received_amount = 0

            receivable.status = "pending"

            receivable.save()

            messages.success(
                request,
                "Receivable added successfully."
            )

            return redirect(
                "receivable-list"
            )

    else:

        form = ReceivableForm()

    return render(
        request,
        "receivables/add_receivable.html",
        {
            "form": form
        }
    )


@login_required
def receive_payment(
    request,
    receivable_id
):

    receivable = get_object_or_404(
        Receivable,
        id=receivable_id,
        user=request.user
    )

    if receivable.remaining_amount <= 0:

        messages.info(
            request,
            "This receivable is already fully received."
        )

        return redirect(
            "receivable-list"
        )

    if request.method == "POST":

        form = ReceivablePaymentForm(
            request.POST
        )

        if form.is_valid():

            payment = form.save(
                commit=False
            )

            if (
                payment.amount
                > receivable.remaining_amount
            ):

                form.add_error(
                    "amount",
                    "Amount cannot be greater than the remaining receivable."
                )

            else:

                payment.receivable = receivable

                payment.save()

                receivable.received_amount += (
                    payment.amount
                )

                receivable.update_status()

                messages.success(
                    request,
                    "Payment received successfully."
                )

                return redirect(
                    "receivable-detail",
                    receivable_id=receivable.id
                )

    else:

        form = ReceivablePaymentForm()

    return render(
        request,
        "receivables/receive_payment.html",
        {
            "form": form,
            "receivable": receivable
        }
    )


@login_required
def receivable_detail(
    request,
    receivable_id
):

    receivable = get_object_or_404(
        Receivable,
        id=receivable_id,
        user=request.user
    )

    payments = (
        receivable.payments.all()
        .order_by(
            "-date",
            "-created_at"
        )
    )

    return render(
        request,
        "receivables/receivable_detail.html",
        {
            "receivable": receivable,
            "payments": payments
        }
    )