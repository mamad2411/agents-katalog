---
name: ccpa-cpra
description: >-
  CCPA and CPRA: honor California consumer privacy rights, notices and opt-outs of sale or sharing. Covers CCPA. Use when applying the California Consumer Privacy Act. Triggers: CCPA, CPRA.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# CCPA

California Consumer Privacy Act (CCPA) | State of California - Department of Justice - Office of the Attorney General

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when applying the California Consumer Privacy Act.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: CCPA (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **A. GENERAL INFORMATION ABOUT THE CCPA.** "Before suing, you must give the business written notice of which CCPA sections it violated and allow 30 days to respond in writing that it has cured the violations and that no further violations will occur."
2. **A. GENERAL INFORMATION ABOUT THE CCPA.** "The type of personal information that must have been stolen is your first name (or first initial) and last name in combination with any of the following: Your social security number Your driver’s license number, tax identification number, passport number, military identification number, or other unique identification number issued on a government document commonly used to identify a person's…"
3. **A. GENERAL INFORMATION ABOUT THE CCPA.** "In addition, the personal information must have been stolen in a data breach as a result of the business’s failure to maintain reasonable security procedures and practices to protect it."
4. **B. RIGHT TO OPT-OUT OF SALE OR SHARING.** "Businesses must wait at least 12 months before asking you to opt back in to the sale or sharing of your personal information."
5. **B. RIGHT TO OPT-OUT OF SALE OR SHARING.** "For children under the age of 13, that opt-in must come from the child’s parent or guardian."
6. **B. RIGHT TO OPT-OUT OF SALE OR SHARING.** "Businesses also should not require you to verify your identity, though they can ask you basic questions to identify which personal information is associated with you."
7. **B. RIGHT TO OPT-OUT OF SALE OR SHARING.** "If the business does, it must also include that link in its privacy policy."
8. **B. RIGHT TO OPT-OUT OF SALE OR SHARING.** "Businesses must respond as soon as feasibly possible to your request, up to a maximum of 15 business days from the date they received your request to opt-out."

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

- [CCPA](https://oag.ca.gov/privacy/ccpa): Attorney General page, California Attorney General CCPA page, fetched 2026-10-06 (Attorney General page, 2026-10-06), checked 2026-10-06.
