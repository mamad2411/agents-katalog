---
name: task-queue
category: msa
description: "Task Queue 패턴 가이드 — 비동기 작업 분산 처리, 우선순위 큐, 재시도 전략, Worker 오토스케일링 패턴 Use when working with msa 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Task Queue 패턴 가이드

비동기 작업 분산 처리, 우선순위 큐, 재시도 전략, Worker 오토스케일링 패턴

## Quick Reference (결정 트리)

```
Task Queue 필요한가?
    │
    ├─ HTTP 응답 내 완료 가능 ──────> 동기 처리 (REST/gRPC)
    ├─ 수초~수분 소요 작업 ─────────> Task Queue (Celery/BullMQ/asynq)
    ├─ 이벤트 스트림 처리 ─────────> Kafka Consumer (이벤트 드리븐)
    └─ 배치 대량 처리 ─────────────> K8s Job / Spark

기술 선택?
    │
    ├─ Python ──────> Celery 5.6 (Redis/RabbitMQ)
    ├─ Node.js ─────> BullMQ 5.x (Redis Streams)
    ├─ Go ──────────> asynq (Redis 기반)
    └─ Java/Spring ─> Spring + RabbitMQ / Redis

Worker 배포?
    │
    ├─ 상시 실행 + 오토스케일링 ──> K8s Deployment + KEDA
    ├─ 일회성 배치 ──────────────> K8s Job
    └─ 주기적 작업 ──────────────> K8s CronJob
```

---

## CRITICAL: Task Queue 아키텍처

```
Producer (API)           Broker (Redis/RabbitMQ)          Worker Pool
┌──────────┐           ┌────────────────────┐          ┌──────────────┐
│ HTTP API │──enqueue─>│ Priority Queue     │─dequeue─>│ W1  W2  W3   │
│ Webhook  │           │ [P:1][P:5][P:10]   │          │ (KEDA 스케일) │
└──────────┘           │ Dead Letter Queue   │          └──────────────┘
                       └────────────────────┘
```

| 항목 | Celery 5.6 | BullMQ 5.x | Go asynq | Spring+RabbitMQ |
|------|-----------|------------|----------|-----------------|
| 브로커 | Redis/RabbitMQ | Redis Streams | Redis | RabbitMQ/Redis |
| 우선순위 | 지원 | 네이티브 | 가중치 큐 | 네이티브 |
| 지연 실행 | countdown/eta | delay/repeat | ProcessIn | TTL+DLX |
| 워크플로우 | chain/group/chord | FlowProducer | 제한적 | Spring Batch |
| 모니터링 | Flower | BullBoard | asynqmon | RabbitMQ Console |

---

## Celery 5.6 패턴 (Python)

```python
from celery import Celery, chain, group, chord

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/1')
app.conf.update(
    task_acks_late=True,              # 처리 완료 후 ACK (Worker 장애 시 재처리)
    worker_prefetch_multiplier=1,      # 공정한 분배 (우선순위 큐 필수)
    task_reject_on_worker_lost=True,   # Worker 비정상 종료 시 재큐잉
    task_routes={
        'tasks.send_email': {'queue': 'email'},
        'tasks.generate_report': {'queue': 'reports', 'priority': 5},
    },
)

@app.task(bind=True, max_retries=3, acks_late=True)
def validate_order(self, order_id: str) -> dict:
    try:
        order = OrderService.validate(order_id)
        return {"order_id": order_id, "status": "validated"}
    except ValidationError as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

@app.task(bind=True, max_retries=3)
def charge_payment(self, validated: dict) -> dict:
    idempotency_key = f"payment:{validated['order_id']}"
    result = PaymentService.charge(validated['order_id'], idempotency_key)
    return {"order_id": validated['order_id'], "payment_id": result.id}

@app.task
def send_notification(result: dict): NotificationService.send(result['order_id'])
@app.task
def update_inventory(result: dict): InventoryService.decrease(result['order_id']); return result
@app.task
def finalize_order(results: list): OrderService.finalize(results[0]['order_id'])

# Chain: 순차 (validate -> charge -> notify)
chain(validate_order.s("ord-123"), charge_payment.s(), send_notification.s()).apply_async()
# Group: 병렬
group(send_notification.s({"order_id": "ord-123"}), update_inventory.s({"order_id": "ord-123"})).apply_async()
# Chord: 병렬 후 콜백 (모든 태스크 완료 후 finalize)
chord([send_notification.s({"order_id": "ord-123"}), update_inventory.s({"order_id": "ord-123"})], finalize_order.s()).apply_async()
```

