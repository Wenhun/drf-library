from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        SOFT = "soft"
        HARD = "hard"

    title = models.CharField(max_length=255)
    author = models.ManyToManyField(
        Author, on_delete=models.SET_NULL, null=True, blank=True
    )
    cover = models.CharField(
        max_length=10, choices=CoverChoices.choices, default=CoverChoices.HARD
    )
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = models.DecimalField(default=0)

    def __str__(self) -> str:
        return (
            f"Book {self.title} has price {self.daily_fee}. Inventory {self.inventory}"
        )
