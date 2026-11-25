---
name: webhook-design
description: Design reliable webhook systems with retries, idempotency, and signature verification. Outputs webhook endpoints, delivery guarantees, and security patterns.
argument-hint: [event types, delivery SLA, security requirements]
allowed-tools: Read, Write, Bash
---

# Webhook Design

Design reliable webhook delivery systems. Not fire-and-forget HTTP calls — retries, exponential backoff, signature verification, and delivery guarantees.

## Process

1. **Define events.** What triggers webhooks (order.created, payment.failed).
2. **Design payload.** JSON schema, versioning, metadata.
3. **Implement delivery.** Async queue, retry logic, exponential backoff.
4. **Add security.** HMAC signatures, IP allowlisting, HTTPS-only.
5. **Handle failures.** Dead letter queue, manual replay, alerts.
6. **Provide monitoring.** Delivery success rate, latency, retry count.
7. **Document endpoints.** Event catalog, payload examples, testing webhooks.

## Output Format

### Webhook System: [Application Name]

**Events:** 12 types (order.*, payment.*, user.*)  
**Delivery:** At-least-once with retries  
**Security:** HMAC-SHA256 signatures  
**Retry Policy:** 5 attempts, exponential backoff  
**Success Rate:** 99.5% first-attempt delivery

---

## Webhook Architecture

```
┌─────────────┐
│   Event     │ (order.created)
│  Triggers   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Webhook    │ (Format payload, sign)
│  Publisher  │
└──────┬──────┘
       │ Push to queue
       ▼
┌─────────────┐
│   Queue     │ (SQS, RabbitMQ)
│  (Async)    │
└──────┬──────┘
       │ Worker pulls
       ▼
┌─────────────┐
│  Delivery   │ (HTTP POST with retries)
│   Worker    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Subscriber │ (Customer endpoint)
│   Endpoint  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Delivery   │ (Log success/failure)
│   Logs      │
└─────────────┘
```

---

## Event Design

### Event Types (Naming Convention)
```
{resource}.{action}

Examples:
- order.created
- order.updated
- order.cancelled
- payment.succeeded
- payment.failed
- user.registered
- subscription.renewed
```

### Payload Structure
```json
{
  "event_id": "evt_1234567890",
  "event_type": "order.created",
  "created_at": "2024-03-22T10:30:00Z",
  "api_version": "2024-01-15",
  "data": {
    "object": "order",
    "id": "ord_abc123",
    "customer_id": "cust_xyz789",
    "total": 99.99,
    "currency": "USD",
    "status": "pending",
    "items": [
      {
        "product_id": "prod_123",
        "quantity": 2,
        "price": 49.99
      }
    ],
    "created_at": "2024-03-22T10:30:00Z"
  },
  "previous_attributes": null  // For *.updated events
}
```

---

## Webhook Publisher

```python
import hmac
import hashlib
import json
import requests
from datetime import datetime

class WebhookPublisher:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def publish_event(self, event_type, data, subscriber_url):
        """Publish webhook event to subscriber"""
        
        # Build payload
        payload = {
            "event_id": generate_event_id(),
            "event_type": event_type,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "api_version": "2024-01-15",
            "data": data
        }
        
        # Sign payload
        signature = self.generate_signature(payload)
        
        # Send to queue (async delivery)
        queue.send_message({
            "payload": payload,
            "subscriber_url": subscriber_url,
            "signature": signature,
            "attempt": 0
        })
    
    def generate_signature(self, payload):
        """Generate HMAC signature for payload"""
        
        payload_str = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            self.secret_key.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return signature

# Usage
publisher = WebhookPublisher(secret_key="your-secret-key")

# Publish order.created event
publisher.publish_event(
    event_type="order.created",
    data={
        "id": "ord_abc123",
        "total": 99.99,
        "status": "pending"
    },
    subscriber_url="https://customer.com/webhooks"
)
```

---

## Delivery Worker

