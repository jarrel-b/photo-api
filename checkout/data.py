from django.core.exceptions import ValidationError

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def format_address(form) -> str:
    if not form.address_line_one:
        raise ValidationError(
            "Address field can not be empty.", code="invalid",
        )
    return " ".join(
        i for i in (form.address_line_one, form.address_line_two) if i
    )


def process_order(form):
    if form.is_valid():
        saved_form = form.save(commit=True)
    else:
        raise ValidationError(
            "Order form is invalid. Reason: %(errors)s",
            code="invalid",
            params={"errors": form.errors},
        )
    details = {
        "id": saved_form.id,
        "status": saved_form.status,
        "placed_on": saved_form.time_placed.strftime(DATETIME_FORMAT),
        "items_ordered": [
            {
                "title": saved_form.photo_id.title,
                "size": saved_form.print_id.size,
            }
        ],
        "shipping_summary": {
            "ship_to": " ".join([saved_form.first_name, saved_form.last_name]),
            "email": saved_form.email,
            "phone": saved_form.primary_phone,
            "address": format_address(saved_form),
            "city": saved_form.city,
            "state_or_region": saved_form.state_or_region,
            "postal_code": saved_form.postal_code,
            "country": saved_form.country,
        },
        "billing_summary": {
            "order_total": float(saved_form.print_id.total_cost()),
            "shipping_total": float(saved_form.print_id.shipping_cost),
            "item_total": float(saved_form.print_id.print_cost),
        },
    }
    return details
