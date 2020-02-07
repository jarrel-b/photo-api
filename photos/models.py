import os

from django.db import models

IMAGE_NOT_AVAILABLE_PATH = os.path.join("path", "to", "placeholder.png")


class Catalog(models.Model):
    def __str__(self) -> str:
        return f"{self.title}, {self.location}, {self.year}"

    title = models.CharField("name of image", max_length=50, null=True)
    location = models.CharField("location taken", max_length=50, null=True)
    year = models.IntegerField("year taken", null=True)
    path = models.CharField(
        "path to file",
        max_length=200,
        unique=False,
        null=False,
        default=IMAGE_NOT_AVAILABLE_PATH,
    )
