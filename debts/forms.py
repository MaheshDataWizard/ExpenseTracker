from django import forms

from .models import Debt


class DebtForm(forms.ModelForm):

    class Meta:

        model = Debt

        fields = [
            "person_name",
            "borrowed_amount",
            "date",
            "notes",
        ]

        widgets = {

            "person_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Person name"
                }
            ),

            "borrowed_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter amount",
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

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional notes",
                    "rows": 3
                }
            ),
        }