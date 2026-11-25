---
name: secret-hygiene
description: This skill activates when detecting hardcoded strings that look like API keys or credentials, creating .env files, referencing process.env or os.environ without Infisical, or working with configuration files that contain sensitive values. It enforces secret hygiene practices and recommends moving secrets to Infisical.
---

# Secret Hygiene

Patterns for detecting, preventing, and remediating hardcoded secrets in codebases.

## Detection Patterns

### Common Secret Patterns

Watch for these patterns in code:

```
# AWS
AKIA[0-9A-Z]{16}                    # AWS Access Key ID
[0-9a-zA-Z/+]{40}                    # AWS Secret Access Key

# API Keys
sk_live_[0-9a-zA-Z]{24,}            # Stripe secret key
sk_test_[0-9a-zA-Z]{24,}            # Stripe test key
SG\.[0-9A-Za-z\-_]{22}\.[0-9A-Za-z\-_]{43}  # SendGrid
xoxb-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}    # Slack bot token

# Tokens
ghp_[0-9a-zA-Z]{36}                 # GitHub personal access token
glpat-[0-9a-zA-Z\-_]{20}            # GitLab personal access token
eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+  # JWT token

# Database
postgres://.*:.*@                    # PostgreSQL connection string
mysql://.*:.*@                       # MySQL connection string
mongodb(\+srv)?://.*:.*@             # MongoDB connection string
redis://.*:.*@                       # Redis connection string

# Private Keys
-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----
-----BEGIN PGP PRIVATE KEY BLOCK-----
```

### When to Flag

Flag code that contains:
- String literals matching secret patterns above
- Hardcoded connection strings with credentials
- Base64-encoded values assigned to `secret`, `key`, `token`, or `password` variables
- Configuration files with inline credentials

## Remediation

### Step 1: Move Secret to Infisical

```bash
# Add the secret to Infisical
infisical secrets set STRIPE_SECRET_KEY=sk_live_abc123 --env=dev
infisical secrets set STRIPE_SECRET_KEY=sk_live_xyz789 --env=production
```

### Step 2: Replace Hardcoded Value

**Python (Django)**:
```python
# Before
STRIPE_KEY = "sk_live_abc123"

# After
import os
STRIPE_KEY = os.environ["STRIPE_SECRET_KEY"]
```

**TypeScript (NestJS/Next.js/Hono)**:
```typescript
// Before
const stripeKey = "sk_live_abc123"

// After
const stripeKey = process.env.STRIPE_SECRET_KEY!
```

**Flutter (Dart)**:
```dart
// Before
const apiKey = "sk_live_abc123";

// After
final apiKey = const String.fromEnvironment('STRIPE_SECRET_KEY');
```

### Step 3: Run with Infisical

```bash
# Development
infisical run --env=dev -- npm run dev

# Production
infisical run --env=production -- node server.js
```

## .env Hygiene

### .gitignore Requirements

Every project must have these in `.gitignore`:

```gitignore
# Environment files with secrets
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.env.*.local

# Keep example committed
!.env.example
```

### .env.example Maintenance

Maintain `.env.example` with every secret key (no values):

```bash
# Generate from Infisical
infisical secrets generate-example-env --env=dev > .env.example
```

Format with comments:
```bash
# Application
NODE_ENV=
PORT=
APP_URL=

# Database
DATABASE_URL=
DB_POOL_SIZE=

# Authentication
JWT_SECRET=
SESSION_SECRET=

# External Services
STRIPE_SECRET_KEY=
SENDGRID_API_KEY=
```

## Git Hygiene

### Pre-Commit Scanning

Install the Infisical pre-commit hook:

```bash
infisical scan install --pre-commit-hook
```

Or use `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: infisical-scan
        name: Infisical Secret Scan
        entry: infisical scan git-changes --staged
        language: system
        pass_filenames: false
```

### If a Secret Was Committed

1. **Rotate immediately** - the secret is compromised
2. **Remove from code** and replace with env var reference
3. **Update in Infisical** with the new rotated value
4. **Do NOT just delete the commit** - the secret exists in git history

```bash
# Rotate: generate new credential at the provider
# Update in Infisical
infisical secrets set COMPROMISED_KEY=new_rotated_value --env=production

# Revoke the old credential at the provider
```

## Framework-Specific Patterns

### Django

```python
# settings.py
import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
```

Run: `infisical run --env=dev -- python manage.py runserver`

### Next.js

```typescript
// next.config.js - server-side only
// NEXT_PUBLIC_ prefix exposes to browser - use sparingly
const config = {
  env: {
    // These are available server-side via process.env
    // Do NOT prefix with NEXT_PUBLIC_ unless intentionally public
  }
}
```

Run: `infisical run --env=dev -- npm run dev`

### NestJS

```typescript
// app.module.ts
@Module({
  imports: [
    ConfigModule.forRoot({
      // Infisical injects env vars, ConfigModule reads them
      isGlobal: true,
    }),
  ],
})
export class AppModule {}
```

Run: `infisical run --env=dev -- npm run start:dev`

### Hono (Cloudflare Workers)

```typescript
// For local dev with wrangler
// .dev.vars is the CF Workers equivalent of .env
// Export from Infisical:
// infisical export --env=dev > .dev.vars
```

Run: `infisical run --env=dev -- wrangler dev`

## Anti-Patterns

### Hardcoded Secrets in Code
```python
# NEVER do this
API_KEY = "sk_live_abc123"
DB_PASSWORD = "supersecret"
```

### Same Secrets Across Environments
Each environment (dev, staging, production) must have unique credentials. Sharing production secrets with development is a security risk.

### Secrets as CLI Arguments
```bash
# NEVER - visible in process list and shell history
node server.js --db-password=secret123

# CORRECT
infisical run --env=production -- node server.js
```

### Secrets in Docker Image Layers
```dockerfile
# NEVER - persists in image history
ENV API_KEY=sk_live_abc123
RUN echo "password=secret" > /app/.env

# CORRECT - inject at runtime
CMD ["infisical", "run", "--env=production", "--", "node", "server.js"]
```

### Secrets in Log Output
```typescript
// NEVER
console.log(`Connecting with key: ${process.env.API_KEY}`)

// CORRECT
console.log("Connecting to API service...")
```

### Committing .env Files
```bash
# Verify .env is not tracked
git ls-files --error-unmatch .env 2>/dev/null && echo "WARNING: .env is tracked!"
```

If `.env` is already tracked:
```bash
git rm --cached .env
echo ".env" >> .gitignore
git commit -m "fix: remove .env from tracking"
```
