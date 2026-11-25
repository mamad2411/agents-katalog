---
name: to-prd
description: Turn the current conversation context into a PRD and write it to .context/prd/ so it can be sliced into iudex tickets. Use when the user wants to create a PRD from the current context.
---

This skill takes the current conversation context and codebase understanding and produces a PRD. Do NOT interview the user — just synthesize what you already know. (If the idea still needs hardening, run **grill-me** or **grill-with-docs** first.)

## Where the PRD goes

PRDs are tracked project documentation, written to `.context/prd/<slug>.md` (kebab-case slug derived from the feature name, e.g. `.context/prd/agent-spawn-templates.md`). Create `.context/prd/` lazily if it doesn't exist.

`.context/` is committed (unlike the gitignored `.iudex/`), so the PRD travels into iudex ticket worktrees and an impl or QA agent can read the originating spec. Keep PRDs in the `prd/` subfolder — every top-level `*.md` directly in `.context/` is read as domain glossary, so a PRD must never sit at the top level.

## Requirement format

Capture the hard requirements as **requirement headings** the iudex CLI can parse. This is what makes a PRD a browsable, trackable spec — surfaced by the GUI's Specifications view — instead of just prose. The rule is tiny:

- A requirement is a heading whose text is `REQ-<n>: <title>` (any heading level). Write the number as a placeholder — `### REQ-?: <title>` — and assign real, file-scoped ids in the numbering pass (step 4). **Never hand-number**, and never reuse or renumber an existing id.
- Optionally mark status with a `> status:` line directly under the heading: `active` (the default — omit it), `parked` (deferred but intended), or `out-of-scope` (deliberately won't build).
- Everything else is free prose. This section and the numbering pass (step 4) are the canonical definition of the format.

```markdown
### REQ-?: Card payment via Stripe
Users complete purchase with a saved or new card; failures surface a retryable error.

### REQ-?: Gift receipts
> status: parked
Hide prices on a printable receipt.
```

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Read the domain glossary — every top-level `*.md` in `.context/` — and use its vocabulary throughout the PRD. Respect any ADRs in `.context/adr/` that touch the area you're working in.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can.

   Check with the user that these seams match their expectations.

3. Write the PRD using the template below to `.context/prd/<slug>.md`.

4. **Number the requirement ids.** Ids are scoped to this one file — other PRDs'
   numbers are irrelevant. Do this as a final pass, never while drafting:
   a. Find the highest id already in the file:
      `grep -oE 'REQ-[0-9]+' .context/prd/<slug>.md | grep -oE '[0-9]+' | sort -n | tail -1`
      If there is no match, the highest is 0.
   b. Replace each `REQ-?` placeholder with the next integer, in the order the
      placeholders appear in the file: the first gets highest+1, the next
      highest+2, and so on.
   c. Hard rules: NEVER renumber or reuse an id that already has a number, even
      if its requirement is out-of-scope or struck through. NEVER restart at 1
      when editing an existing PRD. NEVER leave a `REQ-?` in the finished file.
   d. Verify: `grep -c 'REQ-?' .context/prd/<slug>.md` must print 0, and
      `grep -oE 'REQ-[0-9]+:' .context/prd/<slug>.md | sort | uniq -d` must print
      nothing (no duplicate ids). Fix and re-verify if either check fails.

5. Tell the user the PRD path and that the next step is **to-issues** — it slices this PRD into independently-grabbable iudex tickets and registers them in the queue.

<prd-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## Requirements

The hard requirements, each a `### REQ-?:` heading (see "Requirement format" above). Be extensive — cover every aspect of the feature, one requirement per distinct capability. Frame each requirement's body as the user value it delivers ("As an <actor>, I want <capability>, so that <benefit>"), plus whatever pins down what "done" means. Mark anything deferred or cut with a `> status:` line rather than dropping it, so the spec records the decision instead of losing it.

<requirements-example>
### REQ-?: View account balances
As a mobile bank customer, I want to see the balance on my accounts, so that I can make better-informed decisions about my spending. Covers every account type; refreshes on pull-to-refresh.

### REQ-?: Gift receipts
> status: parked
Hide prices on a printable receipt. Revisit post-launch.
</requirements-example>

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>
