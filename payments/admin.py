from django.contrib import admin
from .models import Payment
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'amount', 'is_paid', 'created_at', 'paid_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('order_id',)