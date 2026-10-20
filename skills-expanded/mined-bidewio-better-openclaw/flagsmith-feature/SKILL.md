---
name: flagsmith-feature
description: Feature flags and remote config with Flagsmith
version: 1.0.0
tags: [feature-flags, config, devops, ab-testing]
---

# Flagsmith – Feature Flag Management

Flagsmith provides feature flags, remote config, and A/B testing
for managing feature rollouts across environments.

- **GitHub**: github.com/Flagsmith/flagsmith (5 000+ ⭐)
- **License**: BSD-3-Clause
- **Security**: Enterprise-grade. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{FLAGSMITH_URL}}` | API URL |
| `{{FLAGSMITH_API_KEY}}` | Environment API key |

## Usage Examples

### Get all flags for an environment

```bash
curl -s "{{FLAGSMITH_URL}}/api/v1/flags/" \
  -H "X-Environment-Key: {{FLAGSMITH_API_KEY}}"
```

### Get flags for a specific identity

```bash
curl -s "{{FLAGSMITH_URL}}/api/v1/identities/?identifier=user123" \
  -H "X-Environment-Key: {{FLAGSMITH_API_KEY}}"
```

## AI Agent Tips

- Feature flags with environment-specific overrides.
- Remote config values for dynamic application settings.
- A/B testing and percentage-based rollouts.
- SDKs for 20+ languages and platforms.
