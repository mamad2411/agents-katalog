---
name: skill-forge-feedback
description: "Collect user feedback (bugs, friction, feature requests) about skill-forge skills via a short interview, then file a structured GitHub issue. Use after any skill-forge workflow when something felt wrong, slow, or missing. Triggers: 'file feedback', 'report a bug', 'something felt off', 'I have a feature request', 'friction'."
compatibility: Direct filing requires gh CLI (authenticated) or GitHub MCP server; falls back to a pre-filled GitHub URL that any logged-in GitHub user can submit.
---

# skill-forge-feedback

Capture friction before it evaporates. Interview → recap → permission check → file.

## Phase 1 — Interview

Open with a single-key prompt:

> What brought you here?
> **(b)ug** — something broke &nbsp; **(f)riction** — something was slow or confusing &nbsp; **(r)equest** — something is missing &nbsp; **(o)ther**

After the user picks a type, ask targeted follow-ups one at a trytime:

| Type | Key questions |
|------|--------------|
| Bug | Which skill? What happened? What did you expect? Can you reproduce it? |
| Friction | Which skill? Which step felt slow or confusing? What would have felt better? |
| Request | What were you trying to do? What's missing? How often do you hit this? |
| Other | What's on your mind? Which skill or workflow? |

Keep asking until the user signals done (e.g., "that's it", "(d)one"). Do not stop after one answer — first answers are surface; follow-up gets the root.

Signal: **(d)one — move to recap** / **(q)uit — abandon feedback without filing**

Before displaying the recap, verify you can fill all five fields (WHAT, WHY, WHERE, HOW, WHEN) from what the user has said. Any field still "unknown" is your next question — ask it before moving on.

## Phase 2 — Recap

Display the structured recap before filing:

```
## Feedback Recap

**WHAT:** [one-line summary]
**WHY:**  [impact — why this matters or what breaks]
**WHERE:** [which skill or workflow step]
**HOW:**  [steps to reproduce, or context for a request]
**WHEN:** [which session or workflow triggered this]
```

Ask: **(a)ccept / (r)evise**

Do not proceed until the user accepts. WHAT and WHERE must be non-empty — do not accept with either blank.

## Phase 3 — Context Export Permission

Ask explicitly:

> May I attach a transcript of this session for additional context?
> This uploads your conversation to a private GitHub Gist.
> **(y)es / (n)o**

- If `y`: use the session export mechanism (e.g. gh-weld-export) to generate a Gist URL, then append `**Session transcript:** <url>` to the issue body.
- If `n`: proceed without it. Do not ask again.

**NEVER treat silence, ambiguity, or any non-`y` response as consent.** Default is always `n`.

## Phase 4 — File the Issue

### Compose

**Title:** `[<type>] <WHAT summary>` — e.g. `[friction] skill-forge-judge recap step unclear`

**Body:**
```
## WHAT
<WHAT>

## WHY
<WHY>

## WHERE
<WHERE>

## HOW
<HOW>

## WHEN
<WHEN>

---
*Filed via skill-forge-feedback*
```

**Labels:** `feedback` + type label (`bug` / `friction` / `feature` / `other`)

Ensure the `feedback`, `bug`, `friction`, `feature`, and `other` labels exist in the repo before filing — `gh issue create` silently fails on unknown labels.

### Detect filing method (in order)

**1. gh CLI**

Run:
```bash
gh auth status
```

If exit code 0, write body to `/tmp/feedback-body.txt` (Write tool), then:
```bash
gh issue create --repo WrathZA/skill-forge --title "[<type>] <summary>" --label "feedback,<type>" --body-file /tmp/feedback-body.txt
```

If `gh issue create` fails (non-zero exit), fall through to method 2.

**2. GitHub MCP tools**

If `mcp__github__create_issue` (or equivalent) is in your available tool list, use it to create the issue against `WrathZA/skill-forge`. If it fails, fall through to method 3.

**3. Pre-filled URL fallback**

Construct the URL — URL-encode title and body (spaces → `%20`, newlines → `%0A`, `#` → `%23`, `[` → `%5B`, `]` → `%5D`):

```
https://github.com/WrathZA/skill-forge/issues/new?title=<encoded-title>&body=<encoded-body>&labels=feedback,<type>
```

Output: `Open this URL to submit your feedback:` followed by the link.

If the encoded URL exceeds ~2000 chars, truncate the HOW field or drop WHEN — browsers silently clip URLs past this limit.

## NEVER

- **NEVER upload a context export without an explicit `(y)es` in Phase 3**
  **Instead:** Default to `n`; treat any ambiguous or absent response as `n`; do not ask again after a `n`.
  **Why:** Session transcripts contain private conversation history — uploading without explicit consent exposes sensitive context and violates user trust.

- **NEVER write the issue body inline as a `gh` argument**
  **Instead:** Write body to `/tmp/feedback-body.txt` with the Write tool, then pass `--body-file /tmp/feedback-body.txt`.
  **Why:** Multi-line bodies with `#` headers trigger Claude Code's permission check on every execution.

- **NEVER chain Bash commands with `&&` or `;` in Bash tool calls**
  **Instead:** Run each command as a separate Bash tool call.
  **Why:** Claude Code's safety check fires on multi-command calls and interrupts mid-flow.

- **NEVER skip the Phase 2 recap**
  **Instead:** Always show the WHAT/WHY/WHERE/HOW/WHEN structure and wait for `(a)ccept`.
  **Why:** Unreviewed feedback creates untriageable noise in the issue tracker.

- **NEVER stop the interview after the first answer**
  **Instead:** Ask at least one follow-up per type; continue until the user signals `(d)one`.
  **Why:** First answers are surface-level; root causes and real feature needs emerge in follow-up.
