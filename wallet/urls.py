from django.urls import path
from .views import *

urlpatterns = [
	path('init',WalletInitService.as_view()),
    path('wallet',WalletService.as_view()),
    path('wallet/deposits',DepositService.as_view()),
    path('wallet/withdrawals',WithdrawService.as_view()),
]