---

## BullMQ 5.x 패턴 (Node.js / TypeScript)

```typescript
import { Queue, Worker, FlowProducer } from 'bullmq';
const connection = new IORedis({ host: 'redis', port: 6379, maxRetriesPerRequest: null });

const orderQueue = new Queue('order-processing', { connection,
  defaultJobOptions: {
    attempts: 3, backoff: { type: 'exponential', delay: 1000 },  // 1s, 2s, 4s
    removeOnComplete: { age: 86400 }, removeOnFail: { age: 604800 },
  },
});

// Job 등록: 우선순위, 지연, cron 반복
await orderQueue.add('send-invoice', { orderId: 'ord-123' }, { priority: 1 });
await orderQueue.add('generate-report', { type: 'monthly' }, { delay: 60000 });
await orderQueue.add('daily-summary', {}, { repeat: { pattern: '0 9 * * *' } });

// Worker: concurrency + Rate Limiting
const worker = new Worker('order-processing', async (job) => {
  if (job.name === 'send-invoice') return InvoiceService.generate(job.data.orderId);
  if (job.name === 'generate-report') {
    await job.updateProgress(10);
    const report = await ReportService.generate(job.data.type);
    await job.updateProgress(100);
    return { reportUrl: report.url };
  }
}, { connection, concurrency: 5, limiter: { max: 100, duration: 60000 } });

worker.on('failed', (job, err) => {
  if (job && job.attemptsMade >= (job.opts.attempts ?? 3))
    alertService.notify(`DLQ 도달: ${job.name}, error: ${err.message}`);
});

// FlowProducer: children 완료 후 parent 실행
const flow = new FlowProducer({ connection });
await flow.add({
  name: 'finalize-order', queueName: 'order-processing', data: { orderId: 'ord-123' },
  children: [
    { name: 'charge-payment', queueName: 'order-processing', data: { orderId: 'ord-123' } },
    { name: 'update-inventory', queueName: 'order-processing', data: { orderId: 'ord-123' } },
  ],
});
```

---

## Go asynq 패턴

### Client (태스크 발행)

```go
const (
    TypeOrderProcess   = "order:process"
    TypeReportGenerate = "report:generate"
)
type OrderPayload struct {
    OrderID    string `json:"order_id"`
    CustomerID string `json:"customer_id"`
}

func NewOrderTask(orderID, customerID string) (*asynq.Task, error) {
    payload, _ := json.Marshal(OrderPayload{OrderID: orderID, CustomerID: customerID})
    return asynq.NewTask(TypeOrderProcess, payload,
        asynq.MaxRetry(5), asynq.Timeout(30*time.Second),
        asynq.Queue("critical"), asynq.Unique(24*time.Hour),  // 24시간 중복 방지
    ), nil
}

func main() {
    client := asynq.NewClient(asynq.RedisClientOpt{Addr: "redis:6379"})
    defer client.Close()
    task, _ := NewOrderTask("ord-123", "cust-456")
    client.Enqueue(task)                                  // 즉시 실행
    client.Enqueue(task, asynq.ProcessIn(10*time.Minute)) // 10분 후 실행
    // 스케줄러: cron 패턴
    scheduler := asynq.NewScheduler(asynq.RedisClientOpt{Addr: "redis:6379"}, nil)
    scheduler.Register("0 9 * * *", asynq.NewTask(TypeReportGenerate, nil))
    scheduler.Run()
}
```

