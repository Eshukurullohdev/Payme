# payments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('pay/<str:order_id>/', views.pay_view, name='pay'),
    path('', views.index_view, name='index'),
    path('prepare/<str:order_id>/', views.prepare_view, name='prepare'),
    path('pay/<str:order_id>/', views.pay_view, name='pay'),
    path('callback/', views.callback_view, name='callback'),
]
