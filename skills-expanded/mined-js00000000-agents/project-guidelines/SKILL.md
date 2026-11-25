---
name: project-guidelines
description: Fusion Labs project-specific guidelines template. Use this as a reference when creating project-specific skills for new projects.
---

# Project Guidelines (Fusion Labs Template)

This is a template for project-specific skills. Use it when documenting the architecture, patterns, and workflows for individual projects in the Fusion Labs workspace.

## When to Use

Reference this template when:
- Setting up guidelines for a new project
- Documenting an existing project's architecture
- Onboarding contributors to a project

---

## Architecture Overview

**Tech Stack:**
- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Backend**: Go (Gin framework, GORM)
- **Database**: PostgreSQL (via Docker)
- **Cache**: Redis (via Docker)
- **AI**: Gemini API integration
- **Deployment**: Docker, GitHub Actions

**Services:**
```
┌──────────────────────────────────┐
│         Frontend (Vite)          │
│  React + TypeScript + Tailwind   │
│  Port: 5173 (dev)               │
└──────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│         Backend (Gin)            │
│  Go + GORM + JWT                │
│  Port: 8080                     │
└──────────────────────────────────┘
                │
        ┌───────┼────────┐
        ▼       ▼        ▼
  ┌──────────┐ ┌──────┐ ┌──────┐
  │PostgreSQL│ │Redis │ │Gemini│
  │  :5432   │ │:6379 │ │ API  │
  └──────────┘ └──────┘ └──────┘
```

---

## File Structure

```
project/
├── backend/
│   ├── cmd/
│   │   └── server/
│   │       └── main.go           # Entry point
│   ├── internal/
│   │   ├── config/               # Configuration
│   │   ├── handler/              # HTTP handlers
│   │   ├── middleware/           # Auth, CORS, logging
│   │   ├── model/                # GORM models
│   │   ├── repository/           # Data access
│   │   └── service/              # Business logic
│   ├── migrations/               # SQL migrations
│   ├── go.mod
│   ├── go.sum
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── ui/               # Generic UI
│   │   │   └── features/         # Feature components
│   │   ├── hooks/                # Custom hooks
│   │   ├── lib/                  # Utilities, API client
│   │   ├── types/                # TypeScript types
│   │   └── styles/               # Global styles
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
└── README.md
```

---

## Code Patterns

### API Response Format (Go/Gin)

```go
type APIResponse struct {
    Success bool        `json:"success"`
    Data    interface{} `json:"data,omitempty"`
    Error   string      `json:"error,omitempty"`
    Meta    *Meta       `json:"meta,omitempty"`
}

func Success(c *gin.Context, data interface{}) {
    c.JSON(http.StatusOK, APIResponse{Success: true, Data: data})
}

func Error(c *gin.Context, status int, message string) {
    c.JSON(status, APIResponse{Success: false, Error: message})
}
```

### Frontend API Calls (TypeScript)

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`/api${endpoint}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...options?.headers },
    })
    if (!response.ok) return { success: false, error: `HTTP ${response.status}` }
    return await response.json()
  } catch (error) {
    return { success: false, error: String(error) }
  }
}
```

### Custom Hooks (React)

```typescript
export function useApi<T>(fetchFn: () => Promise<ApiResponse<T>>) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const execute = useCallback(async () => {
    setLoading(true)
    setError(null)
    const result = await fetchFn()
    if (result.success) {
      setData(result.data!)
    } else {
      setError(result.error!)
    }
    setLoading(false)
  }, [fetchFn])

  return { data, loading, error, execute }
}
```

---

## Testing Requirements

### Backend (Go)

```bash
go test ./...
go test -cover ./...
go test -race ./...
```

### Frontend (TypeScript)

```bash
npm run test
npm run test -- --coverage
```

**Coverage target:** 80% minimum

---

## Deployment Workflow

### Pre-Deployment Checklist

- [ ] All tests passing
- [ ] `go build ./...` succeeds
- [ ] `npm run build` succeeds
- [ ] No hardcoded secrets
- [ ] Environment variables documented
- [ ] Database migrations ready

### Local Development

```bash
# Start infrastructure
cd system/infra && docker-compose up -d

# Start backend
cd backend && go run ./cmd/server

# Start frontend
cd frontend && npm run dev
```

### Environment Variables

```bash
# Backend
DATABASE_URL=postgresql://devuser:devpassword@localhost:5432/devdb
REDIS_URL=redis://:devpassword@localhost:6379/0
JWT_SECRET=your-secret-key-min-32-chars
GIN_MODE=debug
PORT=8080

# Frontend
VITE_API_URL=http://localhost:8080
```

---

## Critical Rules

1. **Immutability** — never mutate objects or arrays in React
2. **TDD** — write tests before implementation for core logic
3. **80% coverage** minimum
4. **Small files** — 200-400 lines typical, 800 max
5. **No console.log** in production code
6. **No fmt.Println** in production Go code
7. **Proper error handling** with context wrapping
8. **Input validation** with Gin binding tags / Zod

---

## Related Skills

- `coding-standards` — General coding best practices
- `gin-patterns` — Gin framework patterns
- `react-typescript` — React and TypeScript patterns
- `security-review` — Security checklist
- `tdd-workflow` — Test-driven development

---

*Copy this template and customize it for each new project in the Fusion Labs workspace.*
