---
name: use-checklist-format
description: "Convert a procedure into a checklist with observable completion criteria and clear dependencies."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["checklists", "pre-flight", "deployment-checklists", "task-execution", "markdown", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask for Interactive Checklist Format (The Pre-Flight Gate) (AI Skill)

## Overview
When asking an AI how to execute a complex, multi-step process (*"How do I migrate our database to AWS?"* or *"How do I prepare for our product launch?"*), standard outputs provide long narrative paragraphs. In high-pressure operational environments, paragraphs are easily misread, causing skipped steps and unforced errors.

The **Interactive Checklist Protocol** enforces the aviation-standard **Pre-Flight Checklist Model**, formatting every procedure into actionable, phase-gated Markdown checkboxes (`- [ ]`) with explicit verification criteria.

---

## Narrative Paragraphs vs. Phase-Gated Checklists

```
┌─────────────────────────────────────────────────────────────┐
│                 Procedural Clarity Mapping                  │
│                                                             │
│  Narrative Guide (High Risk of Human Error):                │
│  "Make sure you take a snapshot of the database before you  │
│   run the migration script, and remember to check that the  │
│   S3 backup bucket has public access disabled..."           │
│  ↳ Dense text, easy to skip the S3 bucket permission check  │
│                                                             │
│  Phase-Gated Markdown Checklist:                            │
│  ### Phase 1: Pre-Flight Safety Checks                      │
│ - [ ] 1. Trigger manual RDS snapshot: `db-snapshot-v2`     │
│ - [ ] 2. Verify S3 bucket encryption is set to AES-256     │
│ - [ ] 3. Confirm `DATABASE_URL` is set on staging          │
│  ↳ Zero-Ambiguity, Linear Execution, 1-Click Verification   │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Checklist Prompt Templates

### Pattern 1: The 3-Phase Operational Pre-Flight Checklist
Use for technical deployments, migrations, and event launches:

```markdown
I need to execute [PROCEDURAL TASK: e.g. Deploying Next.js 15 app with Stripe to production].

Generate an executable **3-Phase Markdown Checklist** with interactive checkboxes (`- [ ]`):
1. **Phase 1: Pre-Flight (Prerequisites & Backups)** - Mandatory verification before touching production.
2. **Phase 2: Live Cutover (Execution Steps)** - Step-by-step sequential commands in exact order.
3. **Phase 3: Post-Flight QA & Verification** - Health checks, smoke tests, and rollback trigger condition.

Rules:
- Include exact terminal commands / URLs where applicable.
- State the specific Rollback Trigger: "If [X] fails within 5 mins, execute [Y]".
```

---

## Real-World Case Study

### Scenario: Zero-Downtime Production Database Migration Checklist

```markdown
### 🔒 Phase 1: Pre-Flight Safety Checks (T-Minus 30 Mins)
- [ ] 1. Verify point-in-time recovery (PITR) is enabled on AWS RDS.
- [ ] 2. Create manual snapshot: `aws rds create-db-snapshot --db-instance-identifier prod-db`.
- [ ] 3. Verify replication lag is $<1.0\text{s}$ on read replicas.
- [ ] 4. Announce planned maintenance window in `#internal-ops` Slack channel.

### ⚡ Phase 2: Live Migration Execution (T-Minus 0 Mins)
- [ ] 5. Run schema migration: `npm run db:migrate:deploy`.
- [ ] 6. Verify all table indexes built with `CONCURRENTLY` flag.
- [ ] 7. Deploy new application container image (v2.4.1).

### 🩺 Phase 3: Post-Flight Smoke Tests (T-Plus 15 Mins)
- [ ] 8. Send test payload to `/api/health` and verify `200 OK`.
- [ ] 9. Place a live test payment with test card; verify webhook logs in Stripe Dashboard.
- [ ] 10. Confirm CPU utilization remains $<45\%$ in Datadog metrics.

### 🚨 Emergency Rollback Trigger
- [ ] If HTTP 5xx error rate exceeds $1.0\%$ for $>2$ minutes:  
      Rollback container: `kubectl rollout undo deployment/api-server`.
```

---

## Summary Best Practices
- **Always demand `- [ ]` markdown format**: Allows you to copy directly into GitHub issues, Linear, Notion, or Obsidian and check off items interactively.
- **Always include an Emergency Rollback step**: An operational checklist is incomplete without an explicit undo trigger.
