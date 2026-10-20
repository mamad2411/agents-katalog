---
name: never-paste-private-passwords
description: "Replace passwords, API keys, payment details, and personal identifiers with placeholders before sharing prompts or examples."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["cybersecurity", "secrets-management", "privacy", "api-keys", "data-protection", "safety"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Never Paste Passwords, Keys, or PII (Zero-Secrets Hygiene) (AI Skill)

## Overview
Pasting real database passwords, production API keys (`sk-proj-...`, `AKIA...`), SSH private keys, credit cards, or customer Personally Identifiable Information (PII) into an AI chat creates immediate, catastrophic security exposure. 

Chat logs can be accessed by human data annotators during model training, stored in unencrypted browser caches, exposed via shared workspace links, or compromised in third-party API breaches.

The **Zero-Secrets Hygiene Protocol** establishes strict rules and automated dummy placeholder habits to keep your credentials 100% secure.

---

## The Secret Leak Exposure Vector

```
┌─────────────────────────────────────────────────────────────┐
│                 Where Pasted Secrets Travel                 │
│                                                             │
│  User Pastes Real AWS Key / API Secret into Chat Box        │
│                           │                                 │
│                           ▼                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ • Stored in SaaS provider server logs & vector indices │  │
│  │ • Visible to human RLHF / model review annotators     │  │
│  │ • Visible to teammates in shared organization chats   │  │
│  │ • Risk of model weights ingestion in public training  │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           ▼                                 │
│  [ SECURITY COMPROMISE: Treat Any Pasted Key as Revoked ]   │
└─────────────────────────────────────────────────────────────┘
```

---

## High-Risk Credentials Checklist

Never paste any string matching these patterns into an AI prompt:

| Credential Type | Real Example Pattern | Safe Dummy Placeholder to Use |
| :--- | :--- | :--- |
| **OpenAI / Anthropic Keys** | `sk-proj-49f8a...`, `sk-ant-...` | `os.getenv("OPENAI_API_KEY")` |
| **AWS Access Keys** | `AKIAIOSFODNN7EXAMPLE` | `YOUR_AWS_ACCESS_KEY_ID` |
| **GitHub Tokens** | `ghp_39d8fj29...` | `YOUR_GITHUB_TOKEN` |
| **Database URLs** | `postgres://user:pass@db:5432` | `postgresql://USER:PASSWORD@HOST:5432/DB` |
| **Private SSH / RSA Keys** | `-----BEGIN RSA PRIVATE KEY-----` | **NEVER PASTE. USE ENVIRONMENT VARIABLES** |
| **Financial / Personal IDs** | Credit cards, CVVs, SSNs, Passports | Synthetic dummy numbers (`4111 1111...`) |

---

## Safe Code Scaffolding: The `.env` Standard

When asking an AI to write integration code, always instruct it to use **Environment Variables** rather than hardcoded credentials:

```markdown
Write a Python script to send transactional emails using SendGrid.

Security Rules:
- Load the API key from environment variables: `os.environ["SENDGRID_API_KEY"]`.
- Do NOT hardcode any strings or fake keys in the script.
- Include a sample `.env.example` file showing the required key names.
```

---

## Emergency Protocol: What to Do If You Accidentally Paste a Key

If you accidentally submit a real password or API key to an AI assistant:

```
┌───────────────────────────────────────────────────────────────────────────┐
│ 1. REVOKE IMMEDIATELY: Go to the provider console and DELETE the key.     │
│ 2. REGENERATE: Generate a new key and update your production `.env`.      │
│ 3. AUDIT LOGS: Check CloudTrail / API access logs for unauthorized use.  │
│ 4. DELETE CHAT: Delete the conversation thread from the AI platform.      │
└───────────────────────────────────────────────────────────────────────────┘
```
*(Note: Deleting the chat alone is NOT enough. The moment a key hits an external server, you must treat it as permanently compromised and rotate it immediately).*

---

## Summary Rule of Thumb
> **"If a string can authorize money, access private data, or log into a server, it belongs in an environment variable - NEVER in a chat box."**
