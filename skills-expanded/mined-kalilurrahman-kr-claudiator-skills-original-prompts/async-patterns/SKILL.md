---
name: async-patterns
description: Design asynchronous processing patterns for background jobs, event-driven systems, and non-blocking I/O. Outputs queues, workers, retry logic, and monitoring.
argument-hint: [task type, processing requirements, failure tolerance]
allowed-tools: Read, Write, Bash
---

# Asynchronous Processing Patterns

Design async systems that handle background jobs, event-driven workflows, and non-blocking operations reliably. Not "throw it in a queue" — specific queue choices, worker architectures, retry strategies, dead letter handling, and observability.

## Process

1. **Identify async tasks.** Email sending, image processing, report generation, long-running computations.
2. **Choose queue system.** Redis, RabbitMQ, AWS SQS, Kafka (based on volume, ordering, persistence).
3. **Design worker architecture.** Thread pool, process pool, distributed workers.
4. **Set retry logic.** Exponential backoff, max attempts, idempotency.
5. **Handle failures.** Dead letter queue, alerts, manual retry.
6. **Plan scaling.** Auto-scale workers based on queue depth.
7. **Monitor.** Queue depth, processing time, error rate, worker health.

## Output Format

### Async Processing Strategy: [System Name]

**Task Types:** 5 (Email, Image Processing, Report Gen, Webhook, Data Sync)  
**Queue System:** Redis (Celery) for low latency, AWS SQS for high reliability  
**Worker Count:** 10-50 (auto-scaled)  
**Retry Strategy:** Exponential backoff, max 3 attempts  
**Monitoring:** CloudWatch + Datadog dashboards  

---

## Task Categories

### 1. Fire-and-Forget (Best Effort)
**Example:** Send welcome email  
**Requirements:** Fast enqueue, acceptable failure rate  
**Queue:** Redis (in-memory, fast)  
**Retry:** 3 attempts, then drop  
**Monitoring:** Error rate alert if > 5%

### 2. Guaranteed Delivery (At-Least-Once)
**Example:** Payment processing, order confirmation  
**Requirements:** Must complete, can retry multiple times  
**Queue:** AWS SQS (persistent, durable)  
**Retry:** Unlimited with exponential backoff  
**Monitoring:** Dead letter queue alert

### 3. Ordered Processing (FIFO)
**Example:** User action timeline, event stream  
**Requirements:** Process in order per user/entity  
**Queue:** Kafka partitions by user_id  
**Retry:** Retry in place (block queue until success)  
**Monitoring:** Processing lag per partition

### 4. Scheduled Tasks (Cron-like)
**Example:** Daily reports, data cleanup  
**Requirements:** Run at specific time  
**Queue:** Celery Beat, AWS EventBridge  
**Retry:** Next scheduled run if failed  
**Monitoring:** Missed execution alerts

### 5. Long-Running Tasks (Minutes to Hours)
**Example:** Video transcoding, data export  
**Requirements:** Progress tracking, cancellation  
**Queue:** Separate high-priority queue  
**Retry:** Manual retry after failure investigation  
**Monitoring:** Timeout alerts (> 1 hour)

---

## Queue System Comparison

| Queue | Latency | Persistence | Ordering | Throughput | Cost |
|-------|---------|-------------|----------|------------|------|
| Redis | < 1ms | In-memory (optional disk) | No | 100k msg/s | $50/mo (self-hosted) |
| RabbitMQ | 1-5ms | Disk | Per queue | 50k msg/s | $100/mo (self-hosted) |
| AWS SQS | 10-50ms | Durable | FIFO option | Unlimited | $0.40/million msgs |
| Kafka | 2-10ms | Disk (replicated) | Per partition | 1M msg/s | $200/mo (MSK) |

**Decision Matrix:**
- **Low latency needed:** Redis
- **High reliability needed:** SQS, Kafka
- **Ordered processing needed:** Kafka (partitions), SQS FIFO
- **High throughput needed:** Kafka
- **Simplicity/managed:** SQS
- **Complex routing:** RabbitMQ (exchanges)

---

## Architecture Patterns

### Pattern 1: Celery + Redis (Simple, Low Latency)

**Components:**
- Celery: Task queue framework (Python)
- Redis: Message broker
- Workers: Python processes

**Flow:**
```
Django app → Celery task → Redis queue → Worker picks up → Process → Update DB
```

