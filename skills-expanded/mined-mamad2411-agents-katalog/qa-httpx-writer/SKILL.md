---
name: qa-httpx-writer
description: Generate httpx/requests API tests for Python with async support, session management, and schema validation using pytest.
output_dir: tests/api
dependencies:
  recommended:
    - qa-api-contract-curator
---

# QA httpx Writer

## Purpose

Write Python API tests using httpx (or requests) from test case specifications and API contracts. Transform structured test cases (from qa-testcase-from-docs, qa-manual-test-designer) and OpenAPI contracts (from qa-api-contract-curator) into executable pytest API tests with async support, session management, response schema validation, and authentication handling.

## Trigger Phrases

- "Write httpx tests for [API/endpoint]"
- "Generate Python API tests from OpenAPI contract"
- "Create httpx API tests for [resource]"
- "Add httpx tests with Pydantic validation"
- "API tests with httpx.AsyncClient"
- "Python API tests from test cases"
- "httpx tests with auth and retry logic"
- "requests API tests for [endpoint]"

## Key Features

| Feature | Description |
| ------- | ----------- |
| **Async support** | `httpx.AsyncClient` for async tests; `httpx.Client` for sync |
| **Session management** | Connection pooling, cookie persistence, header reuse |
| **Response validation** | Pydantic models, JSON Schema for contract compliance |
| **Authentication** | Bearer token, API key, OAuth2, Basic Auth, cookies |
| **Retry logic** | Configurable retries for transient failures |
| **Context managers** | `with httpx.Client()` / `async with httpx.AsyncClient()` |

## Workflow

1. **Read test cases + API contract** — From qa-testcase-from-docs, qa-manual-test-designer, or qa-api-contract-curator (OpenAPI)
2. **Generate pytest API test files** — Produce `test_{resource}_api.py` with test functions per endpoint
3. **Add fixtures** — `conftest.py` with `base_url`, client fixtures (sync/async)
4. **Validate responses** — Status codes, headers, JSON body; Pydantic/JSON Schema validation

## Context7 MCP

Use **Context7 MCP** for httpx documentation when:
- API signatures or async/sync usage are uncertain
- Transport options, timeout, or retry configuration need verification
- Response streaming or file upload APIs require clarification

## Key Patterns

| Pattern | Usage |
| ------- | ----- |
| `httpx.Client()` | Sync client; use as context manager |
| `httpx.AsyncClient()` | Async client; use with `async with` |
| `response.status_code` | Assert HTTP status |
| `response.json()` | Parse JSON body |
| `response.headers` | Access response headers |
| `client.get(url)` / `client.post(url)` | HTTP methods |
| `client.get(url, headers=...)` | Custom headers (auth, etc.) |
| Pydantic validation | `Model.model_validate(response.json())` |
| pytest fixtures | `base_url`, `client`, `async_client` in conftest |

See `references/patterns.md` for CRUD, auth, file upload, streaming, async.

## Test Structure

- **conftest.py** — `base_url`, `client` (sync), `async_client` (async) fixtures
- **test_{resource}_api.py** — One file per resource/endpoint group
- **describe/it** equivalent — `class TestUsersAPI:` with `def test_*` methods

## Auth Patterns

| Type | Usage |
| ---- | ----- |
| **Bearer token** | `headers={"Authorization": f"Bearer {token}"}` |
| **API key** | `headers={"X-API-Key": api_key}` or `params={"api_key": key}` |
| **OAuth2** | `httpx.OAuth2Client` or manual token in headers |
| **Basic Auth** | `auth=httpx.BasicAuth(user, password)` |
| **Cookies** | Session cookies via `client.cookies` or `headers={"Cookie": ...}` |

## File Naming

- `test_{resource}_api.py` — e.g., `test_users_api.py`, `test_products_api.py`
- Place in `tests/` or `tests/api/` per project convention

## Scope

**Can do (autonomous):**
- Generate httpx/requests API tests from test cases and OpenAPI contracts
- Add conftest.py with base_url, client fixtures (sync/async)
- Use Pydantic or JSON Schema for response validation
- Implement auth patterns (Bearer, API key, Basic, cookies)
- Add retry logic, timeout configuration
- Call qa-api-contract-curator for contract when needed
- Use Context7 MCP for httpx docs

**Cannot do (requires confirmation):**
- Change production API implementation
- Add dependencies not in requirements.txt/pyproject.toml
- Override project test config without approval

**Will not do (out of scope):**
- Execute tests (user runs `pytest`)
- Write E2E browser tests (use qa-playwright-ts-writer)
- Modify CI/CD pipelines

## References

- `references/patterns.md` — CRUD, auth, file upload, streaming, async
- `references/assertions.md` — Status codes, JSON body, headers, Pydantic/JSON Schema validation
- `references/config.md` — conftest.py, fixtures, environment config, base URL
- `references/best-practices.md` — Async vs sync, session reuse, schema validation, test isolation

## Quality Checklist

- [ ] Tests match test case steps and expected results
- [ ] Each endpoint has success and error scenarios (validation, 401, 404)
- [ ] Auth setup is correct and isolated per test
- [ ] No hardcoded secrets; use env vars or fixtures
- [ ] Response assertions are specific (status, body shape, headers)
- [ ] File naming follows `test_{resource}_api.py`
- [ ] Client fixtures use context managers; proper teardown
- [ ] Schema validation used where contract specifies response shape

## Troubleshooting

| Symptom | Likely Cause | Fix |
| ------- | ------------ | --- |
| Connection refused | Wrong base_url or server not running | Verify `base_url` in conftest; ensure API is up |
| Tests pass individually, fail together | Shared client state or connection pool | Use function-scoped client fixture; avoid session reuse across tests |
| `response.json()` fails | Non-JSON response (204, HTML error) | Check `response.status_code`; use `response.text` for non-JSON |
| Async tests fail | Missing pytest-asyncio | Add `@pytest.mark.asyncio`; install pytest-asyncio; set `asyncio_mode = "auto"` |
| Auth not working | Token expired or wrong header | Check `Authorization` format; ensure token in scope |
| Pydantic validation error | Response shape differs from model | Align model with API contract; use `model_validate` with `strict=False` if needed |
| Timeout errors | Slow API or network | Increase `timeout` in client; add retry for transient failures |
