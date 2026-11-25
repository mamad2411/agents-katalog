---
name: target-dossier-system
description: Persistent target-memory workflow for offsec campaigns. Use when you need structured memory for actors, objects, state transitions, secrets, hypotheses, and chain candidates on a real target.
sources: field_recon
report_count: 50
---

# Target Dossier System

The agent should not hunt from scratch every turn. Maintain a dossier.

## File system convention

Use repo-local notes, not just chat memory:
- `.offsec/templates/target-dossier.md`
- `.offsec/templates/campaign-plan.md`
- `.offsec/templates/exploit-chain-card.md`

Recommended working tree:

```text
.offsec/
  campaigns/
    <target-slug>/
      TARGET.md
      CAMPAIGN.md
      request-map.md
      chains/
        <chain-name>.md
      evidence/
      imports/
```

## What belongs in the dossier

Always capture:
- crown jewel objective
- actor matrix
- object families
- state transitions
- auth artifacts
- request-map summaries
- helper objects
- secondary objects
- integration surfaces
- tested and disproven hypotheses
- chain candidates

## What belongs in memory tool

Only durable, cross-session facts:
- target uses GraphQL with global IDs
- target has invite plus owner-transfer workflow
- admin/support panel exists on subdomain X
- imports trigger background jobs through service Y

Do not put the whole notebook in memory.

## Update discipline

After any meaningful test:
- update the dossier if the target model changed
- update `request-map.md` if the user provides HAR/Burp/raw HTTP traffic
- add chain candidates when a primitive appears
- mark disproven branches so the next turn does not repeat work

If the dossier does not evolve, the hunt quality will drift downward.

## Automation hooks

Use the lighter operator-facing command when possible:

```bash
python skills/offsec/meta/target-dossier/scripts/init_dossier.py "<target>"
python skills/offsec/meta/request-import/scripts/har_burp_mapper.py "<traffic.har>" -o ".offsec/campaigns/<target-slug>/request-map.md"
```

Prefer `/target-dossier` and `/request-import` in normal conversation. Use the scripts directly only when the user asks for explicit file creation or when the mode needs deterministic output.
