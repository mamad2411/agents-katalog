---
name: software-engineer
description: >-
  Software engineering toolkit, one skill with sub-skills. (1) release-docs: the release report for the PM,
  the BA and QA (what goes up in vX.Y.Z, before/after screenshots per change, open BA decisions, the staging
  test plan) from a Thai or English template, checked by a script and rendered to PDF in the documentation
  house style. Use WHENEVER the work is "the release report", "release docs", "release document for the PM",
  "test plan for the release", "สรุปรายการที่จะขึ้น release เป็นเอกสาร", "เอกสาร release", "แผนเทส release".
  Read the sub-skill's SKILL.md before acting.
---

# software-engineer: sub-skills

| When the work is… | Read | Scripts |
|---|---|---|
| "the release report", "release docs", "test plan for the release", "เอกสาร release" | [`release-docs/SKILL.md`](release-docs/SKILL.md) + [`references/template-th.md`](release-docs/references/template-th.md) / [`template-en.md`](release-docs/references/template-en.md) | `release-docs/scripts/check_report.py`; renders with `documentation/doc-style/scripts/build_doc.py --css release-docs/assets/release.css` |

It chains with two other skills: `devops-release-scope` collects what goes up (`scope.md`), `release-docs`
writes the document, and `documentation-doc-style` renders it.

## Rules every sub-skill keeps

- **Ground every fact in the source**: the ticket, the retest result, the PR. Never invent a number.
- **Reuse before building**: one theme and one renderer (documentation's `build_doc.py`); a sub-skill adds a
  stylesheet, not a second pipeline.
- No real hosts, company names, people or client data in a template or example. Mock names use the
  thai-mock-naming markers.
