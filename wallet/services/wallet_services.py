import enum
import uuid

from wallet.models import Wallet
from django.db.models import Sum


class WalletAction(enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class WalletServices:
    wallet = None
    user_id = None
    errorMessage = None

    def __init__(self, acct_id=None, user_id=None):
        self.user_id = user_id
        if acct_id is not None:
            result = self.getAccount(acct_id)
            if type(result) is Wallet:
                if result.user_id != user_id:
                    self.errorMessage = "You can only perform operations on your account"
                self.wallet = result
            else:
                self.errorMessage = result

    def getAccount(self, acct_id):
        try:
            wallet = Wallet.objects.get(uuid=uuid.UUID(acct_id))
            if wallet.status != "ACTIVE":
                raise Exception("No operation is allowed on this wallet")
            return wallet
        except ValueError as e:
            return "Unable to retrieve wallet"
        except Exception as e:
            print(e)
            return str(e)

    def getBalance(self):
        if self.errorMessage is not None:
            return self.errorMessage
        total = 0
        if self.wallet is None:
            total = Wallet.objects.filter(user_id=self.user_id).aggregate(total=Sum('balance'))['total']
        else:
            total = self.wallet.balance
        return total

    def creditDebitWallet(self, amount, action, wallet=None):
        if self.errorMessage is not None:
            return self.errorMessage

        if wallet is not None:
            self.wallet = wallet

        try:
            amount = float(amount)

            if action is WalletAction.CREDIT:
                self.wallet.balance += amount

            elif action == WalletAction.DEBIT:
                if self.wallet.balance < amount:
                    return "Insufficient balance"
                self.wallet.balance -= amount
            else:
                return "Unknown operation"
            self.wallet.save()

        except Exception as e:
            print(e)
            return "Error occurred while performing operation"
        return None
