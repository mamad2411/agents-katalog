# AI Service App Memory

Apply this inside `ai-service/app/`.

- Keep FastAPI entrypoints, routers, schemas, and domain logic separated.
- Use Pydantic models for request and response boundaries.
- Keep patient-sensitive behavior explicit and typed.
- Preserve strict `mypy app` compatibility.
- Do not let LLM or ML outputs become clinical decisions.
