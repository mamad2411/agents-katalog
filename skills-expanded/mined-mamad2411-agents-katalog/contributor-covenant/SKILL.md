---
name: contributor-covenant
description: >-
  Contributor Covenant: adopt and enforce a code of conduct for an open source community. Covers Contributor Covenant 3.0, Contributor Covenant 2.1 (supported). Use when adopting a code of conduct. Triggers: Contributor Covenant.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Contributor Covenant

The Contributor Covenant code of conduct, stewarded by the Organization for Ethical Source, read from the `code_of_conduct.md` sources for version 3.0 and version 2.1 in the EthicalSource/contributor_covenant repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Maintainer adopting the code of conduct in a repository, or a community moderator enforcing it.
- Target version: Contributor Covenant 3.0 (current); Contributor Covenant 2.1 (supported). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **3.0 § Restricted Behaviors.** "We agree to restrict the following behaviors in our community. Instances, threats, and promotion of these behaviors are violations of this Code of Conduct."
2. **3.0 § Restricted Behaviors.** "**Harassment.** Violating explicitly expressed boundaries or engaging in unnecessary personal attention after any clear request to stop."
3. **3.0 § Reporting an Issue.** "To report a possible violation, **[NOTE: describe your means of reporting here.]**"
4. **3.0 § Reporting an Issue.** "Community Moderators will keep investigation and enforcement actions as transparent as possible while prioritizing safety and confidentiality."
5. **3.0 § Addressing and Repairing Harm.** "Depending on the severity of a violation, lower rungs on the ladder may be skipped."
6. **3.0 § Scope.** "This Code of Conduct applies within all community spaces, and also applies when an individual is officially representing the community in public or other spaces."
7. **3.0 § Attribution.** "This Code of Conduct is adapted from the Contributor Covenant, version 3.0, permanently available at"
8. **2.1 § Enforcement.** "Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the community leaders responsible for enforcement at [INSERT CONTACT METHOD]."
9. **2.1 § Enforcement.** "All community leaders are obligated to respect the privacy and security of the reporter of any incident."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] The reporting placeholder (3.0 § Reporting an Issue, or `[INSERT CONTACT METHOD]` in 2.1 § Enforcement) is replaced by a real contact method.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `reuse`, `editorconfig`, `keep-a-changelog`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Contributor Covenant 3.0 Code of Conduct](https://raw.githubusercontent.com/EthicalSource/contributor_covenant/7255a28d23d5bc296de2e4e4e9bb5ee1126f1345/content/version/3/0/code_of_conduct.md): Released version, Version 3.0, release branch at commit 7255a28, checked 2026-10-06.
- [Contributor Covenant 2.1 Code of Conduct](https://raw.githubusercontent.com/EthicalSource/contributor_covenant/7255a28d23d5bc296de2e4e4e9bb5ee1126f1345/content/version/2/1/code_of_conduct.md): Released version, Version 2.1, release branch at commit 7255a28, checked 2026-10-06.
