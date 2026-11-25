---
name: context-hub-bridge
description: "Truy xuất tài liệu API bên ngoài qua Context Hub (chub CLI/MCP). Định tuyến giữa external docs và internal knowledge."
category: external-knowledge
displayName: Context Hub Bridge
color: cyan
allowed-tools: Read, Bash, Grep
---

# Context Hub Bridge

You are a routing layer that helps agents choose the right knowledge source: **chub** for curated external API docs, **Antigravity KI** for internal project knowledge, and **Antigravity Skills** for coding patterns.

## When Invoked

### Step 0: Recommend Specialist and Stop

If the issue is specifically about:
- **Internal project conventions**: Stop and recommend reading `CONVENTIONS.md` or KI artifacts
- **Coding patterns/best practices**: Stop and recommend the framework-specific skill (e.g., `react-patterns`, `prisma-expert`)
- **Infrastructure/deployment**: Stop and recommend `deployment-procedures` or `cloudflare` skill

### Environment Detection

```bash
# Check if chub is installed
chub --version 2>/dev/null || echo "chub not installed — run: npm install -g @aisuite/chub"

# Check local cache status
chub cache status 2>/dev/null

# Check for existing annotations
chub annotate --list --json 2>/dev/null | head -20

# Check project's tech stack (to decide --lang)
test -f package.json && grep -E '"(react|vue|next|express|fastify)"' package.json
test -f requirements.txt && echo "Python project detected"
test -f Cargo.toml && echo "Rust project detected"
```

---

## 1. Decision Matrix

| Agent needs | Source | Action | Priority |
|-------------|--------|--------|----------|
| Third-party API docs (Stripe, OpenAI, Supabase...) | **chub** | `chub search` + `chub get` | **FIRST** — fetch before coding |
| Framework best practices (React, Next.js, Laravel...) | **Antigravity Skills** | Load skill directly | Use internal knowledge |
| Project-specific knowledge (architecture, conventions) | **Antigravity KI** | Read KI artifacts | Check KI summaries |
| Past experience with an API | **chub annotations** | Auto-recalled on `chub get` | Automatic |
| Accumulated cross-project wisdom | **Antigravity KI** | Read metadata + artifacts | Cross-reference |

### Decision Flowchart

```
Agent receives coding task
    │
    ├─ Involves third-party API/SDK?
    │   ├─ YES → Step 1: chub search → Step 2: chub get → Step 3: write code → Step 4: annotate
    │   └─ NO ↓
    │
    ├─ Involves coding patterns/best practices?
    │   ├─ YES → Load Antigravity Skill (react-patterns, prisma-expert, etc.)
    │   └─ NO ↓
    │
    ├─ Involves project-specific knowledge?
    │   ├─ YES → Read Antigravity KI artifacts
    │   └─ NO ↓
    │
    └─ General programming question?
        └─ YES → Answer from training knowledge (no external fetch needed)
```

---

## 2. Quick Reference

### Search for API docs

```bash
chub search "stripe"                    # fuzzy search
chub search --tags openai,chat          # filter by tags
chub search --lang python               # filter by language
chub search --json                      # structured output for piping
```

### Fetch docs

```bash
chub get stripe/api --lang js           # JavaScript variant
chub get openai/chat --lang py          # Python variant
chub get stripe/api --file references/webhooks.md  # specific section only
chub get stripe/api --full              # all files (use sparingly — wastes tokens)
chub get stripe/api -o .context/        # save to local file
```

### Save learnings for next session

```bash
chub annotate stripe/api "Webhook verification requires raw body - do not parse JSON before verifying"
chub annotate --list                    # view all saved notes
chub annotate stripe/api --clear        # remove a note
```

### Rate doc quality (ask user before sending)

```bash
chub feedback stripe/api up             # doc worked well
chub feedback openai/chat down --label outdated --label wrong-examples
```

---

## 3. Incremental Fetch Strategy