### Server 및 Handler (태스크 처리)

```go
func main() {
    srv := asynq.NewServer(asynq.RedisClientOpt{Addr: "redis:6379"}, asynq.Config{
        Concurrency: 10,
        Queues: map[string]int{"critical": 6, "default": 3, "low": 1},
        RetryDelayFunc: func(n int, e error, t *asynq.Task) time.Duration {
            return time.Duration(math.Pow(2, float64(n))) * time.Second // 지수 백오프
        },
        ErrorHandler: asynq.ErrorHandlerFunc(func(ctx context.Context, task *asynq.Task, err error) {
            retried, _ := asynq.GetRetryCount(ctx)
            maxRetry, _ := asynq.GetMaxRetry(ctx)
            if retried >= maxRetry { log.Printf("[DLQ] task=%s, error=%v", task.Type(), err) }
        }),
    })
    mux := asynq.NewServeMux()
    mux.HandleFunc(TypeOrderProcess, HandleOrderProcess)
    srv.Run(mux)
}

func HandleOrderProcess(ctx context.Context, t *asynq.Task) error {
    var p OrderPayload
    if err := json.Unmarshal(t.Payload(), &p); err != nil {
        return fmt.Errorf("페이로드 파싱 실패: %w", err)
    }
    if processed, _ := orderRepo.IsProcessed(ctx, p.OrderID); processed {
        return nil // 이미 처리됨
    }
    if err := orderService.Process(ctx, p.OrderID); err != nil {
        return fmt.Errorf("주문 처리 실패: %w", err) // 에러 → 자동 재시도
    }
    return nil
}
```

---

## Spring 통합 (RabbitMQ)

```java
@Configuration
public class TaskQueueConfig {
    @Bean public Queue taskQueue() {
        return QueueBuilder.durable("task-queue")
            .withArgument("x-max-priority", 10)              // 우선순위 큐
            .withArgument("x-dead-letter-exchange", "dlx")
            .withArgument("x-dead-letter-routing-key", "dlq").build();
    }
    @Bean public Queue deadLetterQueue() { return QueueBuilder.durable("task-dlq").build(); }
    @Bean public DirectExchange dlxExchange() { return new DirectExchange("dlx"); }
    @Bean public Binding dlqBinding() {
        return BindingBuilder.bind(deadLetterQueue()).to(dlxExchange()).with("dlq");
    }
}

@Service @RequiredArgsConstructor
public class TaskProducer {
    private final RabbitTemplate rabbitTemplate;
    public void enqueue(String taskType, Object payload, int priority) {
        rabbitTemplate.convertAndSend("task-queue", payload, message -> {
            message.getMessageProperties().setPriority(priority);
            message.getMessageProperties().setHeader("taskType", taskType);
            message.getMessageProperties().setHeader("idempotencyKey", UUID.randomUUID().toString());
            return message;
        });
    }
}

@Component @RequiredArgsConstructor
public class TaskWorker {
    private final ProcessedTaskRepository processedTaskRepo;
    @RabbitListener(queues = "task-queue", concurrency = "3-10")
    public void process(Message message) {
        String key = message.getMessageProperties().getHeader("idempotencyKey");
        if (processedTaskRepo.existsById(key)) return; // 중복 무시
        try {
            String taskType = message.getMessageProperties().getHeader("taskType");
            taskHandlerRegistry.handle(taskType, message.getBody());
            processedTaskRepo.save(new ProcessedTask(key, Instant.now()));
        } catch (Exception e) {
            throw new AmqpRejectAndDontRequeueException("처리 실패"); // → DLQ
        }
    }
}
```

---

## CRITICAL: 핵심 패턴

### Priority Queue

