from rest_framework import serializers
from .models import Profile, Account, DepositTransaction, TransferTransaction

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'

class DepositTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepositTransaction
        fields = '__all__'


class TransferTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransferTransaction
        fields = '__all__'
