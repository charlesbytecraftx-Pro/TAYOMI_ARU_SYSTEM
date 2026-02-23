from django.urls import path
from . import views

urlpatterns = [
    # Dashboard ya Malipo pekee
    path('dashboard/', views.user_dashboard, name='payment_dashboard'),
    
    path('my-payments/', views.payment_list, name='payment_list'),
    path('submit/<int:payment_id>/', views.submit_payment, name='submit_payment'),
    path('receipt/download/<int:payment_id>/', views.download_receipt, name='download_receipt'),

    # Admin Portal (Viongozi)
    path('admin/verify-payments/', views.admin_payment_list, name='admin_payment_list'),
    path('admin/confirm/<int:payment_id>/', views.confirm_payment, name='confirm_payment'),
    path('contribution/add/', views.add_contribution_type, name='add_contribution_type'),
    path('contribution/edit/<int:pk>/', views.edit_contribution_type, name='edit_contribution_type'),
    path('contribution/delete/<int:pk>/', views.delete_contribution_type, name='delete_contribution_type'),
]
