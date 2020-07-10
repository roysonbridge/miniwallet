import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

TTYPE = [('CR', 'Credit'),('DR', 'Debit')]

class Customer(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    owned_by = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)
    status  = models.BooleanField(default=True)
    enabled_at = models.DateTimeField(null=True)
    disabled_at = models.DateTimeField(null=True)

    def deposit(self,value):
        self.balance += value
        self.save()
        return True

    def withdraw(self,value):
        if value > self.balance or self.balance < 1:
            return False

        self.balance -= value
        self.save()
        return True
    
    def enable(self):
        self.status = True
        self.enabled_at = timezone.now()
        self.save()
        return self.status

    def disable(self):
        self.status = False
        self.disabled_at = timezone.now()
        self.save()
        return self.status

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    by = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=2, choices=TTYPE)
    reference_id = models.CharField(max_length=100,unique = True)
    amount = models.FloatField()
    at = models.DateTimeField()
