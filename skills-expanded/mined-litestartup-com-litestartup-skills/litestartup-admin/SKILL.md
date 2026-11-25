---
name: litestartup-admin
description: >
  Initialize, configure and manage SaaS applications using the litesaas-admin
  boilerplate with LiteStartup backend. Use when the user asks to create a new
  SaaS project, scaffold an admin panel, set up LiteStartup integration, or
  add LS-powered features like email, AI, or storage.
metadata:
  author: litestartup-com
  version: "0.1.0"
---

# LiteStartup Admin Skill

Scaffold and manage SaaS applications powered by [litesaas-admin](https://github.com/litestartup-com/litesaas-admin) + LiteStartup backend.

## Security

- API keys stored at `~/.litestartup/credentials`
- **NEVER** read, display, or echo the key in conversation
- **NEVER** ask user to paste the key in chat — guide them to write the file directly
- If auth fails → tell user to check key scope at LS dashboard

## Prerequisites

Check for `.env.local` containing `LS_API_KEY` in the project directory.
- Found → project is configured, proceed with requested action
- Missing → guide user through init (see `references/init.md`)

## Capability Router

When the user makes a request, determine intent and load the relevant file:

| User Intent | Load |
|-------------|------|
| "init saas", "create project", "scaffold", "initialize" | `references/init.md` |
| "configure", "set up env", "connect to LS" | `references/configure.md` |
| "status", "check project" | `references/status.md` |

When the user wants to **add features**, load the relevant section:

| Feature Request | Load |
|----------------|------|
| "send email", "welcome email", "notification" | `references/ls-capabilities.md` § Email |
| "file upload", "avatar", "storage" | `references/ls-capabilities.md` § Storage |
| "ai generate", "ai html", "ai chat" | `references/ls-capabilities.md` § AI |
| "contacts", "crm", "user tags" | `references/ls-capabilities.md` § Contacts |
| "newsletter", "bulk email" | `references/ls-capabilities.md` § Newsletter |

## Project Layout (after init)

```
<project-dir>/
├── .env.local             ← LS credentials (gitignored)
├── app/api/               ← Next.js API routes (server-side proxy to LS)
├── lib/ls-client.ts       ← LS backend client (auth, AI, profile)
├── docker-compose.yml     ← Production deployment
└── ...                    ← Standard Next.js structure
```

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Key expired/invalid | Update `~/.litestartup/credentials` |
| 403 | Missing scope | Key needs `auth` scope (add at LS dashboard) |
| 404 | LS endpoint unreachable | Check `LS_API_URL` in `.env.local` |
| 422 | Configuration error | Verify `.env.local` against `references/env-config.md` |

## DO NOT

- Read or display API keys
- Modify files outside the project directory
- Auto-start `npm run dev` without user confirmation
- Skip scope verification during init
- Hard-code API keys in source files (use `.env.local` only)
- Install global npm packages without asking
