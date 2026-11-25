---
name: error-handling-logging
description: Implement comprehensive error handling and structured logging patterns. Use when handling errors, setting up logging, debugging, or when the user asks about error handling, logging, debugging, or exception handling.
---

# Error Handling & Logging Best Practices

Implement robust error handling and structured logging for production-ready applications.

## Error Types & Hierarchy

### Custom Error Classes

```typescript
// Base error class
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code?: string,
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Specific error types
export class ValidationError extends AppError {
  constructor(
    message: string,
    public errors?: Record<string, string[]>,
  ) {
    super(message, 400, "VALIDATION_ERROR");
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super(
      id ? `${resource} with id ${id} not found` : `${resource} not found`,
      404,
      "NOT_FOUND",
    );
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = "Unauthorized") {
    super(message, 401, "UNAUTHORIZED");
  }
}

export class ForbiddenError extends AppError {
  constructor(message = "Forbidden") {
    super(message, 403, "FORBIDDEN");
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(message, 409, "CONFLICT");
  }
}
```

## Error Handling Patterns

### Try-Catch with Specific Handling

```typescript
async function createUser(data: CreateUserData) {
  try {
    // Validate
    if (!data.email) {
      throw new ValidationError("Email is required", {
        email: ["Email is required"],
      });
    }

    // Check for duplicates
    const existing = await User.findOne({ where: { email: data.email } });
    if (existing) {
      throw new ConflictError("User with this email already exists");
    }

    // Create user
    return await User.create(data);
  } catch (error) {
    // Re-throw known errors
    if (error instanceof AppError) {
      throw error;
    }

    // Handle unexpected errors
    logger.error("Unexpected error creating user", { error, data });
    throw new AppError("Failed to create user", 500, "INTERNAL_ERROR");
  }
}
```

### Error Handler Middleware

```typescript
export const errorHandler = (
  err: Error | AppError,
  req: Request,
  res: Response,
  next: NextFunction,
): Response => {
  const requestId = (req as any).id || "unknown";

  // Log error with context
  logger.error("Request error", {
    requestId,
    path: req.path,
    method: req.method,
    error: {
      name: err.name,
      message: err.message,
      stack: err.stack,
    },
    statusCode: err instanceof AppError ? err.statusCode : 500,
  });

  // Handle known AppError types
  if (err instanceof AppError) {
    if (err instanceof ValidationError) {
      return res.status(err.statusCode).json({
        error: {
          message: err.message,
          code: err.code,
          errors: err.errors,
        },
      });
    }

    return res.status(err.statusCode).json({
      error: {
        message: err.message,
        code: err.code,
      },
    });
  }

  // Handle database errors
  if (err.name === "SequelizeValidationError") {
    const errors: Record<string, string[]> = {};
    (err as any).errors?.forEach((error: any) => {
      const field = error.path || "unknown";
      if (!errors[field]) errors[field] = [];
      errors[field].push(error.message);
    });
    return res.status(400).json({
      error: {
        message: "Validation error",
        code: "VALIDATION_ERROR",
        errors,
      },
    });
  }

  // Default error response
  const message =
    config.env === "production" ? "Internal server error" : err.message;

  return res.status(500).json({
    error: {
      message,
      code: "INTERNAL_ERROR",
      ...(config.env !== "production" && { stack: err.stack }),
    },
  });
};
```

## Structured Logging

### Logger Setup

```typescript
import winston from "winston";

const logFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json(),
);

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  format: logFormat,
  defaultMeta: { service: "api" },
  transports: [
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" }),
  ],
});

if (process.env.NODE_ENV !== "production") {
  logger.add(
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple(),
      ),
    }),
  );
}
```

### Logging Levels

```typescript
// ERROR - System errors, exceptions
logger.error("Database connection failed", { error, host, port });

// WARN - Warning conditions, recoverable errors
logger.warn("Rate limit approaching", { userId, requests: 95, limit: 100 });

// INFO - General informational messages
logger.info("User created", { userId, email });

// DEBUG - Detailed debugging information
logger.debug("Processing request", { requestId, method, path });

// VERBOSE - Very detailed tracing
logger.verbose("Cache hit", { key, ttl });
```

### Structured Logging with Context

```typescript
// Add context to all logs
class ContextLogger {
  private context: Record<string, any> = {};

  setContext(key: string, value: any) {
    this.context[key] = value;
    return this;
  }

  info(message: string, meta?: any) {
    logger.info(message, { ...this.context, ...meta });
  }

  error(message: string, error?: Error, meta?: any) {
    logger.error(message, {
      ...this.context,
      error: error
        ? {
            name: error.name,
            message: error.message,
            stack: error.stack,
          }
        : undefined,
      ...meta,
    });
  }
}

// Usage
const requestLogger = new ContextLogger()
  .setContext("requestId", req.id)
  .setContext("userId", req.user?.id);

requestLogger.info("Processing order", { orderId: 123 });
```

## Request Tracing

### Request ID Middleware

```typescript
import { v4 as uuidv4 } from "uuid";

export const requestIdMiddleware = (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  const requestId = (req.headers["x-request-id"] as string) || uuidv4();
  (req as any).id = requestId;
  res.setHeader("X-Request-ID", requestId);
  next();
};
```

### Correlation IDs

```typescript
// Pass correlation ID through async operations
async function processOrder(orderId: string, correlationId: string) {
  logger.info("Processing order", { orderId, correlationId });

  // Pass to downstream services
  await emailService.send({
    to: user.email,
    subject: "Order confirmed",
    correlationId,
  });

  await paymentService.charge({
    amount: order.total,
    correlationId,
  });
}
```

## Error Recovery Patterns

### Retry with Exponential Backoff

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  initialDelay = 1000,
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (attempt < maxRetries) {
        const delay = initialDelay * Math.pow(2, attempt);
        logger.warn(`Retry attempt ${attempt + 1} after ${delay}ms`, { error });
        await sleep(delay);
      }
    }
  }

  throw lastError!;
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
      logger.error("Circuit breaker opened", { failures: this.failures });
    }
  }
}
```

## User-Friendly Error Messages

### Transform Technical Errors

```typescript
function getUserFriendlyMessage(error: Error): string {
  if (error instanceof ValidationError) {
    return "Please check your input and try again";
  }

  if (error instanceof NotFoundError) {
    return "The requested resource was not found";
  }

  if (error.message.includes("ECONNREFUSED")) {
    return "Service temporarily unavailable. Please try again later";
  }

  if (error.message.includes("timeout")) {
    return "Request timed out. Please try again";
  }

  return "An unexpected error occurred. Please try again later";
}
```

## Best Practices

1. **Use specific error types** - Create custom error classes
2. **Log with context** - Include request ID, user ID, etc.
3. **Never expose internals** - Hide stack traces in production
4. **Handle errors at boundaries** - Catch at API boundaries
5. **Use structured logging** - JSON format for parsing
6. **Include correlation IDs** - Trace requests across services
7. **Implement retry logic** - For transient failures
8. **Use circuit breakers** - Prevent cascading failures
9. **Provide user-friendly messages** - Don't expose technical details
10. **Monitor error rates** - Set up alerts for high error rates

## When Handling Errors

1. **Catch specific errors** - Handle known error types
2. **Log before throwing** - Capture context before re-throwing
3. **Transform errors** - Convert technical errors to user-friendly messages
4. **Include request context** - Request ID, user ID, etc.
5. **Don't swallow errors** - Always handle or re-throw
6. **Use appropriate status codes** - Match HTTP status to error type
7. **Provide actionable messages** - Tell users what went wrong
8. **Log at appropriate levels** - ERROR for errors, WARN for warnings
