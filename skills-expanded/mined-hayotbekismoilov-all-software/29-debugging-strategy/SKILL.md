---
name: debugging-strategy
description: |
  Systematic debugging strategies for frontend and backend issues. Apply when diagnosing
  bugs, errors, performance issues, or unexpected behavior. Covers binary search debugging,
  rubber duck method, reading stack traces, browser DevTools, and Django/FastAPI debug tools.
---

# Debugging Strategy

## The Scientific Method for Bugs
1. **Observe** — what exactly happens vs what should happen?
2. **Hypothesize** — what could cause this specific symptom?
3. **Test** — minimal reproduction, change one thing at a time
4. **Verify** — does fixing the root cause fix ALL symptoms?
5. **Document** — why did this happen, how to prevent it?

## Binary Search Debugging
```python
# When you have a long function with unexpected output:
# Instead of reading line by line, use print/log at midpoint

def complex_data_transform(data):
    step1 = process_step1(data)
    print("AFTER STEP1:", step1)  # <- add here first
    step2 = process_step2(step1)
    step3 = process_step3(step2)
    ...

# Output wrong at step1? Problem is in process_step1
# Output correct at step1? Problem is in step2 or later → binary search step2 vs step3
```

## Reading Python Stack Traces
```
# Read BOTTOM UP — the actual error is at the bottom
Traceback (most recent call last):
  File "views.py", line 45, in create_order      ← entry point
    order = OrderService.create(data)
  File "services.py", line 23, in create          ← trace
    total = calculate_total(items)
  File "utils.py", line 12, in calculate_total    ← where error happened
    return sum(item.price * item.qty for item in items)
AttributeError: 'dict' object has no attribute 'price'  ← actual error

# Fix: items is a list of dicts, not objects → use item['price']
```

## Django Debug Tools
```python
# Print all DB queries in a view (development only)
from django.db import connection, reset_queries
reset_queries()
# ... your code ...
for q in connection.queries:
    print(f"{q['time']}s: {q['sql'][:100]}")

# Shell: test queries interactively
python manage.py shell_plus  # pip install django-extensions

# Check what a queryset SQL looks like
print(Order.objects.filter(status='pending').query)
```

## Frontend Debugging
```typescript
// React DevTools tips:
// • "Why did this render?" — Profiler tab → record → find what triggered re-renders
// • "What's in state?" — Components tab → select component → inspect state

// Network debugging
// • Check: Request headers (auth token present?), Response status, Response body
// • If 401: check Authorization header format "Bearer <token>"
// • If CORS: check OPTIONS preflight response headers

// Console debugging without console.log everywhere
const DEBUG = import.meta.env.DEV;
const debug = (...args: unknown[]) => DEBUG && console.log('[DEBUG]', ...args);

// Conditional breakpoint in DevTools Sources:
// Right-click line → Add conditional breakpoint → e.g.: user.id === '123'
```

## Common Bug Patterns & Solutions
```
Symptom: Works locally, fails in prod
→ Check: environment variables, different Node/Python version, missing migration, HTTPS vs HTTP

Symptom: Intermittent failure
→ Check: race condition, missing await, network timeout, rate limit

Symptom: Works for one user, not another
→ Check: permission/role check, timezone difference, user-specific data edge case

Symptom: Memory usage grows over time
→ Check: event listeners not removed, infinite loops in useEffect, large data not garbage collected

Symptom: API returns 200 but data is wrong
→ Check: wrong query params, caching returning stale data, serializer field mismatch

Symptom: Form submits but nothing happens
→ Check: event.preventDefault() missing, onSubmit vs onClick, async handler not awaited
```
