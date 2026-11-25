---
name: idempotency-design
description: Design idempotent APIs and operations. Outputs idempotency keys, deduplication strategies, and retry-safe implementations.
argument-hint: [operation type, reliability requirements, distributed system]
allowed-tools: Read, Write, Bash
---

# Idempotency Design

Design idempotent operations that can be safely retried. Not hope-for-the-best — guaranteed same result regardless of retry count, preventing duplicate charges, double bookings, and data corruption.

## Process

1. **Identify non-idempotent operations.** POST requests, payments, state changes.
2. **Add idempotency keys.** Client-generated unique ID per operation.
3. **Implement deduplication.** Store processed keys, reject duplicates.
4. **Design retry logic.** Exponential backoff, max retries, timeout.
5. **Handle partial failures.** Rollback or complete incomplete operations.
6. **Add logging.** Track retries, deduplications, completion status.
7. **Test edge cases.** Concurrent requests, network failures, crashes.

## Output Format

### Idempotency Implementation: [API/Operation]

**Method:** Idempotency keys (client-generated)  
**Storage:** Redis with 24-hour TTL  
**Protected Operations:** Payments, order creation, email sends  
**Retry Policy:** Exponential backoff, max 3 retries  
**Concurrency:** Distributed locks prevent race conditions

---

## Problem: Non-Idempotent Operations

###Without Idempotency
```
Client sends: POST /orders {amount: 100}
Network timeout (request succeeds on server)
Client retries: POST /orders {amount: 100}
Result: TWO orders created, customer charged twice ❌
```

### With Idempotency
```
Client sends: POST /orders {amount: 100}
Header: Idempotency-Key: uuid-12345
Network timeout (request succeeds on server)
Client retries: POST /orders {amount: 100}
Header: Idempotency-Key: uuid-12345
Server: "Already processed, returning cached response"
Result: ONE order created ✅
```

---

## Idempotency Keys

### Client-Generated UUID
```python
import uuid
import requests

def create_order(amount):
    # Generate idempotency key
    idempotency_key = str(uuid.uuid4())
    
    response = requests.post(
        'https://api.example.com/orders',
        json={'amount': amount},
        headers={'Idempotency-Key': idempotency_key}
    )
    
    # Retry with SAME key on failure
    if response.status_code == 500:
        response = requests.post(
            'https://api.example.com/orders',
            json={'amount': amount},
            headers={'Idempotency-Key': idempotency_key}  # Same key!
        )
    
    return response.json()
```

### Server Implementation
```python
from flask import Flask, request, jsonify
import redis
import json

app = Flask(__name__)
r = redis.Redis()

@app.route('/orders', methods=['POST'])
def create_order():
    idempotency_key = request.headers.get('Idempotency-Key')
    
    if not idempotency_key:
        return jsonify({'error': 'Idempotency-Key required'}), 400
    
    # Check if already processed
    cached = r.get(f'idempotency:{idempotency_key}')
    if cached:
        # Return cached response
        return jsonify(json.loads(cached)), 200
    
    # Process request
    order = {
        'order_id': generate_order_id(),
        'amount': request.json['amount'],
        'status': 'pending'
    }
    
    # Save to database
    db.orders.insert(order)
    
    # Cache response (24 hour TTL)
    r.setex(
        f'idempotency:{idempotency_key}',
        86400,  # 24 hours
        json.dumps(order)
    )
    
    return jsonify(order), 201
```

---

## Deduplication Strategies

### Redis Cache (Recommended)
```python
import redis
import hashlib

class IdempotencyCache:
    def __init__(self):
        self.redis = redis.Redis()
        self.ttl = 86400  # 24 hours
    
    def get_cached_response(self, key):
        """Get cached response if exists"""
        data = self.redis.get(f'idem:{key}')
        if data:
            return json.loads(data)
        return None
    
    def cache_response(self, key, response):
        """Cache response for future requests"""
        self.redis.setex(
            f'idem:{key}',
            self.ttl,
            json.dumps(response)
        )
    
    def is_processing(self, key):
        """Check if request is currently being processed"""
        return self.redis.exists(f'idem:processing:{key}')
    
    def mark_processing(self, key):
        """Mark request as processing (short TTL)"""
        self.redis.setex(
            f'idem:processing:{key}',
            60,  # 1 minute timeout
            '1'
        )
    
    def unmark_processing(self, key):
        """Remove processing marker"""
        self.redis.delete(f'idem:processing:{key}')

# Usage
cache = IdempotencyCache()

@app.route('/payments', methods=['POST'])
def process_payment():
    key = request.headers.get('Idempotency-Key')
    
    # Check cache
    cached = cache.get_cached_response(key)
    if cached:
        return jsonify(cached), 200
    
    # Check if processing
    if cache.is_processing(key):
        return jsonify({'error': 'Request already processing'}), 409
    
    try:
        cache.mark_processing(key)
        
        # Process payment
        result = charge_payment(request.json)
        
        # Cache result
        cache.cache_response(key, result)
        
        return jsonify(result), 201
    finally:
        cache.unmark_processing(key)
```

