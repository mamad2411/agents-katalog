---
name: uk-online-safety-act
description: >-
  UK Online Safety Act 2023: apply the duties for user-to-user and search services, including illegal content and child safety. Covers Online Safety Act 2023. Use when applying the UK Online Safety Act. Triggers: Online Safety Act.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Online Safety Act 2023

2023 CHAPTER 50 An Act to make provision for and in connection with the regulation by OFCOM of certain internet services; for and in connection with communications offences; and for connected purposes.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when applying the UK Online Safety Act.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Online Safety Act 2023 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **(1).** "Subsections (2) to (6) apply to determine which of the duties set out in this Chapter (and, in the case of combined services, Chapter 3) must be complied with by providers of regulated user-to-user services."
2. **(2).** "All providers of regulated user-to-user services must comply with the following duties in relation to each such service which they provide—"
3. **(3).** "Additional duties must be complied with by providers of particular kinds of regulated user-to-user services, as follows."
4. **(4).** "All providers of regulated user-to-user services that are likely to be accessed by children must comply with the following duties in relation to each such service which they provide—"
5. **(5).** "All providers of Category 1 services must comply with the following duties in relation to each such service which they provide—"
6. **(6).** "All providers of combined services must comply with the following duties in relation to the search engine of each such service which they provide—"
7. **(1).** "A duty set out in this Chapter which must be complied with in relation to a user-to-user service that includes regulated provider pornographic content does not extend to—"
8. **(2).** "A duty set out in this Chapter which must be complied with in relation to a combined service does not extend to—"

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Online Safety Act 2023](https://www.legislation.gov.uk/ukpga/2023/50/data.html): Act, Online Safety Act 2023, fetched 2026-10-06 (Act, 2026-10-06), checked 2026-10-06.
