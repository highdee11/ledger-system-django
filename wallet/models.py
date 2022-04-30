import uuid

from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    STATUSES = (
        ("ACTIVE", "Active"),
        ("BLOCKED", "Blocked")
    )

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wallet")
    balance = models.FloatField(default=0)
    status = models.CharField(choices=STATUSES, null=False, default="ACTIVE", max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid) + "(" + str(self.balance) + ")"
