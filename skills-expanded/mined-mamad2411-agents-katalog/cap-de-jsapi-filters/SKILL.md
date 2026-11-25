---
name: cap-de-jsapi-filters
description: Apply runtime filters to embedded Domo dashboards/cards from the host page via the JS API (MessagePort). Covers dynamic filtering, drill events, filter change listeners, iframe resize, pfilter URL params, overrideFilters, and App Studio appData. Use for any client-side Domo embed interaction. Not for server-side programmatic filters (use cap-de-programmatic-filters).
---

# Domo Client-Side Filters (JS API)

Dynamically filter embedded Domo content from your host page after the embed loads. Unlike server-side programmatic filters (baked into the embed token), client-side filters update instantly without re-fetching tokens.

Use for: UI-driven filtering (dropdowns, date pickers), drill-down responses, syncing filters across multiple embeds, passing context to App Studio apps. For server-side filters, see `cap-de-programmatic-filters`.

## How It Works

Domo iframes communicate with the host page via **MessagePort** (JSON-RPC 2.0):

1. Domo iframe posts a `message` event with a `MessagePort` and `referenceId`
2. Host page captures the port and listens for messages
3. Host sends RPC calls (filters) through the port; Domo sends events (drills, filter changes) back

## Setup

### Step 1: Initialize the JS API Listener

Set up a global listener to capture each iframe's MessagePort handshake.

```typescript
// lib/jsapi.ts

const ports: Record<string, MessagePort> = {};

export interface DomoRpcMessage extends MessageEvent {
  data: {
    referenceId?: string;
    method?: string;
    params?: any;
    result?: any;
    error?: any;
    id?: string;
    jsonrpc?: string;
  };
}

export const initializeJsApi = () => {
  if (typeof window === 'undefined') return;

  const handleMessage = (e: MessageEvent) => {
    if (!e.ports || !e.ports[0]) return;

    const referenceId = e.data?.referenceId;
    if (!referenceId) return;

    const port = e.ports[0];
    port.start();

    // Store the port for sending commands later
    ports[referenceId] = port;

    // Listen for events from this iframe
    port.onmessage = (event: MessageEvent) => {
      const data = event.data;
      if (!data) return;

      if (data.method) {
        handleRpcMethod(referenceId, data.method, data.params);
      }

      if (data.error) {
        console.error(`[JsApi] RPC error (ref: ${referenceId}):`, data.error);
      }
    };
  };

  window.addEventListener('message', handleMessage);

  return () => {
    window.removeEventListener('message', handleMessage);
  };
};
```

### Step 2: Mount the Initializer Early

Mount before any Domo iframe loads (app root). React/Next.js:

```typescript
// components/DomoJsApiInitializer.tsx
'use client'

import { useEffect } from 'react'
import { initializeJsApi } from '@/lib/jsapi'

export default function DomoJsApiInitializer() {
  useEffect(() => {
    const cleanup = initializeJsApi()
    return cleanup
  }, [])

  return null
}
```

Then include it in your root layout:

```tsx
// app/layout.tsx
import DomoJsApiInitializer from './components/DomoJsApiInitializer'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <DomoJsApiInitializer />
        {children}
      </body>
    </html>
  )
}
```

### Step 3: Configure Embed Authorized Domains

Add your host domain to **Admin > Network Security > Embed Authorized Domains** in Domo. Without this, the iframe won't send the handshake `message` event. For custom Domo apps, also add to **Custom Apps Authorized Domains**.

### Step 4: Use Embed Tokens (Not Public URLs)

The JS API only works with authenticated embeds (token-based POST flow). Public embed URLs don't initiate the MessagePort handshake. See `cap-de-programmatic-filters` for the token flow.

---

## Applying Filters

Send `/v1/filters/apply` through the stored MessagePort.

### Filter Structure

Client-side filters use `operand` (**not** `operator` like server-side filters — this is the most common bug):

```typescript
interface ClientFilter {
  column: string;
  operand: string;    // 'IN', 'NOT_IN', 'EQUALS', 'BETWEEN', 'CONTAINS', etc.
  values: any[];
  dataType?: string;      // 'STRING' | 'NUMBER' | 'DATE' — disambiguates values
  dataSourceId?: string;  // target a specific dataset in multi-dataset embeds
}
```

