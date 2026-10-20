---
name: api-error-handling
description: Use structured error responses and never leak internal details.
---

# API error handling

Leaked stack traces, SQL, or file paths hand attackers a map of your schema, ORM, and directory layout — turning a 500 into reconnaissance for the next exploit. All API endpoints must return structured, consistent error responses and never expose internal details to clients.

## Response format

Always return errors with a consistent shape:

```json
{ "error": { "code": "NOT_FOUND", "message": "Resource not found" } }
```

## Rules

- Map internal errors to appropriate HTTP status codes.
- Log the full error server-side; return only a safe summary to the client.
- Use a centralized error handler rather than try/catch in every route.
- Validate request input at the boundary and return 400 with field-level details.
- Never return raw database errors, ORM messages, or file paths.

## Examples

```ts
// BAD — leaks stack trace and DB details to the client
app.get('/users/:id', async (req, res) => {
  try {
    const user = await db.query(`SELECT * FROM users WHERE id = ${req.params.id}`)
    res.json(user)
  } catch (err) {
    res.status(500).json({ error: err.message, stack: err.stack })
    // exposes: "relation \"users\" does not exist at character 33"
  }
})

// GOOD — structured response; full error logged server-side only
app.get('/users/:id', async (req, res) => {
  try {
    const user = await db.query('SELECT * FROM users WHERE id = $1', [req.params.id])
    if (!user) return res.status(404).json({ error: { code: 'NOT_FOUND', message: 'User not found' } })
    res.json(user)
  } catch (err) {
    logger.error({ err, userId: req.params.id }, 'Failed to fetch user')
    res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' } })
  }
})
```