```
P1 (Critical) : 결제, 주문 처리 → 즉시  |  큐 분리 (권장): critical/default/low 별도
P5 (Normal)   : 이메일, 알림    → 수초  |  단일 큐 우선순위: priority 필드 브로커 정렬
P10 (Low)     : 리포트, 통계    → 수분  |  (RabbitMQ 네이티브 지원)
```

### Exponential Backoff + Jitter

```python
@app.task(bind=True, max_retries=5, autoretry_for=(TransientError,))
def process_payment(self, order_id: str):
    try:
        PaymentGateway.charge(order_id)
    except TransientError as exc:
        backoff = (2 ** self.request.retries) * 60  # 60s, 120s, 240s, 480s, 960s
        jitter = random.uniform(0, backoff * 0.1)   # 10% 지터 (Thundering Herd 방지)
        raise self.retry(exc=exc, countdown=backoff + jitter)
```

### Idempotency Key

```
1. DB 기반  : processed_tasks 테이블 저장 (가장 안전)
2. Redis    : SET key NX EX 86400 (TTL 24시간, 경량)
3. asynq    : asynq.Unique(duration) (Redis SETNX 내장)
4. BullMQ   : jobId 지정 시 동일 ID 중복 방지
주의: Redis TTL 만료 후 중복 가능 → 부작용 큰 작업은 DB 기반 권장
```

---

## Kubernetes Worker 배포

### Worker Deployment + Graceful Shutdown

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-worker
spec:
  replicas: 2
  template:
    spec:
      terminationGracePeriodSeconds: 300  # 진행 중 태스크 완료 대기
      containers:
        - name: worker
          image: myapp/worker:latest
          resources:
            requests: { cpu: "250m", memory: "512Mi" }
            limits:   { cpu: "1000m", memory: "1Gi" }
          env:
            - name: REDIS_URL
              valueFrom: { secretKeyRef: { name: redis-secret, key: url } }
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "kill -SIGTERM 1 && sleep 30"]
```

### KEDA Queue-Length Scaler

```yaml
# Redis 큐 기반 (Celery, asynq)
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: task-worker-scaler
spec:
  scaleTargetRef: { name: task-worker }
  pollingInterval: 10
  cooldownPeriod: 120
  minReplicaCount: 1       # 0이면 scale-to-zero
  maxReplicaCount: 30
  triggers:
    - type: redis
      metadata:
        address: redis:6379
        listName: celery
        listLength: "50"   # 50개 이상 → 스케일업
        activationListLength: "5"
---
# RabbitMQ 큐 기반 (Spring Worker)
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: rabbitmq-worker-scaler
spec:
  scaleTargetRef: { name: rabbitmq-worker }
  triggers:
    - type: rabbitmq
      metadata:
        host: amqp://guest:guest@rabbitmq:5672/
        queueName: task-queue
        queueLength: "100"
```

### Job vs Deployment 선택

| 기준 | Deployment | Job / CronJob |
|------|-----------|---------------|
| 실행 주기 | 상시 실행 | 일회성 / 주기적 |
| KEDA 연동 | ScaledObject | ScaledJob |
| 장애 복구 | 자동 재시작 | backoffLimit |
| 비용 | 상시 점유 | 실행 시에만 점유 |
| 적합한 작업 | 이메일, 알림 큐 | 리포트, 마이그레이션 |

```yaml
# KEDA ScaledJob (일회성 배치)
apiVersion: keda.sh/v1alpha1
kind: ScaledJob
metadata:
  name: batch-report-job
spec:
  jobTargetRef:
    template:
      spec:
        containers:
          - name: report-worker
            image: myapp/report-worker:latest
        restartPolicy: OnFailure
  maxReplicaCount: 10
  triggers:
    - type: redis
      metadata:
        address: redis:6379
        listName: report-tasks
        listLength: "1"    # 태스크 1개당 Job 1개 생성
