---
name: thai-mock-naming
description: Use this skill whenever you are about to invent Thai personal names, company names, or identity data for anything that is not a real person — seed scripts, database fixtures, Storybook stories, API examples, Swagger/OpenAPI samples, Postman collections, UAT scripts, demo accounts, screenshots, slide decks, user manuals, training material, test plans, or a mock server. Trigger on "mock data", "sample data", "seed data", "test data", "dummy data", "fixture", "placeholder", "demo user", "example record", "ข้อมูลตัวอย่าง", "ข้อมูลจำลอง", "ข้อมูลทดสอบ", "ชื่อสมมุติ", "ตัวอย่างผู้ใช้", and on any request that would otherwise produce สมชาย ใจดี / สมหญิง พอใจ / มานะ มานี ปิติ ชูใจ. Also trigger when reviewing or cleaning an existing codebase's test data, when a screenshot or document will leave the team, or when asked to anonymise Thai records. The rule this skill enforces: a fake Thai person must be unmistakably fake on sight, greppable in a database, and still structurally valid enough to exercise real Thai text handling. Do NOT use for naming variables, functions, files, branches, or products — that is software naming, not identity data.
---

# Thai Mock Naming

Generates Thai names for people, companies, and identity fields that **announce themselves as fake** — instead of the default Thai mock names, which look exactly like real citizens.

## The problem this replaces

Thai mock data converges on a handful of names:

| Common default | Why it is a liability |
|---|---|
| สมชาย ใจดี | สมชาย is one of the most common Thai given names; ใจดี is a real surname. Thousands of real people match. |
| สมหญิง พอใจ | Same shape — a plausible real citizen. |
| มานะ, มานี, ปิติ, ชูใจ | The cast of the Thai ป.1 primary reader. Instantly recognised, but still structurally real names. |
| สมศรี, สมปอง, สมพงษ์ ทองดี | Plausible, common, collides with real records. |

Four concrete failures follow from using them:

1. **You cannot tell test data from production data.** A row reading `สมชาย ใจดี` in a shared database is indistinguishable from a real customer. Cleanup scripts cannot target it, and nobody dares delete it.
2. **Screenshots become a PDPA question.** A demo screenshot or a user manual showing `สมชาย ใจดี` looks like it leaked a real person's record. Reviewers have to stop and verify. Under พ.ร.บ.คุ้มครองข้อมูลส่วนบุคคล (PDPA, B.E. 2562), "it was fake" is an argument you should never have to make.
3. **The reverse failure is worse.** When fake records look real, real records start looking fake. A genuine complaint from a real คุณสมชาย gets closed as "that's just test data."
4. **The name carries no information.** You cannot tell from `สมชาย ใจดี` which test case, which role, or which fixture file the row came from.

## The rule

> **The given-name slot always carries a test marker.**

Everything else in this skill follows from that one rule. A Thai name renders as `ชื่อ นามสกุล`, and the given name is what appears first in nearly every list, sort, salutation, and truncated column. If the marker lives there, the record is legible as fake even when the surname is cut off.

### Canonical form

```
ชื่อ     = <marker>
นามสกุล  = <second marker>  |  <role>  |  <index>
```

**Default, when nothing else is needed:**

| ชื่อ | นามสกุล | Use |
|---|---|---|
| ทดสอบ | นามสมมุติ | The house default. Both halves are markers — truncate either side and it still reads as fake. |
| ตัวอย่าง | ข้อมูลจำลอง | Second generic record, when you need two distinct people. |

**Gendered pair** — the direct replacement for สมชาย / สมหญิง, for exercising title and salutation logic:

| คำนำหน้า | ชื่อ | นามสกุล |
|---|---|---|
| นาย | ทดสอบชาย | นามสมมุติ |
| นางสาว | ทดสอบหญิง | นามสมมุติ |
| นาง | ตัวอย่างหญิง | ข้อมูลจำลอง |
| เด็กชาย | ทดสอบเล็ก | นามสมมุติ |

**Role-bearing** — when several actors appear in one flow and a screenshot must show who is who:

| ชื่อ | นามสกุล |
|---|---|
| ทดสอบ | ผู้ยื่นคำขอ |
| ทดสอบ | ผู้อนุมัติ |
| ทดสอบ | ผู้ตรวจสอบ |
| ทดสอบ | เจ้าหน้าที่รัฐ |
| ทดสอบ | ผู้ดูแลระบบ |

The surname slot is doing a job no real surname does, which is the point — `ทดสอบ ผู้อนุมัติ` reads cleanly in Thai and cannot be mistaken for a person.

**Indexed** — for bulk seeding, where the only requirement is uniqueness:

```
ทดสอบ นามสมมุติ๐๐๑
ทดสอบ นามสมมุติ๐๐๒
...
```

Use Thai numerals (๐๑๒๓๔๕๖๗๘๙) when the system must survive Thai digits; Arabic otherwise. Keep the padding width fixed so string sorting matches numeric sorting.

## Approved token banks

**Given-name markers** — safe because none of these is used as a Thai personal name:

`ทดสอบ` · `ตัวอย่าง` · `ทดลอง` · `สมมุติ` · `นำร่อง` · `ชั่วคราว` · `สาธิต`

**Surname markers:**

`นามสมมุติ` · `ข้อมูลจำลอง` · `นามทดสอบ` · `มิใช่บุคคลจริง` · `ตัวอย่างสกุล` · `ระบบทดสอบ`

