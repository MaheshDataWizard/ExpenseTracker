from django import forms

from .models import Transaction


CATEGORY_CHOICES = [
    ("Petrol", "Petrol"),
    ("Recharge", "Recharge"),
    ("Insurance", "Insurance"),
    ("Light Bill", "Light Bill"),
    ("Food", "Food"),
    ("Travel", "Travel"),
    ("Shopping", "Shopping"),
    ("Medical", "Medical"),
    ("Rent", "Rent"),
    ("Entertainment", "Entertainment"),
    ("Other", "Other"),
]


class TransactionForm(forms.ModelForm):

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:

        model = Transaction

        fields = [
            "transaction_type",
            "category",
            "amount",
            "date",
            "payment_method",
            "description",
        ]

        widgets = {

            "transaction_type": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter amount",
                    "step": "0.01",
                    "min": "0"
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

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional description",
                    "rows": 3
                }
            ),
        }