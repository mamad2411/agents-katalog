---
name: redirection-query-params
description: Guidance on query parameter handling. Use when troubleshooting why URLs with `?param=value` are not redirecting correctly.
---

# Redirection: Query Parameter Handling

Handling URLs with query strings (e.g., `/page/?utm_source=facebook`) requires specific configurations in the Redirection plugin.

## Parameter Matching Options
When editing a redirect, look at the "URL Options / Query Parameters" dropdown:
- **Exact Match**: The redirect will ONLY trigger if the query string matches exactly. E.g., `/page/` will not trigger if the user visits `/page/?source=x`.
- **Ignore all parameters**: The redirect triggers regardless of query strings (the most common requirement).
- **Pass parameters to target**: The plugin redirects the user and appends the original query string to the target URL (critical for maintaining marketing UTM tags).

## Common Issue
"My redirect works for `/about/` but fails for `/about/?ref=google`."
- **Fix**: Change the query parameter setting for that redirect from "Exact Match" to "Ignore and pass parameters to the target".
