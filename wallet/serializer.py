from rest_framework import serializers


class CreditSerializer(serializers.Serializer):
    WALLET_ACTION = (
        ("credit", "credit"),
        ("debit", "debit"),
    )

    account_uuid = serializers.CharField(required=True)
    action = serializers.ChoiceField(required=True, choices=WALLET_ACTION)
    amount = serializers.DecimalField(max_digits=8, decimal_places=5, required=True)


class TransferSerializer(serializers.Serializer):
    sender_id = serializers.CharField(required=True)
    receiver_id = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=8, decimal_places=5, required=True)
