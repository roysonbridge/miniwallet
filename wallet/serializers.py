from rest_framework import serializers
from .models import Customer,Wallet,Transaction

class WalletInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id']

class ActiveWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id','owned_by','status','balance','enabled_at']

class InactiveWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id','owned_by','status','balance','disabled_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id','by','at','amount','reference_id']

