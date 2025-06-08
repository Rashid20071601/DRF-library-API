from django.db import models
from django.forms import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product'),
        ]

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Количество должно быть больше 0.'})

    def __str__(self):
        return f"{self.user} - {self.product.name} x {self.quantity}"