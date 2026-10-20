# FYI/AGENTS.md

> Practical real-world orientation for muShanghai participants — clinics, allergy reminders, provider question sheets. Not used by any skill at runtime. Human-facing only.

## Purpose

Real-world orientation for participants based near the Alibaba Hongqiao Center area.
The folder covers Hongqiao medical resources, food allergy reminders for ordering, and a provider question sheet to bring to clinics or restaurants.
Facts are source-cited where applicable, with shared references in `sources.md`.
No skill loads this folder. AI doesn't consume it at runtime. The reading audience is human participants.

## Files

| File | Purpose | Length |
|---|---|---|
| `README.md` | Folder intro, contents, and safety reminder. | 21 lines |
| `hongqiao-medical-resources.md` | Hongqiao-area legitimate medical institutions and practical verification notes. | 47 lines |
| `food-allergy-note.md` | Ordering reminders for people with severe food allergies. | 27 lines |
| `provider-question-sheet.md` | Print-and-bring question rows for clinics, hospitals, or restaurants. | 61 lines |
| `sources.md` | Source list for clinical and institutional claims. | 25 lines |

## Mandatory File Template

Every new file in `FYI/` MUST open with:
1. H1 title.
2. A blockquote opening with "Reference only:" or "These notes are for orientation only."
3. That blockquote must state explicit non-medical-advice and non-endorsement limits.
4. Then add a TL;DR or a usage block.
Source-cited fact claims, including clinics, hospitals, phone numbers, and websites, MUST be backed by a row in `sources.md`.
If `sources.md` doesn't cover a claim, add the source before merging.

## Hard Rules

- English-only body text. No Chinese characters.
- "Reference only" disclaimer at the top of every file. Never strip or weaken it.
- No diagnosis language. No treatment recommendations. No drug dosing. No emergency-protocol claims.
- No endorsement of specific providers. Use "legitimate, licensed institutions" framing, and let the reader call to verify.
- Always tell readers to verify current hours, departments, appointment rules, language support, insurance, and emergency capability directly with the provider before visiting.
- All clinic, hospital, and website mentions go through `sources.md`.

## Update Workflow

When updating a provider's details, confirm the source is current.
Call the institution if changed details affect safety.
Always update both the fact file, such as `hongqiao-medical-resources.md`, and `sources.md` in the same commit.
For new file types, write the disclaimer block first, then content. Never the other way around.
Run LSP diagnostics on the file after edits.
Never commit without explicit user instruction.

## What This Folder Is NOT

- Not a skill. AI skills live in `skills/`.
- Not a clinical reference. Real medical decisions need a licensed clinician.
- Not part of the longevity experiment protocol. Experiment-specific safety lives in `skills/mushanghai-canon/references/safety.md`, the never-paste list and canonical banner.
- Not committed to the runtime artifact tree, `experiments/<track>/<seed-name>/`.