### applyFilters Function

```typescript
export const applyFilters = (
  filters: Array<{ column: string; operand: string; values: any[] }> = []
) => {
  Object.values(ports).forEach(port => {
    port.postMessage({
      id: `filter-${Date.now()}`,
      jsonrpc: '2.0',
      method: '/v1/filters/apply',
      params: {
        filters
      }
    });
  });
};
```

This broadcasts the filters to all connected Domo iframes. To target a specific iframe, use the `referenceId`:

```typescript
export const applyFiltersToEmbed = (
  referenceId: string,
  filters: Array<{ column: string; operand: string; values: any[] }> = []
) => {
  const port = ports[referenceId];
  if (!port) {
    console.warn(`[JsApi] No port found for referenceId: ${referenceId}`);
    return;
  }

  port.postMessage({
    id: `filter-${Date.now()}`,
    jsonrpc: '2.0',
    method: '/v1/filters/apply',
    params: { filters }
  });
};
```

### Examples

**Filter by a single value:**
```typescript
applyFilters([
  { column: 'Region', operand: 'IN', values: ['West'] }
]);
```

**Multiple filters (ANDed together):**
```typescript
applyFilters([
  { column: 'Region', operand: 'IN', values: ['West', 'East'] },
  { column: 'Year', operand: 'EQUALS', values: [2025] }
]);
```

**Clear all filters:**
```typescript
applyFilters([]);
```

### React Example — Filter Dropdown

```tsx
'use client'

import { useState } from 'react'
import { applyFilters } from '@/lib/jsapi'

const regions = ['All', 'West', 'East', 'North', 'South']

export default function RegionFilter() {
  const [selected, setSelected] = useState('All')

  const handleChange = (region: string) => {
    setSelected(region)

    if (region === 'All') {
      applyFilters([])
    } else {
      applyFilters([
        { column: 'Region', operand: 'IN', values: [region] }
      ])
    }
  }

  return (
    <select value={selected} onChange={(e) => handleChange(e.target.value)}>
      {regions.map(r => (
        <option key={r} value={r}>{r}</option>
      ))}
    </select>
  )
}
```

---

## Handling Events from Domo

Domo sends events back through the MessagePort. Use a subscribe/unsubscribe pattern for clean listener management:

```typescript
// Event subscription pattern
type EventCallback = (referenceId: string, params: any) => void;
const listeners: Record<string, Set<EventCallback>> = {};

export function on(event: string, callback: EventCallback): () => void {
  if (!listeners[event]) listeners[event] = new Set();
  listeners[event].add(callback);
  return () => { listeners[event].delete(callback); };
}
```

Then in your `handleRpcMethod`, dispatch to registered listeners. Handle them in a central switch:

```typescript
function handleRpcMethod(referenceId: string, method: string, params: any) {
  switch (method) {
    case '/v1/onDrill':
      handleDrill(referenceId, params);
      break;
    case '/v1/onFiltersChange':
      handleFiltersChange(referenceId, params);
      break;
    case '/v1/onAppReady':
      handleAppReady(referenceId, params);
      break;
    case '/v1/onAppData':
      handleAppData(referenceId, params);
      break;
    case '/v1/onFrameSizeChange':
      handleFrameResize(referenceId, params);
      break;
    default:
      break;
  }
}
```

### `/v1/onDrill` — Drill Events

Fired when a user clicks a drillable element. Includes filters representing the drill path:

```typescript
function handleDrill(referenceId: string, params: any) {
  const drillFilters = params?.filters;
  // drillFilters: [{ column: 'Region', operand: 'IN', values: ['West'] }]

  // Example: apply the drill filters to another embed on the page
  applyFiltersToEmbed('other-embed-ref', drillFilters);

  // Example: navigate to a detail page
  router.push(`/details?region=${drillFilters[0]?.values[0]}`);
}
```

### `/v1/onFiltersChange` — Filter Change Events

Fired when filters change inside the embed (user interaction, card-to-card, or programmatic). Use to sync host UI:

```typescript
function handleFiltersChange(referenceId: string, params: any) {
  const currentFilters = params?.filters;
  // currentFilters: [{ column: 'Region', operand: 'IN', values: ['West'] }]

  // Example: update your app's filter UI to reflect what's selected in Domo
  setActiveFilters(currentFilters);

  // Example: sync filters to another embed
  applyFiltersToEmbed('second-dashboard-ref', currentFilters);
}
```

### `/v1/onAppReady` — App Studio Ready

Fired when an App Studio app finishes loading. Critical with `overrideFilters=true` — send filters only after this event:

```typescript
function handleAppReady(referenceId: string, params: any) {
  // Now safe to send filters and appData
  applyFiltersToEmbed(referenceId, initialFilters);
  sendAppData(referenceId, { customerId: '12345' });
}
```

### `/v1/onAppData` — App Data from Domo

Fired when an App Studio app sends data back to the host:

```typescript
function handleAppData(referenceId: string, params: any) {
  const appData = params?.appData;
  // Handle data sent from the App Studio app
  console.log('App data received:', appData);
}
```

### `/v1/onFrameSizeChange` — Frame Resize

Fired when embed content resizes. Use to adjust iframe container:

```typescript
function handleFrameResize(referenceId: string, params: any) {
  const { width, height } = params || {};
  const iframe = document.querySelector(`iframe[name="${referenceId}"]`);
  if (iframe && height) {
    (iframe as HTMLIFrameElement).style.height = `${height}px`;
  }
}
```

---

## Sending Data to App Studio Apps

Pass arbitrary context to App Studio apps via `/v1/appData/apply`:

```typescript
export const sendAppData = (referenceId: string, appData: any) => {
  const port = ports[referenceId];
  if (!port) return;

  port.postMessage({
    id: `appData-${Date.now()}`,
    jsonrpc: '2.0',
    method: '/v1/appData/apply',
    params: { appData }
  });
};
```

The embedded app receives this via `domo.onAppData()`. Use for passing user IDs, customer context, or preferences.

---

## PFilter URL Parameters

A no-JS alternative: append filters as URL query params. Trade-off: triggers full iframe refresh and filters are visible/modifiable in the URL.

### Structure

```
?pfilters=[{"column":"ColumnName","operand":"OPERATOR","values":["val1","val2"]}]
```

### Example

```
https://example.domo.com/embed/pages/private/ABCDE?pfilters=[{"column":"Region","operand":"IN","values":["West","East"]},{"column":"Year","operand":"EQUALS","values":["2025"],"dataType":"NUMBER"}]
```

### Optional Fields

- `dataSourceId` — target a specific dataset
- `dataType` — `STRING`, `NUMBER`, `DATE`

### When to Use PFilters vs JS API

| | PFilters | JS API |
|---|---------|--------|
| Setup required | None | MessagePort initialization |
| Speed | Slower (iframe refresh) | Instant (no reload) |
| Security | Visible in URL, user-modifiable | Visible in DOM, user-modifiable |
| Multiple updates | Each change refreshes iframe | Updates in place |
| Best for | Simple one-time filters, link sharing | Interactive filtering, dynamic UIs |

**Security warning:** PFilters are visible in the URL and can be modified by end users. They provide no security — use server-side programmatic filters for data isolation.

---

## `overrideFilters` for App Studio

The `overrideFilters=true` URL parameter tells App Studio apps to ignore saved defaults and wait for host-provided filters:

```
https://example.domo.com/embed/pages/private/ABCDE?overrideFilters=true
```

**Behavior:**
- `overrideFilters=true` — app loads with no filters, waits for host to send them
- `overrideFilters=false` or omitted — app loads its saved defaults normally

**Important:** You must send at least one `/v1/filters/apply` (even empty `[]`) or the app stays in a waiting state. Listen for `/v1/onAppReady` first.

```typescript
function handleAppReady(referenceId: string, params: any) {
  // App is ready — send the initial filter state
  applyFiltersToEmbed(referenceId, userFilters.length > 0 ? userFilters : []);
}
```

Other useful URL parameters for embedded content:

| Parameter | Purpose |
|-----------|---------|
| `transparentBackground=true` | Makes dashboard background transparent |
| `appData=value` | Pass initial context to App Studio apps (spaces as `+`) |
| `viewId=abc123` | Specify which App Studio page view to display |

---