### Database Unique Constraint
```sql
CREATE TABLE idempotency_keys (
    idempotency_key VARCHAR(255) PRIMARY KEY,
    response_body TEXT,
    status_code INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at)
);

-- Cleanup old keys (run daily)
DELETE FROM idempotency_keys
WHERE created_at < NOW() - INTERVAL 24 HOUR;
```

```python
@app.route('/orders', methods=['POST'])
def create_order():
    key = request.headers.get('Idempotency-Key')
    
    try:
        # Try to insert key
        db.execute(
            "INSERT INTO idempotency_keys (idempotency_key, response_body, status_code) VALUES (?, ?, ?)",
            (key, None, None)
        )
    except IntegrityError:
        # Key exists, return cached response
        row = db.query("SELECT response_body, status_code FROM idempotency_keys WHERE idempotency_key = ?", (key,))
        return jsonify(json.loads(row['response_body'])), row['status_code']
    
    # Process order
    order = create_order_logic(request.json)
    
    # Update cached response
    db.execute(
        "UPDATE idempotency_keys SET response_body = ?, status_code = ? WHERE idempotency_key = ?",
        (json.dumps(order), 201, key)
    )
    
    return jsonify(order), 201
```

---

## Distributed Lock (Prevent Race Conditions)

```python
import redis
from contextlib import contextmanager

class DistributedLock:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    @contextmanager
    def acquire(self, key, timeout=10):
        """Acquire distributed lock"""
        lock_key = f'lock:{key}'
        lock_acquired = False
        
        try:
            # Try to acquire lock (SET NX with TTL)
            lock_acquired = self.redis.set(
                lock_key,
                '1',
                nx=True,  # Only set if not exists
                ex=timeout  # Expire after timeout
            )
            
            if not lock_acquired:
                raise Exception('Lock already held')
            
            yield
        finally:
            if lock_acquired:
                self.redis.delete(lock_key)

# Usage
lock = DistributedLock(redis_client)

@app.route('/payments', methods=['POST'])
def process_payment():
    key = request.headers.get('Idempotency-Key')
    
    try:
        with lock.acquire(key, timeout=60):
            # Check cache
            cached = cache.get_cached_response(key)
            if cached:
                return jsonify(cached), 200
            
            # Process payment
            result = charge_payment(request.json)
            cache.cache_response(key, result)
            
            return jsonify(result), 201
    
    except Exception as e:
        if 'Lock already held' in str(e):
            return jsonify({'error': 'Request already processing'}), 409
        raise
```

---

## Idempotent Database Operations

### INSERT with UPSERT
```sql
-- PostgreSQL
INSERT INTO users (user_id, email, name)
VALUES ('123', 'user@example.com', 'John Doe')
ON CONFLICT (user_id)
DO UPDATE SET
    email = EXCLUDED.email,
    name = EXCLUDED.name;

-- MySQL
INSERT INTO users (user_id, email, name)
VALUES ('123', 'user@example.com', 'John Doe')
ON DUPLICATE KEY UPDATE
    email = VALUES(email),
    name = VALUES(name);
```

### Conditional UPDATE
```sql
-- Only update if version matches (optimistic locking)
UPDATE orders
SET status = 'completed', version = version + 1
WHERE order_id = '123'
  AND version = 5;  -- Only update if current version is 5

-- Check affected rows
-- If 0, version mismatch (concurrent update)
```

### State Transitions with CHECK
```sql
-- Only allow valid state transitions
UPDATE orders
SET status = 'shipped'
WHERE order_id = '123'
  AND status = 'paid';  -- Only ship if currently paid

-- If affected_rows = 0, order wasn't in correct state
```

---

## Retry Logic

### Exponential Backoff
```python
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retries():
    """Create session with automatic retries"""
    session = requests.Session()
    
    retry = Retry(
        total=3,
        backoff_factor=1,  # 1s, 2s, 4s
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=['POST', 'PUT', 'DELETE']  # Retry non-idempotent!
    )
    
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session

# Usage
session = create_session_with_retries()

response = session.post(
    'https://api.example.com/orders',
    json={'amount': 100},
    headers={'Idempotency-Key': str(uuid.uuid4())}
)
```

