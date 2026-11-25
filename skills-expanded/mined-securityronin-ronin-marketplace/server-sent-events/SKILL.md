---
name: server-sent-events
description: Server-Sent Events (SSE) for real-time progress updates in Next.js/Vercel. TransformStream patterns, client consumption, progress tracking.
triggers:
  - sse
  - server-sent events
  - streaming
  - progress updates
  - real-time
  - event stream
---

# Server-Sent Events (SSE)

Real-time server-to-client streaming for progress updates, notifications, and live data feeds.

## When to Use SSE vs Alternatives

| Technology | Use When | Limitations |
|------------|----------|-------------|
| **SSE** | Server → Client only, progress updates, live feeds | Unidirectional, limited connections |
| **WebSockets** | Bidirectional chat, gaming, collaboration | More complex, stateful |
| **Polling** | Simple updates, wide compatibility | Inefficient, latency |
| **HTTP Streaming** | Large file downloads | No structured events |

**Choose SSE for:** Progress bars, status updates, notifications, log streaming, live dashboards.

---

## Next.js App Router Implementation

### Server-Side (Route Handler)

```typescript
// app/api/progress/route.ts
import { NextRequest } from 'next/server'

interface SSEMessage {
  progress: number
  message: string
  status: 'progress' | 'complete' | 'error'
}

export async function POST(req: NextRequest) {
  const body = await req.json()

  // SSE Response Headers
  const headers = {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
  }

  // Create transform stream for SSE
  const stream = new TransformStream()
  const writer = stream.writable.getWriter()
  const encoder = new TextEncoder()

  // Helper to send SSE messages
  async function sendSSE(data: SSEMessage) {
    await writer.write(encoder.encode(`data: ${JSON.stringify(data)}\n\n`))
  }

  // Execute work with progress updates (async, don't await)
  ;(async () => {
    try {
      await sendSSE({ progress: 0, message: 'Starting...', status: 'progress' })

      // Simulate work with progress updates
      for (let i = 1; i <= 10; i++) {
        await doSomeWork(i)
        await sendSSE({
          progress: i * 10,
          message: `Processing step ${i} of 10...`,
          status: 'progress'
        })
      }

      await sendSSE({ progress: 100, message: 'Complete!', status: 'complete' })
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error'
      await sendSSE({ progress: 0, message, status: 'error' })
    } finally {
      await writer.close()
    }
  })()

  return new Response(stream.readable, { headers })
}
```

### Client-Side Consumption

```typescript
// React component
'use client'

import { useState } from 'react'

interface ProgressState {
  progress: number
  message: string
  status: 'idle' | 'progress' | 'complete' | 'error'
}

export function ProgressTracker() {
  const [state, setState] = useState<ProgressState>({
    progress: 0,
    message: '',
    status: 'idle'
  })

  async function startProcess() {
    setState({ progress: 0, message: 'Connecting...', status: 'progress' })

    const response = await fetch('/api/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ /* request data */ })
    })

    if (!response.body) {
      setState({ progress: 0, message: 'No response body', status: 'error' })
      return
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })

      // Parse SSE messages from buffer
      const lines = buffer.split('\n\n')
      buffer = lines.pop() || '' // Keep incomplete message in buffer

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6))
          setState({
            progress: data.progress,
            message: data.message,
            status: data.status
          })
        }
      }
    }
  }

  return (
    <div>
      <button onClick={startProcess} disabled={state.status === 'progress'}>
        Start Process
      </button>
      <progress value={state.progress} max={100} />
      <p>{state.message}</p>
    </div>
  )
}
```

---

## SSE Message Format

### Standard Format

```
data: {"key": "value"}\n\n
```

**Rules:**
- Each message ends with `\n\n` (double newline)
- Data line starts with `data: `
- Multiple data lines allowed per message
- Optional `event:`, `id:`, `retry:` fields

### Named Events

```typescript
// Server
async function sendNamedEvent(event: string, data: object) {
  await writer.write(encoder.encode(
    `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`
  ))
}

// Send different event types
await sendNamedEvent('progress', { percent: 50 })
await sendNamedEvent('log', { message: 'Processing...' })
await sendNamedEvent('complete', { result: 'success' })
```

```typescript
// Client with EventSource (for GET endpoints)
const source = new EventSource('/api/events')

source.addEventListener('progress', (e) => {
  const data = JSON.parse(e.data)
  console.log('Progress:', data.percent)
})

source.addEventListener('complete', (e) => {
  const data = JSON.parse(e.data)
  console.log('Done:', data.result)
  source.close()
})
```

---

## Vercel Considerations

### Critical: Background Task Termination

<EXTREMELY-IMPORTANT>
On Vercel, SSE works differently than traditional servers. The function stays alive while the stream is open, but you must manage the lifecycle carefully.
</EXTREMELY-IMPORTANT>

```typescript
// CORRECT: Stream keeps function alive until closed
;(async () => {
  try {
    // Do all work here
    for (const item of items) {
      await processItem(item)
      await sendSSE({ progress: calculateProgress(item) })
    }
    await sendSSE({ status: 'complete' })
  } finally {
    await writer.close() // MUST close to end function
  }
})()

return new Response(stream.readable, { headers })
```

