---
name: target-dossier
description: "Create and maintain a persistent target dossier for authorized offsec campaigns. Use as /target-dossier <target> to initialize or update .offsec/campaigns/<target>/TARGET.md."
sources: field_recon
report_count: 50
---

# Target Dossier Mode

Use this mode when the operator invokes `/target-dossier <target>`.

This command keeps the hunt from resetting every turn. It creates or updates a repo-local campaign dossier and forces every later test to attach to actors, objects, states, hypotheses, evidence, and chains.

## Required Behavior

1. Derive a safe target slug from the user instruction.
2. If the dossier does not exist, run:

```bash
python skills/offsec/meta/target-dossier/scripts/init_dossier.py "<target>"
```

3. Read the created or existing dossier.
4. Update it after meaningful discoveries.
5. Never keep the whole dossier only in chat memory.

## Dossier Layout

```text
.offsec/
  campaigns/
    <target-slug>/
      TARGET.md
      CAMPAIGN.md
      request-map.md
      chains/
      evidence/
      imports/
```

## Update Contract

When updating the dossier, touch the smallest relevant sections:
- crown jewel objective
- asset map
- actor matrix
- object families
- state machines
- request map summary
- high-value surfaces
- hypotheses
- tested branches
- chain candidates
- evidence
- next best actions

## Automatic Dossier Thinking

Every time the user shares recon output, HAR/Burp traffic, a finding, or a failed test, ask internally:
- Does this reveal a new actor?
- Does this reveal a new object family?
- Does this reveal a new state transition?
- Does this reveal a side-effect surface?
- Does this create or kill a chain candidate?
- Does this change the next best action?

If yes, update `TARGET.md` or the relevant chain card.

## Output Contract

Return:
- dossier path
- what changed
- current crown jewel
- strongest hypothesis
- next command to run

