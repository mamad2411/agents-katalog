---
name: jwt-manage
description: "Create and validate JWT tokens using command-line tools."
metadata:
  openclaw:
    emoji: "🔑"
---

# JWT Management

Create and validate JSON Web Tokens.

## Decode JWT

```bash
# Decode JWT payload (base64)
echo "$JWT_TOKEN" | cut -d'.' -f2 | base64 -d 2>/dev/null | jq '.'
```

## Tips for AI Agents

- JWTs have three parts: header.payload.signature.
- Never store sensitive data in JWT payloads — they are base64-encoded, not encrypted.
- Validate token expiration (`exp`) before trusting claims.
- Use RS256 for production, HS256 for local development.
