---
name: skill-configuration-management
description: Secrets management, environment-specific configs, safe defaults, feature flags, configuration-as-code, compliance and audit trails. Use when managing secrets, configuring deployments, or implementing feature flags.
version: 1.0.0
---

# Skill: Configuration Management

Secrets stay secret. Configs are code. Feature flags enable safe rollout.

## Secrets Management

**Never commit secrets**:
```bash
# ✗ Don't
export DATABASE_PASSWORD="my-password"
git add .env
git commit

# ✓ Do
export DATABASE_PASSWORD=$(aws secretsmanager get-secret-value ...)
# or
source <(vault kv get -format=json secret/db | jq -r '.data | to_entries | .[] | "\(.key)=\(.value)"')
```

**Tools**: Vault, AWS Secrets Manager, Azure Key Vault

## Environment Configs

```yaml
# config/environments.yaml

development:
  database:
    host: localhost:5432
    pool_size: 5
  cache:
    ttl: 60s

production:
  database:
    host: db.prod.example.com:5432
    pool_size: 100
  cache:
    ttl: 3600s
```

**Load by environment**:
```python
import yaml
config = yaml.load(open(f'config/{ENV}.yaml'))
```

## Feature Flags

**Safe rollout**:
```
feature_auth_v2: enabled for [10%, 25%, 50%, 100%]

if feature_flag("auth_v2"):
    use_new_auth()
else:
    use_old_auth()
```

**Tools**: LaunchDarkly, Unleash, custom

## Safe Defaults

```
# ✓ Good defaults
class Config:
    DEBUG = False  # Never debug in production
    TIMEOUT = 30   # Reasonable default
    RETRIES = 3    # Sensible retry count

# ✗ Bad defaults
class Config:
    DEBUG = True   # Oops, left it on
    TIMEOUT = 3600  # Way too long
```

---

**Status**: Ready for configuration work  
**Best for**: Secrets, configs, feature flags, environment management
