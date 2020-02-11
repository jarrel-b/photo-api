import enum
import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

US_PHONE_REGEX = r"(\+1\s)?[2-9][0-9]{2}-[2-9][0-9]{2}-[0-9]{4}"


class Statuses(enum.Enum):
    CREATED = "created"
    PENDING = "pending"
    FULFILLED = "fulfilled"
    REJECTED = "rejected"


class Prints(models.Model):
    def __str__(self) -> str:
        return (
            f"{self.size} "
            f"print cost: {self.print_cost} "
            f"shipping cost: {self.shipping_cost}"
        )

    sizes = [("sml", "Small"), ("med", "Medium"), ("lrg", "large")]
    size = models.CharField(max_length=10, choices=sizes)
    print_cost = models.DecimalField(max_digits=5, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=5, decimal_places=2)

    def total_cost(self):
        return self.print_cost + self.shipping_cost


def generate_uuid():
    return uuid.uuid4()


def generate_now():
    return timezone.now()


class Orders(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False
    )
    time_placed = models.DateTimeField(auto_now_add=True, default=generate_now)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    primary_phone = models.CharField(
        max_length=20, validators=[RegexValidator(regex=US_PHONE_REGEX)],
    )
    address_line_one = models.CharField(max_length=100)
    address_line_two = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20)
    state_or_region = models.CharField(max_length=20)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=3)
    print_id = models.ForeignKey("Prints", on_delete=models.PROTECT)
    photo_id = models.ForeignKey("photos.Catalog", on_delete=models.PROTECT)
    status = models.CharField(
        max_length=10,
        choices=[(s.value, s.value) for s in Statuses],
        default=Statuses.CREATED.value,
    )
