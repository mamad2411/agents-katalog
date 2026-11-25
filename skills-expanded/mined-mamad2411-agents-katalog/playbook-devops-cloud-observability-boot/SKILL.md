---
name: playbook-devops-cloud-observability-boot
description: "Golden signals, structured logs, and alerting wired before the first 3am page."
---
# Playbook: Get observability before you need it

> Golden signals, structured logs, and alerting wired before the first 3am page.

**Track:** 🗺️ DevOps & Cloud · **Domain:** Journey Playbooks · **Level:** journey · **~90 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Golden signals, structured logs, and alerting wired before the first 3am page.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Instrument the four golden signals: start with "Emit RED metrics per endpoint: rate, errors, duration histograms"
2. Step 2 — Adopt structured logging that answers questions: start with "Log JSON with timestamp, level, service, route, request_id, user_id"
3. Step 3 — Run a calm incident response flow: start with "Declare early; assign Incident Commander separate from fixers"
4. How it fits together: SLOs from user journeys, alerts on burn rates. Practice the incident flow before the incident.

### Referenced Skills

- `observability-golden-signals`
- `observability-structured-logging`
- `incidents-vercel-incident-response-flow`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill observability-golden-signals && npx skills add aniruddhaadak80/skills --skill observability-structured-logging && npx skills add aniruddhaadak80/skills --skill incidents-vercel-incident-response-flow
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills