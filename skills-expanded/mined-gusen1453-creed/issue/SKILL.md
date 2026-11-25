---
name: issue
description: Use when the user wants to record or file something as an issue — "记一下这个 bug", "提个 issue", "这个先放着", a bug report, a feature request, or anything that should become a trackable GitHub/GitLab issue rather than be acted on now. Composes the draft from the repo's templates or the built-in ones, searches for duplicates first, and asks before creating.
---

# Issue

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

**Turn a sentence into a filed, trackable issue: identify the host → pick a template → compose the draft and title → search for duplicates → resolve labels → confirm → write → report.** A duplicate hit routes to updating that issue instead of filing a new one.

This skill files and updates issues. It does **not** fix them, branch for them, or open PRs for them.

Each stage has its own reference — this file is a router:

| Stage | What | Reference |
|-------|------|-----------|
| **Templates** | host identification, the three tiers, repo-local-first resolution, the optional copy-in step | [references/templates.md](references/templates.md) |
| **Create** | draft + title → dedupe → labels → confirm → create → report; every failure path | [references/create.md](references/create.md) |
| **Host CLI** | the measured `gh` / `glab` commands and the traps | [references/host-cli.md](references/host-cli.md) |

Copy-in candidates live in [assets/](assets/): [bug-report.md](assets/bug-report.md) · [feature-request.md](assets/feature-request.md) · [custom.md](assets/custom.md).

**Core principle: one issue = one reasonably-scoped piece of work, filed only after the user says yes, with the body composed from a template rather than an improvised shape.**

## When to Use

- The user asks to **file / record / track** something: "记一下这个 bug", "提个 issue", "记一条", "这个先放着"
- The user describes a defect or a wanted capability **and shelves it** rather than asking for it now
- A `grill` session reached its exit gate and the user picked the "file an issue first" option

**When NOT to use:** the user wants the thing **done now** (that is the normal flow — grill → write-spec → write-plan → tdd); the user is only discussing or venting (§Trigger); the work is a one-line fix with no product ambiguity.

## The Iron Law (non-negotiable)

```
1. NEVER create or edit an issue without an explicit yes — both are public writes, and neither host keeps version history on an edit.
2. On GitLab, SAY that the write cannot be undone (measured: 403 on delete). Before editing an existing issue, save its current body first.
3. NEVER search without `-s all` (gh) / `-A` (glab) — the default hides closed issues, so a duplicate stays invisible.
4. NEVER create a label. Map to labels that already exist, or file without any.
5. NEVER pass the CLI's `--template` — it cannot work non-interactively. Read the file and compose the body.
6. NEVER identify the host from a URL's spelling, a template directory, or `glab api version` — ask `gh repo view` / `glab repo view`, which read `origin`; if both or neither answer, **ask the user** rather than picking.
7. NEVER retry a write whose outcome is unknown — search again first. A retry is how duplicates happen.
8. NEVER report a still-red normalised read-back as success — it means the body was mangled. And never report an update as if it produced a new issue.
9. NEVER take the branch/PR/spec side of the linkage — supply the number; the other skills use it. One issue = one capability.
10. NEVER invent content for a template field that cannot be determined — write `unconfirmed` / `none`.
```

**Violating the letter is violating the spirit.** "It's obviously what they want", "GitLab probably allows deletion too", and "I'll set up the branch while I'm here" do not count.

## Trigger (the only authoritative statement of it)

The agent may **raise** the idea of filing an issue — it must not file one — when **all three** hold:

1. **Not done yet.** The thing has not been done and is not being done right now — it is not the work in hand.
2. **Shelved.** The user used language that puts it aside: says "记一下" / "提个 issue", or defers it ("这个先放着", "回头处理", "回头弄"). Approximate phrasings count — judge by *is this being shelved*, not by matching a list of words.
3. **Shaped and in scope.** It has enough form to write (a bug has at least a symptom or a repro; a request at least says what is wanted) **and** it belongs to this repo/project — not a personal errand that happens to come up mid-session.

**When the conditions collide, "shelved" wins.** A user discussing X who says "X 先放着，先做 Y" is deferring X — the shelving signal is explicit, and the fact that X also has an in-progress conversation attached does not cancel it. **Raise it** — deferring something is itself the recording intent. Merely refining X's details without deferring it → do not raise it.

