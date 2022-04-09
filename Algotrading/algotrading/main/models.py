from django.db import models

# Create your models here.
class Transactions(models.Model):
    company_name = models.TextField()
    company_ticker = models.CharField(max_length=3)
    date = models.DateField()
    purchase_time = models.TimeField()
    purchase_cost = models.DecimalField(decimal_places=4, max_digits=15)
    selling_cost = models.DecimalField(decimal_places=4, max_digits=15)
    selling_time = models.TimeField()
    profit_loss = models.DecimalField(decimal_places=4, max_digits=15)
    volume = models.IntegerField()