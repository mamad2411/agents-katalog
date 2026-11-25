---
name: lbh-auto-updater
version: 1.0.0
description: Update an installed legal skill to a newer version safely — re-run the security gate on the new version, diff behavior, and keep a rollback point.
author: matrixx0070
tags: [legal, update, versioning, rollback, security]
capabilities: []
---

## When to use

Use this when an installed legal skill has a newer version available and the user wants it. An update is not a no-op: a new version is a new artifact that must clear the gate again. This skill re-vets, diffs, applies, and leaves a clean rollback point.

**Not for:** first-time installs (`lbh-skill-installer`), initial vetting of an unknown skill (`lbh-skills-qa` directly), or removing a skill (`lbh-uninstall`). It also does not silently auto-apply — updates are proposed and confirmed.

## Method

1. Compare installed version to available; if none newer, stop and report current.
2. Treat the new version as untrusted: route it through `lbh-skills-qa`. A new version does not inherit the old version's PASS.
3. Diff the two versions: changed capabilities, new triggers, and — critically — any newly introduced unsafe primitive. Highlight scope creep.
4. Confirm the update with the user, showing the diff and the new QA verdict. Never apply an update that regressed the gate.
5. Snapshot the current install (version + checksum + conditions) as the rollback point before swapping.
6. Apply the update disabled-first if the diff is large, then enable; record the new provenance and keep the rollback point until the next stable window.

## Example

`nda-review@1.4` has 1.5 available. QA on 1.5 passes but the diff shows a new "fetch external clause set" line — a BLOCKER that 1.4 lacked. You do not apply it; you report the regression and keep 1.4. Contrast: `saas-review@2.1 -> 2.2` diff is only prompt wording, QA passes, you snapshot 2.1, apply 2.2, and note rollback is available.

## Pitfalls

- Assuming a version bump is safe because the old one passed. Re-gate every new artifact.
- Applying without a rollback snapshot, so a bad update cannot be cleanly reverted.
- Ignoring capability/trigger creep, where an "update" quietly expands what the skill does.
- Auto-applying on a schedule without user confirmation for legal skills. Propose, then apply.

## Output format

```
# Update — <name> <cur> -> <new>
QA(new): <PASS|FAIL(...)>  (required, not inherited)
DIFF: capabilities=<+/-> triggers=<+/-> unsafe-primitives=<none|NEW:...>
DECISION: apply | hold(<reason>)
ROLLBACK POINT: <name>@<cur> checksum=<hash> stored=<y>
STATE: applied disabled->enabled=<y/n> at=<ts>
```

## Reference

**Skill-vetting checklist (update link):** the new version must independently satisfy the full checklist — identity, no unsafe primitives, disclaimer, pinned coordinate.

**Security-review gate criteria:** any unsafe primitive present in the new version but absent in the old is a regression BLOCKER — hold the update. A new version never inherits a prior PASS.

**Versioning / rollback:** always store the prior `name@version` + checksum before swapping; on any post-update issue, restore that snapshot. Prefer pinned targets over "latest" so updates are deliberate.
