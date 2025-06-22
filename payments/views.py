# payments/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.timezone import now
from .models import Payment
from .utils import generate_click_payment_url, generate_qr_code
from django.conf import settings
import hashlib


def index_view(request):
    order_id = "test_order"
    amount = 15000.0
    payment, _ = Payment.objects.get_or_create(order_id=order_id, defaults={"amount": amount})
    return redirect('prepare', order_id=order_id)


def prepare_view(request, order_id):
    # Mock mode — no external API call
    payment = get_object_or_404(Payment, order_id=order_id)
    # Simulate success response without calling Click
    return redirect('pay', order_id=order_id)


def pay_view(request, order_id):
    payment = get_object_or_404(Payment, order_id=order_id)
    pay_url = generate_click_payment_url(payment.order_id, float(payment.amount))
    qr_image = generate_qr_code(pay_url)
    return render(request, 'pay.html', {'pay_url': pay_url, 'qr_code': qr_image})


@csrf_exempt
def callback_view(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    data = request.POST

    try:
        click_trans_id = data['click_trans_id']
        service_id = data['service_id']
        order_id = data['merchant_trans_id']
        amount = float(data['amount'])
        action = data['action']
        sign_time = data['sign_time']
        sign_string = data['sign_string']
    except KeyError:
        return HttpResponseBadRequest('Missing required parameters')

    try:
        payment = Payment.objects.get(order_id=order_id)
    except Payment.DoesNotExist:
        return HttpResponseBadRequest('Payment not found')

    if payment.amount != amount:
        return HttpResponseBadRequest('Amount mismatch')

    expected_sign = hashlib.md5(
        f"{click_trans_id}{service_id}{settings.CLICK_SECRET_KEY}{order_id}{amount}{action}{sign_time}".encode()
    ).hexdigest()

    if sign_string != expected_sign:
        return HttpResponseBadRequest('Invalid signature')

    payment.is_paid = True
    payment.paid_at = now()
    payment.save()

    return JsonResponse({'success': True})
