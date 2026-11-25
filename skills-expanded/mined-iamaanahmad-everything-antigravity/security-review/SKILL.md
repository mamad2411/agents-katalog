---
name: security-review
description: Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns.
model: gemini-2.0-pro-exp
---

# Security Review Skill

Comprehensive security checklist and patterns for Antigravity projects.

## When to Activate

- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Working with secrets or credentials
- Implementing payment features
- Storing or transmitting sensitive data

## Security Checklist

### 1. Secrets Management

```typescript
// ❌ NEVER
const apiKey = "sk-proj-xxxxx"

// ✅ ALWAYS
const apiKey = process.env.OPENAI_API_KEY
if (!apiKey) throw new Error('OPENAI_API_KEY not configured')
```

- [ ] No hardcoded API keys, tokens, or passwords
- [ ] All secrets in environment variables
- [ ] `.env` in `.gitignore`
- [ ] No secrets in git history

### 2. Input Validation

```typescript
import { z } from 'zod'

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
})

export async function createUser(input: unknown) {
  const validated = CreateUserSchema.parse(input)
  return db.users.create(validated)
}
```

- [ ] All user inputs validated with schemas
- [ ] File uploads restricted (size, type, extension)
- [ ] No direct use of user input in queries

### 3. SQL Injection Prevention

```typescript
// ❌ DANGEROUS
const query = `SELECT * FROM users WHERE email = '${userEmail}'`

// ✅ SAFE
const { data } = await supabase.from('users').select('*').eq('email', userEmail)
```

- [ ] All database queries use parameterized queries
- [ ] No string concatenation in SQL

### 4. Authentication & Authorization

```typescript
// ❌ localStorage (vulnerable to XSS)
localStorage.setItem('token', token)

// ✅ httpOnly cookies
res.setHeader('Set-Cookie', `token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600`)
```

```typescript
// ALWAYS verify authorization first
export async function deleteResource(id: string, requesterId: string) {
  const requester = await db.users.findUnique({ where: { id: requesterId } })
  if (requester.role !== 'admin') {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 403 })
  }
  await db.resources.delete({ where: { id } })
}
```

- [ ] Tokens stored in httpOnly cookies (not localStorage)
- [ ] Authorization checks before sensitive operations
- [ ] Row Level Security enabled in Supabase
- [ ] Role-based access control implemented

### 5. XSS Prevention

```typescript
import DOMPurify from 'isomorphic-dompurify'

function renderUserContent(html: string) {
  const clean = DOMPurify.sanitize(html, { ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'], ALLOWED_ATTR: [] })
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}
```

- [ ] User-provided HTML sanitized
- [ ] CSP headers configured
- [ ] React's built-in XSS protection used

### 6. Rate Limiting

```typescript
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Too many requests'
})
app.use('/api/', limiter)
```

- [ ] Rate limiting on all API endpoints
- [ ] Stricter limits on expensive operations

### 7. Sensitive Data Exposure

```typescript
// ❌ Logging sensitive data
console.log('User login:', { email, password })

// ✅ Redact sensitive data
console.log('User login:', { email, userId })

// ❌ Exposing internal details
catch (error) {
  return NextResponse.json({ error: error.message, stack: error.stack }, { status: 500 })
}

// ✅ Generic error messages
catch (error) {
  console.error('Internal error:', error)
  return NextResponse.json({ error: 'An error occurred. Please try again.' }, { status: 500 })
}
```

- [ ] No passwords, tokens, or secrets in logs
- [ ] Error messages generic for users
- [ ] No stack traces exposed to users

### 8. Dependency Security

```bash
npm audit
npm audit fix
npm outdated
```

- [ ] Dependencies up to date
- [ ] No known vulnerabilities (`npm audit` clean)
- [ ] Lock files committed

## Security Testing

```typescript
test('requires authentication', async () => {
  const response = await fetch('/api/protected')
  expect(response.status).toBe(401)
})

test('requires admin role', async () => {
  const response = await fetch('/api/admin', { headers: { Authorization: `Bearer ${userToken}` } })
  expect(response.status).toBe(403)
})

test('rejects invalid input', async () => {
  const response = await fetch('/api/users', { method: 'POST', body: JSON.stringify({ email: 'not-an-email' }) })
  expect(response.status).toBe(400)
})
```

## Pre-Deployment Security Checklist

- [ ] No hardcoded secrets
- [ ] All user inputs validated
- [ ] All queries parameterized
- [ ] User content sanitized (XSS)
- [ ] CSRF protection enabled
- [ ] Tokens in httpOnly cookies
- [ ] Authorization checks in place
- [ ] Rate limiting enabled
- [ ] HTTPS enforced
- [ ] Security headers configured (CSP, X-Frame-Options)
- [ ] No sensitive data in error messages or logs
- [ ] Dependencies up to date
- [ ] Row Level Security enabled in Supabase

**Remember**: Security is not optional. One vulnerability can compromise the entire platform. When in doubt, err on the side of caution.
