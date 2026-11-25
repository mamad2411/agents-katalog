---
name: thai-resume
description: Use this skill for any task drafting a Thai or bilingual Thai-English resume/CV, especially for JobsDB, JobThai, or LinkedIn Thailand. Trigger on "เขียนเรซูเม่", "resume ภาษาไทย", "CV ไทย", "สมัครงาน JobsDB", "สมัครงาน JobThai". If the target is a Western/international company outside Thailand with no Thai-market context, use standard international resume conventions instead — the DOB/photo/religion fields this skill discusses are specifically a Thai-market convention, not a universal one.
---

# Thai Resume / CV

## Overview

Thai resumes traditionally include fields — photo, date of birth, marital status, sometimes religion, military-service status for men — that Western resume conventions explicitly avoid for anti-discrimination reasons. A model without this skill either drops these fields by default (which can hurt a candidate applying through a traditional Thai channel that expects them) or includes them by default (which is inappropriate for an international company's Thailand office that follows global norms). The judgment call depends on the target employer, and this skill exists to make that call explicit instead of silent.

## When to use

- เขียนเรซูเม่ภาษาไทยหรือ bilingual TH-EN
- สมัครงานผ่าน JobsDB, JobThai, หรือแพลตฟอร์มไทยอื่นๆ
- ตัดสินใจว่าควรใส่ข้อมูลส่วนตัว (DOB, รูปถ่าย, ศาสนา) หรือไม่ ตามบริษัทเป้าหมาย

## When NOT to use

- Applying to a company outside Thailand, or a Thailand office that has explicitly adopted international hiring norms (common at large multinational tech/finance firms) — use standard international resume conventions (no photo, no DOB, no marital status) instead

## Core knowledge

**Structure**: ข้อมูลส่วนตัว (personal info) → ประวัติการศึกษา (education) → ประสบการณ์ทำงาน (work experience) → ทักษะ (skills) → ผลงาน/เกียรติประวัติ (portfolio/awards, optional). Usually 1-2 pages.

**DOB / photo / marital status / religion — ask, don't assume**:

| Field | Still commonly expected by | Increasingly dropped by |
|---|---|---|
| Photo (formal headshot) | Traditional Thai companies, government/state-enterprise roles, JobsDB/JobThai-style applications | International companies, tech-sector startups |
| วันเกิด (DOB) | Same as above | Same as above |
| สถานภาพ (marital status) | Traditional/older-style Thai companies | Most modern companies |
| ศาสนา (religion) | Rare even in traditional Thai resumes now; mostly government/specific-context roles | Most companies |
| ภาวะทางทหาร (military service status, male applicants) | Still commonly expected across most Thai employers for male candidates — signals eligibility to work without interruption for conscription | Rarely dropped in a fully domestic-Thai context |

Default recommendation: **ask which channel/employer this is for** before deciding. If the user doesn't know or it's ambiguous, lean toward including the traditional fields for JobsDB/JobThai-style domestic applications (that's the platform norm) and omitting them for LinkedIn/international-facing applications — but say explicitly which default was chosen and why, so the user can override.

**Bilingual formatting**: when producing a bilingual TH-EN resume, keep section labels paired (e.g. "ประสบการณ์ทำงาน / Work Experience") rather than two fully separate resumes — this is the common convention for JobsDB/LinkedIn Thailand profiles that get viewed by both Thai and international recruiters.

## Common mistakes

1. Defaulting to full Western-style omission of photo/DOB for a JobsDB/JobThai application, where the platform norm still expects them.
2. Defaulting to including religion or marital status without checking whether the target employer actually expects it — these are the two fields most likely to be seen as outdated even in a traditional Thai context now.
3. Forgetting military-service status for a male applicant applying through a domestic Thai channel — this is one of the more Thailand-specific fields with no direct Western equivalent, and its absence can prompt an unnecessary follow-up question from the employer.
4. Silently choosing to include or exclude the sensitive fields without telling the user which choice was made — this is a judgment call that should be visible, not buried.

## Templates

- `template-bilingual.md` — bilingual TH-EN structure with the optional-field decision surfaced explicitly

## Known limitations

- Convention is shifting — what counts as "traditional" vs. "modern" Thai hiring practice varies by industry, company size, and generation of the hiring manager. Treat the table above as a starting heuristic, not a fixed rule, and prefer asking the user over guessing when the stakes are real (a real job application, not a practice draft).
