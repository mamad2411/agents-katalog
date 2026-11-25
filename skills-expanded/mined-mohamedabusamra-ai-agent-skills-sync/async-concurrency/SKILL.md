---
name: async-concurrency
description: Handle asynchronous operations and concurrency patterns correctly in Node.js. Use when writing async code, handling promises, managing concurrency, or when the user asks about async/await, promises, concurrency, or race conditions.
---

# Async/Await & Concurrency Patterns

Handle asynchronous operations and concurrency correctly in Node.js applications.

## Async/Await Basics

### Proper Error Handling

```typescript
// ✅ Good - Try-catch with async/await
async function fetchUser(id: number) {
  try {
    const user = await User.findByPk(id);
    if (!user) {
      throw new NotFoundError("User", id.toString());
    }
    return user;
  } catch (error) {
    logger.error("Failed to fetch user", { id, error });
    throw error;
  }
}

// ❌ Bad - Unhandled promise rejection
async function fetchUser(id: number) {
  const user = await User.findByPk(id); // No error handling
  return user;
}
```

### Parallel Execution

```typescript
// ✅ Good - Execute in parallel
async function fetchUserData(userId: number) {
  const [user, orders, notifications] = await Promise.all([
    User.findByPk(userId),
    Order.findAll({ where: { userId } }),
    Notification.findAll({ where: { userId } }),
  ]);
  return { user, orders, notifications };
}

// ✅ Good - Handle partial failures
async function fetchUserDataSafe(userId: number) {
  const [user, orders, notifications] = await Promise.allSettled([
    User.findByPk(userId),
    Order.findAll({ where: { userId } }),
    Notification.findAll({ where: { userId } }),
  ]);

  return {
    user: user.status === "fulfilled" ? user.value : null,
    orders: orders.status === "fulfilled" ? orders.value : [],
    notifications:
      notifications.status === "fulfilled" ? notifications.value : [],
  };
}
```

## Promise Patterns

### Promise Chaining

```typescript
// ✅ Good - Clear promise chain
function processOrder(orderId: number) {
  return getOrder(orderId)
    .then((order) => validateOrder(order))
    .then((order) => processPayment(order))
    .then((order) => sendConfirmation(order))
    .catch((error) => {
      logger.error("Order processing failed", { orderId, error });
      throw error;
    });
}
```

### Promise Utilities

```typescript
// Timeout wrapper
function withTimeout<T>(promise: Promise<T>, timeoutMs: number): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error("Operation timed out")), timeoutMs),
    ),
  ]);
}

// Usage
const user = await withTimeout(fetchUser(id), 5000);
```

## Concurrency Control

### Limit Concurrent Operations

```typescript
class ConcurrencyLimiter {
  private running = 0;
  private queue: Array<() => void> = [];

  constructor(private maxConcurrent: number) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      const run = async () => {
        this.running++;
        try {
          const result = await fn();
          resolve(result);
        } catch (error) {
          reject(error);
        } finally {
          this.running--;
          if (this.queue.length > 0) {
            const next = this.queue.shift()!;
            next();
          }
        }
      };

      if (this.running < this.maxConcurrent) {
        run();
      } else {
        this.queue.push(run);
      }
    });
  }
}

// Usage
const limiter = new ConcurrencyLimiter(5);
const results = await Promise.all(
  items.map((item) => limiter.execute(() => processItem(item))),
);
```

### Batch Processing

```typescript
async function processBatch<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  batchSize: number = 10,
): Promise<R[]> {
  const results: R[] = [];

  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map((item) => processor(item)),
    );
    results.push(...batchResults);
  }

  return results;
}

// Usage
const processed = await processBatch(orders, processOrder, 5);
```

## Race Conditions

### Prevent Race Conditions

```typescript
// ❌ Bad - Race condition
let counter = 0;
async function increment() {
  const current = counter;
  await someAsyncOperation();
  counter = current + 1; // Race condition!
}

// ✅ Good - Use locks
import { Mutex } from "async-mutex";

const mutex = new Mutex();
let counter = 0;

async function increment() {
  const release = await mutex.acquire();
  try {
    const current = counter;
    await someAsyncOperation();
    counter = current + 1;
  } finally {
    release();
  }
}
```

### Atomic Operations

```typescript
// ✅ Good - Use database transactions for atomicity
async function transferFunds(fromId: number, toId: number, amount: number) {
  const transaction = await sequelize.transaction();
  try {
    const fromAccount = await Account.findByPk(fromId, {
      transaction,
      lock: true,
    });
    const toAccount = await Account.findByPk(toId, { transaction, lock: true });

    if (fromAccount.balance < amount) {
      throw new Error("Insufficient funds");
    }

    await fromAccount.update(
      { balance: fromAccount.balance - amount },
      { transaction },
    );
    await toAccount.update(
      { balance: toAccount.balance + amount },
      { transaction },
    );

    await transaction.commit();
  } catch (error) {
    await transaction.rollback();
    throw error;
  }
}
```

## Background Jobs

### Queue-Based Processing

```typescript
import Bull from "bull";

const emailQueue = new Bull("email", {
  redis: { host: "localhost", port: 6379 },
});

// Add job
async function sendEmail(data: EmailData) {
  await emailQueue.add("send-email", data, {
    attempts: 3,
    backoff: {
      type: "exponential",
      delay: 2000,
    },
  });
}

// Process jobs
emailQueue.process("send-email", async (job) => {
  const { to, subject, body } = job.data;
  await emailService.send({ to, subject, body });
});
```

### Scheduled Tasks

```typescript
import cron from "node-cron";

// Run every day at midnight
cron.schedule("0 0 * * *", async () => {
  await cleanupExpiredTokens();
});

// Run every 5 minutes
cron.schedule("*/5 * * * *", async () => {
  await processPendingOrders();
});
```

## Error Handling Patterns

### Retry with Exponential Backoff

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  initialDelay: number = 1000,
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (attempt < maxRetries) {
        const delay = initialDelay * Math.pow(2, attempt);
        await sleep(delay);
      }
    }
  }

  throw lastError!;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
```

### Circuit Breaker

```typescript
class CircuitBreaker {
  private failures = 0;
  private state: "closed" | "open" | "half-open" = "closed";
  private nextAttempt = Date.now();

  constructor(
    private threshold = 5,
    private timeout = 60000,
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === "open") {
      if (Date.now() < this.nextAttempt) {
        throw new Error("Circuit breaker is open");
      }
      this.state = "half-open";
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = "closed";
  }

  private onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = "open";
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
```

## Best Practices

1. **Always handle errors** - Use try-catch with async/await
2. **Use Promise.all for parallel operations** - When operations are independent
3. **Use Promise.allSettled** - When you need all results regardless of failures
4. **Limit concurrency** - Prevent resource exhaustion
5. **Use transactions** - For atomic operations
6. **Implement retry logic** - For transient failures
7. **Use circuit breakers** - Prevent cascading failures
8. **Avoid race conditions** - Use locks or transactions
9. **Process in batches** - For large datasets
10. **Use queues** - For background processing

## When Writing Async Code

1. **Handle errors** - Always wrap in try-catch
2. **Use async/await** - Prefer over promise chains
3. **Execute in parallel** - Use Promise.all when possible
4. **Limit concurrency** - Prevent overwhelming resources
5. **Use transactions** - For data consistency
6. **Implement retries** - For transient failures
7. **Avoid race conditions** - Use proper synchronization
8. **Process in batches** - For large operations
9. **Use queues** - For background jobs
10. **Monitor performance** - Track async operation times