## Known RPC Methods

### Host → Domo (Commands)

| Method | Description |
|--------|-------------|
| `/v1/filters/apply` | Apply or clear runtime filters |
| `/v1/appData/apply` | Send context data to App Studio apps |

### Domo → Host (Events)

| Method | Description |
|--------|-------------|
| `/v1/onDrill` | User drilled into a data point |
| `/v1/onFiltersChange` | Filters changed inside the embed |
| `/v1/onAppReady` | App Studio app finished loading, ready for input |
| `/v1/onAppData` | App Studio app sent data back to host |
| `/v1/onFrameSizeChange` | Embedded content changed dimensions |

---

## Combining with Server-Side Filters

- **Server-side:** Security boundary. Enforced by Domo, user cannot bypass. Use for data isolation.
- **Client-side:** UX convenience. User can change. Use for interactive filtering.

Client-side filters narrow within server-side permitted data — they cannot override server-side restrictions.

---

## Gotchas and Best Practices

### Port Availability Timing
Calling `applyFilters` before the handshake completes silently fails. Two approaches:

**Dashboards/cards:** Queue and flush on connect:
```typescript
const pendingFilters: Record<string, Array<{ column: string; operand: string; values: any[] }>> = {};

// When storing the port after handshake, flush pending filters
ports[referenceId] = port;
if (pendingFilters[referenceId]) {
  applyFiltersToEmbed(referenceId, pendingFilters[referenceId]);
  delete pendingFilters[referenceId];
}
```

**App Studio apps:** Listen for `/v1/onAppReady` first, then send filters. Required with `overrideFilters=true`.

### operand vs operator
Client-side uses `operand`, server-side uses `operator`. Mixing them up causes silent failures.

### referenceId Mapping
The `referenceId` is assigned by the Domo iframe — you don't control it. For multiple embeds, correlate handshake timing with render order. For a single embed, use the broadcast `applyFilters()`.

### Operator Typo in Domo API
`GREATER_THAN_EQUALS_TO` sometimes appears as `GREAT_THAN_EQUALS_TO` (missing `ER`). Try both spellings if comparison operators fail.

### Multiple Iframes
Each iframe gets its own port. `applyFilters` broadcasts to all; use `applyFiltersToEmbed` with a specific `referenceId` for independent filtering.

### Public Embeds Don't Support JS API
Only authenticated (token-based) embeds initiate the MessagePort handshake. Public embed URLs don't work.

### Supported Operands
`IN`, `NOT_IN`, `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `GREATER_THAN_EQUALS_TO`, `LESS_THAN`, `LESS_THAN_EQUALS_TO`, `BETWEEN` (exactly two values), `CONTAINS` (partial string match).

### No SQL Filters Client-Side
`/v1/filters/apply` only supports standard filter objects. SQL filters are server-side only.

### Security
Client-side filters and pfilters are for UX only — visible and modifiable by end users. Use server-side programmatic filters for data isolation.

---

## TypeScript Type Definitions

```typescript
type ClientFilterOperand =
  | 'IN'
  | 'NOT_IN'
  | 'EQUALS'
  | 'NOT_EQUALS'
  | 'GREATER_THAN'
  | 'GREATER_THAN_EQUALS_TO'
  | 'LESS_THAN'
  | 'LESS_THAN_EQUALS_TO'
  | 'BETWEEN'
  | 'CONTAINS';

interface ClientFilter {
  column: string;
  operand: ClientFilterOperand;
  values: (string | number | boolean)[];
  dataType?: 'STRING' | 'NUMBER' | 'DATE';
  dataSourceId?: string;
}

interface DomoRpcRequest {
  id: string;
  jsonrpc: '2.0';
  method: string;
  params: Record<string, any>;
}

interface DomoRpcEvent {
  method: string;
  params?: Record<string, any>;
  result?: any;
  error?: { code: number; message: string };
}

interface DrillEventParams {
  filters: ClientFilter[];
}

interface FiltersChangeParams {
  filters: ClientFilter[];
}

interface FrameSizeChangeParams {
  width: number;
  height: number;
}

interface AppDataParams {
  appData: any;
}
```

---

## Quick Reference

Read `references/rpc-methods.md` for the full RPC method reference and message format details.
