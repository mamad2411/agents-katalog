---
name: python-http-clients-servers
description: Change or review a Python HTTP client or server request, response, route, middleware, timeout, retry, streaming body, status mapping, or idempotency behavior. Use for FastAPI, Django, Flask, requests, httpx, aiohttp, and standard-library HTTP code.
---

# HTTP clients and servers

**Risk:** retries or timeouts duplicate a non-idempotent operation or leave a response body/resource open.

1. Trace method, URL/route, authentication, input validation, timeout, retry, status mapping, and body lifetime end to end.
2. Give every client call a bounded timeout and retry only operations with an explicit idempotency/recovery rule.
3. Do not pass untrusted URLs/headers downstream without validation or map internal exceptions directly to public responses.
4. Test the success and representative timeout/error response paths.

```bash
uv run pytest -q -k http
```
