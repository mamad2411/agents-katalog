---
name: loopflow
description: Create and run Loop (.loop) flows — a natural-language DSL for loop engineering. Use when the user wants to author, write, run, or execute a self-correcting or human-gated AI coding loop, turn an epic into a pipeline, fix a bug "as a loop", build a feature or whole app "as a loop", learn what Loop is or how to use it, or mentions a .loop file or "loop engineering". Not for one-off questions or trivial edits — the skill's four-condition gate decides and de-escalates. Invoked as /loopflow (the name avoids colliding with the built-in /loop scheduler).
---

# Loop

Loop is a small natural-language DSL for **loop engineering**: a `.loop` file describes a
staged, self-correcting, human-gated coding workflow — its objective, the context it may
read, the actions it may take, how it verifies itself, when it stops, and where a human
steps in.

You do two things with this skill: **create** `.loop` files, and **run** them — natively,
in this conversation, so the user watches every step and answers gates right here.

## When NOT to loop — the gate comes first

Before authoring anything, run the **four-condition test** (the full version lives in
`AGENTS.md` → "When to write a `.loop`"): does the task **repeat**? is **"done" checkable**
by a command/test/review skill? are the **iterations affordable**? can the loop **verify
itself**? **Any condition fails → don't force a loop.** Say so in one line — e.g. *"one-off
edit, doing it directly"* — then answer the question or make the change normally, without
loop ceremony. A rename, a one-off question, an unverifiable ask: never a loop. The user
can always override with an explicit request.

---

## The language

Vocabulary (the whole DSL):

```
loop "<name>":            a self-correcting loop
pipeline "<name>":        a sequence of stages (an epic)
stage "<name>":           one stage of a pipeline (its body is a loop; a story)

flow "<name>":            a chain of whole .loop files, run in order (handoff is text)
  run "<file.loop>"         a flow step: run that whole file
  then run "<file.loop>"    the next step; the prior file's summary carries forward as context
  ... with the result of <step>   pull the handoff from a named earlier step instead of the previous
  for each <var> in "<file>":   run the child template once per item in <file>
    run "<template.loop>"

# `for each` source: .yaml/.yml (a list, or items under a single key) or .md (each `## ` section).
# Each item's text becomes the template's context for that run.

goal: <text>              what "done" means, in plain language
done when <predicate>     how the loop verifies itself
look at: <files>, and the last failure   context to read before acting
allow edits automatically, but ask me before <classes>   action policy
each cycle: plan, then act, then observe   the repeated steps (any subset, in order)
also: <pass>, <pass>      extra finishing passes after the goal is met
use skills: <a>, <b>      named skills the loop may invoke during plan/act
remember in "<file.md>"   cross-run memory: read lessons on start, append an outcome on stop
when it fails: reflect on <focus>, then plan again
when it passes and the goal is met: stop
when blocked: ask a human
after <N> tries: stop and warn "<message>"   thrash guard
a human approves the plan first              human plan gate
a human reviews before stopping              human review gate
a human approves before <action>             stage gate (in a stage)

# config tier (top of file): how the loop is powered & scheduled
use the <method> method      pull a preset (e.g. BMAD) as the base
models: fast <m>, strong <m> model tiering — plan/reflect/also→fast, act→strong
                             (cascades; override e.g. `act fast`, `all strong`)
schedule: <when>             run unattended on a cadence
runner: <agent>              which agent executes the loop
target: <dir>                operate on another directory/repo
```

Predicates:
```
done when the test "file.spec.ts::name" passes
done when "pnpm test" passes              # shell command, exit 0
done when "semgrep --severity=high" finds nothing   # empty output
done when a human confirms "looks right"
done when the skill "email-review" approves         # a review skill: approved / not
done when the skill "email-review" scores 8 or more # a review skill: numeric threshold
```

Rules: indentation is structural (two spaces); `loop`/`pipeline` at column 0; comments
start with `#`. An epic → a `pipeline`; each story → a `stage`.

---

## Creating a .loop — be a guide, not a guesser

Most people reaching for this skill don't yet know what Loop can do. Your job is to
**guide them to the right loop for their purpose** — and teach the language by writing
it in front of them. Never silently guess the loop; interview first, then author. Ask
one topic at a time, and always offer a default so a confident user can accept it all
in one reply.

