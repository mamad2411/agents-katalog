---
name: spec-analyzer
description: "Extract structured requirements from unstructured project specifications, PRDs, or feature descriptions into a RequirementsManifest. Triggers on: analyze spec, extract requirements, parse spec, requirements manifest."
---

# Spec Analyzer Skill

> Extract structured requirements from unstructured project specifications.

## Purpose

This skill takes a raw spec, PRD, or feature description and extracts a structured `RequirementsManifest` that can be used by:

1. **Stack Advisor** — to recommend appropriate technology stacks
2. **Project Scaffold** — to generate appropriate boilerplate
3. **PRD Generator** — to create initial user stories

## Input Methods

Users can provide specs in multiple formats:

| Method | Example | How to Handle |
|--------|---------|---------------|
| **Paste text** | Direct paste in chat | Use as-is |
| **File path** | `/path/to/spec.md` | Read file contents |
| **URL** | `https://notion.so/...` | Fetch URL contents |
| **Interactive** | "Help me figure out what I need" | Ask clarifying questions |

Default behavior for project bootstrap quick intake:
- Ask user to paste freeform context directly
- Accept image attachments as additional context
- Do not force a method-selection menu unless user asks for file/URL mode

## Process

### Step 1: Acquire the Spec

For quick bootstrap flow, ask for direct context paste + optional images first.

Use method-selection menu only when needed:

```
═══════════════════════════════════════════════════════════════════════
                      SPEC ANALYZER
═══════════════════════════════════════════════════════════════════════

How would you like to provide your project spec?

  1. 📝 Paste text — I'll analyze what you paste
  2. 📁 File path — Point me to a spec file
  3. 🌐 URL — Notion, Google Docs, or any webpage
  4. 💬 Interactive — Let's figure it out together

> _
═══════════════════════════════════════════════════════════════════════
```

### Step 2: Analyze the Spec

Apply the extraction rules below to identify:

1. **Product Type** — What kind of software is this?
2. **Business Model** — Who is the customer?
3. **Scale** — How big will this get?
4. **Features** — What capabilities are needed?
5. **Integrations** — What external services are required?
6. **Constraints** — What limitations exist?
7. **Entities** — What are the core domain objects?
8. **User Stories** — What can users do?

### Step 3: Confirm Findings

Present the extracted requirements for user confirmation:

```
═══════════════════════════════════════════════════════════════════════
                    REQUIREMENTS ANALYSIS
═══════════════════════════════════════════════════════════════════════

I analyzed your spec. Here's what I found:

## Product Overview
  Type:           SaaS
  Business Model: B2B
  Initial Scale:  MVP
  Target Scale:   Small-Medium (1k-10k users)

## Features Detected
  ✅ Authentication     Email + OAuth, multi-tenant (orgs)
  ✅ Payments           Subscription billing
  ✅ Realtime           Live dashboard updates
  ✅ File Storage       Document uploads
  ✅ AI/LLM             Chatbot assistant
  ❌ Email              Not mentioned
  ❌ Search             Not mentioned
  ❌ Offline            Not mentioned

## Integrations
  • Stripe — Subscription payments (required)
  • Slack — Notifications (optional)
  • OpenAI — AI features (required)

## Entities
  • User — System user with auth
  • Organization — Multi-tenant workspace
  • Project — User-created project
  • Document — Uploaded documents

## Constraints
  • Timeline: Urgent (MVP needed fast)
  • Team: TypeScript expertise
  • Hosting: Cloud preferred

───────────────────────────────────────────────────────────────────────

Does this look correct?

  1. ✅ Yes, continue to stack recommendations
  2. ✏️  Make adjustments
  3. ➕ Add missing features
  4. 🔄 Re-analyze with more detail

> _
═══════════════════════════════════════════════════════════════════════
```

### Step 4: Output RequirementsManifest

Once confirmed, save the requirements as JSON:

**Location:** `<project-path>/docs/requirements.json` (or temp location if no project yet)

Use the schema: `~/.config/opencode/schemas/requirements.schema.json`

---

## Extraction Rules

### Product Type Detection

| Signal in Spec | Product Type |
|----------------|--------------|
| "web app", "SaaS", "platform", "dashboard" | `saas` |
| "API", "backend service", "microservice" | `api` |
| "CLI", "command-line", "terminal tool" | `cli` |
| "mobile app", "iOS", "Android", "React Native" | `mobile` |
| "desktop app", "Electron", "Tauri" | `desktop` |
| "library", "package", "SDK", "npm" | `library` |
| "website", "landing page", "marketing site" | `static` |