### Timeout Limits

| Plan | Max Duration |
|------|--------------|
| Hobby | 10 seconds |
| Pro | 60 seconds |
| Enterprise | 900 seconds |

For long operations, consider:
- Breaking into smaller chunks
- Using background jobs (Vercel Cron, external queue)
- Providing estimated time warnings

---

## Progress Patterns

### Percentage-Based

```typescript
interface PercentageProgress {
  progress: number  // 0-100
  message: string
  status: 'progress' | 'complete' | 'error'
}

// Calculate progress for known item count
const total = items.length
for (let i = 0; i < items.length; i++) {
  await processItem(items[i])
  await sendSSE({
    progress: Math.floor(((i + 1) / total) * 100),
    message: `Processing ${i + 1} of ${total}...`,
    status: 'progress'
  })
}
```

### Phase-Based

```typescript
interface PhaseProgress {
  phase: string
  phaseProgress: number
  overallProgress: number
  message: string
}

const phases = [
  { name: 'validate', weight: 10 },
  { name: 'process', weight: 70 },
  { name: 'finalize', weight: 20 },
]

// Track progress across phases
let overallProgress = 0
for (const phase of phases) {
  await sendSSE({
    phase: phase.name,
    phaseProgress: 0,
    overallProgress,
    message: `Starting ${phase.name}...`
  })

  // Do phase work...

  overallProgress += phase.weight
}
```

### Indeterminate with Logs

```typescript
interface LogProgress {
  type: 'log' | 'warning' | 'error' | 'complete'
  message: string
  timestamp: string
}

// For operations where progress can't be calculated
await sendSSE({
  type: 'log',
  message: 'Connecting to external service...',
  timestamp: new Date().toISOString()
})
```

---

## Error Handling

### Server-Side

```typescript
;(async () => {
  try {
    await riskyOperation()
    await sendSSE({ status: 'complete', message: 'Done!' })
  } catch (error) {
    // Always send error to client before closing
    await sendSSE({
      status: 'error',
      message: error instanceof Error ? error.message : 'Unknown error',
      progress: 0
    })
  } finally {
    // ALWAYS close the stream
    await writer.close()
  }
})()
```

### Client-Side

```typescript
async function consumeSSE(url: string, body: object) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      body: JSON.stringify(body)
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    // Process stream...
  } catch (error) {
    // Handle network errors, aborts, etc.
    if (error.name === 'AbortError') {
      console.log('Request cancelled')
    } else {
      console.error('SSE failed:', error)
    }
  }
}
```

### Cancellation

```typescript
// Client with AbortController
const controller = new AbortController()

const response = await fetch('/api/progress', {
  method: 'POST',
  body: JSON.stringify(data),
  signal: controller.signal
})

// Cancel button handler
function handleCancel() {
  controller.abort()
}
```

---

## Real-World Example: Batch Processing

```typescript
// app/api/batch/route.ts
export async function POST(req: NextRequest) {
  const { items } = await req.json()

  const stream = new TransformStream()
  const writer = stream.writable.getWriter()
  const encoder = new TextEncoder()

  const sendSSE = async (data: object) => {
    await writer.write(encoder.encode(`data: ${JSON.stringify(data)}\n\n`))
  }

  ;(async () => {
    const results = { success: 0, failed: 0, errors: [] as string[] }

    try {
      await sendSSE({
        status: 'progress',
        progress: 0,
        message: `Processing ${items.length} items...`
      })

      for (let i = 0; i < items.length; i++) {
        try {
          await processItem(items[i])
          results.success++
        } catch (err) {
          results.failed++
          results.errors.push(`Item ${i}: ${err.message}`)
        }

        await sendSSE({
          status: 'progress',
          progress: Math.floor(((i + 1) / items.length) * 100),
          message: `Processed ${i + 1} of ${items.length}`,
          results: { ...results }
        })
      }

      await sendSSE({
        status: 'complete',
        progress: 100,
        message: `Complete: ${results.success} succeeded, ${results.failed} failed`,
        results
      })
    } catch (error) {
      await sendSSE({
        status: 'error',
        message: error instanceof Error ? error.message : 'Batch failed',
        results
      })
    } finally {
      await writer.close()
    }
  })()

  return new Response(stream.readable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    }
  })
}
```

---

## Quick Reference

```typescript
// Minimal SSE endpoint
export async function POST(req: NextRequest) {
  const stream = new TransformStream()
  const writer = stream.writable.getWriter()
  const encoder = new TextEncoder()

  ;(async () => {
    await writer.write(encoder.encode(`data: {"message":"Hello"}\n\n`))
    await writer.close()
  })()

  return new Response(stream.readable, {
    headers: { 'Content-Type': 'text/event-stream' }
  })
}
```

```typescript
// Minimal client consumption
const res = await fetch('/api/sse', { method: 'POST' })
const reader = res.body!.getReader()
const decoder = new TextDecoder()

while (true) {
  const { done, value } = await reader.read()
  if (done) break
  console.log(decoder.decode(value))
}
```

---

## Resources

- [MDN: Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Vercel: Streaming](https://vercel.com/docs/functions/streaming)
- [Web Streams API](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API)