### Manual Retry with Backoff
```python
import time

def retry_with_backoff(func, max_retries=3, base_delay=1):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Last attempt, propagate error
            
            delay = base_delay * (2 ** attempt)  # 1s, 2s, 4s
            print(f"Retry {attempt + 1} after {delay}s")
            time.sleep(delay)

# Usage
def create_order():
    return requests.post(
        'https://api.example.com/orders',
        json={'amount': 100},
        headers={'Idempotency-Key': 'uuid-123'}
    )

response = retry_with_backoff(create_order, max_retries=3)
```

---

## Idempotent Email Sending

```python
class EmailService:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def send_email_idempotent(self, recipient, subject, body, idempotency_key):
        """Send email only once per idempotency key"""
        
        # Check if already sent
        sent_key = f'email:sent:{idempotency_key}'
        if self.redis.exists(sent_key):
            print(f"Email already sent for key {idempotency_key}")
            return {'status': 'already_sent'}
        
        # Send email
        result = self.send_email(recipient, subject, body)
        
        # Mark as sent (TTL 7 days)
        self.redis.setex(sent_key, 604800, '1')
        
        return result
    
    def send_email(self, recipient, subject, body):
        # Actual email sending logic
        import smtplib
        # ... send email ...
        return {'status': 'sent', 'message_id': 'abc123'}

# Usage - Order confirmation email
email_service = EmailService(redis_client)

order_id = '123'
idempotency_key = f'order-confirmation:{order_id}'

email_service.send_email_idempotent(
    recipient='user@example.com',
    subject='Order Confirmation',
    body=f'Your order {order_id} has been confirmed',
    idempotency_key=idempotency_key
)
```

---

## Payment Idempotency (Stripe Example)

```python
import stripe

stripe.api_key = 'sk_test_...'

def charge_customer(amount, customer_id, idempotency_key):
    """Charge customer with idempotency"""
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            customer=customer_id,
            idempotency_key=idempotency_key  # Stripe handles deduplication
        )
        return {
            'status': 'success',
            'charge_id': charge.id,
            'amount': charge.amount
        }
    except stripe.error.IdempotencyError:
        # Same key, different parameters
        return {'status': 'error', 'message': 'Idempotency key reused with different parameters'}
    except stripe.error.CardError as e:
        return {'status': 'error', 'message': str(e)}

# Safe to retry with same key
result = charge_customer(
    amount=1000,
    customer_id='cus_123',
    idempotency_key='order-456'
)
```

---

## Testing Idempotency

```python
import pytest
import uuid

def test_idempotent_order_creation():
    """Test that duplicate requests create only one order"""
    idempotency_key = str(uuid.uuid4())
    
    # First request
    response1 = client.post('/orders', 
        json={'amount': 100},
        headers={'Idempotency-Key': idempotency_key}
    )
    assert response1.status_code == 201
    order_id_1 = response1.json['order_id']
    
    # Duplicate request (same key)
    response2 = client.post('/orders',
        json={'amount': 100},
        headers={'Idempotency-Key': idempotency_key}
    )
    assert response2.status_code == 200  # Not 201
    order_id_2 = response2.json['order_id']
    
    # Same order returned
    assert order_id_1 == order_id_2
    
    # Only one order in database
    orders = db.query("SELECT COUNT(*) FROM orders WHERE order_id = ?", (order_id_1,))
    assert orders[0]['count'] == 1

def test_concurrent_requests():
    """Test concurrent requests with same key"""
    import threading
    
    idempotency_key = str(uuid.uuid4())
    results = []
    
    def make_request():
        response = client.post('/orders',
            json={'amount': 100},
            headers={'Idempotency-Key': idempotency_key}
        )
        results.append(response.json['order_id'])
    
    # Send 10 concurrent requests
    threads = [threading.Thread(target=make_request) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # All return same order_id
    assert len(set(results)) == 1
```

## Rules

- Client generates idempotency key, not server — client controls retry identity.
- Use UUIDs for idempotency keys — avoid collisions, unpredictable.
- Cache responses for 24 hours minimum — covers retry window for most failures.
- Idempotency required for non-idempotent HTTP methods — POST, PATCH, DELETE need keys.
- Return cached response with same status code — exact replay of original response.
- Use distributed locks for critical operations — prevent race conditions in concurrent retries.
- Reject reused keys with different parameters — same key, different data = error.
- Log all idempotency cache hits — visibility into retry behavior.
- Test concurrent requests — race conditions only appear under load.
- Database unique constraints for strong guarantees — Redis cache + DB constraint = defense in depth.