**Check the template library first.** If the repo has a `templates/` directory (see
`templates/README.md`), and the user's request matches one — a bug fix, a feature, a
brownfield change, a CI/security/architecture gate, delivering an existing spec, building
a greenfield app — start from that template instead of a blank file: read it, copy it, and
fill in its `# TODO` lines with the user's specifics. Still interview them for the goal,
the real `done when`, and what to gate; the template is the skeleton, not the answer.

### Step 0 — scope the purpose first (ask this before anything else)

Open with **"What do you want the loop to accomplish?"** and show the range, so the
user sees what's possible and picks a scale:

| Scale | Example purpose | Shape in Loop |
|-------|-----------------|---------------|
| **Tiny** | "Make this one failing test pass." | a single `loop` |
| **Small** | "Fix this bug across a few files; gate the migration." | a `loop` + policy + gate |
| **Medium** | "Build the checkout feature — a few stories, each tested." | a `pipeline` of `stage`s |
| **Large** | "Build a whole app, A-to-Z." | a `flow`: discover → design → build each story |

Name the shape their answer implies (*"that's a **pipeline** — a sequence of stages"*)
so the vocabulary attaches to their own goal. This one question turns a vague request
into a scoped loop and teaches the three top-level forms at once.

### Step 1 — do they already have a plan?

Ask **"Do you have a spec, plan, ticket, or epic already?"**
- **Yes** → point `look at:` at it; if it's an epic / story list, turn each story into a
  `stage` of a `pipeline` (or `for each` over the plan file).
- **No, and it's medium/large** → invoke `superpowers:brainstorming` **before** writing any `.loop`. The brainstorming skill explores project context, asks clarifying questions one at a time (offering a browser visual when a design choice benefits from it), proposes 2-3 approaches, gets user approval, and produces a spec doc at `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`. Once the spec is approved and saved:
  - The approved goal → `goal:` in the loop
  - The spec file → `look at: docs/superpowers/specs/<name>.md`
  - Sub-tasks in the spec → `stage`s in a `pipeline`, or `for each <var> in "plan.yaml"`

  This replaces the old "discovery loop" pattern — brainstorming handles the interview natively in-session and produces a richer, visually-validated artifact.
- **No, and it's small** → skip planning; go straight to the loop.

### Step 2 — which quality passes? (offer the menu — don't wait to be asked)

This is what makes Loop worth running. Proactively offer the quality sub-loops:

> "Want the loop to enforce quality every cycle too? Common ones: **tests** (write/keep
> green), **security** (a scan that must find nothing), **code review**, **clean
> architecture** (boundary checks). I can add these as `also:` finishing passes on one
> loop, or as their own gated `stage`s in a pipeline."

Translate their picks into syntax in front of them so they see the mapping:
- tests → `done when "<test cmd>" passes`
- security → `also: a security scan`, or `done when "semgrep --severity=high" finds nothing`
- review / architecture → `also: <pass>`, or a `stage` with `a human approves before <X>`

### Step 3 — the remaining decisions (defaults offered, one reply to accept)

Walk these quickly, naming the keyword each time so they learn it:
1. **Goal** → `goal:` — "what does *done* look like?" Required; never guess this one.
2. **Verification** → `done when` — a test passing, a command passing, a scan finding
   nothing, or a human confirming. The most important line; always pin it down.
3. **Context** → `look at:` — offer to infer the files from the repo; append `and the last failure`.
4. **Actions** → policy — "anything risky to gate: migrations, pushes, deploys?" Default:
   `allow edits automatically`, nothing else gated.
5. **Stopping** → `after N tries: stop and warn` (default 6) + `when it fails: reflect … then plan again`.
6. **Human gates** → `a human approves the plan first` / `a human reviews before stopping`
   — default none unless the work is risky.