```python
import time
import requests
from exponential_backoff import ExponentialBackoff

class WebhookDeliveryWorker:
    def __init__(self, max_retries=5):
        self.max_retries = max_retries
        self.backoff = ExponentialBackoff(base=2, max_delay=3600)
    
    def deliver_webhook(self, message):
        """Deliver webhook with retries"""
        
        payload = message['payload']
        url = message['subscriber_url']
        signature = message['signature']
        attempt = message['attempt']
        
        headers = {
            'Content-Type': 'application/json',
            'X-Webhook-Signature': signature,
            'X-Event-ID': payload['event_id'],
            'X-Event-Type': payload['event_type']
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                # Success
                log_delivery_success(payload['event_id'], attempt)
                return True
            
            elif response.status_code >= 500:
                # Server error - retry
                raise DeliveryError(f"HTTP {response.status_code}")
            
            else:
                # Client error (4xx) - don't retry
                log_delivery_failure(
                    payload['event_id'],
                    f"HTTP {response.status_code}",
                    final=True
                )
                return False
        
        except requests.exceptions.RequestException as e:
            # Network error - retry
            raise DeliveryError(str(e))
    
    def process_message(self, message):
        """Process webhook delivery with retries"""
        
        attempt = message['attempt']
        
        try:
            success = self.deliver_webhook(message)
            
            if success:
                # Remove from queue
                queue.delete_message(message)
            
        except DeliveryError as e:
            attempt += 1
            
            if attempt >= self.max_retries:
                # Move to dead letter queue
                dead_letter_queue.send_message(message)
                queue.delete_message(message)
                log_delivery_failure(message['payload']['event_id'], str(e), final=True)
            
            else:
                # Retry with backoff
                delay = self.backoff.calculate(attempt)
                
                message['attempt'] = attempt
                queue.send_message(message, delay_seconds=delay)
                queue.delete_message(message)  # Remove original
                
                log_retry_scheduled(message['payload']['event_id'], attempt, delay)

# Worker loop
worker = WebhookDeliveryWorker(max_retries=5)

while True:
    messages = queue.receive_messages()
    
    for message in messages:
        worker.process_message(message)
```

---

## Retry Policy

### Exponential Backoff
```
Attempt 1: Immediate
Attempt 2: 2^1 = 2 seconds
Attempt 3: 2^2 = 4 seconds
Attempt 4: 2^3 = 8 seconds
Attempt 5: 2^4 = 16 seconds

Total time: ~30 seconds
```

```python
class ExponentialBackoff:
    def __init__(self, base=2, max_delay=3600):
        self.base = base
        self.max_delay = max_delay
    
    def calculate(self, attempt):
        """Calculate delay for retry attempt"""
        delay = min(self.base ** attempt, self.max_delay)
        
        # Add jitter (±20%) to prevent thundering herd
        jitter = delay * 0.2 * (random.random() - 0.5)
        
        return delay + jitter
```

---

## Signature Verification (Subscriber)

```python
import hmac
import hashlib
import json

def verify_webhook_signature(payload, signature, secret):
    """Verify webhook signature"""
    
    # Recreate signature
    payload_str = json.dumps(payload, sort_keys=True)
    expected_signature = hmac.new(
        secret.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Constant-time comparison (prevent timing attacks)
    return hmac.compare_digest(signature, expected_signature)

# Express.js webhook endpoint
@app.post('/webhooks')
def receive_webhook():
    payload = request.json
    signature = request.headers.get('X-Webhook-Signature')
    
    # Verify signature
    if not verify_webhook_signature(payload, signature, SECRET_KEY):
        return {'error': 'Invalid signature'}, 401
    
    # Process event
    event_type = payload['event_type']
    
    if event_type == 'order.created':
        handle_order_created(payload['data'])
    elif event_type == 'payment.succeeded':
        handle_payment_succeeded(payload['data'])
    
    # Return 200 immediately (process async)
    return {'received': True}, 200
```

---

## Idempotency

### Event ID Deduplication
```python
# Subscriber tracks processed events
processed_events = set()  # Or Redis set

@app.post('/webhooks')
def receive_webhook():
    payload = request.json
    event_id = payload['event_id']
    
    # Check if already processed
    if event_id in processed_events:
        # Idempotent - return success
        return {'received': True, 'status': 'duplicate'}, 200
    
    # Process event
    handle_event(payload)
    
    # Mark as processed
    processed_events.add(event_id)
    redis.setex(f"event:{event_id}", 86400, "processed")  # 24h TTL
    
    return {'received': True}, 200
```

---

## Webhook Management API

### Subscribe to Webhooks
```http
POST /webhook-subscriptions
Content-Type: application/json

{
  "url": "https://customer.com/webhooks",
  "events": ["order.created", "order.updated"],
  "description": "Production webhook endpoint"
}

Response:
{
  "id": "sub_abc123",
  "url": "https://customer.com/webhooks",
  "events": ["order.created", "order.updated"],
  "secret": "whsec_xyz789...",  // Use for signature verification
  "status": "active",
  "created_at": "2024-03-22T10:30:00Z"
}
```

