---
name: document-endpoint
description: "Writes reference docs for one endpoint from the real code: parameters, responses, errors and a working example call."
disable-model-invocation: true
---

Write reference documentation for this endpoint: $ARGUMENTS

1. Locate the route, its handler, validation schema, auth middleware and tests. Read all of them.
2. Look for existing API docs (docs folder, README, OpenAPI file). Match their headings and tone. If none exist, use plain Markdown.
3. Document, in this order: purpose in one sentence, method and path, authentication and required roles, path and query parameters, request body fields (type, required, limits), success response with status and fields, every error status with its cause and body, rate limits if any.
4. Build a request example that really works (curl with a dummy token) and the matching real-shaped response. Take values from tests or fixtures, never invent fields the code does not return.
5. If the code, tests and any older doc disagree, do not choose silently. List each mismatch.

Show the finished page. Ask before saving it or overwriting an existing doc file.
