---
description: Refresh legal-compliance source freshness. Walks each source in your jurisdiction's sources.yml, checks for material changes, and updates last_checked_on dates. Run quarterly or before any client-facing legal memo.
argument-hint: "(no arguments)"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch"]
---

# Legal & Compliance Update

Quarterly refresh of the loaded jurisdiction's source set. Walks each source, prompts you to web-search it, captures any material changes, and updates `last_checked_on:` dates so the skill stops flagging the source as stale.

## Procedure

1. **Verify install.** If `core/identity.md` does not exist, reply: `Founder OS not set up here. Say "set up Founder OS" first.` and stop.

2. **Read jurisdiction.** Open `core/identity.md` and find the `jurisdiction:` field. If missing, reply: `No jurisdiction set. Say "set up legal" first.` and stop.

3. **Open sources.yml.** Read `skills/legal-compliance/references/<jurisdiction>/sources.yml`. If missing, reply: `No source set loaded for <jurisdiction>. Say "set up legal" to create the scaffold, or "add a legal source" to add sources directly.` and stop.

4. **Identify stale sources.** Today's date minus each source's `last_checked_on:`. Anything >180 days old is "stale". Anything >90 days old is "warming". Anything ≤90 days is "fresh".

5. **Show the user the audit:**

```
Source freshness audit for <jurisdiction> as of <today>:

Stale (>6 months - refresh now):
  - <source-key>: <name>, last checked <date>, <N> days ago
  - ...

Warming (3-6 months - refresh recommended):
  - <source-key>: <name>, last checked <date>
  - ...

Fresh (<3 months - no action):
  - <source-key>: <name>, last checked <date>
  - ...
```

6. **Walk each stale source one at a time.** Ask: "Refresh `<source-key>` (<name>)? Options: yes / skip / mark-checked-no-changes / drop-source"

   - **yes:** WebFetch the source URL. Look for material changes (new amendments, ministerial decisions, threshold updates, fee changes). Show the user a summary: "Found / did not find material changes since <last_checked_on>." If material changes are found, ask: "Add a one-line note to `sources.yml`'s `notes:` field for this source AND update the relevant domain file's '## Material Changes Since' block? (yes / no)". If yes, do both edits. Update `last_checked_on:` to today's date.
   - **skip:** leave as-is, move to next source.
   - **mark-checked-no-changes:** update `last_checked_on:` to today's date without web-fetching. Use when the user has already verified the source themselves.
   - **drop-source:** the source is no longer authoritative. Remove the entry from `sources.yml` after a confirmation prompt: "Drop `<source-key>` permanently? Will not auto-restore. (yes / no)"

7. **Repeat for warming sources** if the user wants to be thorough. Ask once: "Also refresh the 3-6 month sources? (yes / no - only stale by default)".

8. **Update `last_full_review:`** in the top of `sources.yml` to today's date.

9. **Domain file freshness.** Glob `skills/legal-compliance/references/<jurisdiction>/*.md`. For each, check the `## Last Verified:` header. If >90 days old AND any of its underlying sources got refreshed in this run, prompt: "Refresh the `## Last Verified:` header on `<file>` to today? (yes / no)". If yes, edit only the date line.

10. **Summary.** Print a one-screen recap:

```
Legal-update complete for <jurisdiction>.

Refreshed: <N> sources
Material changes found: <N>
Domain files updated: <N>
Sources dropped: <N>
last_full_review: <today>

Next legal-update recommended: <today + 90 days>
```

## Rules

- Walk sources ONE at a time. Do not bulk-process unless the user explicitly says "auto-confirm all stale".
- WebFetch the canonical primary URL only. Never substitute a secondary source (Big 4 article, law firm note) for the primary source's URL.
- Never invent material changes. If WebFetch fails or the page hasn't changed, say so honestly and leave `last_checked_on:` un-updated.
- If a source URL is now dead (404, redirect to an unrelated page), surface it: "Source `<key>` at `<url>` returns <status>. Replace with a new primary URL or drop?"
- No em dashes or en dashes.