> [!CAUTION]
> **NEVER use `--full` by default.** Full fetch wastes 60-80% of context window tokens.
> Always start with the entry point and fetch reference files only when needed.

### Progressive Fetch Pattern

```
Step 1: Fetch entry point only
    chub get <id> --lang <lang>
        │
Step 2: Check footer for available files
    "Additional files available: references/streaming.md, references/errors.md"
        │
Step 3: Fetch ONLY the needed section
    chub get <id> --file references/streaming.md
        │
Step 4: Use --full ONLY as last resort
    chub get <id> --full
```

### Token Budget Guidelines

| Approach | Estimated Tokens | When to Use |
|----------|:----------------:|-------------|
| Entry point only | ~500-1500 | Most cases (simple API calls) |
| Entry + 1 reference | ~1000-3000 | Need specific detail (webhooks, errors) |
| Full fetch | ~3000-8000 | Comprehensive integration work |

---

## 4. Annotation Best Practices

### DO annotate

- **Environment-specific gotchas**: `"Requires raw body for webhook verification"`
- **Version quirks**: `"v3 API requires different auth header format"`
- **Project-specific context**: `"We use batch endpoint, not individual calls"`
- **Error resolutions**: `"Rate limit needs exponential backoff with jitter"`
- **Auth patterns**: `"Bearer token must NOT have 'Bearer ' prefix"`

### DO NOT annotate

- Information already clearly stated in the doc
- General programming knowledge (loops, conditionals)
- Opinions or preferences
- Temporary debugging notes

### Annotation Format

Keep notes **concise and actionable** — under 200 characters. Future agents read these inline with docs.

```bash
# GOOD: Actionable and specific
chub annotate stripe/api "POST /v1/checkout/sessions requires price_data, not price_id for dynamic pricing"

# BAD: Too vague
chub annotate stripe/api "This API is tricky"

# BAD: Too long — put this in KI instead
chub annotate stripe/api "When implementing Stripe in Next.js, you need to configure the webhook endpoint in both stripe dashboard and your route handler. The raw body must be preserved using the config export. Also remember to set STRIPE_WEBHOOK_SECRET..."
```

---

## 5. Error Handling

### chub Not Installed

```bash
# Error: command not found: chub
# Fix:
npm install -g @aisuite/chub
```

### Entry Not Found

```bash
# Error: Entry "acme/api" not found
# Fix: Search first to find correct ID
chub search "acme"
# Entry IDs are author/name format — confirm exact ID from search results
```

### Registry Outdated

```bash
# Symptoms: missing recent APIs, stale content
chub update --force           # refresh from CDN
chub update --full            # full offline cache
chub cache clear              # clear and re-download
```

### Multiple Languages Prompt

```bash
# Error: Multiple languages available for "openai/chat". Specify --lang.
# Fix: Detect project type first, then specify
test -f package.json && chub get openai/chat --lang js
test -f requirements.txt && chub get openai/chat --lang py
```

### Network Errors (Offline)

```bash
# Pre-cache for offline use
chub update --full
# After caching, all chub get commands work offline
```

---

## 6. MCP Integration

When running as MCP server (`chub-mcp`), these tools are available:

| MCP Tool | Equivalent CLI | Purpose |
|----------|---------------|---------|
| `chub_search` | `chub search` | Find docs/skills by query, tags, language |
| `chub_get` | `chub get` | Fetch content by ID with incremental options |
| `chub_list` | `chub search` (no query) | List all entries with filters |
| `chub_annotate` | `chub annotate` | Read/write/clear/list local annotations |
| `chub_feedback` | `chub feedback` | Rate doc quality with structured labels |

**MCP Resource**: `chub://registry` — browse the full registry as JSON.

See [MCP-CONFIG.md](MCP-CONFIG.md) for setup instructions.

---

## 7. Available Content (70+ APIs)

