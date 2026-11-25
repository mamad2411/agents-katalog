# Security Hardening Skill

## Overview

This skill defines security requirements for production systems. Apply these patterns to prevent common vulnerabilities.

**Persona**: You are a Security Engineer who has responded to:
- Credential leaks in git history
- SQL injection attacks on production databases
- Command injection via unsanitized user input
- Data breaches from overly permissive IAM roles

You build security in from the start, not as an afterthought.

---

## Checklist

### Critical (Blocks Deploy)

- [ ] No secrets in code or git history
- [ ] All user input validated and sanitized
- [ ] SQL uses parameterized queries only
- [ ] Shell commands use subprocess with list args, not string interpolation
- [ ] HTTPS enforced for all external communication

### High Priority

- [ ] Principle of least privilege for IAM/RBAC
- [ ] Sensitive data encrypted at rest and in transit
- [ ] Authentication tokens have expiration
- [ ] Rate limiting on public endpoints
- [ ] Security headers set (CORS, CSP, X-Frame-Options)

### Best Practices

- [ ] Dependency scanning enabled (Dependabot, Snyk)
- [ ] Container images from trusted sources only
- [ ] Non-root user in containers
- [ ] Read-only filesystem where possible

---

## Patterns

### Secrets Management

```python
# ❌ NEVER
API_KEY = "sk-abc123..."
DB_PASSWORD = "hunter2"

# ❌ ALSO BAD
API_KEY = os.getenv("API_KEY", "sk-abc123...")  # Default reveals secret

# ✅ CORRECT
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str = Field(..., description="API key (no default)")
    db_password: str = Field(...)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Fails at startup if not set
settings = Settings()
```

### Input Validation

```python
# ❌ SQL INJECTION
query = f"SELECT * FROM users WHERE name = '{name}'"

# ✅ PARAMETERIZED
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (name,))

# ❌ COMMAND INJECTION
os.system(f"ls {user_path}")
subprocess.run(f"grep {pattern} {file}", shell=True)

# ✅ SAFE
subprocess.run(["ls", user_path], check=True)
subprocess.run(["grep", pattern, file], check=True)
```

### Path Traversal Prevention

```python
# ❌ PATH TRAVERSAL
def read_file(filename):
    with open(f"/data/{filename}") as f:
        return f.read()
# Attacker sends: "../../../etc/passwd"

# ✅ SAFE
from pathlib import Path

def read_file(filename: str) -> str:
    base = Path("/data").resolve()
    target = (base / filename).resolve()

    # Ensure target is under base directory
    if not str(target).startswith(str(base)):
        raise ValueError("Path traversal detected")

    return target.read_text()
```

### API Key Security

```python
# ❌ KEY IN URL
requests.get(f"https://api.example.com?key={api_key}")

# ✅ KEY IN HEADER
requests.get(
    "https://api.example.com",
    headers={"Authorization": f"Bearer {api_key}"}
)
```

### Docker Security

```dockerfile
# ❌ INSECURE
FROM python:3.12
COPY . /app
CMD ["python", "main.py"]

# ✅ HARDENED
FROM python:3.12-slim AS base

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

# Copy only what's needed
COPY --chown=app:app pyproject.toml ./
COPY --chown=app:app src/ ./src/

# Install deps
RUN pip install --no-cache-dir .

CMD ["python", "-m", "myapp"]
```

```yaml
# docker-compose.yml security
services:
  app:
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp
```

### IAM / RBAC

```hcl
# ❌ OVERLY PERMISSIVE
resource "aws_iam_policy" "bad" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["*"]
      Resource = ["*"]
    }]
  })
}

# ✅ LEAST PRIVILEGE
resource "aws_iam_policy" "good" {
  policy = jsonencode({
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:ListBucket"
      ]
      Resource = [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }]
  })
}
```

---

## Security Review Checklist

Before PR, verify:

```markdown
## Security Review

### Secrets
- [ ] No secrets in code
- [ ] No secrets in comments
- [ ] No default values for secrets
- [ ] .env files in .gitignore

### Input
- [ ] All user input validated
- [ ] SQL parameterized
- [ ] Commands use subprocess lists
- [ ] Paths validated against traversal

### Network
- [ ] HTTPS only
- [ ] API keys in headers, not URLs
- [ ] CORS configured correctly
- [ ] Rate limiting enabled

### Infrastructure
- [ ] IAM follows least privilege
- [ ] Containers run as non-root
- [ ] Dependencies scanned for vulnerabilities
```

---

## References

- OWASP Top 10: https://owasp.org/Top10/
- CWE/SANS Top 25: https://cwe.mitre.org/top25/
- Docker Security: https://docs.docker.com/engine/security/
