---
name: payment-integration
description: |
  Payment system integration for Uzbekistan market (Payme, Click, Uzum) and international.
  Apply when implementing payment flows, webhooks, order status management, or refunds.
  Covers webhook signature verification, idempotency, transaction logging, and test mode.
---

# Payment Integration (UZ Market)

## Payme Integration
```python
import hashlib, hmac

class PaymeService:
    def __init__(self):
        self.merchant_id = settings.PAYME_MERCHANT_ID
        self.secret_key = settings.PAYME_SECRET_KEY
        self.test_mode = settings.PAYME_TEST_MODE
        self.base_url = "https://checkout.paycom.uz" if not self.test_mode else "https://test.paycom.uz"

    def create_payment_url(self, order_id: str, amount_tiyins: int, return_url: str) -> str:
        """Amount must be in TIYINS (sum * 100)"""
        params = {
            "m": self.merchant_id,
            "ac.order_id": order_id,
            "a": amount_tiyins,
            "l": "uz",
            "c": return_url,
        }
        encoded = base64.b64encode(
            "&".join(f"{k}={v}" for k, v in params.items()).encode()
        ).decode()
        return f"{self.base_url}/{encoded}"

    def verify_webhook(self, auth_header: str) -> bool:
        if not auth_header.startswith("Basic "):
            return False
        credentials = base64.b64decode(auth_header[6:]).decode()
        _, password = credentials.split(":", 1)
        return password == self.secret_key

    def handle_webhook(self, method: str, params: dict) -> dict:
        handlers = {
            "CheckPerformTransaction": self._check_perform,
            "CreateTransaction": self._create_transaction,
            "PerformTransaction": self._perform_transaction,
            "CancelTransaction": self._cancel_transaction,
            "CheckTransaction": self._check_transaction,
        }
        handler = handlers.get(method)
        if not handler:
            return {"error": {"code": -32601, "message": "Method not found"}}
        return handler(params)

    def _perform_transaction(self, params: dict) -> dict:
        transaction_id = params["id"]
        transaction = Transaction.objects.get(payme_id=transaction_id)
        transaction.status = "paid"
        transaction.save()
        order = transaction.order
        order.payment_status = "paid"
        order.status = "processing"
        order.save()
        # Trigger fulfillment
        process_order.delay(order.id)
        return {"result": {"transaction": transaction_id, "perform_time": int(time.time() * 1000), "state": 2}}
```

## Click Integration
```python
class ClickService:
    def verify_signature(self, params: dict) -> bool:
        sign_string = (f"{params['click_trans_id']}{params['service_id']}"
                      f"{settings.CLICK_SECRET_KEY}{params['merchant_trans_id']}"
                      f"{params['amount']}{params['action']}{params['sign_time']}")
        expected = hashlib.md5(sign_string.encode()).hexdigest()
        return expected == params['sign_string']

    def prepare(self, params: dict) -> dict:
        if not self.verify_signature(params):
            return {"error": -1, "error_note": "Invalid signature"}
        order = Order.objects.get(id=params['merchant_trans_id'])
        if abs(float(params['amount']) - float(order.total)) > 0.01:
            return {"error": -2, "error_note": "Wrong amount"}
        return {"error": 0, "click_trans_id": params['click_trans_id'], "merchant_trans_id": order.id}
```

## Transaction Model
```python
class Transaction(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='transaction')
    provider = models.CharField(max_length=20, choices=[('payme','Payme'),('click','Click'),('uzum','Uzum')])
    provider_transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default='pending',
        choices=[('pending','Pending'),('paid','Paid'),('cancelled','Cancelled'),('refunded','Refunded')])
    raw_request = models.JSONField(default=dict)   # Always log raw provider data
    raw_response = models.JSONField(default=dict)
    paid_at = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['provider', 'provider_transaction_id']),
            models.Index(fields=['status', 'created_at']),
        ]
```