**Cooling off:** once the user declines in a session, do not raise it again that session. (The `grill` gate option stays visible regardless — that is the user's own path, not the agent raising it.)

If only one or two conditions hold, **do not raise it** — plain discussion, a bare complaint ("这设计真丑"), work in progress, work already done.

Raising it is one sentence with the draft points already in hand (do not start an intake interview). Only a yes moves into the create flow.

## Workflow (when invoked)

Announce "Using issue to …", then follow [create.md](references/create.md):

1. **Identify the host** — ask each CLI to resolve `origin`: `gh repo view` exits 0 → GitHub, `glab repo view` exits 0 → GitLab. Never by the URL's spelling, a template directory, or `glab api version` (it ignores `origin`) ([templates.md](references/templates.md) §2)
2. **Pick the template** — repo-local first, then [assets/](assets/) ([templates.md](references/templates.md) §2)
3. **Compose the draft + title** — in conversation, nothing written to the remote; bug titles stay symptom-shaped ([create.md](references/create.md) §1)
4. **Search for duplicates** — keywords from the template fields, closed issues included ([host-cli.md](references/host-cli.md) §3). A hit adds a **routing** question first — update that issue / open a new one / cancel — which is *not* the confirmation ([create.md](references/create.md) §2a); "update" then goes through §2b, which saves the old body before writing
5. **Resolve labels** — read the repo's list; use only names in it, or none ([create.md](references/create.md) §3a)
6. **Confirm — once** — show title + body + target repo + labels, for whichever body step 4 routed to; say the write cannot be undone (GitLab: no delete; either host: no edit history) ([create.md](references/create.md) §3)
7. **Write** — create, or edit when updating; temp files outside the worktree; then read back and compare with normalisation — a still-red diff means *report the mismatch*, not success ([create.md](references/create.md) §4)
8. **Report** — new issue: URL + branch-name suggestion + the note that `Closes` / spec-header linkage belongs to the neighbouring skills; update: the existing URL + what changed ([create.md](references/create.md) §5)

The optional copy-in step (§8 of create.md) is **opt-in and branch-checked** — never offered by default.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "The user clearly wants this filed" | Clear intent is not consent to a public write. Ask. |
| "It's an edit, not a create — lighter touch" | Neither host keeps edit history. Save the old body, then ask. |
| "It's GitLab, deletion is probably fine" | Measured 403. An accidental issue stays visible forever. |
| "Timeout — I'll just retry" | Retrying is how you get two issues. Search first. |
| "`glab api version` works, so this is GitLab" | It never reads `origin` — it answers 0 inside a GitHub repo. Use `glab repo view`. |
| "The repo has no labels, so I'll make one" | Never create labels; GitLab will silently oblige. File without one. |
| "The diff is red but that's just normalisation" | Normalise first. If it is still red, the body was mangled — say so. |
| "A bug title reads better as 'Fix X'" | The fix has not happened. Keep the symptom: "X crashes when Y". |
| "I'll create the branch too, it's one command" | Out of scope. Suggest the name only. |

## Red Flags — stop immediately

- About to run a create **or edit** command without the user's yes
- About to edit an existing issue without having saved its current body first
- On GitLab and the confirmation never mentioned that the write cannot be undone
- Passing `--template` to either CLI
- Host decided by a URL's spelling, a template directory, or `glab api version`
- Both `repo view` probes succeed and a host was picked without asking
- A label name that was not read from `gh label list` / `glab label list`
- Searched without `-s all` (gh) or `-A` (glab)
- Retrying a write whose outcome is unknown
- A branch, PR, or spec file touched by this skill
- Two capabilities bundled into one draft
- A template field filled with a guess instead of `unconfirmed` / `none`
- A normalised read-back diff that is still red, reported as success
- An update reported as if it produced a new issue URL or number

**Any hit → stop, return to the Iron Law.**

## Checklist

- [ ] Trigger conditions checked (all three) before raising it; no raising after a decline
- [ ] Host identified by `gh repo view` / `glab repo view`; ambiguity (both, or neither) resolved by asking, not guessing
- [ ] Template chosen repo-local-first for that host
- [ ] Body composed from the template; **title follows the title rule** (bug = symptom, feature/custom = outcome verb)
- [ ] Nothing invented — `unconfirmed` / `none` where the input is missing
- [ ] One capability per issue
- [ ] Duplicate search ran with `-s all` / `-A`; candidates shown, not auto-resolved
- [ ] On a hit: routed (update / new / cancel) **before** confirming; the user was asked to confirm exactly once
- [ ] Labels read from the repo's own list; a name that was not in it is absent from the command
- [ ] User confirmed; target `owner/repo` stated; **irreversibility stated** (GitLab: no delete; either host: no edit history)
- [ ] Body via file (gh) / inline (glab); temp files outside the worktree, deleted once the read-back is judged and on every failure path
- [ ] Read back and compared with line-ending normalisation; a still-red normalised diff was reported, not excused
- [ ] **If updating:** current body saved to `before.md` first; merged rather than replaced; issue count verified unchanged; restore path used if the write mangled the body
- [ ] Reported: new issue → URL + branch-name suggestion + "the linkage belongs to the other skills"; update → existing URL + what changed (no new number)
- [ ] No label created; no branch, PR, or spec touched

## Hand-off

This skill ends by **filing** something. The next actor depends on where the user is:

- Filed from the **cold start** → done; the issue is the artifact.
- Filed at **`grill`'s exit gate** → **return to that same gate** — the one grill already owns. Do not ask a second question of your own; `grill`'s gate is where "proceed to write-spec" lives, and asking it here would double the question (the spec's acceptance requires the gate be asked once).
- The issue gets **implemented later** → the normal flow, with the number available for `Closes #<N>`.

When reached from `grill`, the number is handed back for the spec header (`Issue: #<N>`) — `grill` carries the flow from there.
