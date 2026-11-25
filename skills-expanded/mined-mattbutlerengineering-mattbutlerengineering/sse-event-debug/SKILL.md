# Skill: sse-event-debug

How to triage SSE event divergence in the reservations service.

## Problem Patterns

1. Publisher fired event but subscriber didn't receive it
2. Reservation state machine stuck in transition
3. SSE connection drops unexpectedly

## Debug Workflow

### Step 1: Check SSE Broadcaster State

```bash
# Inspect active SSE connections
curl -s http://localhost:3004/api/v1/events/stream?venueId=<id> -H "Authorization: Bearer $TOKEN" &
# In another terminal, check broadcaster internals
node -e "const { getBroadcaster } = require('./dist/services/sse.js'); console.log(getBroadcaster().getStats());"
```

### Step 2: Verify Event Was Published

```bash
# Check reservation event log in DB
node -e "const { prisma } = require('./dist/services/database.js'); prisma.reservationEvent.findMany({ orderBy: { createdAt: 'desc' }, take: 10 }).then(console.log);"
```

### Step 3: Inspect Reservation State Machine

```typescript
// Check current reservation status
const res = await prisma.reservation.findUnique({
  where: { id: reservationId },
  select: { status: true, updatedAt: true },
});
console.log("State:", res.status, "Updated:", res.updatedAt);
```

## State Machine Transitions

```
PENDING → CONFIRMED (seat guest)
CONFIRMED → COMPLETED (dining finished)
CONFIRMED → CANCELLED (cancelled)
CONFIRMED → NO_SHOW (guest didn't arrive)
```

## Common Fixes

- **Missing subscriber**: Verify `Last-Event-ID` header for resumption
- **Stale connection**: Check exponential backoff (1s, 2s, 4s, ... 30s max)
- **Event dedup**: Verify event ID is unique and monotonic
