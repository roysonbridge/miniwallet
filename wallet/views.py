from django.utils import timezone
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import WalletInitSerializer,ActiveWalletSerializer,InactiveWalletSerializer,TransactionSerializer
from .models import Wallet

class WalletInitService(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self,request):
        serializer = WalletInitSerializer(data = {'id':request.data.get('customer_xid')})
        if serializer.is_valid():
            serializer.save()
            wobj = Wallet.objects.create(owned_by=serializer.instance,enabled_at=timezone.now())
            wobj.save()
            token, _ = Token.objects.get_or_create(user = serializer.instance)
            return Response({'data':{'token':token.key},'status':'success'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class WalletService(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        wallet = Wallet.objects.get(owned_by=request.user)
        serializer = ActiveWalletSerializer(wallet)
        return Response({'status':'success','data':{'wallet':serializer.data}},status=status.HTTP_200_OK)
    

    def post(self,request):
        wallet = Wallet.objects.get(owned_by=request.user)
        serializer = ActiveWalletSerializer(wallet)
        serializer.instance.enable()
        return Response({'status':'success','data':{'wallet':serializer.data}},status=status.HTTP_200_OK)

    
    def patch(self,request):
        wallet = Wallet.objects.get(owned_by=request.user)
        serializer = InactiveWalletSerializer(wallet)
        serializer.instance.disable()
        return Response({'status':'success','data':{'wallet':serializer.data}},status=status.HTTP_200_OK)


class DepositService(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        wallet = Wallet.objects.get(owned_by=request.user.id)
        transaction_data = {'by':request.user.id,'at':timezone.now(),'amount':int(request.data.get('amount')),'reference_id':request.data.get('reference_id')}
        serializer = TransactionSerializer(data=transaction_data)
        if serializer.is_valid():
            with transaction.atomic():
                deposit_status = wallet.deposit(int(request.data.get('amount')))
                serializer.save(wallet=wallet,transaction_type='CR')
                return Response({'status':'success','data':{'wallet':serializer.data}},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class WithdrawService(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        wallet = Wallet.objects.get(owned_by=request.user.id)
        transaction_data = {'by':request.user.id,'at':timezone.now(),'amount':int(request.data.get('amount')),'reference_id':request.data.get('reference_id')}
        serializer = TransactionSerializer(data=transaction_data)
        if serializer.is_valid():
            with transaction.atomic():
                withdraw_status = wallet.withdraw(int(request.data.get('amount')))
                if not withdraw_status:
                    return Response({'status':'failed','data':{'wallet':serializer.data,'message':'Insufficient fund'}},status=status.HTTP_200_OK)
                serializer.save(wallet=wallet,transaction_type='DR')
                return Response({'status':'success','data':{'wallet':serializer.data}},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