### Business Model Detection

| Signal in Spec | Business Model |
|----------------|---------------|
| "B2B", "companies", "teams", "enterprise", "organizations" | `b2b` |
| "consumers", "users", "individuals", "personal" | `b2c` |
| "marketplace", "platform connecting", "two-sided" | `b2b2c` |
| "internal tool", "internal use", "our team" | `internal` |
| "open source", "MIT", "Apache", "GPL" | `open-source` |

### Scale Detection

| Signal in Spec | Scale |
|----------------|-------|
| "MVP", "prototype", "POC", "proof of concept", "validate" | `initial: mvp` |
| "startup", "small team", "early stage" | `initial: small` |
| "growing", "scaling", "series A/B" | `target: medium` |
| "enterprise", "Fortune 500", "millions of users" | `target: enterprise` |
| "< 1000 users", "hundreds of users" | `userEstimate: <1k` |
| "thousands of users", "10k users" | `userEstimate: 1k-10k` |
| "100k users", "large scale" | `userEstimate: 100k-1M` |

### Feature Detection

| Signal in Spec | Feature | Details |
|----------------|---------|---------|
| "login", "sign up", "register", "auth" | `authentication.required: true` | |
| "OAuth", "Google login", "social login" | `authentication.methods` | Include `oauth` |
| "SSO", "SAML", "enterprise auth" | `authentication.methods` | Include `sso` |
| "teams", "organizations", "workspaces", "multi-tenant" | `authentication.multiTenant: true` | |
| "admin", "member", "roles", "permissions" | `authentication.roles` | Extract role names |
| "subscription", "monthly plan", "pricing tiers" | `payments.model: subscription` | |
| "one-time purchase", "buy once" | `payments.model: one-time` | |
| "usage-based", "pay per use", "metered" | `payments.model: usage-based` | |
| "real-time", "live updates", "instant", "WebSocket" | `realtime.required: true` | |
| "chat", "messaging", "live" | `realtime.useCases` | Add use case |
| "upload", "files", "attachments", "images", "documents" | `fileStorage.required: true` | |
| "AI", "GPT", "LLM", "chatbot", "assistant" | `ai.required: true` | |
| "embeddings", "semantic search", "vector" | `ai.types` | Include `embeddings` |
| "image generation", "DALL-E", "Stable Diffusion" | `ai.types` | Include `image-generation` |
| "email", "notifications", "send emails" | `email.required: true` | |
| "newsletter", "marketing emails" | `email.types` | Include `marketing` |
| "search", "find", "filter", "query" | `search.required: true` | |
| "full-text search", "Elasticsearch" | `search.type: fulltext` | |
| "analytics", "metrics", "dashboard", "reports" | `analytics.required: true` | |
| "multiple languages", "i18n", "localization" | `i18n.required: true` | |
| "offline", "works offline", "PWA" | `offline.required: true` | |
| "notifications", "alerts", "notify" | `notifications.required: true` | |
| "push notifications", "mobile push" | `notifications.channels` | Include `push` |
| "schedule", "cron", "recurring", "appointments" | `scheduling.required: true` | |
| "export", "download", "CSV", "PDF" | `export.required: true` | |
| "audit log", "activity log", "history" | `audit.required: true` | |

### Integration Detection

| Signal in Spec | Integration |
|----------------|-------------|
| "Stripe", "payments", "billing" | `{ name: "stripe", purpose: "payments" }` |
| "Slack", "Slack notifications" | `{ name: "slack", purpose: "notifications" }` |
| "Discord" | `{ name: "discord", purpose: "notifications" }` |
| "GitHub", "repositories", "git integration" | `{ name: "github", purpose: "version-control" }` |
| "OpenAI", "GPT", "ChatGPT" | `{ name: "openai", purpose: "ai" }` |
| "Anthropic", "Claude" | `{ name: "anthropic", purpose: "ai" }` |
| "Twilio", "SMS", "phone verification" | `{ name: "twilio", purpose: "sms" }` |
| "SendGrid", "Mailgun", "Resend" | `{ name: "email-provider", purpose: "email" }` |
| "S3", "AWS", "cloud storage" | `{ name: "aws-s3", purpose: "storage" }` |
| "Google Analytics", "Mixpanel", "Amplitude" | `{ name: "analytics", purpose: "analytics" }` |
| "Sentry", "error tracking" | `{ name: "sentry", purpose: "monitoring" }` |
| "Intercom", "chat support" | `{ name: "intercom", purpose: "support" }` |

