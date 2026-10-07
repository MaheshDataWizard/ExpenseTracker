from datetime import date

from django import forms

from .models import DefaultIncome, Transaction


CATEGORY_CHOICES = [
    ("Salary", "Salary"),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        if not self.initial.get("date") and not self.data.get("date"):
            self.initial["date"] = today
        if "date" in self.fields and not self.fields["date"].initial:
            self.fields["date"].initial = today

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


# class DefaultIncomeForm(forms.ModelForm):
#     class Meta:
#         model = DefaultIncome
#         fields = [
#             "source_name",
#             "amount",
#             "category",
#             "day_of_month",
#             "description",
#             "is_active",
#         ]
#         widgets = {
#             "source_name": forms.TextInput(
#                 attrs={
#                     "class": "form-control",
#                     "placeholder": "Salary, Freelance, etc.",
#                 }
#             ),
#             "amount": forms.NumberInput(
#                 attrs={
#                     "class": "form-control",
#                     "placeholder": "Enter monthly amount",
#                     "step": "0.01",
#                     "min": "0",
#                 }
#             ),
#             "category": forms.Select(
#                 attrs={
#                     "class": "form-control",
#                     "options": CATEGORY_CHOICES,
#                 }
#             ),
#             "day_of_month": forms.NumberInput(
#                 attrs={
#                     "class": "form-control",
#                     "min": "1",
#                     "max": "31",
#                 }
#             ),
#             "description": forms.Textarea(
#                 attrs={
#                     "class": "form-control",
#                     "placeholder": "Optional note",
#                     "rows": 3,
#                 }
#             ),
#             "is_active": forms.CheckboxInput(
#                 attrs={
#                     "class": "form-check-input",
#                 }
#             ),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["category"].choices = [
#             ("Salary", "Salary"),
#             ("Freelance", "Freelance"),
#             ("Business", "Business"),
#             ("Rent", "Rent"),
#             ("Other", "Other"),
#         ]



class DefaultIncomeForm(forms.ModelForm):

    INCOME_CATEGORY_CHOICES = [
        ("Salary", "Salary"),
        ("Freelance", "Freelance"),
        ("Business", "Business Income"),
        ("Rental Income", "Rental Income"),
        ("Interest", "Interest Income"),
        ("Dividends", "Dividend Income"),
        ("Pension", "Pension"),
        ("Commission", "Commission"),
        ("Bonus", "Bonus"),
        ("Investment", "Investment Income"),
        ("Agriculture", "Agriculture Income"),
        ("Gift", "Gift"),
        ("Refund", "Refund"),
        ("Other", "Other"),
    ]

    category = forms.ChoiceField(
        choices=INCOME_CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = DefaultIncome
        fields = [
            "source_name",
            "amount",
            "category",
            "day_of_month",
            "description",
            "is_active",
        ]
        widgets = {
            "source_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Company Salary"
            }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter monthly amount",
                "step": "0.01",
                "min": "0.01",
            }),
            "day_of_month": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1",
                "max": "31",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Optional note",
                "rows": 3,
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }
