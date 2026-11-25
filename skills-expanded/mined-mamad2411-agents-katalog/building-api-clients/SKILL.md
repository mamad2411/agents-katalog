---
name: building-api-clients
description: "Type-safe API clients: HTTP client, Zod validation, Result pattern, Swagger codegen. Use when creating API integrations or working with backend services. ALWAYS load this skill when working with APIs in react clients"
---

# Building Type-Safe API Clients

## 1. Architecture Overview

```
Feature API Layer (hello-api.ts, items-api.ts)
  | imports
Global API Layer (src/lib/api/)
  - api-client.ts        (typedGet/Post/Put/Delete, apiRequestWrapper)
  - api.types.ts         (ApiResult, ApiError, ErrorCode)
  - error-handler.ts     (extractMessage, dev error toasts)
  - query-utils.ts       (query strings, pagination)
  - validation-utils.ts  (Zod validation helpers)
  | fetch()
Backend API
```

Feature API files live alongside the feature they serve (e.g., `src/mfes/items/api/items-api.ts`). They import shared utilities from the global API layer at `src/lib/api/`. The global layer handles HTTP mechanics, error normalization, and validation. Feature layers handle endpoint-specific logic, Zod schemas, and type exports.

---

## 2. Core Types

### Result Pattern

```typescript
// src/lib/result.ts
export type Result<T, E> =
  | { readonly success: true; readonly data: T }
  | { readonly success: false; readonly error: E };

// src/lib/api/api.types.ts
import { Result } from '../result';

export type ApiResult<T> = Result<T, ApiError>;
```

### ApiError

```typescript
export type ApiError = Readonly<{
  code: ErrorCode;
  message: string;
  fields?: FieldErrors;
  status?: number;
  details?: unknown;
  url?: string;
}>;

export interface FieldErrors {
  readonly [fieldName: string]: readonly string[];
}
```

### ErrorCode

```typescript
export type ErrorCode =
  | 'VALIDATION_ERROR'
  | 'NETWORK_ERROR'
  | 'SERVER_ERROR'
  | 'RATE_LIMITED'
  | string;
```

`ErrorCode` is an open union (`| string`) — the backend may return additional codes beyond the known set. Every API call returns `ApiResult<T>`. Callers never catch exceptions from the API layer — they check `result.success` instead.

---

## 3. API Client Functions

### Typed HTTP Methods

| Function | Signature | Notes |
|---|---|---|
| `typedGet` | `typedGet<T>(url: string, additionalHeaders?: Record<string, string>): Promise<T>` | GET request |
| `typedPost` | `typedPost<T>(url: string, data?: unknown): Promise<T>` | POST |
| `typedPut` | `typedPut<T>(url: string, data?: unknown): Promise<T>` | PUT |
| `typedPatch` | `typedPatch<T>(url: string, data?: unknown): Promise<T>` | PATCH |
| `typedDelete` | `typedDelete<T>(url: string, data?: unknown): Promise<T>` | DELETE |
| `apiRequestWrapper` | `apiRequestWrapper<T>(request: () => Promise<T>): Promise<ApiResult<T>>` | Wraps async logic, catches all errors, returns `ApiResult<T>` |

### makeRequest Implementation Pattern

```typescript
// src/lib/api/api-client.ts

import { env } from '@/env';
import type { ApiError, ErrorCode } from './api.types';
import { extractMessage } from './error-handler';

async function makeRequest<T>(
  url: string,
  method = 'GET',
  body?: unknown,
  additionalHeaders?: Record<string, string>
): Promise<T> {
  const baseUrl = env.NEXT_PUBLIC_API_URL;
  const fullUrl = url.startsWith('http') ? url : `${baseUrl}${url}`;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(additionalHeaders ?? {})
  };

  let response: Response;
  try {
    response = await fetch(fullUrl, {
      method,
      headers,
      credentials: 'include',
      signal: AbortSignal.timeout(30000),
      ...(body !== undefined ? { body: JSON.stringify(body) } : {})
    });
  } catch (error) {
    const cleanUrl = getCleanUrl(url);

    if (error instanceof Error && error.name === 'AbortError') {
      throw {
        code: 'NETWORK_ERROR' as ErrorCode,
        message: 'Server response timeout exceeded',
        status: 408,
        url: cleanUrl
      };
    }
    throw {
      code: 'NETWORK_ERROR' as ErrorCode,
      message: 'Failed to connect to server. Check your internet connection',
      status: 0,
      url: cleanUrl
    };
  }

  // Read body as text first, then parse JSON if applicable
  const contentType = response.headers.get('content-type');
  let responseData: unknown;
  const rawBody = await response.text();

  if (contentType?.includes('application/json')) {
    try {
      responseData = JSON.parse(rawBody);
    } catch {
      responseData = rawBody;
    }
  } else {
    responseData = rawBody;
  }

  // Check for error responses (HTTP errors or { success: false } in body)
  const responseObj =
    responseData !== null &&
    typeof responseData === 'object' &&
    !Array.isArray(responseData)
      ? (responseData as Record<string, unknown>)
      : null;

  const isErrorResponse =
    !response.ok ||
    (responseObj !== null &&
      'success' in responseObj &&
      typeof responseObj.success === 'boolean' &&
      !responseObj.success);

  if (isErrorResponse) {
    const errorData = responseObj ?? {};
    const cleanUrl = getCleanUrl(url);

    throw {
      code: (errorData.errorCode ?? errorData.code ?? 'SERVER_ERROR') as ErrorCode,
      message: extractMessage(errorData, response.status),
      status: response.status,
      details: rawBody,
      url: cleanUrl
    };
  }

  return responseData as T;
}
```

### Typed HTTP Wrappers

```typescript
export async function typedGet<T>(
  url: string,
  additionalHeaders?: Record<string, string>
): Promise<T> {
  return makeRequest<T>(url, 'GET', undefined, additionalHeaders);
}

export async function typedPost<T>(url: string, data?: unknown): Promise<T> {
  return makeRequest<T>(url, 'POST', data);
}

export async function typedPut<T>(url: string, data?: unknown): Promise<T> {
  return makeRequest<T>(url, 'PUT', data);
}

export async function typedPatch<T>(url: string, data?: unknown): Promise<T> {
  return makeRequest<T>(url, 'PATCH', data);
}

export async function typedDelete<T>(url: string, data?: unknown): Promise<T> {
  return makeRequest<T>(url, 'DELETE', data);
}
```

### apiRequestWrapper

This is the boundary between "throwing world" and "Result world". Everything inside the callback can throw. The wrapper catches all exceptions and returns `ApiResult<T>`. In development mode, it automatically shows error toasts via `showDevErrorToast`:

```typescript
import { showDevErrorToast } from './error-handler';

async function apiRequestWrapper<T>(
  request: () => Promise<T>
): Promise<ApiResult<T>> {
  try {
    return { success: true, data: await request() };
  } catch (error) {
    let apiError: ApiError;

    if (
      error !== null &&
      error !== undefined &&
      typeof error === 'object' &&
      'code' in error &&
      'message' in error &&
      typeof (error as ApiError).code === 'string' &&
      typeof (error as ApiError).message === 'string'
    ) {
      apiError = error as ApiError;
    } else {
      apiError = {
        code: 'REQUEST_UNKNOWN_ERROR',
        message: 'Unknown error occurred'
      };
    }

    const result: ApiResult<T> = { success: false, error: apiError };

    // Show toast notification in development mode
    showDevErrorToast(result);

    return result;
  }
}
```

### Error Handler

```typescript
// src/lib/api/error-handler.ts

import { toast } from 'sonner';
import type { ApiResult } from './api.types';

export function extractMessage(
  errorData: Record<string, unknown>,
  status?: number
): string {
  // Checks errorData.message, errorData.error, errorData.title (RFC 9110),
  // then falls back to status-based messages
  const msg = errorData.message;
  if (typeof msg === 'string' && msg.trim() !== '') {
    return msg.trim();
  }
  // ... fallback logic for status codes
  return 'An error occurred. Please try again';
}

/**
 * Shows toast notification for API errors in development mode.
 * Called automatically by apiRequestWrapper — no need to call manually.
 */
export function showDevErrorToast<T>(result: ApiResult<T>): void {
  if (
    !result.success &&
    typeof window !== 'undefined' &&
    process.env.NODE_ENV === 'development'
  ) {
    const url = result.error.url ?? 'Unknown endpoint';
    toast.error(`Request failed: ${url}`, {
      description: `${result.error.code}: ${result.error.message}`
    });
  }
}
```

---

## 4. Creating Feature API Clients (Complete Pattern)

Every feature API file follows the same structure: import shared utilities, define endpoint functions using `apiRequestWrapper`, validate responses with Zod, and export as a namespace object.

```typescript
// src/mfes/hello-world/api/hello-api.ts

import { z } from 'zod';

import { apiRequestWrapper, typedGet, typedPost } from '@/lib/api/api-client';
import type { ApiResult } from '@/lib/api/api.types';
import { handleZodValidationOrThrow } from '@/lib/api/validation-utils';

import {
  getApiHelloResponse,
  postApiHelloBody,
  postApiHelloResponse
} from './generated/hello/hello';

// Infer TypeScript types from Zod schemas
export type HelloResponse = z.infer<typeof getApiHelloResponse>;
export type PostHelloBody = z.infer<typeof postApiHelloBody>;
export type PostHelloResponse = z.infer<typeof postApiHelloResponse>;

// --- GET /api/hello ---
async function getHello(): Promise<ApiResult<HelloResponse>> {
  return apiRequestWrapper(async () => {
    const response: unknown = await typedGet<unknown>('/api/hello');
    return handleZodValidationOrThrow(
      getApiHelloResponse.safeParse(response),
      'getHello'
    );
  });
}

// --- POST /api/hello ---
async function postHello(
  body: PostHelloBody
): Promise<ApiResult<PostHelloResponse>> {
  return apiRequestWrapper(async () => {
    const validatedBody = handleZodValidationOrThrow(
      postApiHelloBody.safeParse(body),
      'postHello: body'
    );
    const response: unknown = await typedPost<unknown>(
      '/api/hello',
      validatedBody
    );
    return handleZodValidationOrThrow(
      postApiHelloResponse.safeParse(response),
      'postHello'
    );
  });
}

// Export as namespace object
export const helloApi = { getHello, postHello };
```

Key points:
- `typedGet<unknown>` -- the raw response is untyped until Zod validates it
- `handleZodValidationOrThrow` -- throws on validation failure; `apiRequestWrapper` catches it and returns `ApiResult`
- Export as `const helloApi = { ... }` so consumers import a single namespace

---

## 5. Common Request Patterns

### GET Request

```typescript
async function getItem(id: string): Promise<ApiResult<ItemResponse>> {
  return apiRequestWrapper(async () => {
    const response: unknown = await typedGet<unknown>(`/api/items/${id}`);
    return handleZodValidationOrThrow(
      getApiItemResponse.safeParse(response),
      'getItem'
    );
  });
}
```

### POST with Body

```typescript
async function createItem(body: CreateItemBody): Promise<ApiResult<ItemResponse>> {
  return apiRequestWrapper(async () => {
    const validatedBody = handleZodValidationOrThrow(
      postApiItemsBody.safeParse(body),
      'createItem: body'
    );
    const response: unknown = await typedPost<unknown>('/api/items', validatedBody);
    return handleZodValidationOrThrow(
      getApiItemResponse.safeParse(response),
      'createItem'
    );
  });
}
```

### GET with Query Parameters

```typescript
import { buildQueryString } from '@/lib/api/query-utils';

async function searchItems(params: SearchParams): Promise<ApiResult<PaginatedItems>> {
  return apiRequestWrapper(async () => {
    const query = buildQueryString({
      search: params.search,
      page: params.page,
      pageSize: params.pageSize,
      sortBy: params.sortBy,
    });
    const response: unknown = await typedGet<unknown>(`/api/items${query}`);
    return handleZodValidationOrThrow(
      paginatedItemsResponse.safeParse(response),
      'searchItems'
    );
  });
}
```

### PUT / PATCH

```typescript
async function updateItem(
  id: string,
  body: UpdateItemBody
): Promise<ApiResult<ItemResponse>> {
  return apiRequestWrapper(async () => {
    const validatedBody = handleZodValidationOrThrow(
      updateItemBodySchema.safeParse(body),
      'updateItem: body'
    );
    const response: unknown = await typedPut<unknown>(
      `/api/items/${id}`,
      validatedBody
    );
    return handleZodValidationOrThrow(
      getApiItemResponse.safeParse(response),
      'updateItem'
    );
  });
}

async function patchItem(
  id: string,
  body: Partial<UpdateItemBody>
): Promise<ApiResult<ItemResponse>> {
  return apiRequestWrapper(async () => {
    const response: unknown = await typedPatch<unknown>(`/api/items/${id}`, body);
    return handleZodValidationOrThrow(
      getApiItemResponse.safeParse(response),
      'patchItem'
    );
  });
}
```

### DELETE

```typescript
async function deleteItem(id: string): Promise<ApiResult<void>> {
  return apiRequestWrapper(async () => {
    await typedDelete<void>(`/api/items/${id}`);
    return undefined;
  });
}
```

---

## 6. Zod Validation Pattern

### Rules

1. **Always `safeParse()`, never `parse()`** -- we want a Result, not an exception at the call site. The throw happens inside `apiRequestWrapper` where it gets caught and converted to `ApiResult`.
2. **Validate both request bodies and response data** -- never trust either direction.
3. **Infer TypeScript types from Zod schemas** -- single source of truth.

### handleZodValidationOrThrow

```typescript
// src/lib/api/validation-utils.ts

import type { ErrorCode } from './api.types';
import type { ZodError } from 'zod';

function formatZodError(error: ZodError): string {
  return error.issues
    .map((issue) => {
      const path = issue.path.length > 0 ? issue.path.join('.') : 'root';
      return `${path} (${issue.code}): ${issue.message}`;
    })
    .join('; ');
}

export function handleZodValidationOrThrow<TInput, TOutput>(
  parseResult:
    | { success: true; data: TOutput }
    | { success: false; error: ZodError<TInput> },
  validationName: string
): TOutput {
  if (parseResult.success === false) {
    const error = parseResult.error;

    // Log validation errors in development
    if (
      typeof window !== 'undefined' &&
      process.env.NODE_ENV === 'development'
    ) {
      console.error(
        `%c[zod validation] ${validationName} failed`,
        'color: red; font-weight: bold;',
        formatZodError(error)
      );
    }

    // Throw a validation error — caught by apiRequestWrapper
    throw {
      code: 'VALIDATION_ERROR' as ErrorCode,
      message: `Zod validation failed for ${validationName}: ${formatZodError(error)}`,
      status: 200, // HTTP was 200, but validation failed
      details: error.issues
    };
  }

  return parseResult.data;
}
```

### Type Inference from Schemas

```typescript
import { z } from 'zod';

// Define schema (or import from generated code)
const itemSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  quantity: z.number().int().nonneg(),
  createdAt: z.string().datetime(),
});

// Infer the TypeScript type -- never define the type manually
type Item = z.infer<typeof itemSchema>;
// Result: { id: string; name: string; quantity: number; createdAt: string }

// For arrays
const itemsResponseSchema = z.array(itemSchema);
type ItemsResponse = z.infer<typeof itemsResponseSchema>;
```

### Validation Flow

```
Raw response (unknown)
  | safeParse(response)
  |
  +-- success: true  --> return validated data (typed as TOutput)
  +-- success: false --> throw { code: 'VALIDATION_ERROR', ... }
                          --> caught by apiRequestWrapper
                          --> returned as ApiResult with success: false
```

---

## 7. Swagger to Zod Codegen (Orval)

Orval generates Zod schemas from OpenAPI/Swagger specs. This keeps API types in sync with the backend automatically.

### Configuration

```typescript
// scripts/api-codegen/config.ts

export const CODEGEN_CONFIG: CodegenConfig[] = [
  {
    name: 'items',
    swaggerFilters: { tags: ['Items'] },
    outputPath: '../../src/mfes/items/api/generated',
  },
  {
    name: 'hello',
    swaggerFilters: { tags: ['Hello'] },
    outputPath: '../../src/mfes/hello-world/api/generated',
  },
];
```

### Generate Schemas

```bash
# Generate schemas for a specific API
pnpm api:gen items

# Generate all schemas
pnpm api:gen

# This creates files like:
# src/mfes/items/api/generated/items/items.ts
#   - getApiItemsResponse (Zod schema for GET /api/items response)
#   - postApiItemsBody    (Zod schema for POST /api/items request body)
#   - getApiItemByIdResponse (Zod schema for GET /api/items/:id response)
#   ... etc.
```

### Usage with Generated Schemas

```typescript
// Import generated schemas
import {
  getApiItemsResponse,
  postApiItemsBody,
  getApiItemByIdResponse,
} from './generated/items/items';

// Infer types from generated schemas
export type ItemsResponse = z.infer<typeof getApiItemsResponse>;
export type CreateItemBody = z.infer<typeof postApiItemsBody>;
export type ItemByIdResponse = z.infer<typeof getApiItemByIdResponse>;
```

### When to Regenerate

- Backend adds or changes endpoints
- Backend modifies request/response shapes
- Swagger spec is updated
- After pulling changes that update the OpenAPI spec

Generated files should be committed to the repository. Do not edit them manually -- they will be overwritten on next generation.

---

## 8. Query and Pagination Utilities

### buildQueryString

```typescript
// src/lib/api/query-utils.ts

export type QueryValue = string | number | boolean | Date | null | undefined;

export function buildQueryString(params: Record<string, QueryValue>): string {
  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null) {
      return;
    }

    const normalized = value instanceof Date ? value.toISOString() : value;
    if (normalized === '') {
      return;
    }

    searchParams.set(key, String(normalized));
  });

  const result = searchParams.toString();
  return result.length > 0 ? `?${result}` : '';
}
```

Usage:

```typescript
buildQueryString({ search: 'widget', page: 1, pageSize: 20, category: undefined });
// => '?search=widget&page=1&pageSize=20'

buildQueryString({});
// => ''
```

### Pagination Normalizer

```typescript
// src/lib/api/query-utils.ts

export interface PaginatedResponseWithNullableItems<Item> {
  readonly items?: readonly Item[] | null;
  readonly totalCount: number;
  readonly page: number;
  readonly pageSize: number;
  readonly totalPages?: number;
}

export interface PaginatedResultLike<Item> {
  readonly items: readonly Item[];
  readonly totalCount: number;
  readonly page: number;
  readonly pageSize: number;
  readonly totalPages?: number;
}

/**
 * Maps a raw paginated API response into a normalized shape.
 * Handles backends that return nullable/optional items arrays.
 */
export function mapPaginatedResult<Item, Output = Item>(
  parsed: PaginatedResponseWithNullableItems<Item>,
  mapItem?: (item: Item) => Output
): PaginatedResultLike<Output> {
  const mapper: (item: Item) => Output =
    mapItem ?? ((item: Item) => item as unknown as Output);
  const items = (parsed.items ?? []).map(mapper);

  return {
    items,
    totalCount: parsed.totalCount,
    page: parsed.page,
    pageSize: parsed.pageSize,
    totalPages: parsed.totalPages
  };
}
```

---

## 9. Best Practices

### DO

1. **Always wrap with `apiRequestWrapper()`** -- every feature API function must return `ApiResult<T>`, never throw.
2. **Validate all params and responses with Zod** -- use `safeParse()` + `handleZodValidationOrThrow` inside the wrapper.
3. **Handle both Result branches** -- always check `result.success` before accessing `result.data` or `result.error`.
4. **Export API as namespace object** -- `export const itemsApi = { getItems, createItem, ... }` for clean imports.
5. **Use relative paths for endpoints** -- `/api/items`, not `https://example.com/api/items`. The base URL is handled by `makeRequest`.
6. **Infer types from Zod schemas** -- `z.infer<typeof schema>` is the single source of truth.
7. **Use the early return pattern** when consuming results:

```typescript
const result = await itemsApi.getItems();
if (!result.success) {
  handleError(result.error);
  return;
}
// success path at top-level indentation
processItems(result.data);
```

### DON'T

1. **Don't throw exceptions from feature API functions** -- return `ApiResult<T>`. The only place throws are acceptable is inside `apiRequestWrapper`'s callback (they get caught).
2. **Don't skip Zod validation** -- even if "the backend is trusted." Schemas catch breaking changes, typos, and drift.
3. **Don't hardcode base URLs** -- use `env.NEXT_PUBLIC_API_URL` via the global client.
4. **Don't access error fields without checking `result.success`** -- TypeScript narrows the union, but only after the check.
5. **Don't use `parse()` at the API boundary** -- use `safeParse()` + `handleZodValidationOrThrow` so errors flow through the Result pattern.
6. **Don't manually define types that duplicate Zod schemas** -- use `z.infer<typeof schema>` instead.

---

## 10. Bootstrap a New Feature API (Step-by-step)

### Step 1: Configure Codegen

Add entry in `scripts/api-codegen/config.ts`:

```typescript
{
  name: 'orders',
  swaggerFilters: { tags: ['Orders'] },
  outputPath: '../../src/mfes/orders/api/generated',
}
```

### Step 2: Generate Schemas

```bash
pnpm api:gen orders
```

This creates Zod schemas in `src/mfes/orders/api/generated/orders/orders.ts`.

### Step 3: Create Feature API Client

```typescript
// src/mfes/orders/api/orders-api.ts

import { z } from 'zod';

import { apiRequestWrapper, typedGet, typedPost, typedPut } from '@/lib/api/api-client';
import { buildQueryString } from '@/lib/api/query-utils';
import { handleZodValidationOrThrow } from '@/lib/api/validation-utils';

import type { ApiResult } from '@/lib/api/api.types';
import {
  getApiOrdersResponse,
  getApiOrderByIdResponse,
  postApiOrdersBody,
  putApiOrderByIdBody,
} from './generated/orders/orders';

export type OrdersResponse = z.infer<typeof getApiOrdersResponse>;
export type OrderResponse = z.infer<typeof getApiOrderByIdResponse>;
export type CreateOrderBody = z.infer<typeof postApiOrdersBody>;
export type UpdateOrderBody = z.infer<typeof putApiOrderByIdBody>;

async function getOrders(params?: {
  readonly page?: number;
  readonly pageSize?: number;
  readonly status?: string;
}): Promise<ApiResult<OrdersResponse>> {
  return apiRequestWrapper(async () => {
    const query = buildQueryString({
      page: params?.page,
      pageSize: params?.pageSize,
      status: params?.status,
    });
    const response: unknown = await typedGet<unknown>(`/api/orders${query}`);
    return handleZodValidationOrThrow(
      getApiOrdersResponse.safeParse(response),
      'getOrders'
    );
  });
}

async function getOrderById(id: string): Promise<ApiResult<OrderResponse>> {
  return apiRequestWrapper(async () => {
    const response: unknown = await typedGet<unknown>(`/api/orders/${id}`);
    return handleZodValidationOrThrow(
      getApiOrderByIdResponse.safeParse(response),
      'getOrderById'
    );
  });
}

async function createOrder(body: CreateOrderBody): Promise<ApiResult<OrderResponse>> {
  return apiRequestWrapper(async () => {
    const validatedBody = handleZodValidationOrThrow(
      postApiOrdersBody.safeParse(body),
      'createOrder: body'
    );
    const response: unknown = await typedPost<unknown>('/api/orders', validatedBody);
    return handleZodValidationOrThrow(
      getApiOrderByIdResponse.safeParse(response),
      'createOrder'
    );
  });
}

async function updateOrder(
  id: string,
  body: UpdateOrderBody
): Promise<ApiResult<OrderResponse>> {
  return apiRequestWrapper(async () => {
    const validatedBody = handleZodValidationOrThrow(
      putApiOrderByIdBody.safeParse(body),
      'updateOrder: body'
    );
    const response: unknown = await typedPut<unknown>(
      `/api/orders/${id}`,
      validatedBody
    );
    return handleZodValidationOrThrow(
      getApiOrderByIdResponse.safeParse(response),
      'updateOrder'
    );
  });
}

export const ordersApi = { getOrders, getOrderById, createOrder, updateOrder };
```

