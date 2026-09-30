from django import forms

from .models import Receivable


class ReceivableForm(forms.ModelForm):

    class Meta:

        model = Receivable

        fields = [
            "person_name",
            "amount",
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

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Amount to receive",
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