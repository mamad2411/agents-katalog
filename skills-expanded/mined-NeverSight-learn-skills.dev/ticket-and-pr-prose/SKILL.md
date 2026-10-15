---
name: ticket-and-pr-prose
description: "Write a Linear ticket or a pull request description in the standalone, progressive-disclosure prose style: a fixed 'Why this matters (plain language) / Where this fits / What we're building (or What this changes)' spine sliding into engineering detail, with the flow shown as mermaid diagrams (before + after when behavior changes). Use when asked to create/write/rewrite a ticket or a PR description, write up a change so a non-engineering audience can follow it, or make a PR reviewable by someone with no context. Triggers: 'create a linear ticket', 'write this up as a ticket', 'write the PR description', 'fill in the PR body', 'make this PR reviewable', 'ticket for non-eng audience'."
---

# ticket-and-pr-prose

Write a **Linear ticket** or a **pull request description** that a non-engineer understands at the top and an implementing or reviewing engineer can work from at the bottom — one document, sliding from plain language into engineering detail. The method below IS the format, so you never need to open a reference ticket or PR.

The two artifacts share one spine and one set of rules. They differ only in tense (a ticket proposes, a PR reports), in the last few detail sections, and in how you publish them.

## The one rule that governs everything: progressive disclosure

A reader starts at the top knowing nothing and stops reading the moment they hit their depth — and must have gotten real value by then. So each section is more technical than the last. A PM reads the first two sections and understands *why* and *where*. A staff engineer reads all of it and can implement or review. Never open with jargon; never bury the "why" under the mechanism.

## Standalone — no outside references

The document is its own source of truth. **Do not reference other tickets, PRs, ADRs by ID, design history, or "the thought process behind this."** When sibling work matters, describe it by *what it does* ("the shared token issuer already shipped with the deployed-app lane"), never by ticket number. A reader with zero context and no other tabs open must fully understand the change.

Two narrow exceptions, both pointers rather than explanation:

- A live delivery-status table may cite the PR or sub-ticket that lands each piece.
- A PR may carry a single ticket link line (`Closes ENG-1234`) at the very top or bottom. The *reviewer must never need to open it* — everything they need to review the diff is in the PR body itself.

## The section spine (in order)

The top three headings are **required and verbatim** — same names, same order. Only the third differs between the two artifacts:

| # | Linear ticket | Pull request |
| -- | -- | -- |
| 1 | **Why this matters (plain language)** | **Why this matters (plain language)** |
| 2 | **Where this fits** | **Where this fits** |
| 3 | **What we're building** | **What this changes** |

Everything after that third heading is **"the rest of the details"** — the deeper technical layer, ordered from most- to least-relevant. Drop a detail section only if it genuinely has no content; never reorder the top three.

**Tense is the tell.** A ticket is written forward ("we will mint a short-lived token"), a PR backward ("the gateway now mints a short-lived token"). Never leave a PR description in proposal tense — it reads as unfinished work.

### Title
States **what changes and the payoff**, in one line a non-engineer parses. Lead with the capability, not the mechanism. For a PR, this is the PR title, and it must still satisfy whatever commit convention the repo uses (e.g. `feat(auth): mint per-user tokens so preview apps stop impersonating`).

### Why this matters (plain language)
- Open with a **concrete, product-level scenario** the reader can picture ("When you build an app in the live preview and ask it to 'list my Slack channels'…").
- Name **today's behavior and why it's a problem**, in plain words ("Today it does that by impersonation… nothing checks that you allowed it").
- State **what this change delivers**, still in plain words (the outcome, not the implementation).
- Zero jargon. If a term is unavoidable, define it inline in five words.

### Where this fits
Situate the change in the larger effort so the reader knows the boundaries of *this* piece — self-contained, describing siblings by function not ID. What machinery already exists and is reused; what is unique to this piece; what is explicitly a *different* piece of work. On a stacked PR, this is where you say what the PR below it already landed — by function, not by number.

### What we're building *(ticket)* / What this changes *(PR)*
The pivot into engineering. One tight paragraph naming **the mechanism** ("The mechanism is a short-lived signed token…"), then the **flow diagram(s)** (see the diagram rules below). Follow the diagram with any prose it can't carry.

On a PR, this paragraph describes what the diff actually does — including the parts that turned out differently from the plan. If the implementation diverged from the ticket, say so here in plain terms; do not silently describe the plan.

---
*The rest of the details — as deep as the change warrants:*

### The contract / the detail (as many subsections as needed)
The deepest technical layer: identifiers, token/claim shapes, invariants, the authorities each call needs. **Use tables for dense structured facts** (e.g. `Claim | Value | Notes`, `Authority | Question it answers | Where enforced`). This is where a staff engineer lives; earlier readers have already stopped.

### How it's delivered — the moving pieces *(ticket)*
A status table so anyone can see the shape and progress of the work:

| Piece | What it does | Where it lives | Status |
| -- | -- | -- | -- |

`Status` is where a ✅/⏳ plus a PR or sub-ticket link is allowed. Optionally follow with a **component graph** (`graph TB`) showing the services/pods and the arrows between them.

