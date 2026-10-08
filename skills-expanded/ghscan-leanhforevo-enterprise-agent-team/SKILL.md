# Dev Agent — Implementation Skill

## Core principle: Lazy-dev (always active)

```
1. Does this need to exist?          → YAGNI. If no: skip.
2. Stdlib/built-in covers it?        → Use it. Zero installs.
3. Native platform feature covers it? → CSS over JS. DB constraint over app code.
4. Existing installed dep covers it? → Use it. Never add new dep for <10 lines.
5. Can it be one expression?         → One expression.
6. Otherwise                         → Minimum code that works. Boring over clever.
```

---

## Edit Discipline

- Read the file section before editing — never assume structure
- Use `multi_replace_string_in_file` for ≥2 edits in one session — never sequential single edits
- Include 3-5 lines of unchanged context around every replacement — never ambiguous
- After editing: `get_errors` immediately — fix before moving on
- Never modify files outside the Architect's plan without documenting why
- **Distinct URL per View/Page/Mode**: Every distinct page, screen, tab, or form mode (e.g. login/register) must have its own unique URL pathname synchronized with browser history (HTML5 history / pushState).

---

## Self-check pattern

Every non-trivial function gets ONE inline self-check:
```js
// assert: validatePhone('0912345678') === true
// assert: validatePhone('123') === false
```
```python
assert parse_date('2026-01-01') == datetime(2026, 1, 1)
```
Not a test file. One comment block. Runnable.

---

## React/Vite patterns

### Controlled inputs
```jsx
// Derive counter from existing state — no new useState
<textarea value={formData.notes} onChange={update('notes')} maxLength={200} />
<small className="notes-char-counter">{(formData.notes || '').length}/200</small>
```

### CSS — extend don't duplicate
```css
/* In existing src/styles/base.css or component CSS */
.notes-char-counter { display: block; text-align: right; font-size: 10px; color: #70849f; }
```

### Conditional class pattern
```jsx
className={`btn${isActive ? ' btn--active' : ''}`}
```

### Error boundary — only add if explicitly asked
```jsx
// ponytail: no error boundary — add when component fetches async data
```

---

## Python/FastAPI patterns

### Route pattern
```python
@router.post("/endpoint", response_model=ResponseSchema)
async def endpoint(data: RequestSchema, db: Session = Depends(get_db)):
    # implementation
    return result
```

### Error pattern
```python
from fastapi import HTTPException
raise HTTPException(status_code=400, detail="Descriptive message")
```

### Never bare except
```python
# ❌ except:
# ✅ except ValueError as e: logger.error(e); raise HTTPException(400, str(e))
```

---

## n8n patterns

### Expression syntax
```
{{ $json.fieldName }}
{{ $node["NodeName"].json.field }}
{{ $now.toISO() }}
```

### Code node — only when expressions can't do it
```js
// Input: $input.all()
const items = $input.all();
return items.map(item => ({ json: { ...item.json, processed: true } }));
```

---

## Node.js patterns

### Async error handling
```js
router.post('/endpoint', async (req, res, next) => {
  try {
    const result = await service.doThing(req.body);
    res.json(result);
  } catch (err) {
    next(err); // let existing error middleware handle it
  }
});
```

---

## Ponytail comments (deliberate simplifications)

Mark anything intentionally simplified:
```js
// ponytail: no debounce on search input — add when API calls are expensive
// ponytail: no pagination — add when list exceeds 50 items
// ponytail: no optimistic UI — add when network latency becomes UX issue
```

---

## What never to simplify away
- Input validation at trust boundaries (user input, API input)
- Error handling that prevents data loss
- Security (auth checks, SQL injection, XSS)
- Accessibility attributes explicitly requested
- Anything the user explicitly asked for