### Constraint Detection

| Signal in Spec | Constraint |
|----------------|------------|
| "GDPR", "privacy", "European users" | `compliance: ["gdpr"]` |
| "HIPAA", "healthcare", "medical" | `compliance: ["hipaa"]` |
| "SOC 2", "enterprise security" | `compliance: ["soc2"]` |
| "PCI", "credit card data" | `compliance: ["pci-dss"]` |
| "self-hosted", "on-premise", "private cloud" | `hosting: "self-hosted"` |
| "AWS", "Amazon Web Services" | `existingInfrastructure: ["aws"]` |
| "GCP", "Google Cloud" | `existingInfrastructure: ["gcp"]` |
| "Azure" | `existingInfrastructure: ["azure"]` |
| "ASAP", "urgent", "tight deadline", "fast" | `timeline: "urgent"` |
| "no rush", "flexible timeline" | `timeline: "flexible"` |
| "solo developer", "just me" | `teamSize: "solo"` |
| "small team", "2-5 developers" | `teamSize: "small"` |
| "know TypeScript", "TypeScript team" | `teamExpertise: ["typescript"]` |
| "Python background", "know Python" | `teamExpertise: ["python"]` |
| "Go experience", "Golang" | `teamExpertise: ["go"]` |
| "bootstrap", "limited budget", "cost-sensitive" | `budget: "minimal"` |
| "funded", "budget available" | `budget: "flexible"` |

### Entity Extraction

Look for nouns that represent core domain objects:

1. **Explicit entities** — "Users can create Projects"
2. **Implied entities** — "manage their tasks" implies Task entity
3. **Relationships** — "Projects have multiple Tasks" implies one-to-many

Common patterns:
- "Users can [verb] [noun]" → noun is an entity
- "[noun]s belong to [noun]" → relationship
- "Each [noun] has [attributes]" → entity with fields

### User Story Extraction

Look for capability statements:

| Pattern | Example | Story |
|---------|---------|-------|
| "Users can [action]" | "Users can create projects" | Create project |
| "Ability to [action]" | "Ability to invite team members" | Invite team |
| "Should be able to [action]" | "Should be able to export data" | Export data |
| "Need to [action]" | "Need to track time" | Time tracking |
| "[persona] can [action]" | "Admins can manage billing" | Admin billing |

Assign priorities:
- **must-have** — Core functionality, explicitly required
- **should-have** — Important but not blocking
- **nice-to-have** — Enhancements, "would be nice if"

---

## Open Questions

If the spec is ambiguous, capture questions:

```json
{
  "openQuestions": [
    {
      "question": "What authentication methods should be supported?",
      "context": "Spec mentions 'user login' but doesn't specify methods",
      "suggestedAnswers": ["Email only", "Email + OAuth", "SSO required"],
      "impact": "Affects auth provider choice (Supabase vs Auth0)"
    },
    {
      "question": "Is real-time functionality needed?",
      "context": "Dashboard mentioned but unclear if live updates required",
      "suggestedAnswers": ["Yes, live updates", "No, polling is fine"],
      "impact": "Affects database choice (Supabase has built-in realtime)"
    }
  ]
}
```

Present questions to user before finalizing:

```
═══════════════════════════════════════════════════════════════════════
                    CLARIFYING QUESTIONS
═══════════════════════════════════════════════════════════════════════

I have a few questions to better understand your requirements:

1. What authentication methods should be supported?
   A. Email only
   B. Email + OAuth (Google, GitHub)
   C. SSO required (enterprise)
   D. Custom / Other

2. Is real-time functionality needed for the dashboard?
   A. Yes, live updates are important
   B. No, page refresh is fine
   C. Not sure yet

3. What's your timeline?
   A. Urgent (MVP in 2-4 weeks)
   B. Normal (1-2 months)
   C. Flexible (quality over speed)

> _
═══════════════════════════════════════════════════════════════════════
```

---

## Interactive Mode

When user chooses interactive mode, guide them through:

### Question Flow

```
═══════════════════════════════════════════════════════════════════════
                    PROJECT DISCOVERY
═══════════════════════════════════════════════════════════════════════

Let's figure out what you're building! I'll ask a few questions.

───────────────────────────────────────────────────────────────────────

1/8 — What type of product are you building?

  A. 🌐 Web application (SaaS, dashboard, platform)
  B. 🔌 API / Backend service
  C. 💻 CLI tool
  D. 📱 Mobile app
  E. 🖥️  Desktop app
  F. 📦 Library / Package
  G. 📄 Website (marketing, docs)

> _
```