```

---

## 모니터링

```
Queue Depth:        평시 5배 이상 → 경보  | redis_list_length, rabbitmq_queue_messages
Processing Latency: P95 SLO 설정         | task_processing_duration_seconds (histogram)
Worker Utilization: 70% 이상 → 스케일업   | active_workers / total_workers
Failure Rate:       5% 이상 → 경보       | task_failures_total / task_processed_total
DLQ Size:           0 아니면 즉시 확인    | dlq_messages_count
```

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: task-queue-alerts
spec:
  groups:
    - name: task-queue
      rules:
        - alert: HighQueueDepth
          expr: redis_list_length{list="celery"} > 500
          for: 5m
          annotations: { summary: "큐 깊이 500 초과 ({{ $value }})" }
        - alert: HighTaskFailureRate
          expr: rate(task_failures_total[5m]) / rate(task_processed_total[5m]) > 0.05
          for: 3m
          labels: { severity: critical }
        - alert: DLQNotEmpty
          expr: dlq_messages_count > 0
          for: 1m
          labels: { severity: critical }
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 멱등성 미구현 | 재시도 시 중복 처리 (이중 결제) | Idempotency Key + DB/Redis 중복 체크 |
| 무한 재시도 | 영구 실패 태스크가 큐 점유 | max_retries + DLQ 이동 |
| 고정 재시도 간격 | Thundering Herd | Exponential Backoff + Jitter |
| ACK 먼저 전송 | Worker 장애 시 태스크 유실 | acks_late=True (처리 완료 후 ACK) |
| 큐 하나로 통합 | 저우선순위가 고우선순위 블로킹 | 우선순위별 큐 분리 + 가중치 |
| Worker 타임아웃 없음 | hang 태스크가 Worker 점유 | task timeout 필수 설정 |
| 큐 깊이 모니터링 없음 | 메모리 초과 | KEDA 스케일링 + 알림 |
| Graceful Shutdown 없음 | 배포 시 태스크 손실 | terminationGracePeriodSeconds + SIGTERM |
| Fat Payload | 브로커 메모리 과다 | ID만 큐잉, 데이터는 DB/S3 조회 |
| 결과 저장소 미정리 | Redis 메모리 누수 | result_expires / removeOnComplete |

---

## 체크리스트

### 설계 단계
- [ ] Task Queue vs Event Streaming 경계를 명확히 구분했는가?
- [ ] 태스크 우선순위 레벨을 정의하고 큐를 분리했는가?
- [ ] 모든 태스크에 멱등성 키(Idempotency Key)를 부여했는가?
- [ ] 태스크 타임아웃과 최대 재시도 횟수를 설정했는가?
- [ ] Dead Letter Queue 및 실패 알림을 구성했는가?

### 구현 단계
- [ ] 지수 백오프 + Jitter로 재시도 전략을 구현했는가?
- [ ] acks_late=True로 처리 완료 후 ACK를 보내는가?
- [ ] Worker의 Graceful Shutdown을 구현했는가? (SIGTERM 처리)
- [ ] 페이로드를 최소화하고 대용량 데이터는 참조만 전달하는가?
- [ ] 결과 저장소(backend)의 TTL/정리 정책을 설정했는가?

### 배포/운영 단계
- [ ] KEDA ScaledObject로 큐 깊이 기반 오토스케일링을 구성했는가?
- [ ] terminationGracePeriodSeconds를 최대 태스크 처리 시간 이상으로 설정했는가?
- [ ] Queue Depth, Processing Latency, Failure Rate 메트릭을 수집하는가?
- [ ] DLQ 모니터링 알림을 설정하고 재처리 절차를 문서화했는가?
- [ ] Job vs Deployment 중 적합한 배포 방식을 선택했는가?

---

## 참조 스킬

- `/redis-streams` - Redis Streams 기반 메시징 패턴
- `/rabbitmq` - RabbitMQ 큐 설계, Exchange/Binding 패턴
- `/k8s-autoscaling` - KEDA, HPA, VPA 오토스케일링 전략
- `/msa-event-driven` - 이벤트 드리븐 아키텍처, Kafka, Outbox 패턴
