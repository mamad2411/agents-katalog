---
description: Run Observability and Monitoring Standards Check
globs:
  [
    '**/monitoring/**/*.ts',
    '**/otel/**/*.ts',
    '**/metrics/**/*.ts',
    'prometheus.yml',
    'grafana/*.json',
  ]
---

# Observability: Monitoring & Observability Standards

<audit_rules>

- You MUST implement structured logging with correlation IDs for distributed tracing across all services.
- You MUST configure OpenTelemetry instrumentation for automatic metrics, traces, and logs collection.
- You MUST define and track key performance indicators (KPIs) and service level objectives (SLOs).
- You MUST implement proper error tracking with stack traces, context, and user impact assessment.
- You MUST configure alerting rules with appropriate thresholds, escalation policies, and on-call rotations.
- You MUST ensure all external dependencies are monitored with circuit breaker patterns and health checks.
- You MUST implement distributed tracing for all API calls and database queries with proper span attributes.
- You MUST configure business metrics tracking for user behavior, conversion funnels, and feature adoption.
- You MUST ensure log aggregation with proper retention policies and searchable indexes.
  </audit_rules>

<example_good>

```typescript
import { trace, metrics, context } from '@opentelemetry/api'
import { logger } from '@/lib/logger'

const tracer = trace.getTracer('payment-service')
const meter = metrics.getMeter('payment-service')

const paymentCounter = meter.createCounter('payment_attempts', {
  description: 'Number of payment attempts',
})

const paymentDuration = meter.createHistogram('payment_duration', {
  description: 'Payment processing duration',
  unit: 'ms',
})

export async function processPayment(paymentData: PaymentData) {
  const span = tracer.startSpan('process_payment', {
    attributes: {
      'payment.amount': paymentData.amount,
      'payment.currency': paymentData.currency,
      'payment.method': paymentData.method,
    },
  })

  const correlationId = context.active().traceId

  try {
    logger.info('Processing payment', {
      correlationId,
      paymentId: paymentData.id,
      amount: paymentData.amount,
    })

    const startTime = Date.now()
    paymentCounter.add(1, { method: paymentData.method })

    const result = await paymentProvider.charge(paymentData)

    paymentDuration.record(Date.now() - startTime, {
      status: result.success ? 'success' : 'failed',
    })

    span.setAttributes({
      'payment.status': result.success ? 'success' : 'failed',
      'payment.transaction_id': result.transactionId,
    })

    logger.info('Payment processed', {
      correlationId,
      paymentId: paymentData.id,
      status: result.success,
      transactionId: result.transactionId,
    })

    return result
  } catch (error) {
    span.recordException(error)
    span.setStatus({ code: SpanStatusCode.ERROR })

    logger.error('Payment processing failed', {
      correlationId,
      paymentId: paymentData.id,
      error: error.message,
      stack: error.stack,
    })

    throw error
  } finally {
    span.end()
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No observability, no structured logging, no metrics
export async function processPayment(paymentData: any) {
  try {
    // BAD: No tracing, no metrics, no correlation ID
    console.log('Processing payment...')

    const result = await paymentProvider.charge(paymentData)

    // BAD: No structured logging, no context
    console.log('Payment done:', result.success)

    return result
  } catch (error) {
    // BAD: No proper error tracking, no context
    console.error('Payment failed:', error.message)
    throw error
  }
}
```

</example_bad>
