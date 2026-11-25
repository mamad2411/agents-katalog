---
name: "onboarding-patterns"
description: "Onboarding documentation patterns: time-to-first-success benchmarks and measurement, the quickstart principle, expected output at every step, prerequisites tables, copy-paste safety, progressive disclosure, and anti-patterns. Use when writing or reviewing onboarding docs."
---

# Onboarding Documentation Patterns

## Time-to-First-Success Optimization

The single most important metric for onboarding documentation is time-to-first-success (TTFS): the time from a user arriving at your documentation to completing their first meaningful action.

### TTFS benchmarks by product type
| Product Type | Target TTFS |
|--------------|-------------|
| CLI tool | < 5 minutes |
| SDK/library | < 10 minutes |
| API | < 15 minutes |
| Platform/SaaS | < 30 minutes |

### Measuring TTFS
1. Recruit a new user who has never seen the product
2. Start a timer when they open the quickstart
3. Stop when they complete the defined success action
4. Repeat 3-5 times with different users

Every minute above target is a step that can be simplified, automated, or removed.

## The Quickstart Principle

A quickstart should contain exactly what is necessary to reach the first success state. Nothing more.

```markdown
# Bad quickstart structure
## Overview
## Architecture
## Philosophy
## Prerequisites (long prose)
## Installation
## Configuration (all options)
## Your first request
## Advanced configuration

# Good quickstart structure
## Prerequisites (table: tool, version, check command, install link)
## Install (one command)
## Configure (one or two required values only)
## Run (one command + expected output)
## Next steps (links to depth)
```

**The litmus test**: Can a new user follow this quickstart in one uninterrupted session without leaving the page to search for information?

## Expected Output at Every Step

Every step that produces output must show what that output looks like. The user has no baseline for "is this working?" without it.

```markdown
# Bad: no expected output
Install the dependencies:
```bash
npm install
```

# Good: expected output shows success
Install the dependencies:
```bash
npm install
```

Expected output:
```
added 142 packages in 12s
```

If you see `npm ERR!`, see [Troubleshooting npm installation](/guides/troubleshoot-npm).
```

## Prerequisites Table Format

Never write prerequisites in prose. Every item in a prerequisites table should be verifiable:

```markdown
| Requirement | Minimum Version | Verify | Install |
|-------------|----------------|--------|---------|
| Node.js | 20.0.0 | `node --version` | [nodejs.org](https://nodejs.org) |
| PostgreSQL | 15.0 | `psql --version` | [install guide](/install/postgres) |
| Acme account | N/A | [Sign up free](https://acme.com/signup) | N/A |
```

The `Verify` column prevents the most common setup confusion: user thinks they have it installed but have an incompatible version.

## Copy-Paste Safety

Every code block in an onboarding document must be safe to copy-paste without understanding:

```bash
# Bad: placeholder that breaks if copy-pasted
export API_KEY=YOUR_API_KEY_HERE

# Good: named placeholder that is clearly a placeholder
export API_KEY=<your-api-key>  # Get your API key at https://app.example.com/settings/api
```

When a command requires a value the user must supply:
1. Use angle brackets: `<your-api-key>`
2. Immediately follow with where to get it
3. Show an example of the complete filled-in command

## Progressive Disclosure in Onboarding

The quickstart should not contain everything. The quickstart should make the user successful fast, then link to depth.

```markdown
# Quickstart (5 minutes)
- One install command
- One config (just what's required)
- One run command
- One example output

# Getting Started Guide (30 minutes)
- Quickstart
- Core concepts explanation
- Three common use cases
- Configuration overview
- Next steps

# Full Documentation
- Complete configuration reference
- All API methods
- Integration guides
- Advanced patterns
```

## Onboarding Anti-Patterns

### "Clone the repo first" quickstart
```markdown
# Bad: requires cloning the entire repo to try the tool
git clone https://github.com/acme/product.git
cd product
npm install
npm start

# Good: install from package registry
npm install -g @acme/product
acme init
acme start
```

### Configuration by inference
```markdown
# Bad: user must infer the config format
Create a config.yaml file with the required settings.

# Good: show the exact config
Create a config.yaml file:
```yaml
api_key: <your-api-key>      # from app.example.com/settings
database_url: postgres://localhost/mydb
log_level: info
```
```

### Quickstart that assumes a running service
```markdown
# Bad: quickstart calls localhost:8080 but never showed how to start the server
curl http://localhost:8080/health

# Good: start the server as a step before the first request
3. Start the server:
   ```bash
   acme serve
   ```

   Expected output:
   ```
   Server running at http://localhost:8080
   ```

4. Test the health endpoint:
   ```bash
   curl http://localhost:8080/health
   ```
```

### Missing success state
```markdown
# Bad: user doesn't know if it worked
Run the setup:
```bash
./setup.sh
```

# Good: success is explicit
Run the setup:
```bash
./setup.sh
```

Expected output:
```
✓ Database initialized
✓ Configuration created at ~/.acmerc
✓ Dependencies installed

Setup complete. Run `acme start` to begin.
```
```

## References
- [Stripe's API quickstart](https://stripe.com/docs/quickstart) - industry benchmark for TTFS
- [Twilio's quickstarts](https://www.twilio.com/docs/quickstart) - language-specific paths
- [Google Codelabs format](https://codelabs.developers.google.com/) - structured interactive tutorials
- [User Onboarding teardowns](https://www.useronboard.com/user-onboarding-teardowns/) - product onboarding UX analysis
