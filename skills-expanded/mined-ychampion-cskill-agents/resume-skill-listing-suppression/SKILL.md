---
name: resume-skill-listing-suppression
description: "Mark the current skill listing as already sent when resuming so the transcript does not receive a redundant payload."
metadata:
  author: ychampion
---

# SKILL: Resume Skill Listing Suppression
**Domain:** command-surfaces  
**Trigger:** Apply when a resume flow already contains a previous `skill_listing` attachment and injecting another would waste ~600 tokens.
**Source Pattern:** Distilled from reviewed command-surface and listing-control patterns.

## Core Method
Treat a resume run as continuing an existing transcript: before recomputing `skill_listing`, mark every command that already exists in the transcript as sent by setting `suppressNext = true` and filling `sentSkillNames` for that `agentId`. Return early without emitting any listing so the resume session does not repeat the large skill payload, even though the future process loses the ability to announce cross-process deltas until the next full session.

## Key Rules
- Expose `suppressNextSkillListing()` so external flows (conversation recovery) can set a flag that the next listing should be skipped.
- When building the attachment, check `suppressNext`; if true, mark all current commands as sent, reset the flag, and return `[]`.
- Accept the trade-off: cross-process delta coverage is deferred to the next non-resume session, but transcripts stay lean and avoid bursting the turn with redundant data.
- Keep the marking logic scoped to the process-local `sentSkillNames` map keyed by `agentId` (main thread uses empty string) so per-agent delta tracking remains correct.

## Example Application
When a session is resumed, call `suppressNextSkillListing()` right before `getSkillListingAttachments` so it returns `[]` and the transcript keeps the listing it already has instead of receiving another copy.

## Anti-Patterns (What NOT to do)
- Do not clear `sentSkillNames` or unset `suppressNext` during resume; you need to pretend the listing is still current.
- Do not let resume inject the full listing even once; the ~600-token delta is expensive for every restart.
