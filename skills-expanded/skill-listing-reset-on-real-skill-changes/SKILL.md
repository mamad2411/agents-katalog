---
name: skill-listing-reset-on-real-skill-changes
description: "Reset skill-listing announcement state only when the underlying skill set actually changes, not on compaction or transcript churn."
metadata:
  author: ychampion
---

# SKILL: Skill Listing Reset on Real Skill Changes
**Domain:** command-surfaces  
**Trigger:** Apply when a system tracks which skills have already been announced and must decide when that sent-state should be cleared.
**Source Pattern:** Distilled from reviewed command-surface and listing-control patterns.

## Core Method
Tie announcement-state resets to real changes in the underlying skill inventory, such as plugin reloads or skill file changes on disk. Do not clear the sent-state for compaction, transcript recovery, or other conversation-level churn, because that would force expensive re-injections of essentially unchanged listings. This keeps listing deltas meaningful and avoids paying thousands of tokens to restate the same inventory after every context-management event.

## Key Rules
- Reset the sent-state when the registry itself changes, not when the conversation representation changes.
- Keep reset triggers narrow and explicit, such as plugin reload or skill-file mutation hooks.
- Do not piggyback listing resets onto compaction, resume, or transcript maintenance paths unless those paths also change the actual registry.
- Clear any paired suppression flags together with the sent-state so the next genuine delta announcement starts from a clean slate.

## Example Application
If a desktop agent reloads plugins and the available skill set changes, clear the sent-skill tracking map so the next listing can announce the new tools. If the conversation merely compacts or rehydrates from transcript, leave the sent-state alone so the agent does not spend tokens repeating an unchanged listing.

## Anti-Patterns (What NOT to do)
- Do not reset announcement state on every compaction or replay event; that turns context maintenance into repeated full-list reinjection.
- Do not leave suppression flags out of sync with the reset; partial resets create confusing one-off gaps in later announcements.
