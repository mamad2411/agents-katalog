---
name: owasp-aivss
description: >-
  OWASP AIVSS: score the severity of vulnerabilities in AI and agentic systems. Covers OWASP AIVSS. Use when scoring AI vulnerability severity. Triggers: AIVSS.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OWASP AIVSS

The OWASP AI Vulnerability Scoring System (AIVSS) v0.8: it takes a vulnerability's CVSS v4.0 base score, adds an Agentic Uplift (AARS) computed from ten risk amplification factors and a threat multiplier, and scales the sum by a mitigation factor. Read from the project's published PDF, pinned at a commit of its GitHub repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Assessor scoring a vulnerability in an agentic AI system, or the owner of the vulnerability management process that consumes AIVSS scores.
- Target version: OWASP AIVSS (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Part 2 § 3.1.1.** "AIVSS requires CVSS v4.0 as its baseline scoring input."
2. **Part 2 § 3.3.1.** "AARS = (10 - CVSS_Base) * (Factor_Sum / 10) * ThM"
3. **Part 2 § 3.4.** "AIVSS = (CVSS_Base + AARS) * Mitigation_Factor"
4. **Part 2 § 3.4.0.** "Report the final score: AIVSS = RoundHalfUp(AIVSS_raw, 1) (nearest tenth)"
5. **Part 2 § 3.2.** "Do not average scores across findings."

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
- [ ] Each score records its CVSS v4.0 base, the ten factor values, ThM and Mitigation_Factor, and the final AIVSS value equals RoundHalfUp((CVSS_Base + AARS) * Mitigation_Factor, 1).
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `cvss`, `ssvc`, `owasp-agentic`, `owasp-ai-exchange`, `epss`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [AIVSS Scoring System For OWASP Agentic AI Core Security Risks v0.8](https://raw.githubusercontent.com/OWASP/www-project-artificial-intelligence-vulnerability-scoring-system/84856b290f62f2327f70eb0027be64351dd2e6de/assets/publications/AIVSS%20Scoring%20System%20For%20OWASP%20Agentic%20AI%20Core%20Security%20Risks%20v0.8.pdf): OWASP Project document (draft), v0.8, commit 84856b290f62 (2026-09-09), checked 2026-10-06.
