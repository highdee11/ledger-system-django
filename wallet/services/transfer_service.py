import enum
import uuid

from wallet.models import Wallet
from .wallet_services import WalletServices, WalletAction


class TransferServices:
    user_id = None
    sender = None
    beneficiary = None
    errorMessage = None
    walletService = WalletServices()

    def __init__(self, user_id):
        self.user_id = user_id

    def sendFrom(self, acct_id):
        result = self.walletService.getAccount(acct_id)
        if type(result) is Wallet:
            if result.user_id != self.user_id:
                raise Exception("You can only perform transaction on your account")
            self.sender = result
            return self
        else:
            raise Exception("Invalid sender account")

    def to(self, acct_id):
        result = self.walletService.getAccount(acct_id)
        if type(result) is Wallet:
            self.beneficiary = result
            return self
        else:
            raise Exception("Invalid receiver account")

    def transfer(self, amount):
        try:
            amount = float(amount)
            debit_response = self.walletService.creditDebitWallet(amount, WalletAction.DEBIT, self.sender)
            if debit_response is not None:
                return debit_response
            self.walletService.creditDebitWallet(amount, WalletAction.CREDIT, self.beneficiary)
        except:
            return "Error occurred while performing operation"
        return None
