---
name: kickoff-dm-design
description: "Manual-invocation skill — run only when the user explicitly asks for \"kickoff-dm-design\" or invokes it as a slash command. Do not auto-trigger on adjacent topics. Inverted-flow design-room kickoff for Darkmatter teammates. Operator creates a Claude Design project manually, drops the URL — this skill creates the Linear ticket, posts the kickoff to #design-room, and cross-links Linear ⇄ Slack ⇄ Claude Design. Non-interactive — never asks for a brief, team, or confirmation. Derives screen name + brief from the URL itself. Idempotent on rerun."
---

# Darkmatter design-room kickoff

Inverted-flow kickoff for new UI/screen design work. The operator creates the Claude Design project themselves (because they need to be in there to iterate on the prompt anyway). When ready to broadcast to the team, they paste the URL into an agent session running this skill. The skill creates the Linear ticket, posts the kickoff to `#design-room`, and cross-links the artifacts.

**v1 audience:** Darkmatter teammates with a Linear seat AND access to the Linear and Slack integrations of their agent runtime — MCP server for code agents (Claude Code, Codex), built-in connector for claude.ai. Contractors without Linear seats remain in the workaround path (paste URL in `#design-room`, an employee invokes this skill); see "v1.1 expansion" notes at the bottom.

## When to use

- Operator pastes a `https://claude.ai/design/p/<uuid>` URL into the agent chat and wants the team looped in
- "kick off a design room for <screen>" / "broadcast this design"
- Recovery on a partial-failure rerun — this skill is idempotent on the same URL
- After the operator has already created and iterated on a Claude Design project and is ready to broadcast it to the team

## When NOT to use

- The operator does not yet have a Claude Design URL — this skill never creates the project, only kicks off around an existing one
- The work is not a screen/flow design — for general feature kickoff, use the project's regular Linear flow
- The agent runtime has no Linear or Slack integration available — the skill hard-fails preflight rather than degrading

## Why this shape

The skill's job is small and reliable: validate a URL, derive a screen name + brief from it, create a ticket, post a thread, cross-link. Earlier shapes that auto-created the Claude Design project via browser automation added brittleness (account-bound, single-tab, fails when UI shifts) and didn't actually save much time — the operator still has to think about what they want before kicking off. Earlier shapes that asked the operator a follow-up question (brief, share-dialog confirmation) added friction with no real safety benefit. This shape never asks anything: the URL is the input, Linear + Slack are the outputs, one shot.

Claude Design is the iteration surface. Slack is the discussion surface. Linear is the work-tracking surface. This skill stitches them together; it doesn't generate them.

## Required integrations

- **Linear** (write access) — MCP server (code agents) or Linear connector (claude.ai). Hard-required.
- **Slack** (write access to `#design-room`, channel ID `C0AV067EY83`) — MCP server (code agents) or Slack connector (claude.ai). Hard-required.
- **Web fetch** (optional, best-effort) — `WebFetch`, `claude-in-chrome`, or any URL-fetching tool the runtime offers. Used for enrichment only; never blocks the run.

## Invocation

```text
/kickoff-dm-design <claude-design-url> [optional brief]
```

The Claude Design URL is required — must match `https://claude.ai/design/p/<uuid>(\?file=...)?`. The `?file=...` suffix is preserved in stored URLs (deep-links to the right file when collaborators open).

**No follow-up questions.** The skill is non-interactive by design. It must always derive the screen name and brief from the URL itself plus any context already available in the chat — and proceed straight through to creating Linear + Slack artifacts. If the operator supplies an inline brief, prefer it. Otherwise, infer.

### Deriving screen name and brief from the URL

1. **Screen name (Linear title):** parse the `?file=<Name>.html` query param. `Filesystem.html` → "Filesystem screen". If the URL has no `file` param, fall back to "New design — <short uuid prefix>" (e.g., "New design — 019dd5b7").
2. **Brief (Linear description + Slack body):** generate a 2-sentence brief from:
   - The screen name (primary signal — e.g., "Filesystem screen" → "UI design for the Filesystem screen.")
   - Any free-text the operator added after the URL in the invocation
   - Any context already present in the current chat (prior messages, prior artifact context)
   - Best-effort enrichment: attempt to fetch the URL with whatever web-fetching tool is available. The Claude Design page is an authenticated SPA, so the fetch will usually return only metadata (page title, OG tags) — capture whatever it gives. If the fetch fails, ignore it and continue. **Never** block on this fetch.
