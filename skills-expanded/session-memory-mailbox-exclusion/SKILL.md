---
name: session-memory-mailbox-exclusion
description: "Prevent session-memory background forks from draining teammate mailbox attachments that belong to the main lead thread."
metadata:
  author: ychampion
---

# SKILL: Session Memory Mailbox Exclusion
**Domain:** multi-agent  
**Trigger:** Apply when a background or forked agent shares team context with a leader thread and must not consume mailbox messages intended for the leader.
**Source Pattern:** Distilled from reviewed multi-agent coordination and child-runtime patterns.

## Core Method
Treat mailbox-draining attachments as ownership-sensitive, not universally thread-safe. When a background fork shares the same team context as the lead agent, exclude the mailbox attachment path for that fork so it cannot mark leader messages as read and silently steal them from the permanent conversation stream. Keep the exclusion narrow and source-based so the main thread and legitimate teammate consumers still receive mailbox attachments normally.

## Key Rules
- Identify fork classes that share mailbox state with the leader and exclude them from the mailbox drain path.
- Keep the exclusion focused on the mailbox attachment only; other safe shared attachments should continue to run.
- Prefer a source or role check that is stable at attachment time so the guard cannot drift with transient runtime conditions.
- Document why the exclusion exists: the failure mode is message theft, not just redundant work.

## Example Application
If a session-memory extractor runs as a background fork against the same team context as the lead agent, skip its teammate mailbox attachment. The leader still receives teammate DMs as durable conversation turns, while the background worker avoids consuming them as ephemeral side attachments.

## Anti-Patterns (What NOT to do)
- Do not let every fork drain the shared mailbox; one background consumer can mark the leader's unread messages as handled.
- Do not disable all shared attachments for background forks just to solve mailbox theft; keep the guard scoped to the unsafe mailbox path.
