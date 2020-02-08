from django.forms import ModelForm

from .models import Orders


class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = [
            "first_name",
            "last_name",
            "email",
            "primary_phone",
            "address_line_one",
            "address_line_two",
            "city",
            "state_or_region",
            "postal_code",
            "country",
            "print_id",
            "photo_id",
        ]