### Review guide *(PR)*
The PR's counterpart to the delivery table — where to look and in what order, so a reviewer doesn't have to reverse-engineer the diff:

| File / area | What changed | What to check |
| -- | -- | -- |

Lead with the file that carries the load-bearing change, not whatever sorts first. Call out the parts that are mechanical (renames, generated code, moved files) so the reviewer can skim them and spend their attention on the real change.

### Security / correctness properties the design guarantees
Bullets of load-bearing **invariants** stated as guarantees ("Fail closed everywhere.", "The subject is always server-derived."). One bold lead phrase per bullet, then the mechanism that makes it true. This is what a reviewer checks against.

### Done when *(ticket)*
**Observable, terminal behavior** — what a person can watch happen — never a list of implementation steps. Drive the real user-visible trigger through to the terminal side effect ("Driving a real preview app's action mints a token…, the connector service verifies it, and the user's actual Slack channels return"). Include the guardrail cases (a revoked grant → the next action fails closed; a spoofed identity → denied).

### How this was verified *(PR)*
The same bar as `Done when`, in past tense and **only for things actually run**. State the trigger you drove and the terminal side effect you observed, including the guardrail cases. "Tests pass" is not verification of behavior — name what you exercised end to end. If something on the ticket's `Done when` list was *not* verified, say which and why; never imply coverage you don't have.

### Risk and rollback *(PR, when the change can break something live)*
What breaks if this is wrong, what the blast radius is, what flag or revert brings it back, and whether anything is irreversible (migrations, backfills, data deletion, published artifacts). One short paragraph or a few bullets — skip the section entirely for changes with no runtime surface.

### Out of scope
Explicit boundaries — the adjacent things this does **not** do, so no reviewer assumes a gap is a bug. Describe them by function; a sibling-ticket ID here is acceptable since it's a pointer, not explanatory prose. On a PR, follow-ups you deliberately deferred belong here.

## Diagrams carry the flow (mermaid — required)

**The flow is explained with mermaid diagrams, not prose walkthroughs.** Prose sets up the diagram and notes what it can't show; the diagram is where the reader sees the actual sequence of calls. Both Linear descriptions and GitHub PR bodies render mermaid in fenced ` ```mermaid ` blocks.

**Before / after — always both.** When the change replaces or alters an existing behavior, draw **two** diagrams: a **"Before"** one showing how it works today (and, where relevant, *why that's the problem* — e.g. the impersonation/unchecked step drawn explicitly) and an **"After"** one showing the new flow. The contrast must be visible side by side, same participants where possible so the delta is obvious. A change with no prior behavior (net-new capability) needs only the after flow.

Conventions (non-negotiable):

- **Never use `;`** anywhere in a diagram.
- **Default to a `sequenceDiagram` with `autonumber`** for data flows. Show *what is sent/returned at each step* (payload shapes, key fields), not just "calls X".
- **Label participants with real entity names** — actual deployable services or the human actor (`api-gateway-service`, `forge-identity-service`, `User X in the browser`), never generic "Service A".
- Use **`Note over A,B:`** lines to separate phases and to annotate a non-obvious step ("the provider OAuth token never leaves the connector service").
- Add a **`graph TB` component diagram** when topology (who-talks-to-whom) adds clarity the sequence can't — this is in addition to, not a replacement for, the before/after flow diagrams.

## Method

1. **Gather the real mechanism first.** For a ticket, read the code/design so the engineering sections are true, not aspirational — if a fact is unknown, run a spike or ask, never invent a flow for the diagram. For a PR, read your own diff (`git diff <base>...`) end to end and write from what it does, not from what you set out to do.
2. **Draft top-down**, checking after each section: "has a reader who stops *here* gotten a complete thought at this depth?"
3. **Strip every outside reference** from the explanatory prose. Replace "as in TICKET-XXXX" with the actual explanation.
4. **Build the diagrams from the true call graph**, then verify each arrow against the code. If the change alters existing behavior, draw both the *before* and *after* flow.
5. **Write the acceptance section as things you can watch happen** — `Done when` for a ticket, `How this was verified` for a PR — then confirm each is a terminal side effect, not a boundary or a receipt. On a PR, only claim what you actually ran.
6. **Sweep the tense** before publishing. A PR body in "we will" tense is a draft, not a description.

## Publish

**Linear ticket** — use the Linear MCP `save_issue`, asking for the team if the user hasn't named one. Pass the description as Markdown with **literal newlines, no escape sequences**. To update an existing ticket, pass its `id`.

**Pull request** — write the body to a file and pass it by path, so mermaid fences and backticks survive the shell:

```bash
gh pr create --base <base> --title "<title>" --body-file <path>
gh pr edit <number> --body-file <path>   # update an existing PR
```

Never put coding-agent attribution (`Co-Authored-By`, "generated with…") in a PR description, commit message, or ticket.

The operational tail (branch handoff, implementing, landing) is per-request, not part of this skill — the user specifies it when they want it. This skill's job is the prose.
