# Demonstrate Artifact Rendering

Show that this terminal's tools return **typed artifacts**, not walls of text.
Every call below goes through the same governed path as any other tool —
scope check, secret scan, blocklist, rate limit — and lands one artifact on
the shelf (the chip in the terminal header). When you summarise, point the
viewer at each tool row's **view result** button: the preview it opens is the
same server-side render an MCP host would show, not a second renderer.

## When to Use

Use this when someone asks what the artifact shelf is, how tool results are
rendered, or wants to see each artifact type on screen.

## The Protocol

Make all eight calls at once, then report once. In order:

1. In a **single turn**, issue **all eight** `render_artifact` calls as one
   parallel batch — one call per `artifact_type` listed below, each type
   exactly once, no duplicates. Do not narrate between them; do not spread them
   across turns.
2. Wait for all eight results.
3. Call `mcp__systemprompt__governance_stats`.
4. Only now write the summary.

One turn, not eight, is deliberate: this terminal runs each tool call in its own
task precisely so a model can fan out, and every call in the batch still gets its
own scope check, secret scan, blocklist check, rate-limit check, and its own row
on the audit spine. Eight parallel calls are eight governed decisions — the fan-out
costs the demo nothing and removes seven chances to lose the thread mid-run.

Rules that override everything else in this file:

- **Never write a sentence about an artifact whose tool result has not yet
  appeared in this conversation.** The list below is a menu of calls to make,
  not a script of outcomes to report. If six results came back, you describe
  six artifacts — not eight.
- **Never state a total yourself.** "All eight calls were allowed" is a claim
  only `governance_stats` can make. If you did not call it, you do not know the
  number.

Claiming a render that did not happen is worse than the failure it papers
over: this skill exists to show the audit spine, and a fabricated line is the
one thing the spine will contradict — the viewer can open the audit trail and
count.

**A denial changes the report, not the batch.** A blocked call comes back
alongside the others rather than stopping a loop, so there is nothing to
abort — but do not summarise the batch as successful. Name the refused call,
quote the reason verbatim, and call `governance_stats` to find the deciding
policy, because the reason the model receives is deliberately generic. A block
on `human_approval` means a person declined or the approval lapsed (it times
out, and it is abandoned if the terminal tab has no live viewer); that is the
approval gate doing its job, not the four-stage policy chain refusing the tool.
Say which of the two it was, or say you cannot tell — never guess.

## The Calls

Eight calls, one per `artifact_type`, all in the same turn:

```
mcp__systemprompt__render_artifact {"artifact_type": "table"}
mcp__systemprompt__render_artifact {"artifact_type": "chart"}
mcp__systemprompt__render_artifact {"artifact_type": "dashboard"}
mcp__systemprompt__render_artifact {"artifact_type": "list"}
mcp__systemprompt__render_artifact {"artifact_type": "presentation_card"}
mcp__systemprompt__render_artifact {"artifact_type": "copy_paste_text"}
mcp__systemprompt__render_artifact {"artifact_type": "message"}
mcp__systemprompt__render_artifact {"artifact_type": "text"}
```

What each one shows, for the summary you write afterwards:

- **table** — recent governance decisions for this session: when, which tool,
  allow or deny, and the policy that decided. A fresh session gets one
  illustrative row that says so.
- **chart** — the same spine, aggregated: allowed and denied counts per policy
  stage.
- **dashboard** — verdict totals, provider spend, and the four pipeline stages
  as status items.
- **list** — the four governance stages.
- **presentation_card** — what systemprompt.io is.
- **copy_paste_text** — the setup commands, in an artifact built for one-click
  copying.
- **message** — info, warning, and success notices rendered from structured
  data.
- **text** — how all of this works.

The first three are built from **this session's own governance spine** — the
same rows `governance_stats` reports — so they change as the session does. The
rest carry curated content.

## Close — let the spine state the count

This step is not optional. Before writing any summary, call:

```
mcp__systemprompt__governance_stats {}
```

Read the `render_artifact` allow count back to the viewer, quoting the number
the spine returned — not the number of types listed in this file, and not your
own tally. Eight `allow` verdicts means the shelf holds one artifact of every
type; anything less is the more interesting result, and is worth showing:
say which calls landed, which did not, and point at the audit trail as the
proof.
