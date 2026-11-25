---
name: crown-jewel
description: "Attack-mode entry point for crown-jewel hunting. Use at the beginning of an authorized bug bounty or pentest session to choose the highest-impact objective before recon or exploitation."
sources: field_recon, hackerone_public
report_count: 50
---

# Crown Jewel Mode

Use this mode when the operator invokes `/crown-jewel <target or program>`.

The goal is to stop generic hunting before it starts. First identify the target's highest-value harm, then route every recon and manual test toward that harm.

## Output Contract

Produce a concise plan with:
- `engagement_type`: bug bounty, pentest, red team, or internal audit
- `target`: target/program/client
- `primary_crown_jewel`: the one impact objective to prioritize
- `secondary_crown_jewels`: 2-4 fallback objectives
- `highest_value_surfaces`: concrete surfaces to map first
- `first_attack_modes`: which modes to invoke next
- `dossier_path`: where the target dossier should live
- `kill_signals`: what would make this target or path low-value

If the user does not provide enough context, make a best-effort assumption from the target type and state it. Ask only if scope/authorization is impossible to infer.

## Crown Jewel Taxonomy

Choose the strongest realistic objective:

| Target type | Primary crown jewels | High-yield surfaces |
|---|---|---|
| SaaS / B2B | cross-tenant data, org admin takeover, support/operator access | workspace switchers, exports, roles, invites, support panels, GraphQL, AI/RAG |
| Fintech / billing | money movement, credits/refunds, invoice data, privileged treasury actions | checkout, coupons, refunds, invoices, webhooks, archived prices, ledgers |
| Auth / identity | account takeover, SSO bypass, OAuth token theft, tenant takeover | recovery, OAuth/OIDC, SAML, device code, MFA reset, invite flows |
| Developer platform | source code, CI/CD secrets, package publishing, runner execution | repos, imports, webhooks, GitHub Apps, runners, artifacts, tokens |
| Marketplace / ecommerce | seller takeover, order manipulation, refunds, PII | seller onboarding, product import, orders, refunds, coupons, shipping |
| Healthcare / HR | PII/PHI, employee data, document disclosure | exports, attachments, portals, support views, search, delegated access |
| Cloud / infra | cloud creds, control plane, internal services, workload execution | metadata, storage, dashboards, CI, Kubernetes, service tokens |
| AI / agent product | cross-tenant docs, prompt/tool secrets, unauthorized actions | threads, vector stores, tools, citations, uploaded files, support transcripts |

## Decision Loop

1. Name the business model.
2. Name the attacker role that is easiest to obtain.
3. Name the asset that would hurt most if compromised.
4. Name the workflow most likely to touch that asset.
5. Route into a concrete mode:
   - `/target-dossier` to create the persistent campaign memory
   - `/request-import` when the user has HAR/Burp traffic
   - `/deep-hunt recovery|billing|graphql|import|ai|roles|export|support|race`
   - `/attack-chain` when any primitive appears

## Operator Prompts

Use these questions internally:
- What would make this a P1/P2 instead of a P4?
- Which workflow has the fewest eyes and the most authority?
- Which actor can be created for free?
- Which object moves between tenants, roles, states, or background workers?
- Which secondary object would expose the crown jewel even if the primary endpoint is protected?
- Which recently shipped or legacy path probably reused auth incorrectly?

## Next Step Rule

Always end with one concrete next command. Example:

```text
Next command:
/target-dossier acme-saas --objective "cross-tenant invoice/export data"
```