**Example (Django + Celery):**
```python
from celery import shared_task
import time

@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_id):
    try:
        user = User.objects.get(id=user_id)
        send_email(user.email, "Welcome!", template="welcome.html")
    except SMTPException as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
    except Exception as e:
        # Log error, don't retry
        logger.error("Failed to send email", user_id=user_id, error=str(e))
        raise

# Enqueue task
send_welcome_email.delay(user.id)
```

**Pros:** Fast (< 1ms latency), simple setup  
**Cons:** Redis is in-memory (message loss risk on crash)

---

### Pattern 2: AWS SQS + Lambda (Serverless, High Reliability)

**Components:**
- SQS: Message queue (fully managed)
- Lambda: Serverless workers (auto-scale)

**Flow:**
```
API → Put message in SQS → Lambda triggered → Process → Update DynamoDB
```

**Example (Node.js Lambda):**
```javascript
const AWS = require('aws-sdk');
const sqs = new AWS.SQS();

// Enqueue task
await sqs.sendMessage({
  QueueUrl: 'https://sqs.us-east-1.amazonaws.com/123456/my-queue',
  MessageBody: JSON.stringify({ user_id: '123', event: 'signup' })
}).promise();

// Lambda handler (auto-invoked by SQS)
exports.handler = async (event) => {
  for (const record of event.Records) {
    const message = JSON.parse(record.body);
    await processSignup(message.user_id);
  }
};
```

**Pros:** Fully managed, auto-scales, durable  
**Cons:** Higher latency (10-50ms), Lambda cold starts

---

### Pattern 3: Kafka + Consumer Groups (High Throughput, Ordered)

**Components:**
- Kafka: Distributed event log
- Consumer Group: Multiple workers processing in parallel

**Flow:**
```
Producer → Kafka topic (partitioned by user_id) → Consumers read in parallel → Process
```

**Example (Python Kafka Consumer):**
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['kafka:9092'],
    group_id='event-processor',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    event = message.value
    process_event(event['user_id'], event['action'])
    consumer.commit()  # Mark as processed
```

**Pros:** High throughput, ordered per partition, durable  
**Cons:** Complex setup, overkill for simple tasks

---

## Retry Strategies

### 1. Fixed Delay
```python
@task(retry_backoff=10)  # Retry every 10 seconds
def process_order(order_id):
    ...
```
**When:** Transient errors (network glitch)

### 2. Exponential Backoff
```python
@task(max_retries=5)
def process_payment(payment_id):
    try:
        charge_card(payment_id)
    except Exception as e:
        retry_delay = 2 ** self.request.retries  # 2s, 4s, 8s, 16s, 32s
        raise self.retry(exc=e, countdown=retry_delay)
```
**When:** Unknown failure cause, avoid overwhelming downstream service

### 3. Jittered Exponential Backoff
```python
import random

retry_delay = (2 ** self.request.retries) + random.uniform(0, 1)
```
**When:** Many workers retrying same task (avoid thundering herd)

### 4. Dead Letter Queue (DLQ)
```python
@task(max_retries=3, default_retry_delay=60)
def process_webhook(webhook_id):
    try:
        send_webhook(webhook_id)
    except Exception as e:
        if self.request.retries >= 3:
            # Move to DLQ for manual investigation
            logger.error("Webhook failed after 3 retries", webhook_id=webhook_id)
            save_to_dlq(webhook_id, error=str(e))
        else:
            raise self.retry(exc=e)
```
**When:** Task fails repeatedly, requires human intervention

---

## Idempotency

### Problem: Task Runs Twice
```
Task: Charge user $10
Retry after timeout → User charged $20 (double charge)
```

### Solution 1: Idempotency Key
```python
def charge_user(user_id, amount, idempotency_key):
    # Check if already processed
    if Payment.objects.filter(idempotency_key=idempotency_key).exists():
        return  # Already processed, skip
    
    # Process payment
    stripe.charge(user_id, amount, idempotency_key=idempotency_key)
    
    # Record payment
    Payment.objects.create(
        user_id=user_id,
        amount=amount,
        idempotency_key=idempotency_key
    )
```

### Solution 2: Database Constraint
```sql
CREATE TABLE payments (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    idempotency_key VARCHAR(255) UNIQUE NOT NULL  -- Prevents duplicates
);
```

---

## Worker Architecture

### Thread Pool (I/O-Bound Tasks)
```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=20)

def process_task(task):
    # I/O-bound: API call, database query
    response = requests.get(task.url)
    save_response(response)

# Submit tasks
for task in tasks:
    executor.submit(process_task, task)
```

**When:** Tasks spend time waiting (HTTP requests, DB queries)  
**Workers:** 20-100 threads per machine

---

### Process Pool (CPU-Bound Tasks)
```python
from multiprocessing import Pool

def process_image(image_path):
    # CPU-bound: Image resizing, ML inference
    img = load_image(image_path)
    resized = resize(img, 800, 600)
    save_image(resized)

# Use all CPU cores
with Pool() as pool:
    pool.map(process_image, image_paths)
```

**When:** Tasks use CPU intensively  
**Workers:** 1 process per CPU core

---

### Distributed Workers (High Scale)
```python
# Celery workers on multiple machines
# Machine 1: 10 workers
celery -A myapp worker --concurrency=10

# Machine 2: 10 workers
celery -A myapp worker --concurrency=10

# Auto-scaling (Kubernetes HPA)
kubectl autoscale deployment celery-worker --min=5 --max=50 --cpu-percent=70
```

**When:** Single machine cannot handle load  
**Workers:** 5-500 workers across cluster

---

## Monitoring & Alerting

### Key Metrics

#### Queue Depth
```
current_queue_depth = messages_in_queue
```
**Alert if:** > 1000 messages (workers can't keep up)

#### Processing Time (p50, p95, p99)
```
task_duration_seconds{task="send_email", quantile="0.95"} > 10
```
**Alert if:** p95 > 10 seconds (tasks getting slower)

#### Error Rate
```
error_rate = (failed_tasks / total_tasks) * 100
```
**Alert if:** > 5% (something is broken)

#### Worker Health
```
active_workers = count(workers with recent heartbeat)
```
**Alert if:** < 5 workers (capacity issue)

---

### Dashboards (Prometheus Queries)

**Queue depth over time:**
```promql
celery_queue_length{queue="default"}
```

**Task processing rate:**
```promql
rate(celery_task_total[5m])
```

**Error rate by task type:**
```promql
rate(celery_task_failed_total[5m]) / rate(celery_task_total[5m])
```

---

## Scaling Strategy

### Manual Scaling
```bash
# Add more workers
celery -A myapp worker --concurrency=20  # Was 10, now 20
```

### Auto-Scaling (Kubernetes)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: celery-worker
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: celery-worker
  minReplicas: 5
  maxReplicas: 50
  metrics:
  - type: External
    external:
      metric:
        name: celery_queue_length
      target:
        type: Value
        value: "100"  # Scale up if queue > 100 per worker
```

### Auto-Scaling (AWS Lambda)
```
Lambda automatically scales based on SQS queue depth
Reserved concurrency: 50 (max simultaneous executions)
```

---

## Common Patterns

### Fan-Out (One Task → Many Sub-Tasks)
```python
@task
def process_batch(user_ids):
    # Split into individual tasks
    for user_id in user_ids:
        process_user.delay(user_id)

@task
def process_user(user_id):
    # Process single user
    ...
```

### Chain (Task A → Task B → Task C)
```python
from celery import chain

workflow = chain(
    download_file.s(url),
    process_file.s(),
    upload_result.s()
)
workflow.apply_async()
```

### Chord (Parallel Tasks → Aggregate Results)
```python
from celery import chord

# Process files in parallel, then merge
workflow = chord(
    [process_file.s(file) for file in files]
)(merge_results.s())

workflow.apply_async()
```

---

## Best Practices

### DO:
- Use idempotency keys for critical tasks (payments, orders)
- Set task timeouts (prevent infinite loops)
- Monitor queue depth and error rates
- Use dead letter queue for failed tasks
- Log task start, end, and errors with task_id
- Scale workers based on queue depth

### DON'T:
- Enqueue tasks inside loops (batch instead)
- Pass large objects as task arguments (pass IDs, fetch in task)
- Retry forever (set max_retries)
- Ignore failed tasks (alert on DLQ depth)
- Block queue processing (use timeouts)

## Rules

- Every async task must have a timeout — infinite tasks will block workers.
- Tasks must be idempotent — retries should not cause duplicate side effects (double charges, double emails).
- Critical tasks (payments, orders) must use durable queues (SQS, Kafka), not in-memory (Redis).
- Retry logic must use exponential backoff to avoid overwhelming failed services.
- Dead letter queue is mandatory for tasks with max retries — failed tasks need manual investigation.
- Queue depth > 1000 means workers cannot keep up — scale workers or investigate slow tasks.
- Error rate > 5% indicates systemic issue — alert and investigate.
- Task arguments should be small (IDs, not full objects) — large messages slow down queue.
- Workers must send heartbeats — detect and alert on dead workers.
- Ordered processing requires partitioned queues (Kafka) or FIFO queues (SQS FIFO) — standard queues do not guarantee order.
