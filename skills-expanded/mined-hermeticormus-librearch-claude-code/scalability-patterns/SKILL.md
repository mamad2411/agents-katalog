---
name: "scalability-patterns"
description: "Scaling patterns with code: Kubernetes HPA on custom metrics, KEDA scaling for Kafka consumers, stateless sessions in Redis, read/write splitting in Spring Boot, and queue-based load leveling with SQS and Lambda. Use when scaling a service or planning capacity."
---

# Scalability Patterns

> Named patterns with code for Kubernetes HPA, KEDA queue-based scaling, database read routing, stateless session design, and queue-based load leveling.

## Patterns

### Pattern: Kubernetes HPA with Custom Metrics

```yaml
# Scale order-service based on RPS (custom metric from Prometheus adapter)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 2
  maxReplicas: 50
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30  # React quickly to traffic spikes
      policies:
        - type: Pods
          value: 4       # Add at most 4 pods per scaling event
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
        - type: Percent
          value: 10      # Remove at most 10% per scaling event
          periodSeconds: 60
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: External
      external:
        metric:
          name: http_requests_per_second
          selector:
            matchLabels:
              service: order-service
        target:
          type: AverageValue
          averageValue: "1000"
```

### Pattern: KEDA Kafka Consumer Auto-Scaling

```yaml
# Scale consumer pods based on Kafka consumer group lag
# Scales to zero when no messages — no idle consumer cost
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: inventory-consumer-scaler
spec:
  scaleTargetRef:
    name: inventory-consumer
  pollingInterval: 15     # Check lag every 15 seconds
  cooldownPeriod: 30      # Wait 30s before scaling to zero
  minReplicaCount: 0      # Scale to zero when no lag
  maxReplicaCount: 12     # Max = partition count
  triggers:
    - type: kafka
      metadata:
        bootstrapServers: kafka:9092
        consumerGroup: inventory-service
        topic: orders.placed
        lagThreshold: "100"   # Scale when lag > 100 messages per partition
        activationLagThreshold: "1"  # Wake from zero when any lag exists
```

### Pattern: Stateless Service with Redis Session (Node.js)

```typescript
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

const redisClient = createClient({
  url: process.env.REDIS_URL,
  socket: { reconnectStrategy: (retries) => Math.min(retries * 50, 2000) },
});

await redisClient.connect();

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,        // HTTPS only
    httpOnly: true,      // No JS access
    maxAge: 3600000,     // 1 hour TTL
    sameSite: 'strict',
  },
  // Sessions stored in Redis — any pod handles any request
  // Load balancer does not need sticky sessions
}));

// Session data is in Redis — scales horizontally
app.get('/api/cart', (req, res) => {
  const cart = req.session.cart ?? [];
  res.json({ cart, itemCount: cart.length });
});
```

### Pattern: Database Read/Write Splitting (Spring Boot)

```java
// Route @Transactional(readOnly = true) to replica, others to primary
@Aspect
@Component
@Order(Ordered.LOWEST_PRECEDENCE - 1)  // Must run before @Transactional opens connection
public class ReadOnlyRoutingAspect {

    @Around("@annotation(transactional)")
    public Object routeByTransactionType(ProceedingJoinPoint pjp, Transactional transactional)
            throws Throwable {
        if (transactional.readOnly()) {
            DataSourceContextHolder.setReplica();
        } else {
            DataSourceContextHolder.setPrimary();
        }
        try {
            return pjp.proceed();
        } finally {
            DataSourceContextHolder.clear();
        }
    }
}

public class DataSourceContextHolder {
    private static final ThreadLocal<String> context = new ThreadLocal<>();

    public static void setPrimary() { context.set("primary"); }
    public static void setReplica() { context.set("replica"); }
    public static String get() { return context.get() != null ? context.get() : "primary"; }
    public static void clear() { context.remove(); }
}

// Usage: annotate read-only service methods
@Service
public class OrderQueryService {

    @Transactional(readOnly = true)  // Routes to replica automatically
    public List<OrderSummary> findByCustomer(CustomerId customerId) {
        return orderRepo.findByCustomerId(customerId);
    }
}
```

### Pattern: Queue-Based Load Leveling (AWS SQS + Lambda)

```typescript
// Producer: write to SQS instead of processing synchronously
// Queue absorbs the spike; Lambda processes at a steady rate

// Producer (API handler)
async function handleOrderRequest(event: APIGatewayEvent): Promise<APIGatewayProxyResult> {
  const order = JSON.parse(event.body!);

  // Enqueue — returns immediately (O(1) latency)
  await sqs.send(new SendMessageCommand({
    QueueUrl: process.env.ORDER_PROCESSING_QUEUE_URL,
    MessageBody: JSON.stringify(order),
    MessageGroupId: order.customerId,    // FIFO: order per customer
    MessageDeduplicationId: order.idempotencyKey,
  }));

  // Return 202 Accepted — processing is async
  return { statusCode: 202, body: JSON.stringify({ message: 'Order queued' }) };
}

// Consumer Lambda — triggered by SQS, processes at controlled concurrency
export const processOrder: SQSHandler = async (event) => {
  for (const record of event.Records) {
    const order = JSON.parse(record.body);
    await orderService.processOrder(order);
    // SQS auto-deletes on success; sends to DLQ on Lambda failure
  }
};
```

Lambda SQS trigger configuration:
```yaml
# Concurrency controls how many order-processing Lambdas run simultaneously
# ReservedConcurrency = max concurrent executions = max load on downstream DB
ReservedConcurrency: 20       # Limits to 20 concurrent order processors
BatchSize: 10                 # Each Lambda invocation processes up to 10 messages
```

## Anti-Patterns

### Anti-Pattern: Scaling a Stateful Service Horizontally Without Shared State

Adding replicas to a service that stores session data in local memory. Users hitting replica A have a different session than users hitting replica B. Users get logged out or lose cart data on every other request.

Fix: move all session state to Redis. Verify with a test that sends requests to different pods for the same session.

### Anti-Pattern: Scaling Application Servers When the Database Is the Bottleneck

Adding 10 more application server pods when the database is at 100% CPU. Each new pod opens more connections to the already-saturated database. Performance gets worse, not better.

Fix: identify the actual bottleneck with metrics before scaling. Add read replicas, add query caching, or optimize slow queries. Application pods scale after the database bottleneck is resolved.

### Anti-Pattern: Thundering Herd on Cache Miss

All cache keys for a popular resource expire at the same time (same TTL, all set at the same moment during a cache warmup). All requests simultaneously miss the cache and flood the database.

Fix: add random jitter to TTL: `ttl = BASE_TTL + random(0, BASE_TTL * 0.1)`. Use the PER algorithm for probabilistic early expiration. Add a distributed lock (mutex) so only one request regenerates the value.

### Anti-Pattern: No Scale-Down Cooldown

HPA configured to scale down as aggressively as it scales up. Load spike → 20 pods → load returns to normal → scale down to 2 pods → next request spike → 20 pods again. Each scale-up event takes 30-60 seconds. Users experience latency spikes on every traffic fluctuation.

Fix: set `scaleDown.stabilizationWindowSeconds` to 300 (5 minutes). Scale up aggressively; scale down conservatively.

## References

- Abbott, Martin, and Michael Fisher. _The Art of Scalability_, 2nd ed. Addison-Wesley, 2015.
- Kubernetes HPA documentation: kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale
- KEDA: keda.sh/docs/concepts
- AWS SQS + Lambda event source mapping: docs.aws.amazon.com/lambda/latest/dg/with-sqs.html
