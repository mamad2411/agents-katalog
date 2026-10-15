---
name: api-add-route
description: >-
  Use when adding or changing an HTTP route under services/api. Walks the exact
  steps so the new route follows Helpline's gateway conventions.
paths: services/api/**
---

# Adding an API route

Activates for work in `services/api`. Follow these steps in order.

1. **Write the handler** in the matching module (`tickets.py` for ticket
   routes, a new module for a new noun). Signature is
   `(request: dict) -> dict`.
2. **Validate inputs first.** Missing/!bad input raises `ValidationError` —
   never return an error dict by hand.
3. **Do no business logic here.** Call a repo (`packages/db`) or another
   service. The handler only orchestrates and shapes the response.
4. **Register the route** in `routes.py` inside `build_app()` —
   `app.route("METHOD /path", handler)`. A route not registered there does not
   exist.
5. **Add a test** in `tests/` that builds the app and dispatches the route.

Full checklist with a worked example: [references/route-checklist.md](references/route-checklist.md).
