---
name: aws-lambda-serverless
description: Builds AWS Lambda functions that handle cold starts, timeouts, memory sizing and retries, with idempotent handlers and clear failure paths.
---

# AWS Lambda serverless

Write for the Lambda lifecycle: cold start, warm reuse, retry and timeout.

## Steps

1. Identify the trigger and its retry behavior. Async invokes and SQS retry; API Gateway does not. Decide what a duplicate event does.
2. Create clients, load config and open connections outside the handler so warm invocations reuse them. Keep imports lean and import only the SDK clients you use.
3. Make the handler idempotent: derive an idempotency key from the event (message ID, request ID or business key) and record it with a conditional write (`attribute_not_exists`) before the side effect.
4. Set the timeout below the upstream limit (API Gateway allows 29 seconds) and use `context.getRemainingTimeInMillis()` to stop long loops early. For SQS, set the queue visibility timeout to at least six times the function timeout.
5. Pick memory by measurement: run the function at 256, 512, 1024 and 2048 MB and choose the cheapest option that meets the latency goal. CPU scales with memory.
6. Configure failure handling: a dead-letter queue or on-failure destination, `ReportBatchItemFailures` for SQS batches, and a bounded retry count.
7. Log one structured JSON line per invocation with the request ID, outcome and duration. Never log full payloads with personal data.
8. Package small: bundle and tree-shake, and move shared code to a layer only if several functions use it.

## Rules

- Never store state in memory between invocations and depend on it.
- Never use unbounded recursion between Lambdas.

## Report

Trigger and retry model, idempotency key, timeout and memory chosen with the measurements behind them.
