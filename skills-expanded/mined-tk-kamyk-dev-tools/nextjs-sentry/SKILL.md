---
name: nextjs-sentry
metadata:
  stack: [nextjs]
description: Apply when working with error handling, logging, performance monitoring, exception capture, or adding Sentry instrumentation in a Next.js frontend.
---

# Sentry Integration Patterns

Use these patterns when adding error handling or monitoring to a Next.js frontend with `@sentry/nextjs`.

## Import

Always import Sentry as namespace:

```javascript
import * as Sentry from '@sentry/nextjs'
```

## Configuration Files

Sentry is initialized in these files (do NOT reinitialize elsewhere):

- `instrumentation-client.ts` - Client-side
- `sentry.server.config.ts` - Server-side
- `sentry.edge.config.ts` - Edge runtime

## Init Configuration

Baseline initialization:

```javascript
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: 'https://373aa554a0c73f86a5313447c367cc3e@o4510396298559488.ingest.de.sentry.io/4510396372090960',
  _experiments: {
    enableLogs: true,
  },
})
```

With console logging integration:

```javascript
Sentry.init({
  dsn: 'https://373aa554a0c73f86a5313447c367cc3e@o4510396298559488.ingest.de.sentry.io/4510396372090960',
  integrations: [
    Sentry.consoleLoggingIntegration({ levels: ['log', 'error', 'warn'] }),
  ],
})
```

## Exception Capture

Use in try/catch blocks:

```javascript
try {
  await riskyOperation()
} catch (error) {
  Sentry.captureException(error)
  // Handle error...
}
```

## Span Instrumentation

Create spans for meaningful actions (button clicks, API calls, functions):

### UI Actions

```javascript
const handleClick = () => {
  Sentry.startSpan({ op: 'ui.click', name: 'Submit Button Click' }, (span) => {
    span.setAttribute('formId', formId)
    submitForm()
  })
}
```

### API Calls

```javascript
const fetchUserData = async (userId: string) => {
  return Sentry.startSpan(
    { op: 'http.client', name: `GET /api/users/${userId}` },
    async () => {
      const response = await fetch(`/api/users/${userId}`)
      return response.json()
    }
  )
}
```

## Logging

Reference the logger from Sentry:

```javascript
const { logger } = Sentry

logger.trace('Starting operation', { context: 'value' })
logger.debug(logger.fmt`Processing user: ${userId}`)
logger.info('Operation completed', { result: 'success' })
logger.warn('Rate limit approaching', { current: 95, max: 100 })
logger.error('Operation failed', { error: err.message })
logger.fatal('Critical failure', { service: 'auth' })
```

Use `logger.fmt` template literal for variables in structured logs.

## Span Attributes

Add meaningful attributes:

```javascript
span.setAttribute('userId', userId)
span.setAttribute('operation', 'checkout')
span.setAttribute('amount', total)
```

## Best Practices

- Use meaningful `op` and `name` values
- Add relevant attributes for debugging
- Capture exceptions at error boundaries
- Create spans for user-facing operations
- Log at appropriate levels (don't over-log)
