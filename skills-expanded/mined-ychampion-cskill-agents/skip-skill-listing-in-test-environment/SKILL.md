---
name: skip-skill-listing-in-test-environment
description: "Suppress skill-listing attachments in test mode so discoverability noise does not interfere with deterministic test behavior."
metadata:
  author: ychampion
---

# SKILL: Skip Skill Listing in Test Environment
**Domain:** command-surfaces  
**Trigger:** Apply when tests exercise attachment-building code paths but do not need discoverability payloads such as skill listings.
**Source Pattern:** Distilled from reviewed command-surface and listing-control patterns.

## Core Method
Treat test runs as a separate operating mode where non-essential discoverability output should be silent by default. Check the environment before computing any listing state, and return an empty result immediately when the process is running under tests. This keeps tests focused on actionable behavior, avoids large incidental payloads in assertions and fixtures, and prevents test outcomes from drifting because of unrelated skill-registry changes.

## Key Rules
- Put the test-environment guard at the top of the attachment builder so no listing work or state mutation happens before the early exit.
- Suppress only non-essential discoverability payloads; do not use the pattern to hide behavior that tests are explicitly meant to verify.
- Prefer deterministic environment checks such as `NODE_ENV === 'test'` over indirect heuristics.
- Keep tests isolated from runtime inventory churn so new skills or registry changes do not force unrelated snapshot or transcript updates.

## Example Application
If a chat runtime test exercises the attachment pipeline to validate message ordering, skip the skill-listing attachment entirely when `NODE_ENV` is `test`. The test still covers the real behavior under examination without needing to account for a changing skill registry or extra discoverability tokens.

## Anti-Patterns (What NOT to do)
- Do not generate large listing attachments in tests when those attachments are irrelevant to the assertion; they add noise and make fixtures brittle.
- Do not place the test guard after registry lookups or sent-state mutation; the point is to avoid both the output and the work.
