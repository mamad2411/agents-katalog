# Frontend API Client Skill

**Purpose**: Guidance for creating API client methods following existing patterns from `frontend/lib/api.ts`.

## Overview

The API client is a centralized library that handles all backend API communication. It automatically attaches JWT tokens, handles errors, implements retry logic, and provides typed TypeScript interfaces.

## Key Patterns from `frontend/lib/api.ts`

### 1. API Configuration

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // ms
```

**Pattern**: Always use environment variables for API base URL with a fallback for development.

### 2. JWT Token Retrieval

```typescript
const getAuthToken = (): string | null => {
  if (typeof window === "undefined") return null;
  const token = localStorage.getItem("auth_token");
  return token;
};
```

**Pattern**: 
- Check for `window` to ensure client-side execution
- Retrieve token from `localStorage` with key `"auth_token"`
- Return `null` if token doesn't exist

### 3. Error Handling with 401 Redirect

```typescript
const handleApiError = (error: any, statusCode?: number): never => {
  // Redirect to login on 401 Unauthorized
  if (statusCode === 401) {
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_token");
      window.location.href = "/signin";
    }
  }

  throw {
    message: error.message || "An error occurred",
    code: error.code || "UNKNOWN_ERROR",
    statusCode: statusCode || 500,
  };
};
```

**Pattern**:
- Always check for 401 status code
- Remove auth token from localStorage
- Redirect to `/signin` page
- Throw structured error object

### 4. Retry Logic Wrapper

```typescript
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {},
  retries = MAX_RETRIES
): Promise<ApiResponse<T>> {
  const token = getAuthToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Attach JWT token if available
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle non-JSON responses
    const contentType = response.headers.get("content-type");
    if (!contentType?.includes("application/json")) {
      if (!response.ok) {
        handleApiError(
          { message: `HTTP error ${response.status}` },
          response.status
        );
      }
      return { success: true, data: {} as T };
    }

    const data = await response.json();

    // Handle errors
    if (!response.ok) {
      handleApiError(data.error || data, response.status);
    }

    return data;
  } catch (error: any) {
    // Retry on network errors
    if (retries > 0 && error.name === "TypeError") {
      await delay(RETRY_DELAY);
      return apiFetch<T>(endpoint, options, retries - 1);
    }

    // Re-throw other errors
    throw error;
  }
}
```

**Pattern**:
- Always use `apiFetch<T>()` wrapper for all API calls
- Automatically attach JWT token in `Authorization` header
- Handle JSON and non-JSON responses
- Retry on network errors (TypeError) up to MAX_RETRIES times
- Use delay between retries

### 5. Query Parameter Handling

```typescript
async getTasks(
  userId: string,
  queryParams?: TaskQueryParams
): Promise<ApiResponse<PaginatedResponse<Task>>> {
  const params = new URLSearchParams();

  if (queryParams?.status) params.append("status", queryParams.status);
  if (queryParams?.sort) params.append("sort", queryParams.sort);
  if (queryParams?.search) params.append("search", queryParams.search);
  if (queryParams?.page) params.append("page", queryParams.page.toString());
  if (queryParams?.limit) params.append("limit", queryParams.limit.toString());

  const queryString = params.toString();
  const endpoint = `/api/${userId}/tasks${queryString ? `?${queryString}` : ""}`;

  return apiFetch<PaginatedResponse<Task>>(endpoint);
}
```

**Pattern**:
- Use `URLSearchParams` to build query strings
- Only append non-undefined values
- Convert numbers to strings
- Build endpoint with conditional query string

### 6. Token Storage After Auth

```typescript
async signup(userData: UserSignupData): Promise<ApiResponse<AuthResponse>> {
  const response = await apiFetch<AuthResponse>("/api/auth/signup", {
    method: "POST",
    body: JSON.stringify(userData),
  });

  // Store token if signup successful
  if (response.success && response.data?.token) {
    if (typeof window !== "undefined") {
      localStorage.setItem("auth_token", response.data.token);
    }
  }

  return response;
}
```

**Pattern**:
- Check for `response.success` and `response.data?.token`
- Store token in `localStorage` with key `"auth_token"`
- Always check for `window` before accessing localStorage

### 7. Token Removal on Signout

```typescript
async signout(): Promise<ApiResponse<void>> {
  const response = await apiFetch<void>("/api/auth/signout", {
    method: "POST",
  });

  // Remove token on signout
  if (typeof window !== "undefined") {
    localStorage.removeItem("auth_token");
  }

  return response;
}
```

**Pattern**:
- Always remove token from localStorage on signout
- Check for `window` before accessing localStorage

## Steps for Adding New API Methods

### Step 1: Define Method in ApiClient Class

```typescript
export class ApiClient {
  async yourNewMethod(
    userId: string,
    data: YourDataType
  ): Promise<ApiResponse<YourResponseType>> {
    // Implementation
  }
}
```

### Step 2: Use apiFetch Helper

```typescript
return apiFetch<YourResponseType>(`/api/${userId}/your-endpoint`, {
  method: "POST", // or GET, PUT, DELETE, PATCH
  body: JSON.stringify(data), // for POST/PUT/PATCH
});
```

### Step 3: Handle Query Parameters (if needed)

```typescript
const params = new URLSearchParams();
if (queryParams?.param1) params.append("param1", queryParams.param1);
const queryString = params.toString();
const endpoint = `/api/${userId}/endpoint${queryString ? `?${queryString}` : ""}`;
```

### Step 4: Return Typed Response

```typescript
return apiFetch<YourResponseType>(endpoint, options);
```

## Complete Example: Adding a New Task Method

```typescript
async createTask(
  userId: string,
  taskData: TaskFormData
): Promise<ApiResponse<Task>> {
  return apiFetch<Task>(`/api/${userId}/tasks`, {
    method: "POST",
    body: JSON.stringify(taskData),
  });
}
```

## Constitution Requirements

- **FR-027**: Centralized API client at `/frontend/lib/api.ts` ✅
- **FR-028**: Auto-attach JWT token ✅
- **FR-029**: Handle 401 errors and redirect ✅
- **FR-030**: Typed TypeScript interfaces ✅
- **FR-031**: Error handling and retry logic ✅
- **FR-032**: Query parameters support ✅

## MCP Server Usage

- **Context7 MCP Server**: Use for understanding existing API patterns and code context
- **Better Auth MCP Server**: Use for JWT token management patterns

## References

- **Specification**: `specs/002-frontend-todo-app/spec.md` - API endpoint specifications
- **Plan**: `specs/002-frontend-todo-app/plan.md` - API contracts section
- **Implementation**: `frontend/lib/api.ts` - Complete API client implementation

## Common Patterns Summary

1. ✅ Always use `apiFetch<T>()` wrapper
2. ✅ Automatically attach JWT token via `getAuthToken()`
3. ✅ Handle 401 errors with redirect to `/signin`
4. ✅ Use `URLSearchParams` for query strings
5. ✅ Store token in localStorage after successful auth
6. ✅ Remove token on signout
7. ✅ Retry on network errors (up to 3 times)
8. ✅ Return typed `ApiResponse<T>` for all methods
9. ✅ Check for `window` before accessing localStorage
10. ✅ Use environment variable for API base URL

