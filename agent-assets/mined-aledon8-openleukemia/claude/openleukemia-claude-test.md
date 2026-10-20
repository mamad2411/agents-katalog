# Frontend Test Memory

Apply this inside `frontend/src/test/`.

- Keep test setup minimal and shared only when multiple tests need it.
- Prefer behavior-oriented Testing Library patterns over implementation details.
- Add setup only for stable browser APIs or matchers used across tests.