### List Subscriptions
```http
GET /webhook-subscriptions

Response:
{
  "data": [
    {
      "id": "sub_abc123",
      "url": "https://customer.com/webhooks",
      "events": ["order.created", "order.updated"],
      "status": "active"
    }
  ]
}
```

### Update Subscription
```http
PATCH /webhook-subscriptions/sub_abc123

{
  "events": ["order.*", "payment.*"]
}
```

### Delete Subscription
```http
DELETE /webhook-subscriptions/sub_abc123
```

---

## Webhook Event Log

```sql
CREATE TABLE webhook_deliveries (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    subscription_id VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    payload JSONB NOT NULL,
    attempts INT DEFAULT 0,
    status VARCHAR(20) NOT NULL,  -- pending, succeeded, failed
    response_code INT,
    response_body TEXT,
    delivered_at TIMESTAMP,
    failed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_event_id (event_id),
    INDEX idx_subscription (subscription_id),
    INDEX idx_status (status)
);
```

```python
def log_delivery_success(event_id, attempt):
    """Log successful delivery"""
    db.execute("""
        UPDATE webhook_deliveries
        SET status = 'succeeded',
            attempts = %s,
            delivered_at = NOW()
        WHERE event_id = %s
    """, (attempt + 1, event_id))

def log_delivery_failure(event_id, error, final=False):
    """Log delivery failure"""
    if final:
        db.execute("""
            UPDATE webhook_deliveries
            SET status = 'failed',
                failed_at = NOW(),
                response_body = %s
            WHERE event_id = %s
        """, (error, event_id))
```

---

## Testing Webhooks

### Webhook Simulator
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/test-webhook', methods=['POST'])
def test_webhook():
    """Test webhook endpoint"""
    
    print(f"Headers: {request.headers}")
    print(f"Body: {request.json}")
    
    # Verify signature
    signature = request.headers.get('X-Webhook-Signature')
    if verify_webhook_signature(request.json, signature, SECRET):
        print("✅ Signature valid")
    else:
        print("❌ Signature invalid")
    
    # Return success
    return {'received': True}, 200

app.run(port=5000)
```

### Webhook Testing Service (Webhook.site alternative)
```python
# Expose local endpoint for testing
ngrok http 5000

# Your local webhook endpoint now accessible at:
# https://abc123.ngrok.io/test-webhook
```

---

## Monitoring

```python
from prometheus_client import Counter, Histogram

webhook_deliveries_total = Counter(
    'webhook_deliveries_total',
    'Total webhook deliveries',
    ['event_type', 'status']
)

webhook_delivery_duration = Histogram(
    'webhook_delivery_duration_seconds',
    'Webhook delivery duration',
    ['event_type']
)

def deliver_webhook(message):
    event_type = message['payload']['event_type']
    
    with webhook_delivery_duration.labels(event_type=event_type).time():
        try:
            response = requests.post(...)
            
            if response.status_code == 200:
                webhook_deliveries_total.labels(
                    event_type=event_type,
                    status='success'
                ).inc()
            else:
                webhook_deliveries_total.labels(
                    event_type=event_type,
                    status='failure'
                ).inc()
        
        except Exception:
            webhook_deliveries_total.labels(
                event_type=event_type,
                status='error'
            ).inc()
```

---

## Security Best Practices

### HTTPS Only
```python
def validate_subscriber_url(url):
    """Ensure webhook URL is HTTPS"""
    if not url.startswith('https://'):
        raise ValueError("Webhook URL must use HTTPS")
```

### IP Allowlisting
```python
ALLOWED_IPS = ['203.0.113.1', '203.0.113.2']

@app.before_request
def check_ip():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)
```

### Rate Limiting (Subscriber)
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/webhooks', methods=['POST'])
@limiter.limit("100/minute")
def receive_webhook():
    ...
```

## Rules

- Sign every webhook with HMAC-SHA256 — prevents tampering and spoofing.
- Include event_id in payload — enables idempotent processing on subscriber side.
- Retry with exponential backoff — 5 attempts over ~30 seconds handles transient failures.
- Return 200 immediately, process async — don't block webhook delivery on slow processing.
- HTTPS-only for subscriber URLs — no plaintext transmission of sensitive data.
- Use queues for delivery — decouples event generation from delivery, enables retries.
- Log all delivery attempts — critical for debugging failed deliveries.
- Dead letter queue after max retries — manual review of persistent failures.
- Don't retry 4xx errors — client errors won't be fixed by retrying.
- Provide webhook testing endpoint — subscribers need way to verify integration before production.
