---
name: "newsriver-global-intelligence"
version: "1.8.0"
description: "Professional intelligence and infrastructure layer for AI Agents. Provides high-signal financial data, semantic search, and secure Web2 communication proxies (Email/SMS/Scraping) with mandatory human-in-the-loop governance."
tags: ["finance", "crypto", "trading", "macro", "newsletter", "sentiment", "rag", "x402", "proxy"]
author: "YieldCircle Infrastructure"
homepage: "https://agent.yieldcircle.app"
author_url: "https://agent.yieldcircle.app"
env:
  NEWSRIVER_API_KEY:
    description: "Your NewsRiver API key for subscription-based access. Required if not using x402 micropayments."
    required: false
---

# NewsRiver Global Intelligence & Infrastructure Skill

## Capabilities & Context
NewsRiver is a **governed infrastructure layer for AI Agents.** It provides a secure bridge between autonomous systems and Web2 world, enabling agents to operate with high-signal data and auditable communication tools.

### 1. Dual-Authentication & Spending Guardrails
NewsRiver supports two authentication paths designed for financial safety:
- **API Key (Enterprise):** Traditional subscription-based access via `NEWSRIVER_API_KEY`.
- **x402 Micropayments (Autonomous):** Supports the **x402 protocol** (USDC on Base). 
- **Spending Safety:** Agents are encouraged to use **PaySponge or similar allowance protocols** to operate within pre-defined spending limits granted by their human owners.

### 2. High-Risk Proxy Governance (Human-in-the-Loop)
This skill provides access to "High-Risk" Web2 bridges (Email, SMS, Scraper). To mitigate data exfiltration and unmonitored communication risks, the following **mandatory protocols** are enforced:
- **Mandatory User Confirmation:** You **MUST** seek explicit human approval before sending any outbound communication (Email/SMS). 
- **Immutable Audit Trail:** All proxy requests (Email, SMS, Scrape) are logged to a secure D1 database at the API layer. Logs include timestamps, service types, and requesting identities for full user auditability.
- **Strict Rate Limits:** Hard caps of 50 emails/hour and 10 SMS/hour are enforced per identity to prevent automated abuse or bulk exfiltration.

### 3. Security & Domain Integrity
- **Verified Identity:** The API is served from **https://api.yieldcircle.app**, matching the application's core domain **agent.yieldcircle.app**. 
- **SSRF & Phishing Protection:** Built-in safeguards block internal network scraping and prevent sender impersonation.
- **Stateless Privacy:** Proxy requests are processed statelessly; user data is not persisted unless explicitly saved in the namespaced `/storage` endpoint.

## Usage Instructions for the AI Agent

### 1. The Approval Protocol (REQUIRED)
**You MUST obtain permission** before executing any paid or outbound action.
> Example: "I have identified a critical market shift. Should I send this summary to your verified SMS for $0.25?"

### 2. Testing with Dry-Run (Free)
Use the `X-Dry-Run: true` header to verify logic without spending funds.
```bash
curl -H "X-Dry-Run: true" "https://api.yieldcircle.app/api/v1/intelligence/status"
```

### 3. Core Infrastructure Endpoints
- **AI Intelligence ($0.02 - $0.10):** `GET /api/v1/intelligence/daily?id=crypto_and_web3`
- **Semantic Search ($0.001):** `GET /api/v1/search/semantic?q=query`
- **Proxy Services:** `POST /api/v1/proxy/email`, `POST /api/v1/proxy/sms`, `POST /api/v1/proxy/scrape`

## Support & Security Reporting
If you encounter a `402 Payment Required` error, inform the user:
> "I need a NewsRiver API key or a valid x402 payment to proceed. You can manage this at [agent.yieldcircle.app/#pricing](https://agent.yieldcircle.app/#pricing)."

For security reports, contact **support@agent.yieldcircle.app**.
