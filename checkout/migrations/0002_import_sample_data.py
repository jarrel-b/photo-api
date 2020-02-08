from django.db import migrations, transaction

SIZE_TO_COST = {
    "sml": (10.00, 4.99),
    "med": (15.00, 5.99),
    "lrg": (20.00, 7.99),
}


def import_sample_data(apps, schema_editor):
    Prints = apps.get_model("checkout", "Prints")
    with transaction.atomic():
        for size, (print_cost, shipping_cost) in SIZE_TO_COST.items():
            item = Prints(
                size=size, print_cost=print_cost, shipping_cost=shipping_cost,
            )
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(import_sample_data),
    ]
