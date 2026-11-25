---
name: project-guidelines-example
description: Example of a project-specific skill template. Use this as a template for your own projects.
---

# Project Guidelines Skill (Example)

This is an example of a project-specific skill. Use this as a template for your own projects.

## When to Use

Reference this skill when working on a specific project. Project skills contain:
- Architecture overview
- File structure
- Code patterns
- Testing requirements
- Deployment workflow

## Architecture Overview

**Tech Stack:**
- **Frontend**: Next.js 15 (App Router), TypeScript, React
- **Backend**: FastAPI (Python) or Node.js
- **Database**: Supabase (PostgreSQL)
- **AI**: Claude/Gemini API with structured output
- **Deployment**: Cloud Run / Vercel
- **Testing**: Playwright (E2E), Jest/Vitest (unit)

**Services:**
```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  Next.js 15 + TypeScript + TailwindCSS                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         Backend                             │
│  FastAPI / Node.js API                                     │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Supabase │   │   LLM    │   │  Redis   │
        │ Database │   │   API    │   │  Cache   │
        └──────────┘   └──────────┘   └──────────┘
```

## File Structure

```
project/
├── src/
│   ├── app/              # Next.js app router pages
│   │   ├── api/          # API routes
│   │   ├── (auth)/       # Auth-protected routes
│   │   └── workspace/    # Main app workspace
│   ├── components/       # React components
│   │   ├── ui/           # Base UI components
│   │   ├── forms/        # Form components
│   │   └── layouts/      # Layout components
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utilities
│   ├── types/            # TypeScript definitions
│   └── config/           # Configuration
├── tests/                # Test files
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

## Code Patterns

### API Response Format

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

// Success
return NextResponse.json({ success: true, data: result })

// Error
return NextResponse.json({ success: false, error: 'Message' }, { status: 400 })
```

### Custom Hooks

```typescript
export function useApi<T>(fetchFn: () => Promise<ApiResponse<T>>) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const execute = useCallback(async () => {
    setLoading(true)
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

## Testing Requirements

```bash
# Run all tests
npm test

# Run with coverage (target: 80%)
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

## Critical Rules

1. **Immutability** - never mutate objects or arrays
2. **TDD** - write tests before implementation
3. **80% coverage** minimum
4. **Many small files** - 200-400 lines typical, 800 max
5. **No console.log** in production code
6. **Proper error handling** with try/catch
7. **Input validation** with Zod schemas

## Related Skills

- `coding-standards` - General coding best practices
- `backend-patterns` - API and database patterns
- `frontend-patterns` - React and Next.js patterns
- `tdd-workflow` - Test-driven development methodology
