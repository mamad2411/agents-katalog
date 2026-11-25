---
name: thai-government-form
description: Use this skill for any task drafting a Thai official letter (หนังสือราชการ), leave request (ใบลา), or power of attorney (หนังสือมอบอำนาจ). Trigger on "หนังสือราชการ", "เขียนหนังสือถึง", "ใบลาป่วย", "ใบลากิจ", "ใบลาพักผ่อน", "หนังสือมอบอำนาจ", "official letter Thai government", "leave request Thai", "power of attorney Thai". If the letter is informal/personal correspondence with no organizational hierarchy involved, plain [thai-translate](../thai-translate/SKILL.md)-style writing is enough — this skill is specifically for the structured, hierarchy-aware government/office document format.
---

# Thai Government Documents (หนังสือราชการ / ใบลา / หนังสือมอบอำนาจ)

## Overview

Thai official correspondence follows a fixed structural convention (ที่/ส่วนราชการ/วันที่/เรื่อง/เรียน/body/ขอแสดงความนับถือ) and a salutation hierarchy (เรียน vs. กราบเรียน vs. นมัสการ) that a model without this skill tends to flatten to a single generic "เรียน" regardless of who the recipient is. This skill is a drafting aid, not a legal reference — the underlying regulation can be amended, and organizational house style often adds local variations on top of the base structure.

**Not legal advice.** For anything with binding legal effect (a power of attorney used in a real transaction, a leave request that affects pay), have the final document reviewed against the current regulation and the issuing organization's own template.

## When to use

- เขียนหนังสือราชการถึงหน่วยงาน/ผู้บังคับบัญชา
- เขียนใบลาป่วย / ใบลากิจส่วนตัว / ใบลาพักผ่อน / ใบลาคลอดบุตร
- ร่างหนังสือมอบอำนาจ (เช่น มอบอำนาจให้ไปทำธุรกรรมแทน)
- Choosing the correct salutation level (เรียน/กราบเรียน/นมัสการ) for a given recipient's rank

## When NOT to use

- Informal or personal letters/messages with no organizational hierarchy — no salutation-level decision is needed, plain writing works
- A power of attorney or letter that will be used in a specific legal proceeding — draft here, then route through a lawyer/notary for the binding version

## Core knowledge

**หนังสือราชการ (official letter) structure**, per the ระเบียบสำนักนายกรัฐมนตรีว่าด้วยงานสารบรรณ:

1. `ที่` — reference number, top area
2. Issuing agency name/letterhead (ครุฑ header for government agencies)
3. `วันที่` — date in formal Thai style (day, full month name, พ.ศ. year — see [thai-date-format](../thai-date-format/SKILL.md))
4. `เรื่อง` — subject line, short and specific
5. `เรียน` — salutation, addressed by position/title, not personal name alone
6. `อ้างถึง` (optional) — reference to prior correspondence
7. `สิ่งที่ส่งมาด้วย` (optional) — enclosures
8. Body — background paragraph, then the substantive request/notice
9. `ขอแสดงความนับถือ` — closing
10. Signature block: signature line, printed name, position
11. Footer: originating unit, phone/fax

**Salutation (คำขึ้นต้น) hierarchy**:

| Salutation | When |
|---|---|
| เรียน | Default for most official letters — general agencies, most position levels |
| กราบเรียน | Very senior recipients (นายกรัฐมนตรี, ประธานองคมนตรี, ประธานศาลฎีกา, or per the organization's own protocol for its highest officers) |
| นมัสการ | Recipient is a Buddhist monk (พระภิกษุสงฆ์) |

Getting this wrong (using เรียน where กราบเรียน is expected) reads as a protocol mistake in a formal setting — when in doubt, ask the user who the recipient is and their rank rather than defaulting silently.

**ใบลา (leave request)** — common types: ใบลาป่วย (sick), ใบลากิจส่วนตัว (personal), ใบลาพักผ่อน (annual/vacation), ใบลาคลอดบุตร (maternity), ใบลาอุปสมบท (ordination). Structure: addressee (ผู้บังคับบัญชา by position), requester's name/position/department, leave type, reason, date range and day count, contact during leave, signature. The number of paid leave days per type is set by each organization's own regulation (civil service vs. private company vs. state enterprise differ) — do not assert a specific day count as universal; ask or leave it as a field for the user to fill in.

**หนังสือมอบอำนาจ (power of attorney)** — must state: ผู้มอบอำนาจ (grantor, full legal name + ID number), ผู้รับมอบอำนาจ (agent, full legal name + ID number), the specific scope of authority granted (be specific — a vague "ทำการแทนทุกอย่าง" is weak and often rejected by the receiving office/bank), validity period, date, signatures of both parties plus **two witnesses**. Many receiving offices (Land Department, banks, DLT) require a revenue stamp (อากรแสตมป์) affixed to the POA — the required denomination depends on the number of grantees/authorized acts and current Revenue Code Schedule; verify the current amount rather than assuming a fixed figure.

## Common mistakes

1. Using เรียน for a recipient who protocol expects กราบเรียน (or vice versa — using กราบเรียน too liberally, which reads as excessive).
2. Writing the date in ค.ศ. instead of พ.ศ. in a formal document.
3. Vague scope of authority in a power of attorney ("ทำการแทนทุกอย่าง") instead of listing specific authorized acts.
4. Missing the two-witness signature block on a power of attorney.
5. Omitting `เรื่อง` or making it too vague to route the letter correctly within an organization.
6. Assuming a universal number of paid leave days — this is organization-specific, not fixed by a single national rule for all employment types.
7. Forgetting the revenue stamp requirement on a power of attorney intended for use at a government office or bank.

## Templates

- `letter-template.md` — general หนังสือราชการ structure with salutation-choice guidance

For ใบลา and หนังสือมอบอำนาจ, follow the structural fields listed under Core knowledge above — these vary more by organization/purpose than the general letter does, so a single fixed template would mislead more than it helps; build the field list into the draft and flag anything organization-specific for the user to confirm.

## Known limitations

- The underlying ระเบียบสำนักนายกรัฐมนตรีว่าด้วยงานสารบรรณ has been amended multiple times — verify the structural details against the current edition for anything with real organizational consequence.
- Leave entitlements (จำนวนวันลา) are set per-organization (civil service regulation vs. Labour Protection Act minimums for private employers vs. individual company policy) — this skill does not assert a specific day count.
- Power-of-attorney revenue stamp amounts are set by the Revenue Code's Schedule of stamp duties, which can change — verify the current amount before a real filing.
- This is a drafting aid, not a substitute for legal review on documents with real legal or financial consequence.
