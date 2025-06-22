# payments/utils.py

import hashlib
import urllib.parse
import qrcode
import base64
from io import BytesIO
from django.conf import settings
from datetime import datetime

def generate_click_payment_url(order_id: str, amount: float) -> str:
    base_url = settings.CLICK_ENDPOINT
    sign_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    action = 0
    params = {
        "merchant_id": settings.CLICK_MERCHANT_ID,
        "merchant_user_id": settings.CLICK_MERCHANT_USER_ID,
        "amount": amount,
        "transaction_param": order_id,
        "action": action,
        "sign_time": sign_time,
    }
    sign_string = f"{settings.CLICK_MERCHANT_ID}{order_id}{amount}{action}{sign_time}{settings.CLICK_SECRET_KEY}"
    sign_hash = hashlib.md5(sign_string.encode()).hexdigest()
    params["sign"] = sign_hash
    full_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return full_url

def generate_qr_code(data: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_base64}"