### Tokens that look safe and are not

| Token | Why it is unsafe |
|---|---|
| จำลอง | A real Thai given name (e.g. the politician จำลอง ศรีเมือง). Safe only as part of a compound like `ข้อมูลจำลอง`, never standing alone in the given-name slot. |
| สมมติ / สมมุติ | Both spellings are valid Thai; pick one per project and stick to it, or your `LIKE` queries will miss half the rows. This skill uses `สมมุติ`. |
| ใจดี, ทองดี, ศรีสุข, สุขใจ, รักเรียน, ดีงาม, แสงทอง | Real, common surnames. Never use as mock surnames. |
| มานะ, มานี, ปิติ, ชูใจ, วีระ, สุดา | Real given names, familiar from schoolbooks. Recognisable ≠ obviously fake. |

## Companies and juristic persons

Same rule — the marker goes in the distinctive part of the name, not the legal-form wrapper:

```
บริษัท ทดสอบระบบ จำกัด
บริษัท ตัวอย่างข้อมูล จำกัด (มหาชน)
ห้างหุ้นส่วนจำกัด นามสมมุติการค้า
ร้านทดสอบพาณิชย์
```

Never generate a plausible trading name (`บริษัท ไทยรุ่งเรือง จำกัด`) — Thailand has over a million registered juristic persons and a plausible name is probably taken.

## How to apply this

1. **Pick a tier.** One actor → the default pair. Several actors in a flow → role-bearing. Bulk rows → indexed.
2. **Fix one marker per project and write it down.** If the project standardises on `ทดสอบ`, every fake person starts with `ทดสอบ`, which makes `WHERE first_name LIKE 'ทดสอบ%'` a complete and reliable census of test records. This is the property that the สมชาย convention can never have.
3. **Keep the shape real.** A fake name must still be a *structurally valid* Thai name — correct character classes, plausible length, no Latin letters unless you are deliberately testing mixed script. Mock data that is too degenerate (`aaa bbb`, `test test`) stops exercising Thai rendering, Thai collation, and font fallback, which is half of why you have Thai test data at all.
4. **Pair it with the identity fields.** A mock person usually arrives with an ID number, a phone number, and an address. Those have their own traps — see `references/identity-fields.md`. In particular, never generate a national ID number with a valid checksum.
5. **Check the existing data.** Before adding to a codebase, run the linter over it; most Thai projects already have สมชาย scattered through their fixtures.

## Scripts

Both scripts are dependency-free Python 3.

**Generate a name set:**

```bash
python3 scripts/gen_names.py --count 10 --format table
python3 scripts/gen_names.py --count 50 --format sql --table users --seed 42
python3 scripts/gen_names.py --roles --format json
python3 scripts/gen_names.py --edge-cases --format json   # the stress-test set
```

`--seed` makes output deterministic, so regenerating a fixture produces a stable diff.

**Audit a codebase for plausible-real Thai mock names:**

```bash
python3 scripts/check_mock_names.py path/to/seeds/
python3 scripts/check_mock_names.py . --quiet     # exit code only, for CI
```

It reports file, line, and the offending token, and exits non-zero when it finds anything — drop it into a pre-commit hook or a CI step.

## References

- `references/name-bank.md` — the full approved token banks, ready-made sets for common scenarios, and the complete unsafe list.
- `references/edge-cases.md` — names built to break things: length boundaries, stacked tone marks, การันต์, `ณ อยุธยา` surnames with internal spaces, ฤ/ฦ, mixed script, whitespace and zero-width characters, and a Thai collation ordering set.
- `references/identity-fields.md` — national ID (with the checksum algorithm and how to deliberately fail it), juristic person numbers, phone numbers, email domains, addresses, and postcodes.

## Related: Thai prose around the data

This skill covers the *identity* fields — names, IDs, companies, addresses. Mock records almost always carry Thai free text as well: `description`, `remark`, `หมายเหตุ`, product names, notification copy, seeded comments, the body of a demo document.

Those fields have the opposite problem. A name must look obviously fabricated; the prose around it must read like a Thai person wrote it, or the demo looks machine-translated. AI-generated Thai tends toward stiff, formal, government-register phrasing and word-for-word English structure.

For that half, use **[kien-thai (เขียนไทย)](https://github.com/chakrit/kien-thai)** by chakrit — a skill that teaches Claude to write Thai that Thai readers find easy to read, built on a framework for Thai sentence and paragraph structure (fronting the topic, putting conditions and time before the main clause, using space and paragraph breaks rather than periods). MIT licensed. Install it alongside this one:

```
.claude/skills/
  thai-mock-naming/    ← names, IDs, companies, addresses
  kien-thai/           ← the Thai prose in every other field
```

The division of labour is clean: **this skill decides what cannot look real; kien-thai decides what must not sound machine-made.** When seeding a Thai system with both, apply this skill to the identity columns and kien-thai to the free-text ones.

kien-thai is also the closest prior art for how this skill is structured — `SKILL.md` plus topic-scoped reference files, with the rules drawn from how Thai is actually written rather than from a style guide.

## When not to use this

If the user is anonymising **real** records for analysis, obviously-fake names may be wrong — pseudonymisation sometimes needs realistic-looking surrogates to preserve how the data behaves. Say so and ask, rather than silently replacing real names with `ทดสอบ`. Everything in this skill assumes the data is *fabricated*, not *de-identified*.
