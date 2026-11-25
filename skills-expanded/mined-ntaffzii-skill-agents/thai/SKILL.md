---
name: thai
description: Route and manage Thai-locale domain-knowledge skills — Thai tax documents, government letters, PDPA notices, national ID/PromptPay validation, BE/CE date conversion, addresses, social captions, customer-service replies, resumes, and translation. Use when the user asks for Thai-specific documents, formats, or validations that a general-purpose agent tends to get wrong, such as VAT/WHT math, พ.ศ./ค.ศ. date conversion, national ID checksum, or register-aware EN-TH translation.
---

# Thai Locale Skills

Use this skill to find or scaffold a Thai-specific domain-knowledge skill under `skills/thai/`.

## Purpose

`skills/thai/` holds content-domain skills for Thai-specific facts, formats, and documents — the kind of task where a general-purpose agent silently guesses wrong (date era, honorific register, legal document structure, checksum validation). This category is content, not workflow. It complements `engineering/`, `productivity/`, and the other buckets, which describe *how* to work, by supplying Thai-specific *what*.

Pattern inspired by [Boom-Vitt/claude-thai-skills](https://github.com/Boom-Vitt/claude-thai-skills) (MIT) — see `NOTICE.md` for attribution. Skills here are written fresh and checked against current sources rather than copied verbatim, because legal and tax figures drift over time and that repo is a single-maintainer side project (its own README flags 8 of 12 skills as unverified v0.1 prose).

## Candidate skills (roadmap)

| Skill | Purpose | Status | Tier |
|---|---|---|---|
| [thai-date-format](thai-date-format/SKILL.md) | พ.ศ./ค.ศ. era conversion, Thai numerals, formal/business date formats | built | validator (`convert.py`, self-test) |
| [thai-id-validate](thai-id-validate/SKILL.md) | Thai national ID checksum, phone normalization, PromptPay QR payload | built | validator (`validate.py`, self-test incl. CRC-16 reference vector) |
| [thai-address](thai-address/SKILL.md) | Thai address parsing, postal code to province lookup (77 provinces) | built | validator (`parse.py` + `provinces.json`, self-test) |
| [thai-invoice](thai-invoice/SKILL.md) | Tax invoice / receipt / quotation / WHT certificate per Revenue Code §86/4 | built | validator (`calc.py`, self-test) + templates |
| [thai-government-form](thai-government-form/SKILL.md) | Official letters, leave requests, power of attorney per PM Office regulations on งานสารบรรณ | built | prose + template |
| [thai-pdpa](thai-pdpa/SKILL.md) | PDPA-compliant privacy notices and consent banners | built | prose + templates |
| [thai-translate](thai-translate/SKILL.md) | EN⇄TH translation preserving register and pronoun choice | built | prose |
| [thai-social-caption](thai-social-caption/SKILL.md) | Thai social captions for FB / TikTok / IG / Threads / X / Pantip | built | prose |
| [thai-customer-service](thai-customer-service/SKILL.md) | LINE OA / Shopee / Lazada reply scripts with an apology ladder | built | prose |
| [thai-resume](thai-resume/SKILL.md) | Thai and bilingual resume conventions | built | prose + template |
| [thai-festival-card](thai-festival-card/SKILL.md) | Festival greetings and taboo avoidance | built | prose |
| [thai-text-processing](thai-text-processing/SKILL.md) | Thai word segmentation, NFC normalization, RTGS romanization | built | prose + examples (`normalize.py` self-tests standalone; `segmentation.py` self-tests the naive-split failure and optionally PyThaiNLP if installed) |

All 12 built as of this pass. "Prose" tier means the content is a drafting aid based on generally stable conventions rather than code-verified math — see each skill's "Known limitations" section for what still needs a human/current-source check before real use (tax rates, legal clause numbers, PDPC guidance, etc.).

## Rules

- Never carry over a legal or tax figure (VAT rate, WHT rate, PDPA clause number) from a source without checking it is current — cite the source and the date it was checked in the skill's "Known limitations" section.
- Every skill that touches legal, tax, or compliance content must carry a "not legal/tax advice" disclaimer. Treat it as load-bearing — do not remove it during later edits.
- Write bilingual, Thai-first trigger phrases in the `description` frontmatter. Claude pattern-matches literally, so list the actual Thai phrases a user would type, not just an English paraphrase.
- Give each skill in this folder one job. If a request spans two rows in the roadmap (e.g. an invoice that also needs a PDPA notice), let the router load both skills rather than merging them.

## Skill template for this folder

```markdown
---
name: thai-skill-name
description: Use this skill for <domain>. Trigger on "<Thai phrase 1>", "<Thai phrase 2>", "<English phrase>". If the task is <out-of-scope case>, use <other skill> instead.
---

# Title (ไทย + English subtitle)

## Overview
สั้น ๆ ว่าทำอะไร และทำไม agent ที่ไม่มีสกิลนี้มักพลาด

## When to use
- ...

## When NOT to use
- ถ้าเป็นกรณี X ให้ใช้ <skill อื่น> แทน

## Core knowledge
ตาราง/สูตร/ระเบียบที่ต้องรู้ — อ้างอิงแหล่งที่มาและวันที่ตรวจสอบล่าสุด

## Common mistakes
1. ...

## Known limitations
- ข้อมูลอิงจากประกาศ/อัตรา ณ วันที่ตรวจสอบ — ถ้ามีการเปลี่ยนแปลงต้องอัปเดต
```

## Workflow to add a new skill here

1. Pick one row from the roadmap table above (or a new one the user asks for).
2. Create `skills/thai/<name>/SKILL.md` from the template.
3. Verify any numeric or legal fact against a current official source; note the check date under "Known limitations".
4. If the skill ships code (validator, calculator), place it beside `SKILL.md` with a self-test that exits non-zero on failure.
5. Run `scripts/validate-skills.ps1` and flip the roadmap row to `built`.
6. Add the new skill to README.md's Skill Categories section.

## Output Format

End with:

- Which roadmap skill was built or updated
- Sources checked for any legal/tax/date figure, with the check date
- Whether the disclaimer (if applicable) is present
- What remains in the roadmap
