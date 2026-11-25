---
name: ts-mcp-server
description: Use when adding MCP tools, modifying the server setup, working with the CatastroGPS API client, handling rate limiting, or structuring tool responses in the MCP server.
metadata:
  author: Dani Roman
  version: "2026.04.08"
  triggers: MCP tool, server.ts, tool registration, catastrogps-api client, rate limit, tool response, get_parcel, get_solar, stdio, SSE
---

> TypeScript MCP Server for CatastroGPS. Each tool in its own file. All HTTP calls through the centralized client. Score and market data are qualitative — no raw formulas.

## Tool Structure

```
src/
  index.ts                   → stdio entry point
  server.ts                  → MCP server setup + tool registration
  sse.ts                     → SSE/HTTP transport
  client/
    catastrogps-api.ts        → Centralized HTTP client — ONLY place for API calls
  tools/
    get-parcel.ts             → Tool: basic parcel data
    get-solar.ts              → Tool: solar potential
    get-agriculture.ts        → Tool: agricultural data
    get-market.ts             → Tool: market data (aggregated only)
    get-score.ts              → Tool: investment score (qualitative factors)
    get-value-history.ts      → Tool: cadastral value history
    compare-parcels.ts        → Tool: compare up to 5 parcels
    shared.ts                 → Shared validation + formatting utilities
  types/
    index.ts                  → TypeScript types
```

## Adding a New Tool

**Step 1** — Create `src/tools/{tool-name}.ts`:

```typescript
// src/tools/get-parcel.ts
import { Tool } from '@anthropic-ai/mcp-sdk';
import { CatastroGPSClient } from '../client/catastrogps-api';
import { validateRefcat, validateCountry } from './shared';

export function createGetParcelTool(client: CatastroGPSClient): Tool {
  return {
    name: 'get_parcel',
    description: 'Get basic parcel data for a cadastral reference',
    inputSchema: {
      type: 'object',
      properties: {
        refcat: {
          type: 'string',
          description: 'Cadastral reference (e.g. "1234567890ABCD01" for Spain)',
        },
        country: {
          type: 'string',
          enum: ['ES', 'PV', 'NA', 'PT', 'FR', 'IT', 'DE'],
          description: 'Country code',
        },
      },
      required: ['refcat', 'country'],
    },
    handler: async (input) => {
      // 1. Validate inputs
      const refcatError = validateRefcat(input.refcat as string, input.country as string);
      if (refcatError) return { error: refcatError };

      // 2. Call API via client
      const parcel = await client.getParcel(input.refcat as string, input.country as string);

      // 3. Return shaped response
      return {
        refcat: parcel.refcat,
        country: parcel.country,
        address: parcel.address,
        area_m2: parcel.areaM2,
        coordinates: { lat: parcel.lat, lon: parcel.lon },
        land_use: parcel.landUse,
        cadastral_value_eur: parcel.cadastralValueEur,
      };
    },
  };
}
```

**Step 2** — Register in `server.ts`:

```typescript
// src/server.ts
import { createGetParcelTool } from './tools/get-parcel';

const client = new CatastroGPSClient(process.env.CATASTROGPS_API_URL!, process.env.CATASTROGPS_API_KEY!);

server.registerTool(createGetParcelTool(client));
```

## CatastroGPS API Client

```typescript
// src/client/catastrogps-api.ts
export class CatastroGPSClient {
  constructor(private baseUrl: string, private apiKey: string) {}

  private async fetch<T>(path: string, params?: Record<string, string>): Promise<T> {
    const url = new URL(`${this.baseUrl}${path}`);
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));

    const res = await fetch(url.toString(), {
      headers: { 'Authorization': `Bearer ${this.apiKey}`, 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`API error ${res.status}: ${await res.text()}`);
    return res.json();
  }

  async getParcel(refcat: string, country: string): Promise<ParcelResponse> {
    return this.fetch<ParcelResponse>(`/api/v1/parcel/${refcat}`, { country });
  }

  async getSolarPotential(refcat: string, country: string): Promise<SolarResponse> {
    return this.fetch<SolarResponse>(`/api/v1/parcel/${refcat}/solar`, { country });
  }
  // ... other endpoints
}
```

## Input Validation (shared.ts)

```typescript
// src/tools/shared.ts
const VALID_COUNTRIES = ['ES', 'PV', 'NA', 'PT', 'FR', 'IT', 'DE'] as const;

export function validateCountry(country: string): string | null {
  if (!VALID_COUNTRIES.includes(country as any)) {
    return `Invalid country. Must be one of: ${VALID_COUNTRIES.join(', ')}`;
  }
  return null;
}

export function validateRefcat(refcat: string, country: string): string | null {
  if (!refcat || refcat.trim().length === 0) return 'refcat is required';
  // Add country-specific format validation as needed
  return null;
}

export function validateParcelList(parcels: string[], max = 5): string | null {
  if (parcels.length === 0) return 'At least one parcel reference required';
  if (parcels.length > max) return `Maximum ${max} parcels allowed`;
  return null;
}
```

## Rate Limiting Rules

- Rate limit per API key, not per user
- Check plan limits: Free 250/mo, Developer 5k, Startup 15k, Growth 50k, Enterprise unlimited
- Return `429` with `{"code": "RATE_LIMIT_EXCEEDED", "plan": "free", "limit": 100}` when exceeded
- Never expose other users' usage data

## Tool Response Rules

| Tool | Rule |
|------|------|
| `get_score` | Return qualitative factors + reasoning, never a numeric formula |
| `get_market` | Return aggregated stats only — never individual transaction prices |
| `compare_parcels` | Return side-by-side comparison object, max 5 parcels |
| All tools | Always include `refcat` and `country` in response for traceability |

## Testing Tools

```typescript
// tests/tools/get-parcel.test.ts
import { createGetParcelTool } from '../../src/tools/get-parcel';

const mockClient = {
  getParcel: jest.fn().mockResolvedValue({
    refcat: '1234567890ABCD01', country: 'ES', lat: 40.41, lon: -3.70,
    areaM2: 1200, landUse: 'residential',
  }),
};

test('get_parcel returns shaped parcel data', async () => {
  const tool = createGetParcelTool(mockClient as any);
  const result = await tool.handler({ refcat: '1234567890ABCD01', country: 'ES' });
  expect(result.coordinates).toEqual({ lat: 40.41, lon: -3.70 });
  expect(mockClient.getParcel).toHaveBeenCalledWith('1234567890ABCD01', 'ES');
});

test('get_parcel rejects invalid country', async () => {
  const tool = createGetParcelTool(mockClient as any);
  const result = await tool.handler({ refcat: 'ABC', country: 'XX' });
  expect(result.error).toMatch(/Invalid country/);
});
```

## Supported Countries

`ES` (Spain), `PV` (País Vasco), `NA` (Navarra), `PT` (Portugal), `FR` (France), `IT` (Italy), `DE` (Germany — NRW only)
