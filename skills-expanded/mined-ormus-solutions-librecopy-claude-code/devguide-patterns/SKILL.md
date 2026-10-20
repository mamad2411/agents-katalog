---
name: "devguide-patterns"
description: "Developer guide patterns: Diátaxis tutorial and how-to traits, code examples that show success and error paths, prerequisites format, progressive tutorial structure, troubleshooting placement, the developer journey, contributing and integration guide structures, and onboarding anti-patterns. Use when writing or reviewing developer-facing guides."
---

# Developer Guide Patterns

## Diátaxis in Practice

### Tutorial characteristics
- The user is in a **learning** state, not trying to accomplish a real task
- Provide a safe sandbox environment (don't operate on real data)
- Every step must succeed - no choices, no optional paths
- Show expected output after every step
- The goal is the learning experience, not the artifact built

```markdown
# Tutorial: Build Your First Webhook Handler

In this tutorial, you will build a simple webhook receiver that logs
incoming events from the payment API.

**What you'll learn:**
- How webhook payloads are structured
- How to verify webhook signatures
- How to respond to webhook events

**What you will NOT need**: an existing account or real payment data.
We use the sandbox environment throughout.
```

### How-To characteristics
- The user **knows what they want** and needs to accomplish it efficiently
- No background explanation in the steps - link to explanation docs instead
- Assume the setup is done - link to getting-started, don't repeat it
- Title is "How to [task]" - always starts with "How to"

```markdown
# How to Configure Webhook Signature Verification

**Prerequisites:**
- Webhook endpoint set up (see [Creating a Webhook Endpoint](/guides/create-webhook))
- Your webhook secret from the dashboard

## Steps

1. Store the webhook secret in an environment variable:

   ```bash
   export WEBHOOK_SECRET="whsec_your_secret_here"
   ```

2. Verify the signature in your handler:

   ```python
   import hmac, hashlib

   def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
       expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
       return hmac.compare_digest(f"sha256={expected}", signature)
   ```

3. Return 200 immediately, process asynchronously:
   ...
```

## Code Example Best Practices

### Minimal but complete
```python
# Bad: incomplete example (what is client? what does .charge return?)
result = client.charge(amount=1000)
print(result)

# Good: complete, runnable, handles the error case
import os
from acme import AcmeClient

client = AcmeClient(api_key=os.environ["ACME_API_KEY"])

try:
    charge = client.charges.create(
        amount=1000,       # $10.00 in cents
        currency="usd",
        source="tok_visa",  # Test card token
        description="Order #1234",
    )
    print(f"Charged {charge.amount_formatted}: {charge.id}")
except acme.CardError as e:
    print(f"Card declined: {e.user_message}")
```

### Show both success and error paths
Every code example in a developer guide should show:
1. The success path
2. At least one likely error and how to handle it

### Expected output blocks
```markdown
Run the server:

```bash
python server.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
```
```

The expected output block prevents "is this working?" anxiety. It is the most underused element in developer documentation.

## Prerequisites Format

Never describe prerequisites in prose. Use a structured table or checklist:

```markdown
| Requirement | Version | Verify | Install |
|-------------|---------|--------|---------|
| Python | 3.11+ | `python --version` | [python.org](https://python.org) |
| pip | 23+ | `pip --version` | Included with Python |
| Redis | 7.0+ | `redis-server --version` | `brew install redis` or [redis.io](https://redis.io) |

**Accounts needed:**
- [ ] Acme account with API key ([sign up free](https://acme.com/signup))
- [ ] Stripe account in test mode (optional, for payment examples)
```

## Progressive Tutorial Structure

Each step should end in a testable state:

```
Step 1: Scaffold → `python app.py` runs without error
Step 2: Add database → `python app.py` connects successfully, logs "DB connected"
Step 3: Add first endpoint → `curl localhost:8000/health` returns `{"status": "ok"}`
Step 4: Add authentication → `curl localhost:8000/users` returns 401 without token
Step 5: Test auth → `curl -H "Authorization: Bearer test" localhost:8000/users` returns user list
```

## Troubleshooting Section Placement

Place troubleshooting at the end of each step that commonly fails, not in a separate appendix.

```markdown
## Step 3: Configure the database

[step content]

**If you see "Connection refused":**
This usually means the database server isn't running.
Start it with: `brew services start postgresql` (macOS) or `sudo systemctl start postgresql` (Linux)

**If you see "role does not exist":**
Create the role: `createuser -s $(whoami)`
```

## Anti-Patterns

### Tutorial that requires production setup
```markdown
# Bad: Tutorial requires existing account with real data
## Prerequisites
- An active subscription (minimum Pro plan)
- API key from production dashboard
- At least 10,000 rows in your database

# Good: Tutorial uses sandbox/demo data
## Prerequisites
- Free developer account (sign up at sandbox.acme.com)
- (All data used in this tutorial is generated test data)
```

### How-to that teaches
```markdown
# Bad: How-to with embedded explanation (slow, distracts from task)
## How to Add Authentication

JWT (JSON Web Token) is an open standard (RFC 7519) that defines a compact
and self-contained way for securely transmitting information as a JSON object.
Tokens consist of three parts separated by dots...
[3 paragraphs of JWT explanation before any steps]

# Good: How-to with link to explanation
## How to Add JWT Authentication

For background on how JWT tokens work, see [Understanding Authentication Tokens](/concepts/jwt).

**Prerequisites:** Running Express app (see [Getting Started](/get-started))

1. Install the JWT library: `npm install jsonwebtoken`
...
```

### Code that only works in the tutorial
Examples should work outside the tutorial context. If a user copies the code into their own project, it should work with minimal changes (environment variable substitution, not architecture rewrites).

## References
- [Diátaxis Framework](https://diataxis.fr/) - Daniele Procida
- [Write the Docs community](https://www.writethedocs.org/)
- [Google Technical Writing Courses](https://developers.google.com/tech-writing)
- [The Documentation System](https://documentation.divio.com/) - Original Divio article by Procida

## Onboarding, contributing, and integration guides

> Patterns for writing developer onboarding documentation, contributing guides, and integration docs.

### Knowledge Base

#### The Developer Journey

Developers interact with a project through distinct phases, each needing different documentation:

```
Discover --> Evaluate --> Adopt --> Build --> Contribute --> Maintain
   |           |          |         |           |            |
 README    Quick Start  Install   Guides    CONTRIBUTING  Architecture
           + Examples   + Setup   + API       + PRs        + ADRs
```

#### Getting Started: The 15-Minute Rule

A new developer should go from `git clone` to running tests in 15 minutes or less. Every minute beyond that is a barrier to contribution.

**Measure your setup time:**
1. Start a timer when running `git clone`
2. Follow your own getting-started guide exactly
3. Stop when tests pass
4. If over 15 minutes, automate or simplify

#### The Prerequisites Table

Never use prose for prerequisites. Use a table:

| Tool | Minimum Version | Check Command | Install Link |
|------|----------------|---------------|-------------|
| Node.js | 20.0.0 | `node --version` | [nodejs.org](https://nodejs.org) |
| Docker | 24.0.0 | `docker --version` | [docker.com](https://docker.com) |
| PostgreSQL | 16.0 | `psql --version` | Via Docker or native |

#### Contributing Guide Structure

Standard sections in order of importance:

1. **Code of Conduct** - Link to or embed the Contributor Covenant
2. **Quick Contribution Guide** - For typo fixes and small changes (minimal process)
3. **Development Setup** - How to get the project running for development
4. **How to Submit Changes** - Branch naming, commit format, PR process
5. **Code Standards** - Linting rules, formatting, naming conventions
6. **Testing Requirements** - What tests are expected with different types of changes
7. **Review Process** - What to expect after opening a PR, SLA for reviews
8. **Release Process** - How changes get from merged PR to released version
9. **Getting Help** - Where to ask questions (Discord, discussions, issues)

#### Integration Documentation Structure

1. **Overview** - What the integration does, architectural diagram
2. **Prerequisites** - Accounts, credentials, access requirements
3. **Authentication** - How to authenticate (API key, OAuth, etc.)
4. **Core Setup** - Install SDK, configure client, first API call
5. **Common Operations** - CRUD operations with code examples
6. **Webhooks** - Receiving events, signature verification, payload schemas
7. **Error Handling** - Error codes, retry strategies, fallback behavior
8. **Testing** - Sandbox environments, mock servers, test credentials
9. **Troubleshooting** - Common issues and their solutions
10. **Migration** - Upgrading from previous versions

### Patterns

1. **Script Aliases**: Document `Makefile` or `package.json` script aliases so developers run `make test` not `docker compose exec app pytest --cov --tb=short -q`.
2. **Environment Variables Table**: List every env var with its purpose, required/optional status, and example value. Never just say "copy .env.example".
3. **Architecture Before Code**: In contributing guides, include a brief architecture overview so contributors understand where their change fits.
4. **Issue Labels as Onboarding**: Document issue label meanings. `good first issue`, `help wanted`, `bug`, `enhancement` should be explained.
5. **Review Checklist**: Provide a PR checklist that contributors can self-review against before requesting review.

### Anti-Patterns

1. **"It's in the code"**: Telling contributors to read the source code instead of documenting architecture. Code shows what, docs explain why.
2. **Implicit prerequisites**: Assuming everyone has Docker, Go, and PostgreSQL installed. List everything.
3. **Stale scripts**: Documenting `npm run test` when the actual command is `pnpm test`. Keep docs in sync with package.json.
4. **No first-issue path**: Contributing docs that only describe the process for major features. Include guidance for small first contributions.
5. **Setup scripts without explanation**: A `setup.sh` that does 20 things silently. Developers need to understand what setup does so they can debug when it fails.

### References

- [GitHub's Guide to CONTRIBUTING.md](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions)
- [Contributor Covenant](https://www.contributor-covenant.org/)
- [First Timers Only](https://www.firsttimersonly.com/)
- [Diataxis - How-to Guides](https://diataxis.fr/how-to-guides/)
