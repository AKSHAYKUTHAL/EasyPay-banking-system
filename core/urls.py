from django.urls import path
from core import views,transfer,transaction,payment_request


app_name = "core"

urlpatterns = [
    path('',views.index,name='index'),

    #Transfers
    path('search_account/',transfer.search_users_account_number,name='search_account'),
    path('amount_transfer/<account_number>/',transfer.amount_transfer,name='amount_transfer'),
    path('amount_transfer_process/<account_number>/',transfer.amount_transfer_process,name='amount_transfer_process'),
    path('transfer_confirmation/<account_number>/<transaction_id>/',transfer.transfer_confirmation,name='transfer_confirmation'),
    path('transfer_process/<account_number>/<transaction_id>/',transfer.transfer_process,name='transfer_process'),
    path('transfer_completed/<account_number>/<transaction_id>/',transfer.transfer_completed,name='transfer_completed'),
    
    # Transactions
    path('transactions/',transaction.transaction_list,name='transactions'),
    path('transaction_detail_sent/<transaction_id>/',transaction.transaction_detail_sent,name='transaction_detail_sent'),
    path('transaction_detail_received/<transaction_id>/',transaction.transaction_detail_received,name='transaction_detail_received'),

    # payment request
    path('request_payment_search_account/',payment_request.request_payment_search_account,name='request_payment_search_account'),
    path('amount_request/<account_number>/',payment_request.amount_request,name='amount_request'),
    path('amount_request_process/<account_number>/',payment_request.amount_request_process,name='amount_request_process'),
    path('amount_request_confirmation/<account_number>/<transaction_id>/',payment_request.amount_request_confirmation,name='amount_request_confirmation'),
    path('amount_request_final_process/<account_number>/<transaction_id>/',payment_request.amount_request_final_process,name='amount_request_final_process'),
    path('amount_request_completed/<account_number>/<transaction_id>/',payment_request.amount_request_completed,name='amount_request_completed'),
    path('request_details_sent/<transaction_id>/',payment_request.request_details_sent,name='request_details_sent'),
    path('request_details_received/<transaction_id>/',payment_request.request_details_received,name='request_details_received'),

    # request settlement confirmation

    path('request_settlement_confirmation/<account_number>/<transaction_id>/',payment_request.request_settlement_confirmation,name='request_settlement_confirmation'),
    path('request_settlement_processing/<account_number>/<transaction_id>/',payment_request.request_settlement_processing,name='request_settlement_processing'),
    path('request_settlement_completed/<account_number>/<transaction_id>/',payment_request.request_settlement_completed,name='request_settlement_completed'),


]
