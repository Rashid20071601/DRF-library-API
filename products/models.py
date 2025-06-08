from django.db import models


class Product(models.Model):
    """
    Модель товара для каталога интернет-магазина.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)


    # Представление модели в виде строки для удобства отображения в админке
    def __str__(self):
        return self.name