---
name: opengitops
description: >-
  OpenGitOps: OpenGitOps is a set of open-source standards, best practices, and community-focused education to help organizations adopt a structured, standardized approach to implementing GitOps . Covers OpenGitOps. Use when applying the OpenGitOps principles. Triggers: OpenGitOps.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OpenGitOps

The GitOps Principles and the GitOps Glossary from the OpenGitOps project (CNCF), release v1.0.0, read from the open-gitops/documents repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Platform or operations team designing GitOps delivery, or a GitOps agent or tool implementer.
- Target version: OpenGitOps (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Principle 1: Declarative.** "A system managed by GitOps must have its desired state expressed declaratively."
2. **Principle 2: Versioned and Immutable.** "Desired state is stored in a way that enforces immutability, versioning and retains a complete version history."
3. **Principle 3: Pulled Automatically.** "Software agents automatically pull the desired state declarations from the source."
4. **Principle 4: Continuously Reconciled.** "Software agents continuously observe actual system state and attempt to apply the desired state."
5. **Glossary: Declarative Description.** "A configuration that describes the desired operating state of a system without specifying procedures for how that state will be achieved."
6. **Glossary: Desired State.** "The aggregate of all configuration data that is sufficient to recreate the system so that instances of the system are behaviourally indistinguishable."
7. **Glossary: Reconciliation.** "Contrary to traditional CI/CD where automation is generally driven by pre-set triggers, in GitOps reconciliation is triggered whenever there is a divergence."
8. **Glossary: State Store.** "A system for storing immutable versions of desired state declarations."
9. **Glossary: State Store.** "This state store should provide access control and auditing on the changes to the Desired State."

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
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `kubernetes-api-conventions`, `slsa`, `in-toto`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [GitOps Principles](https://raw.githubusercontent.com/open-gitops/documents/d36cde829c6ef2c7e5cab662ab98a7173a591a49/PRINCIPLES.md): Release, v1.0.0 (commit d36cde8), checked 2026-10-06.
- [GitOps Glossary](https://raw.githubusercontent.com/open-gitops/documents/d36cde829c6ef2c7e5cab662ab98a7173a591a49/GLOSSARY.md): Release, v1.0.0 (commit d36cde8), checked 2026-10-06.
