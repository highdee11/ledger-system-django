from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CreditSerializer, TransferSerializer
from .services.wallet_services import WalletServices, WalletAction
from .services.transfer_service import TransferServices
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.authtoken.models import Token

class WalletView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request):
        return Response({
            'balance': WalletServices(request.GET.get('account'), request.user.id).getBalance()
        })

    def post(self, request):
        serializer = CreditSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors})

        data = serializer.data
        account_id = data.get('account_uuid')
        amount = data.get('amount')
        action = data.get('action')

        walletService = WalletServices(account_id, request.user.id)
        result = walletService.creditDebitWallet(amount, WalletAction[action.upper()])
        if result is not None:
            return Response({
                'status': False,
                'message': result
            }, status=400)

        print(request.data)
        return Response({
            'status': True,
            'message': action+" was successful",
            'account_balance': walletService.getBalance()
        })


class TransferView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors})

        data = serializer.data
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        amount = data.get('amount')

        try:
            transfer_response = TransferServices(request.user.id) \
                .sendFrom(sender_id) \
                .to(receiver_id) \
                .transfer(amount)

            if transfer_response is not None:
                raise Exception(transfer_response)
        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            }, status=400)

        return Response({
            'status': True,
            'message': "Transfer successful",
        })