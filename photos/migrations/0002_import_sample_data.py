import os
import random

from django.db import migrations, transaction

CATALOG_SIZE = 100
LOCATIONS = ["Los Angeles", "New York", "Paris", "London"]


def import_sample_data(apps, schema_editor):
    Catalog = apps.get_model("photos", "Catalog")
    with transaction.atomic():
        for i in range(CATALOG_SIZE):
            item = Catalog(
                title=f"Photo{i}",
                location=random.choice(LOCATIONS),
                year=random.randrange(1923, 2010),
                path=os.path.join("path", "to", "file", f"{i}.png"),
            )
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ("photos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(import_sample_data),
    ]