7. **Git** → state the safe default ("branch, commit when the goal is met, never push to
   `main`"); ask if they want a PR, a worktree, or to work in place. (Full grammar below.)
8. **Models (LLM policy)** → `models:` — which model does the work. Default: one model
   throughout (the session's). Offer **tiering** for cost/speed: `models: fast <model>,
   strong <model>` → plan/reflect/also run on *fast*, act runs on *strong*; cascades, and
   you can override per phase (`act fast`, `all strong`).
9. **Schedule / runner / target (config tier — only if automating)** → ask only when the
   loop runs unattended or against another repo: `schedule: <when>` (run on a cadence),
   `runner: <agent>` (which agent executes), `target: <dir>` (operate on another directory).
   Skip silently for a normal in-session loop.

Don't forget the menu in Step 2 also covers `use the <method> method` — pull a whole
preset (e.g. BMAD) instead of hand-picking passes.

Offer the defaults inline (*"I'll add a tests + security pass, gate the migration, a
6-try guard, work on a branch, one model throughout, no schedule — sound right?"*) so the
whole interview is one exchange. Name every topic once even when you default it, so the
user knows the knob exists and can override it.
Then **write the `.loop`**, always with a real `done when` and a thrash guard, **print
its flow** (below), and offer to run it.

> **Teach by building.** As you write each clause, say what it is (*"`done when` is how
> the loop checks itself"*). By the end of one loop the user has seen the whole language —
> that is the point of authoring it here, in the open, rather than headless.

## Show the flow — every time it changes

Whenever you **create or edit** a `.loop`, immediately print its flow so the user
watches the shape evolve. If the `loop` CLI is installed, run `loop show <file>`.
Otherwise render the same compact ASCII yourself:

```
loop "fix test"
   ↻  plan → act → observe        (each cycle)
   ↺  on fail: reflect → plan     (the back-edge)
   ✓  done when: test "checkout.spec.ts::tax"
   ⛔ guard: after 6 tries → stop & warn "stuck"
   ·  goal: the tax line is correct
```

For a **pipeline**, list the stages in order and mark 👤 gates; for a **flow**,
show the file chain (`a.loop → b.loop → …`). `loop ls` lists every loop in the repo.

---

## Live browser dashboard

A live animated schematic in the browser — the active cycle node pulses, flow steps
highlight as they execute, and a for-each (sprint) progress bar fills item by item, so the
user always sees **where in the loop / where in the plan** the run currently is.

### Gate it on `loop.config` (in-session runs)

The in-session dashboard is **opt-in via repo config** — off by default so a normal
`/loopflow` run stays entirely in the chat. Before running a loop in this session, read
`loop.config` at the repo root and look for a `live=` line:

- **`live=false`, or the line/file is absent** → **do not** start the dashboard. Run
  normally, narrating the trace in chat (the *Running a .loop* section below). Do not ask.
- **`live=true`** → start the dashboard and drive it as you narrate (mechanism below). You
  may still mention you're opening it.

(`loop.config` is written by `loop init` with `live=false`; the user flips it to `live=true`
to turn the dashboard on. The headless `loop-run run <file> --live` flag is independent of
this config.)

### How the in-session dashboard works

You (the skill) **are** the engine in-session — so you spin up a tiny server, point the
browser at it, and push an event for each step you narrate. The browser renders in real
time. Three pieces, all via the `loop-run` CLI:

1. **Start the server (background) and grab its port:**
   ```bash
   loop-run live <file.loop>      # opens the browser automatically
   ```
   Run it in the **background** (don't block on it). Read its first stdout line —
   `LOOP_LIVE_PORT=<port>` — and keep `<port>` for the rest of the run. The server renders
   the loop's schematic and stays up until you stop it (or the user hits Ctrl-C).

2. **Push an event as you reach each step** — one `emit` per narrated step:
   ```bash
   loop-run emit <port> '<event-json>'
   ```
   `emit` is best-effort (never blocks your narration if the browser is closed). Push the
   same events the engine would emit; the key ones to keep the view truthful:

   | When you… | Push |
   |-----------|------|
   | start a flow | `{"type":"flow-start","name":"<flow>"}` |
   | enter a flow step | `{"type":"flow-step-start","name":"<step>","ref":"<file>"}` |
   | finish a flow step | `{"type":"flow-step-end","name":"<step>","satisfied":true}` |
   | start a `for each` | `{"type":"foreach-start","var":"<var>","source":"<file>","count":<N>,"labels":["<title 1>","<title 2>",…]}` — pass `labels` (one short title per item, e.g. each story's title) so the dashboard lists the real items instead of "story 1..N" |
   | start item i (0-based) | `{"type":"foreach-item-start","var":"<var>","index":<i>,"total":<N>}` |
   | finish item i | `{"type":"foreach-item-end","var":"<var>","index":<i>,"satisfied":true}` |
   | begin a cycle step | `{"type":"node-enter","node":"plan","attempt":<n>}` (then `act`, `observe`) |
   | finish a cycle step | `{"type":"node-exit","node":"plan","attempt":<n>,"ok":true}` |
   | run the done-when check | `{"type":"observe","passed":true,"output":"<first line>"}` |
   | reflect on failure | `{"type":"reflect","text":"<why>"}` then loop-back `{"type":"loop-back","to":"plan"}` |
   | start a pipeline stage | `{"type":"stage-start","name":"<stage>"}` |
   | stop | `{"type":"stop","reason":"done"}` then `{"type":"loop-end","name":"<loop>","satisfied":true}` |

3. **At the end**, leave the server running so the user can review the final state. Mention
   they can Ctrl-C the `loop-run live` process to close it.

The dashboard renders the loop's **actual structure** as a turn-by-turn route (Waze-style):
the real stages / flow steps / for-each items, with a "you are here", the steps ahead, and
human gates flagged. So a sprint (`for each story in "sprint.yaml"`) lists each story by title
with N/total progress, a check on finished stories, and a plan/act/observe tracker on the one
you're working now — exactly "where are we in the loop / in the plan".

### CLI-only alternative (headless)

If the user would rather run it headless (gates answered in the terminal, not chat):
```bash
loop-run run <file.loop> --live
```
The engine itself emits every event to the browser — no manual `emit` needed. Use this only
when the user explicitly wants the headless runner.

## Running a .loop (in this session)

Prefer running it **yourself, here** — that way the whole loop is visible in the
conversation and the user answers gates inline. (Only shell out to the `loop run` CLI if
the user explicitly asks for the headless runner.)

1. **Read the file.** (Or, if the `loop` CLI is installed: `loop parse <file> --json` to
   get the structured spec.)
2. **Execute the loop's semantics, narrating each step:**
   - **memory** — if the loop has `remember in "<file>"`, read that file first (skip if it
     doesn't exist yet) and let its lessons inform your first plan. When the loop stops,
     append a dated entry: `## <date> — <outcome>` with the goal, attempts, and the run's
     lesson (your last reflection). This is how the loop improves across runs.
   - **plan** — inspect the `look at:` files; decide the smallest change toward the goal.
     If the loop declares `use skills:`, you may invoke those named skills (via the Skill
     tool) to do the work — coordinate them rather than re-deriving everything inline.
   - **act** — make the edits. Honor the policy: for `ask me before <X>`, ask the user
     before doing X (migrations, pushes, etc.); auto classes you may do directly.
   - **observe** — run the `done when` check and read pass/fail. For a command or named test,
     run it. For `the skill "<name>" approves` / `scores N or more`, invoke that review skill
     on the work and read back its verdict (approved/rejected, or a score vs. the threshold) —
     this is how an abstract goal gets a verifiable check.
   - on **fail** → **reflect** on why (use the failure output), then **plan again** (the
     back-edge). Repeat.
   - **stop** when `done when` passes, or after the thrash guard's N tries (state the
     warning), or if genuinely blocked (ask the user).
   - **human gates:** `a human approves the plan first` → present the plan and wait for
     approval before acting. `a human reviews before stopping` → ask before declaring done.
     `a human approves before <X>` → ask before that stage runs.
   - **pipelines:** run stages in order; if a stage can't be satisfied, halt the rest.
   - **flows:** run each referenced file in order, the *whole* file. After each, carry a
     short text summary of how it went forward as context for the next file. If a file
     isn't satisfied, halt the rest (fail-fast). `with the result of <step>` redirects
     which earlier summary to carry.
   - **for each `<var>` in `<file>`:** read the source file and split it into items
     (`.yaml` list entries, or `.md` `## ` sections). Run the template loop once per item,
     giving the template that item's text as its context. If an item's checklist fails,
     pause and ask the user: continue to the next item, or stop the whole flow? Continuing
     accepts that item and proceeds; reaching the end means done.
   - **`also:`** finishing passes run only after the goal is met (skip them if it failed).
3. **Report a concise trace** — one line per cycle step (plan / act / observe = PASS|fail /
   reflect / stop), and the final outcome.

Because you are the one running it, the user sees the real work — file reads, edits,
command output — as part of this session, and answers any gate right in the chat.

---

## Interactive discovery (the front of an A-to-Z flow)

A discovery/planning step is just a loop whose goal is to produce a planning artifact (a
spec, PRD, or plan file). Run it as a real conversation:

- Interview the user — ask the questions the method calls for — across as many turns as it
  takes. You're naturally suspended between their answers, so a long session (even an hour)
  is fine; there's nothing to "wait" on.
- The step is **done when its `done when` artifact check passes** — e.g. the plan file
  exists and has the required sections — NOT when the conversation goes quiet. Re-check the
  artifact; when it validates, move on. (The questions come from the loop's goal/context —
  i.e. the method — not from this skill.)

So a full method, end to end, is a `flow`:

    flow "deliver: <feature>":
      run "discover.loop"          # conversation: interview → write the plan file
      then run "design.loop"       # design from it; a human approves
      then for each item in "plan.yaml":
        run "item-template.loop"    # the per-item checklist, once per item

`discover.loop` ends via e.g. `done when "<validator> plan.yaml"`; each item then runs the
same checklist. (Name things to taste — a BMAD setup might use `story`/`sprint.yaml`.)

---

## Git strategy

A `git:` block sets the version-control strategy for the whole file (config tier) or for
a single loop. When there is no `git:` block at all the built-in default applies:
**work on a branch, commit when the goal is met, no push**.

### Line forms

```
work in place                    # edit the current branch as-is
work on a branch                 # create / switch to a feature branch (default)
work on a branch "my-feature"    # name the branch explicitly
work in a worktree               # isolated git worktree
work in a worktree "my-worktree" # named worktree

commit when the goal is met      # one commit when done (default)
commit each cycle                # commit after every plan→act→observe cycle
commit each story                # commit after each stage in a pipeline
commit never / do not commit     # no automatic commits

push when done                   # push the branch when the loop finishes
do not push                      # no push (default)

open a pull request              # open a PR after pushing (requires push when done)
```

### Cascade

Settings resolve in three layers, each refining the one above:

1. **Built-in default** — branch + commit-when-done, no push.
2. **File-level `git:` block** — placed at the top of the `.loop` file, before any loop definition; applies to every loop in the file.
3. **Per-loop `git:` block** — placed inside a single `loop` body; refines the commit cadence for that loop only.

A `use the <method>` preset may also carry a `git:` block; it applies at the file level and is then overridden by the file's own `git:` block if present.

### Always-on safety

Two protections are unconditional and cannot be overridden by any `git:` block:

- **Never push to `main` or `master`.** If the current branch is `main` or `master` (or a branch whose name matches the protected set), any `push when done` directive is an error that surfaces *before the loop runs*, not after.
- **`work in place` + `push when done` on a protected branch** is also rejected up front.

### In-chat runner note

When you run a loop *inside this conversation* (the `/loopflow` skill), you are the git
operator — you execute plan/act/observe yourself. Before acting, check the `git:` block
and honor the policy: if `push when done` is set and the current branch is `main` or
`master`, refuse with a clear message rather than pushing.

---

## Global library — save a loop, reuse it in any project

The user keeps a personal library of loops at **`~/.claude/loopflow/`** — one
`<name>.loop` per saved loop. It lives beside the installed skill, so a loop saved once is
runnable from **every** repo. The library is driven entirely from this chat; there is no
terminal command for it. Create the directory on first save (`mkdir -p ~/.claude/loopflow`).

Four operations — recognize them from `/loopflow <verb>` or from plain language:

- **save** — *"save this as `<name>`"*, *"save it to my library"*, `/loopflow save …`
  Write the loop's `.loop` source to `~/.claude/loopflow/<name>.loop`. Take `<name>` from
  the user; if they don't give one, slugify the loop's name (`"fix the auth test"` →
  `fix-the-auth-test`). **If that file already exists, show the saved version and confirm
  before overwriting.** Report the path you wrote.

- **list** — `/loopflow list`, *"what loops do I have saved"*
  List every `*.loop` in `~/.claude/loopflow/`. For each, print `name — <goal>` (add the
  one-line shape when it helps). An empty or missing dir → say it's empty and how to save one.

- **run** — `/loopflow run <name>`, *"run my security loop here"*
  Read `~/.claude/loopflow/<name>.loop` and run it **in the current repo**, exactly as in
  *Running a .loop (in this session)* above. A bare `<name>` means the library; a path or a
  name ending in `.loop` is a local file, so the library never shadows a loop in the repo.
  If `<name>` isn't in the library, say so and offer `list`.

- **remove** — `/loopflow remove <name>`, *"delete my `<name>` loop"*
  Delete `~/.claude/loopflow/<name>.loop` after confirming. If it doesn't exist, say so.

These are plain files — the user may also open or edit them directly. Saving is a copy, so
removing a library entry never touches the original loop in a repo.

---

## Reference

The full language reference is in `AGENTS.md` and `docs/MANUAL.md` of the loop-lang repo;
the CLI (`loop-run run|viz|parse`) and the VSCode extension are alternative ways to run
the same `.loop` files.