### Step 4: Create Store

Map `ApiResult` to `StoreResult` in the Zustand store (see `managing-state` skill for full pattern):

```typescript
// src/mfes/orders/stores/orders-store.ts

import { create } from 'zustand';

import { ordersApi } from '../api/orders-api';

import type { ApiResult } from '@/lib/api/api.types';
import type { Result } from '@/lib/result';
import type { OrdersResponse } from '../api/orders-api';

// Store-specific types (see managing-state skill for full pattern)
type StoreError = Readonly<{ message: string; details?: unknown }>;
type StoreResult<T> = Result<T, StoreError>;
type StoreErrorState = Readonly<{ error: StoreError; errorMessageForUser: string }>;

function mapApiResultToStoreResult<T>(apiResult: ApiResult<T>): StoreResult<T> {
  if (apiResult.success) {
    return { success: true, data: apiResult.data };
  }
  return {
    success: false,
    error: { message: apiResult.error.message, details: apiResult.error },
  };
}

interface OrdersStore {
  readonly orders: OrdersResponse | null;
  readonly loading: boolean;
  readonly error: StoreErrorState | null;
  readonly fetchOrders: () => Promise<void>;
}

export const useOrdersStore = create<OrdersStore>((set) => ({
  orders: null,
  loading: false,
  error: null,
  fetchOrders: async (): Promise<void> => {
    set({ loading: true, error: null });
    const apiResult = await ordersApi.getOrders();
    const result = mapApiResultToStoreResult(apiResult);
    if (!result.success) {
      set({
        loading: false,
        error: {
          error: result.error,
          errorMessageForUser: 'Failed to load orders',
        },
      });
      return;
    }
    set({ loading: false, orders: result.data });
  },
}));
```

### Step 5: Use in Components

```tsx
// src/mfes/orders/components/OrderList.tsx

import { useEffect } from 'react';

import { useOrdersStore } from '../stores/orders-store';

export function OrderList(): JSX.Element {
  const { orders, loading, error, fetchOrders } = useOrdersStore();

  useEffect(() => {
    void fetchOrders();
  }, [fetchOrders]);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error != null) {
    return <ErrorMessage message={error.errorMessageForUser} />;
  }

  if (orders == null) {
    return <EmptyState message="No orders found" />;
  }

  return (
    <ul>
      {orders.items.map((order) => (
        <li key={order.id}>{order.name}</li>
      ))}
    </ul>
  );
}
```

### Summary Checklist

| Step | Action | File |
|---|---|---|
| 1 | Add codegen config | `scripts/api-codegen/config.ts` |
| 2 | Generate Zod schemas | `pnpm api:gen <name>` |
| 3 | Create feature API client | `src/mfes/<name>/api/<name>-api.ts` |
| 4 | Create Zustand store | `src/mfes/<name>/stores/<name>-store.ts` |
| 5 | Build component | `src/mfes/<name>/components/<Name>.tsx` |