3. **Linear team:** infer from invocation context. If unambiguous (only one Darkmatter team accessible, or context names a team), use it. Otherwise default to the operator's most-active Darkmatter team. **Do not ask** — pick the most likely team, note the choice in the status bundle, and let the operator move the ticket if it's wrong. (Moving a Linear ticket between teams takes 2 clicks; asking takes a round-trip.)

### Brief template (2 sentences)

```
UI design for the <screen name>. See Claude Design link for the current iteration; reply in this thread to weigh in.
```

If the operator supplied free-text after the URL, replace sentence 1 with that text verbatim.

### What never happens

- The skill never asks for a brief.
- The skill never asks for team-access confirmation. (See "Sharing" below — this becomes a one-line nudge in the Slack post, not a gate.)
- The skill never asks the operator to confirm the Linear team.
- The skill never silently fails because of missing input. It always produces Linear + Slack artifacts on the first invocation.

## Successful run

A successful run leaves the team with:

1. One Linear issue, named `<short screen name>` (Linear assigns the ID; canonical reference becomes `<ISSUE-ID> - <short screen name>`)
2. One top-level kickoff post in `#design-room`, with the brief and all three links
3. The Claude Design URL added as a Linear attachment
4. The Slack permalink added as a Linear attachment after step 2 completes
5. Status reported as `kicked off` or `blocked: <reason>`

## Preflight (silent)

Run these checks without prompting the operator. If a hard check fails, report `blocked: <reason>` and stop. Otherwise proceed straight to Linear + Slack creation.

1. **URL validation.** The URL must match `https://claude.ai/design/p/<uuid>(\?file=...)?`. If it doesn't, report `blocked: not a Claude Design URL` and stop.
2. **Linear available.** Linear is required. If unreachable, report `blocked: linear unavailable`.
3. **Slack available.** Slack is required. If unreachable, report `blocked: slack unavailable`.

That's it. No interactive questions.

## Sharing (nudge, not gate)

The Claude Design URL only renders for collaborators if the project's Share dialog is set to *"Anyone at Darkmatter with the link can view + comment."* The skill cannot verify this programmatically.

Instead of gating on it, include a one-line nudge in the Slack kickoff post itself: *"⚠ If the Claude Design link 404s for you, the creator needs to set Share → 'Anyone at Darkmatter with the link.'"* Teammates will self-report mismatches; that's fine.

## Best-effort URL enrichment

Before creating Linear/Slack artifacts, attempt — silently — to fetch the Claude Design URL with whatever web-fetching tool the runtime offers. The Claude Design page is an authenticated SPA, so the most common outcome is a partial fetch (page title, OG tags) or a login wall.

- If the fetch returns a recognizable project title or first-prompt fragment → fold it into the screen name and brief.
- If the fetch returns nothing useful or fails outright → continue with the URL-only inference described above. Do not retry. Do not surface the failure to the operator.

Mark in the status bundle as `enrichment: webfetch-hit | webfetch-miss | chrome-read | skipped`. The run always succeeds regardless of enrichment outcome.

## Linear workflow

If the operator's invocation references an existing Linear issue ID:

1. Read the issue.
2. Add the Claude Design URL as an attachment.
3. Add a one-line comment: *"Design exploration started — see Claude Design project."*
4. Add the Slack kickoff permalink as a second attachment after the Slack post completes.

If no issue exists:

1. **Idempotency check.** Search Linear for any issue whose attachments include this exact Claude Design URL. If found → treat that issue as the canonical one and continue at the existing-issue path above (skip ticket creation; jump to Slack post or skip if Slack permalink already attached).
2. Search Linear briefly for likely duplicates by inferred screen/flow name. If a clear match exists, attach to it instead of creating a new one.
3. Otherwise, create a new Linear issue:
   - **Title:** `<short screen name>` derived from the URL (Linear assigns the ID; canonical reference becomes `<ISSUE-ID> - <short screen name>`).
   - **Description:** the inferred 2-sentence brief, followed by a Links block (template below).
   - **Labels:** none required.
   - **Priority:** Low (P4) unless invocation says otherwise.
   - Add the Claude Design URL as an attachment with title `Claude Design — <short screen name>`.

After Slack is posted, update the Linear issue with the Slack kickoff permalink as a second attachment.

### Linear description template

```markdown
<inferred 2-sentence brief>

Links:
- Claude Design: <url>
- Slack: <kickoff permalink — added after Slack post>
```

