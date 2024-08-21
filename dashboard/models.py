from django.db import models

class FinancialData(models.Model):
    step = models.IntegerField()
    customer = models.CharField(max_length=255)
    # age = models.IntegerField()
    age = models.CharField(max_length=10)  # Store as string
    gender = models.CharField(max_length=10)
    zipcodeOri = models.CharField(max_length=10)
    merchant = models.CharField(max_length=255)
    zipMerchant = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    amount = models.FloatField()
    fraud = models.IntegerField()

    class Meta:
        db_table = 'financial_data'
    
    def __str__(self):
        return f"{self.customer} - {self.amount}"