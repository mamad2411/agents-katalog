---
name: lavish-axi
description: Turn complex or visual agent responses into rich, reviewable HTML artifacts the user can annotate and send feedback on, using the lavish-axi CLI. Use when about to give a plan, comparison, diagram, table, code diff, report, or anything easier to grasp visually than as prose.
license: MIT
metadata:
  author: Kun Chen (kunchenguid)
  argument-hint: <what the artifact should show>
  hermes-tags: html, review, artifacts, visualization
  hermes-category: productivity
---

# lavish-axi

Open an agent-generated HTML artifact in the browser as a review surface a human can annotate, then read that feedback back over a long poll.

## When to reach for it

- A plan, comparison, diagram, table, code view, report, prototype, or decision surface will be clearer as a page than as prose: build the HTML, then open it here.
- Structured input from the user (choices, triage, scope) belongs in an artifact with the `input` playbook, not in a chat question.
- Do NOT reach for it for a short textual answer, or when nobody is at a browser; answer in the conversation instead.
- Sharing outside this machine is `export` (a portable file) or `share` (a hosted page), not the review server.

## Workflows

Build the artifact only after reading the current guidance; it is CLI-owned and installed skills go stale.

```bash
lavish-axi design                  # design-direction priority, CDN snippet, playbook router
lavish-axi playbook                # list playbook ids
lavish-axi playbook plan           # focused guidance for the artifact you are about to write
```

Review loop - open, then wait for the human. The poll is silent by design; never kill it.

```bash
lavish-axi .lavish/report.html                       # prints the session url
lavish-axi poll .lavish/report.html                  # blocks until feedback or session end
lavish-axi poll .lavish/report.html --agent-reply "fixed the pricing table"
```

Hand the artifact to someone who is not on this box.

```bash
lavish-axi export .lavish/report.html --out /tmp/report-standalone.html
lavish-axi share .lavish/report.html --password "<pw>"   # third-party host, public without --password
```

Close out or recover.

```bash
lavish-axi                          # live sessions, or an empty list
lavish-axi end .lavish/report.html  # agent-side end; a later plain open still works
lavish-axi stop                     # shut the background server down
```

## Conventions

Write artifacts under `.lavish/` in the working directory unless the user names a place.
Keep sibling assets in that same directory and reference them with relative paths; a leading `/` does not resolve.

Every response ends with `next_step` or `help:` hints; follow them rather than guessing the next command.
Every command takes `--help`.

Detected layout issues never return the poll. They wait in the user's Layout issues inbox and arrive as an ordinary `layout-warnings` prompt only once the user queues them, so never edit the artifact to chase a layout issue the user did not send.

Run the poll in the foreground unless the harness has a tracked background job that provably wakes the same agent. Never `nohup`, `&`, or `disown` it. A killed poll loses nothing: re-run it.

A browser-side end refuses a later plain reopen; pass `--reopen` only when the user asks or something genuinely needs their eyes.

No global install required: `npx -y lavish-axi ...` runs every command above, and follow-up commands the CLI prints should be run that way too.

## Non-goals

- Not a design system reference: `lavish-axi design` and `lavish-axi playbook <id>` own that, and this file must never restate it.
- Not a flag reference. `--help` is current; this skill is not.
- `share --unpublish` does not delete a hosted page, it overwrites it. The URL still resolves.
- No reverse conversion: whiteboard edits are applied by updating the Mermaid source, never by writing a scene file back.

## Request

$ARGUMENTS

If the request above is non-empty, the user invoked `/lavish-axi` explicitly - fetch the current CLI guidance, then build that artifact.
If it is empty, infer what to visualize from the conversation.
