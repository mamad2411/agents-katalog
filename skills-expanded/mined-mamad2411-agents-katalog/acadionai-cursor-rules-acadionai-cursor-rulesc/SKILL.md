---
alwaysApply: true
---

---
description: AcadionAI backend rules — token-efficient, production-safe
globs: ["app/**/*.py", "tests/**/*.py"]
alwaysApply: true
---

# AcadionAI Cursor Rules

## RESPONSE RULES (token efficiency)
- Output ONLY the changed code. No explanations, no summaries, no "here's what I did".
- If fixing a function, return only that function — not the entire file.
- If adding a method to a class, return only the new method block.
- Do NOT rewrite imports unless the task explicitly requires a new import.
- Do NOT add comments unless the existing code has comments in that pattern.
- Do NOT suggest alternative approaches. Implement exactly what is asked.
- Do NOT add print statements, logging, or debug code unless asked.

## ARCHITECTURE RULES (always enforce)
- Stack: FastAPI + SQLAlchemy 2.0 async + Supabase PostgreSQL + pytest + asyncpg
- Every school-scoped query MUST include: WHERE school_id = user["school_id"]
- school_id always comes from JWT (user dict), NEVER from request body or URL params
- Repositories: session.flush() only — NEVER session.commit()
- Services: session.commit() at end of complete operation only
- All DB queries use: await session.execute(select(Model).where(...))
- Use selectinload() for collections, joinedload() for single required relations
- All endpoints require get_current_user() dependency unless explicitly marked public
- PostgreSQL enums: SAEnum(name="existing_enum_name", create_type=False)
- Never create Python Enum classes — map to existing DB enums only

## TEST RULES
- Test files mirror source: app/modules/X/service.py → tests/modules/X/test_service.py
- Repository tests: use real async DB session from conftest fixture
- Service tests: mock the repository layer, do not hit DB
- Endpoint tests: use httpx AsyncClient with app fixture from conftest
- Every test must be async: async def test_*
- Fixtures in conftest.py only — no fixtures inside test files

## FORBIDDEN
- Never use @codebase or entire directory references
- Never use session.commit() in repository layer
- Never access school_id from request body for security scoping
- Never return SQLAlchemy model objects directly — always convert to schema first
- Never store plaintext Aadhaar or PII — use encryption_service
- Never hard-delete records — use soft_delete() method