Keep it short. The Claude Design conversation is the real artifact; the Linear ticket is just the work-tracking shell. Don't pad the description with TBD checklists or open-question stubs — the team adds those in Slack/Linear if they're needed.

## Slack workflow

Post the kickoff as a top-level message in `#design-room` (`C0AV067EY83`). All discussion happens in replies to that message.

This post is required for a successful run. Do not use a Slack draft as a substitute.

Kickoff template:

```text
*Design room: <ISSUE-ID> - <short screen name>*

<inferred 2-sentence brief>

Links:
• Linear: <url>
• Claude Design: <url>

⚠ If the Claude Design link 404s, the creator needs to set Share → "Anyone at Darkmatter with the link can view + comment."
```

Use Slack `mrkdwn`. No code blocks for the headline. The sharing nudge is always included — it's cheap insurance against silent half-rendering for collaborators.

## Recovery on rerun

If the same Claude Design URL is invoked twice (intentional retry, partial-failure recovery, or accidental double-trigger):

1. Search Linear for an existing issue whose attachments include this Claude Design URL. If found, treat that issue as canonical.
2. Inspect what state already exists:
   - **Both Linear ticket and Slack post exist** → do not duplicate. Reply with the existing links and state `state: already-kicked-off`. Stop.
   - **Linear exists, Slack missing** (Slack failed mid-run) → only post the Slack kickoff and update Linear with the permalink. Do not re-create the Linear issue.
   - **Slack exists, Linear missing** (rare) → create the Linear issue, then update Slack post with the Linear URL via thread reply.
3. Never create a duplicate Linear issue for the same Claude Design URL.

This guarantees the skill is safe to rerun without producing noise or stale links.

## Status bundle

```text
State: kicked off | blocked: <reason> | already-kicked-off
enrichment: webfetch-hit | webfetch-miss | chrome-read | skipped
team: <Linear team chosen, e.g. "Engineering">
Links:
- Linear: <url>
- Slack: <permalink>
- Claude Design: <url>
```

## Failure modes

Fail explicitly when:

- The provided URL is not a valid Claude Design project URL.
- Linear cannot create or update the issue.
- `#design-room` cannot be posted to.
- The cross-link update on Linear fails after the Slack post (mark as partial: `state: blocked, missing: linear-cross-link`).

Partial success is allowed only when one surface fails after the others succeeded. State must be set to `blocked: <missing-surface>`.

## What this skill explicitly does NOT do

- **Does not create the Claude Design project.** The operator does that themselves before invoking.
- **Does not ask the operator any follow-up questions.** No brief prompt, no team-access prompt, no Linear-team prompt. Inputs come only from the URL + invocation text.
- **Does not drive any browser UI for writes.** All writes go through API-backed integrations (Linear MCP/connector, Slack MCP/connector).
- **Does not validate the Claude Design project's actual access state programmatically.** Sharing is handled by the inline nudge in the Slack post, not by gating.
- **Does not iterate on the design.** This skill kicks off; iteration happens in Claude Design directly.
- **Does not write back into the Claude Design project.** Claude Design has no programmatic comment/attach API today, so the design project remains a referent (linked-to, not linking-out). The link-rot problem is mitigated by Linear and Slack carrying the cross-references; revisit when Anthropic ships a Claude Design API.

## v1.1 expansion notes (deferred)

These are NOT in v1; tracked here so the next iteration starts from a clear baseline:

- **Slack-bot trigger** so seatless-contractor-originated kickoffs work without an employee in the loop. Required if measured contractor-originated kickoffs become frequent. Build path: Slack app installed in Darkmatter workspace + listener + service-account creds. The Slack-bot value is identity laundering (let a service account do the Linear/Slack writes on a contractor's behalf), not latency.
- **Configurable Linear team / Slack channel** via skill args, e.g. `/kickoff-dm-design <url> --team=Engineering --channel=#nixmac-design-room`. Useful when DM grows and per-project channels emerge.
- **Higher-fidelity brief extraction** — fold in Claude Design project title and first-prompt content when Anthropic ships an API for it. Today the URL-derived brief is the floor; the inline-brief override is the ceiling. An API would let the skill produce a brief mid-way between the two without operator effort.
- **Bidirectional Claude Design backlinking** when the API ships — write the Linear ticket ID and Slack permalink back into the Claude Design project as a comment or property.