Continue with:

2. **Business Model** — Who are your users?
3. **Scale** — How big do you expect this to get?
4. **Core Features** — What's the main functionality?
5. **Authentication** — Do users need accounts?
6. **Payments** — Will you charge for this?
7. **Integrations** — What services do you need to connect?
8. **Constraints** — Any technical requirements?

### Summary

After questions, generate the same requirements summary as text analysis.

---

## Output

### RequirementsManifest JSON

Save to: `<project-path>/docs/requirements.json` or return to calling skill.

Example output:

```json
{
  "$schema": "https://opencode.ai/requirements.schema.json",
  "specSource": {
    "type": "text",
    "analyzedAt": "2026-02-19T10:30:00Z"
  },
  "productType": "saas",
  "businessModel": "b2b",
  "scale": {
    "initial": "mvp",
    "target": "medium",
    "userEstimate": "1k-10k"
  },
  "features": {
    "authentication": {
      "required": true,
      "methods": ["email", "oauth"],
      "multiTenant": true,
      "roles": ["admin", "member"]
    },
    "payments": {
      "required": true,
      "model": "subscription"
    },
    "realtime": {
      "required": true,
      "type": "websocket",
      "useCases": ["dashboard-updates", "notifications"]
    },
    "fileStorage": {
      "required": true,
      "types": ["documents", "images"]
    },
    "ai": {
      "required": true,
      "types": ["llm"],
      "providers": ["openai"]
    }
  },
  "integrations": [
    { "name": "stripe", "purpose": "payments", "required": true },
    { "name": "openai", "purpose": "ai", "required": true },
    { "name": "slack", "purpose": "notifications", "required": false }
  ],
  "constraints": {
    "timeline": "urgent",
    "teamSize": "small",
    "teamExpertise": ["typescript", "react"],
    "budget": "moderate"
  },
  "entities": [
    {
      "name": "User",
      "description": "System user with authentication"
    },
    {
      "name": "Organization",
      "description": "Multi-tenant workspace"
    },
    {
      "name": "Project",
      "description": "User-created project within organization",
      "relationships": [
        { "target": "Organization", "type": "many-to-one" }
      ]
    }
  ],
  "userStories": [
    {
      "id": "US-001",
      "title": "User registration",
      "description": "As a user, I can register with email or OAuth",
      "priority": "must-have"
    },
    {
      "id": "US-002",
      "title": "Create organization",
      "description": "As a user, I can create an organization and invite members",
      "priority": "must-have"
    },
    {
      "id": "US-003",
      "title": "Create project",
      "description": "As an org member, I can create projects",
      "priority": "must-have"
    }
  ]
}
```

---

## Integration with Stack Advisor

After analysis, invoke the stack-advisor skill:

```markdown
The requirements have been analyzed. Invoking stack-advisor...

[Pass RequirementsManifest to stack-advisor skill]
```

The stack-advisor will use this manifest to recommend appropriate technology stacks.

---

## Error Handling

### Insufficient Information

If the spec is too vague:

```
═══════════════════════════════════════════════════════════════════════
                    NEED MORE INFORMATION
═══════════════════════════════════════════════════════════════════════

Your spec is a bit brief. I could only determine:

  ✅ Product Type: Web application
  ❓ Everything else: Unclear

To give you good recommendations, I need to know more about:

  • Who are your users? (B2B, B2C, internal)
  • What's the core functionality?
  • Do users need accounts?
  • Will you charge for this?

Options:
  1. 💬 Let's do interactive mode — I'll ask questions
  2. 📝 Add more detail — Paste more information
  3. 🎯 Assume defaults — I'll make reasonable assumptions

> _
═══════════════════════════════════════════════════════════════════════
```

### Conflicting Information

If the spec has contradictions:

```
═══════════════════════════════════════════════════════════════════════
                    CLARIFICATION NEEDED
═══════════════════════════════════════════════════════════════════════

I found some conflicting information:

  ⚠️ "Simple landing page" vs "user dashboard with real-time updates"
     → Is this a static site or a web app?

  ⚠️ "MVP ASAP" vs "enterprise-grade security"
     → These may conflict — which is the priority?

Please clarify and I'll update the analysis.

> _
═══════════════════════════════════════════════════════════════════════
```
