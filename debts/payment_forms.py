from django import forms

from .models import DebtPayment


class DebtPaymentForm(forms.ModelForm):

    class Meta:

        model = DebtPayment

        fields = [
            "amount",
            "date",
            "payment_method",
            "notes",
        ]

        widgets = {

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Repayment amount",
                    "step": "0.01",
                    "min": "0.01"
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional notes",
                    "rows": 3
                }
            ),
        }