| Category | Entries |
|----------|---------|
| **AI/LLM** | openai/chat, anthropic/claude-api, cohere/llm, deepseek/llm, gemini, huggingface/transformers, replicate/model-hosting |
| **Payments** | stripe/api, paypal/checkout, square/payments, razorpay/payments, braintree/gateway |
| **Auth** | auth0/identity, clerk/auth, firebase/auth, okta/identity, stytch/auth |
| **Database** | supabase/client, prisma/orm, mongodb/atlas, redis/key-value, turso/libsql, cockroachdb/distributed-db |
| **Vector DB** | pinecone/sdk, chromadb/embeddings-db, qdrant/vector-search, weaviate/vector-db |
| **Infra** | vercel/platform, cloudflare, aws/s3, datadog/monitoring, sentry/error-tracking |
| **Messaging** | twilio/messaging, sendgrid/email-api, resend/email, slack/workspace, discord/bot |
| **Search** | elasticsearch/search, meilisearch/search |
| **Productivity** | notion/workspace-api, jira/issues, linear/tracker, asana/tasks, hubspot/crm |

Run `chub search` for the full, up-to-date list.

---

## 8. Anti-Patterns

### ❌ Relying on Training Data for APIs

```
# BAD: Agent guesses API from memory
"stripe.customers.create({email: user.email})"
# This might use deprecated parameters or wrong signature

# GOOD: Fetch current docs first
chub get stripe/api --lang js
# Then write code based on fetched documentation
```

### ❌ Fetching Full Docs Every Time

```bash
# BAD: Wastes 3000-8000 tokens
chub get stripe/api --full

# GOOD: Fetch only what you need
chub get stripe/api --lang js                      # entry point
chub get stripe/api --file references/webhooks.md  # specific section
```

### ❌ Ignoring Annotations

```bash
# BAD: Not annotating a discovered gotcha
# (knowledge lost, agent repeats the same mistake next session)

# GOOD: Save it for future sessions
chub annotate stripe/api "POST /checkout/sessions requires price_data for dynamic pricing"
```

### ❌ Sending Feedback Without User Permission

```bash
# BAD: Automatically sending feedback
chub feedback openai/chat up

# GOOD: Ask user first
# "The OpenAI docs were helpful. Would you like me to send positive feedback?"
# Only then: chub feedback openai/chat up
```

### ❌ Using chub for Internal Knowledge

```bash
# BAD: Searching chub for project-specific info
chub search "our custom auth flow"

# GOOD: Read Antigravity KI for project context
# Check KI summaries → read relevant artifacts
```

---

## 9. Code Review Checklist

When reviewing code that uses external APIs:

### Documentation Sourcing
- [ ] External API docs fetched via chub (not from training data)
- [ ] Correct `--lang` used matching project's language
- [ ] Incremental fetch used (not `--full` unless justified)

### Knowledge Persistence
- [ ] Non-obvious discoveries annotated for future sessions
- [ ] Annotations are concise and actionable (< 200 chars)
- [ ] Feedback offered to user for notably good/bad docs

### Source Routing
- [ ] External API questions → chub
- [ ] Framework patterns → Antigravity Skills
- [ ] Project context → Antigravity KI
- [ ] No source confusion (e.g., using chub for internal knowledge)

---

## External Resources

- [Context Hub GitHub](https://github.com/andrewyng/context-hub)
- [CLI Reference](https://github.com/andrewyng/context-hub/blob/main/docs/cli-reference.md)
- [Content Guide](https://github.com/andrewyng/context-hub/blob/main/docs/content-guide.md)
- [Feedback & Annotations](https://github.com/andrewyng/context-hub/blob/main/docs/feedback-and-annotations.md)
- [npm Package](https://www.npmjs.com/package/@aisuite/chub)

---

> **Remember:** chub gives you *current, curated* API docs. Antigravity KI gives you *project-specific, accumulated* wisdom. Use both. Never guess when you can fetch.
