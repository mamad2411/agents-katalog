---
name: write-step-by-step-how-to
description: "Write a practical procedure with prerequisites, ordered steps, expected results, and troubleshooting."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["sop-creation", "tutorials", "how-to-guides", "documentation", "procedural-clarity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Write Step-by-Step SOP How-To Guides (AI Skill)

## Overview
Generic how-to guides (*"Go to settings and configure your domain"*) frequently fail users because they omit exact button names, skip prerequisite permission steps, and fail to describe what the screen should look like after a successful action.

The **Linear SOP Protocol** structures every procedural tutorial into the industrial **Standard Operating Procedure (SOP) Schema**: specifying the **Exact Click/CLI Path**, the **Expected System State**, and the **Troubleshooting Pitfall** for each step.

---

## The 4-Component SOP Step Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 The 4-Component SOP Step                    │
│                                                             │
│  [ STEP NUMBER & GOAL ]: Step 2 - Configure CNAME Record    │
│  • EXACT ACTION: Click "Add Record" ──► Select "CNAME"      │
│  • INPUT VALUES: Name = "app", Target = "cname.vercel-dns"  │
│  • EXPECTED STATE: Green checkmark badge "DNS Active"       │
│  • PITFALL / GOTCHA: Turn OFF the orange Cloudflare proxy!  │
└─────────────────────────────────────────────────────────────┘
```

---

## Master SOP Generator Prompt Templates

### Pattern 1: The Industrial SOP / Software Tutorial Generator
Use for software onboarding, devops guides, or employee workflows:

```markdown
Write a step-by-step Standard Operating Procedure (SOP) for [PROCEDURAL TASK: e.g. Setting up AWS S3 Bucket with Private Read Access and CloudFront CDN].

Target Audience: Junior DevOps Engineer.

Structure the guide strictly using this format:
1. **Prerequisites & Required Permissions** (Bullet list of tools/accounts needed).
2. **Sequential Numbered Steps**:
   For EACH step provide:
  - **Action**: Exact UI button clicks or CLI command.
  - **Configuration Values**: Table/list of exact parameters to enter.
  - **Expected Verification**: What the user should see on screen to confirm success.
  - **⚠️ Common Gotcha**: The #1 mistake users make on this specific step.
3. **End-to-End Smoke Test** (1 command or test click to verify the entire system is working).
```

---

## Real-World Case Study

### Scenario: Pointing a Custom Domain to a Vercel Web App via Cloudflare DNS

#### Weak Tutorial (Vague & Frustrating)
> *"Log into Cloudflare, go to DNS, and add a CNAME record pointing to Vercel. Then wait for it to propagate."*
> ❌ *(Omitted proxy toggle; creates infinite SSL redirect loop error 521).*

#### Linear SOP Output (Bulletproof Execution)

```markdown
### 🛠️ Step 1: Add the Root CNAME Record
- **Action**: Navigate to **Cloudflare Dashboard** $\rightarrow$ Click **DNS** $\rightarrow$ **Records** $\rightarrow$ Click **Add Record**.
- **Fields to Enter**:
 - **Type**: `CNAME`
 - **Name**: `@` (or `subdomain`)
 - **Target**: `cname.vercel-dns.com`
 - **Proxy Status**: **DNS ONLY (Grey Cloud)** ⚠️ *CRITICAL*
- **Expected Verification**: Record appears in the table with status `DNS only`.
- **⚠️ Common Gotcha**: If Proxy status is set to *Proxied (Orange Cloud)*, Cloudflare's SSL will conflict with Vercel's SSL, causing an `ERR_TOO_MANY_REDIRECTS` crash.

### 🩺 Step 2: Verification Smoke Test
- In your terminal, run: `dig +short yourdomain.com`
- Expected output: `cname.vercel-dns.com` (Returns in $<100\text{ms}$).
```

---

## Summary Best Practices
- **Never write "Go to settings" without the full breadcrumb**: Write `Settings > Team > Billing > Invoices`.
- **Always include the "Common Gotcha"**: Pointing out the failure mode saves 30 minutes of frustrated debugging.
