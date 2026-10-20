---
name: auto-summary-commit
description: The default commit workflow — after ANY prompt that created, edited, deleted, moved or generated files in a git repository, stage the work and commit it straight away onto the current branch, with the prompt and the user-facing summary as the commit body, so every turn leaves an auditable history and a git-level rollback point. Asks first only when something is majorly wrong or an open question blocks the purpose of the prompt. Use at the end of every file-changing prompt (writing code, editing docs, refactoring, fixing a bug, applying review feedback, running a formatter) unless the user has said not to commit. Also use when a prompt says "auto summary commit", "summary commit", "/auto-summary-commit", or asks to commit the work just done. Hooks in this plugin also invoke it by name at the end of a file-changing turn, with the list of paths that turn changed.
---

# Auto Summary Commit

Commits the work from the prompt that just ran, using the explanation you were about to show the
user as the commit body — so the reasoning behind a change lives in `git log`, not only in a
terminal scrollback that gets closed.

> **This rule was reversed, deliberately.** It used to be opt-in: the skill ran only when a prompt
> asked for it by name, and explicitly forbade committing "because a task merely finished with
> uncommitted changes". That failed in the ordinary case. Most prompts never remembered to ask, so
> the work piled up in the working tree and the explanation — the caveats, the assumptions, the
> things deliberately left out — was lost when the terminal closed. The commit that eventually got
> made covered several prompts at once and could only be described vaguely. Being default-on is
> what makes the body worth having: one prompt, one commit, written while the reasoning is still
> in context.

## What drives it

Two things, and they are deliberately redundant:

- **The frontmatter description**, which asks to load at the end of every file-changing prompt.
- **The hooks shipped with this plugin** (`hooks/auto-summary-commit.sh`, wired to two events). A
  description is a request to the model, not a guarantee — it gets missed on a long turn. The
  hooks are the deterministic half. `UserPromptSubmit` fingerprints every dirty path in the working
  tree *before* the turn runs; `Stop` fingerprints it again, and if anything changed, feeds back
  the instruction to run this skill together with **the list of paths this turn changed**, and the
  conversation continues so you can act on it. Neither commits anything; staging, the summary and
  the question are all still this skill's job.

A turn that changed nothing is never interrupted, even when earlier deferred work is still
outstanding — the deferred paths ride along with the next turn that *does* change something,
rather than becoming a reason to interrupt one that did not.

The baseline is what makes the list trustworthy. Without it the only question a hook can ask is
"is the tree dirty", which is the wrong one: it fires on work that was already uncommitted when
the session started, it re-asks on every later turn once the user has declined, and it would let
`git add -A` sweep somebody else's edits into a commit whose body describes only your work. The
fingerprints are content hashes rather than status codes, so a file that was already modified
before the turn and modified again during it is still correctly attributed to the turn.

The hook raises a given tree state only once, so ending the turn with the work still uncommitted
is always possible — that is what makes "no" in step 3 safe. The hook only ever says "run the
skill"; whether that ends in a question or a straight commit is this skill's decision, not the
hook's. Decline and the tree does not change,
so the same question is not put again.

**Which one invoked you changes step 3.** The hook fires when a turn is *already ending*, which
means your user-facing summary of the work has already been written and is on screen. Do not write
it out a second time to serve as the commit body — see step 3.

## When to run

**By default, at the end of any prompt that changed files in a git repository.** No one has to ask
for it. One prompt produces one commit.

Run it **last**, after every other part of the prompt is finished and verified — tests run,
linters clean, files written. The commit body is a summary of completed work, so there must be no
work left to do when it runs.

Do **not** run it if:

- **The user has switched it off** — by choosing "Stop asking this session" at step 3, or by
  saying so in a prompt ("don't commit", "stop committing"). Either way create the hook's off
  marker, `touch "${TMPDIR:-/tmp}/claude-auto-summary-commit-<session id>.off"`, using the path
  the hook printed rather than reconstructing it. (`AUTO_SUMMARY_COMMIT=off` in the environment
  switches it off permanently, for a user who never wants this.)
- **The work is still in progress within this turn.** Finish it first — the skill runs last. If
  the turn is *ending* with the change broken — a verification step on the work itself still
  failing — that is not a reason to skip silently: it is the "majorly wrong" case in "Whether to
  ask at all", and the user is asked.
- **Nothing git would record changed.** A question answered, a file read, a command run, a
  scratchpad file written, a gitignored or build-output file touched, an edit to a file outside
  the repository — none of these are a change as far as this skill is concerned. If
  `git status --porcelain` is empty, do nothing at all: no commit, no empty commit, and no mention
  of this skill or of the fact that there was nothing to commit. Silence is the correct output.
- **The only changes are ones the prompt did not make** — a dirty tree you inherited. The hook
  already excludes these, so a hook-driven run will not reach you at all. If you got here on your
  own and the dirt is not yours, leave it alone and say so once.
- **The repository is mid-operation** — a rebase, merge, cherry-pick or bisect in progress. Say so
  and stop; committing into someone else's half-finished operation is not recoverable by them.

## Whether to ask at all

**Commit without asking. That is the default, and it should hold for the great majority of
turns.** The commit exists to record the prompt and its outcome — a history of what was done and
why, an audit trail, and a rollback point at the git level for every turn. A commit that waits on
a question is a turn with no rollback point until someone answers it, and a declined one is a gap
in the record.

**Everything the summary says goes into the commit, not in front of it.** Caveats, trade-offs,
assumptions, work deliberately left out, options for a follow-up, an offer to do more, something
found along the way: all of that is exactly what the Summary section is there to preserve, and
recording it is the point rather than a reason to hold off. The user reads it on screen either
way; if they disagree with any of it, the next prompt changes it and the next commit records the
change — or `git reset --soft HEAD~1` undoes it outright. Neither is harder after the commit than
before it.

**Ask only in two cases:**

| Case | Looks like | Is not |
| --- | --- | --- |
| **Something is majorly wrong with what is about to be committed** | Verification failing on the work itself; the change looks destructive in a way the prompt did not ask for (mass deletions, a dropped table, a rewritten history file); the staged set contains paths you cannot account for; the work turns out to contradict what the prompt asked for | A minor caveat, a known limitation, a test that was already failing before the turn and is said so |
| **An open question to the user that functionally blocks the purpose of the prompt** | "I couldn't tell whether you wanted the endpoint renamed or aliased, and these two need different migrations — which?", where the committed work would be the wrong work under one answer | "Want me to update the callers too?" — an offer of further work; the prompt's purpose is met either way |

The test for the second case: **if the user gave the other answer, would this commit need to be
thrown away rather than built on?** If it would be built on — extended, adjusted, followed up —
commit, and leave the question in the summary for them to answer next.

Three cases override all of that:

| The prompt... | Do |
| --- | --- |
| said to hold off — "don't commit yet", "wait before committing" | **Don't commit.** An explicit hold beats everything here |
| said "auto summary commit" | **Commit**, whatever the summary looks like |
| was only a commit request ("/auto-summary-commit") | **Commit** — the user is already looking at the work |

> **Corrected twice.** This first said **always ask**: "never commit unreviewed work the user has
> not seen", with a yes/no on every turn that did any work. The summary is on screen before the
> question either way, so on a routine turn the question reviewed nothing — it just demanded a
> keystroke to confirm what the user had already read.
>
> It then said **ask whenever the summary raises anything** — a question, options, a caveat or
> trade-off, an assumption the user might reject, work left out, a finding that changes the
> picture — under the test "would the commit be different if the user disagreed with a sentence in
> this summary?". That test passes on almost every substantial turn, because almost every
> substantial summary states an assumption or a caveat, so in practice it still asked most of the
> time. It treated the commit as a point of no return when it is the opposite: a commit is the
> cheapest thing in the repository to revise or undo, and an uncommitted turn is the one with
> nothing to roll back to. Worse, a turn that ended in "not yet" or "I'll commit it myself" left
> its prompt and summary unrecorded — the loss this skill exists to prevent. Only a problem that
> would make the commit itself wrong, or a question whose answer decides whether the work is the
> right work at all, justifies holding it back.

Whichever way it goes, the commit is local and reversible — say the short SHA when reporting it,
so `git reset --soft HEAD~1` is available if the user wanted something else.

## Steps

### 1. See what changed

```bash
git status --porcelain         # empty output means stop here, silently — see "When to run"
git status --short --branch    # also shows the current branch and any in-progress operation
git diff --stat
```

`git status --porcelain` is the gate: it lists modified tracked files and new untracked ones, and
excludes everything gitignored. If it prints nothing, the prompt changed nothing git would record
— abandon the skill without saying so.

Read this **before staging anything**, and keep the output — it is the record of what the index
looked like before you touched it, which you need if the user declines in step 3.

**Which paths are yours** is the one thing you must get right, and how you know depends on how you
were invoked:

- **The hook invoked you** — it listed them, computed against a fingerprint of the tree taken
  before the turn started. That list is authoritative; it already excludes anything that was dirty
  beforehand, and it already includes work deferred by an earlier "not yet" that is still
  uncommitted. Use it as given rather than re-deriving it.
- **You invoked yourself** — work it out from what you actually did this turn. Anything in
  `git status` you cannot account for is someone else's: a file you never opened, an in-progress
  edit, a stray build artifact. Leave it, and say what you left.

### 2. Stage this prompt's work

The commit takes **everything in the staging area**, so the stage must contain exactly the paths
from step 1 — no more, no less:

```bash
git add -- <the paths from step 1>      # name them explicitly
git diff --cached --name-only           # this must match step 1's list exactly
```

**Do not use `git add -A`.** It stages the entire working tree, which is only correct when nothing
else in it is dirty — and you cannot rely on that, because the user may have edits in flight, a
tool may have written a file, and a long session accumulates both. The failure it causes is quiet
and hard to unpick later: a commit whose body describes your work and whose diff also contains
somebody else's.

If `git diff --cached --name-only` comes back with anything not on the list, unstage it
(`git restore --staged -- <path>`) before going on.

Note that `git mv` already stages a rename but leaves later edits to the moved file unstaged, so a
rename-plus-edit change needs the file staged again — otherwise the commit records the move
without the content.

### 3. Decide whether to ask, and ask if so

Work out from "Whether to ask at all" above which case this is.

**If no question is warranted — the usual case** — go straight to steps 4–7, commit, then
`rm -f <deferred> <prompt>` as for "Commit it" below, and report it: subject line, short SHA, and
anything you deliberately left unstaged. Do not announce that you skipped a question, and do not
hold the commit back for the caveats or follow-up questions in your summary — they go into its
body.

**If it is warranted** — one of the two cases above, and only those — the user needs the summary in
front of them before they answer. What that takes depends on how you got here:

- **The hook invoked you** — the turn was ending, so your summary of the work is already on screen
  immediately above. It is the commit body; do not restate, re-summarise or re-format it. Print
  only the subject line you intend to use, then ask.
- **You invoked yourself** mid-turn, before writing that summary — print the full user-facing
  summary first, then the subject line, then ask.

Ask with `AskUserQuestion` so the answer comes back in-session, offering **exactly these four
options**:

| Option | What it means | What you do |
| --- | --- | --- |
| **Commit it** | Go ahead | Steps 4–7, then `rm -f <deferred> <prompt>` — nothing is outstanding any more |
| **Not yet, still working** | The change is real but half-finished | `git restore --staged -- <paths>`, then `printf '%s\n' <paths> >> <deferred>` so the eventual commit covers them too |
| **I'll commit it myself** | The user is taking this one | Exactly the same two commands. Auto-commit stays on for later turns |
| **Stop asking this session** | Enough | `git restore --staged -- <paths>`, then `touch <off>` so neither hook raises it again |

`<prompt>`, `<deferred>` and `<off>` are the paths the hook prints under "State files"; use them
verbatim rather than reconstructing them, and `<paths>` is the list it gave you. A deferred turn
keeps its prompt on file, so when the work is finally committed the Prompt section covers every
turn the commit contains.

The middle two look alike and are not: **"not yet" means the work continues**, so it must be
carried into the next commit rather than forgotten, while **"I'll commit it myself" hands that
path to the user** — but both leave auto-commit on, and both record the paths, because either way
those changes are still uncommitted work this session produced. Only "stop asking" switches
anything off.

Order matters. The summary must be on screen *before* the question, and nothing may be committed
until the answer comes back — the point is that the user can read the explanation and inspect the
staged diff (`git diff --cached`) while deciding.

On any of the three declines: put the index back the way step 1 found it (`git restore --staged`
the paths you added), leave the working-tree contents untouched, say the work is left uncommitted,
and stop. Do not stash and do not offer a smaller commit instead.

### 4. Write the subject line

**Hard limit: 80 characters** — characters, not words. One line, summarising the whole change:
the title for the Prompt and Summary sections beneath it, not a restatement of either.

Match the repository's existing style — read it off `git log --format='%s'` rather than assuming,
and defer to the project's own conventions file if it records one. Where the log shows no settled
style, default to lowercase, imperative mood, no trailing full stop and no `type:` prefix: for
example `rename studies endpoint to study_memberships`, not
`Refactor: Renamed the /me/studies endpoint to /me/study_memberships.`

Summarise the *change*, not the process — what the repo looks like now, not that you were asked to
do something.

**If the turn's work came from a stage of a Plan of Action, the subject carries that plan's
prefix** — `<Proposal Name> Proposal <stage>.<section>: ` before the subject above, as in
`User Invitations Proposal 02.1: add the invitations table`. The 80-character limit covers the
prefix too. The `plan-of-action` skill in the sibling `documentation-and-planning` plugin gives
the full rule; this is only the reminder that a plan run's commits are not styled like the rest.

### 5. Write the body: Prompt, then Summary

The body is two sections, in this order, with these headings literally:

```markdown
## Prompt

<what the user asked for, verbatim>

## Summary

<the full user-facing summary of what you did>
```

Both halves earn their place. The summary says what changed and why; the prompt says what was
actually asked for — and those differ more often than they look. A year later the question
`git log` gets asked is usually "why is this like this", and the answer is as often in the request
as in the work.

#### The Prompt section

Verbatim, not paraphrased. The hook records the turn's prompt at the `prompt:` path in its
message — **read that file and use it**, rather than retyping from memory: it is exactly what was
sent, and it survives context compaction on a long turn. If the file is missing or empty (no
`jq` on the machine, or you invoked yourself), reconstruct it from the conversation as closely as
you can, and do not smooth out the wording.

If the turn had more than one user message — a correction, an interruption, an extra instruction
partway — include each in order, separated by a blank line. The record is what was asked across
the whole turn, not just its opening.

The one thing you may change is bulk pasted **data**, per the next section.

#### Summarising pasted data — and when not to

A prompt often has something pasted into it. Some of it must be cut down, and cutting the wrong
kind destroys the record this section exists to keep.

| Summarise it | Keep it verbatim |
| --- | --- |
| Stack traces and exception dumps | Prose instructions, specs, requirements, acceptance criteria |
| Build, test or CI logs; terminal output | A prompt, template or checklist copied from somewhere else |
| JSON/XML/CSV payloads, API responses | Code to be written, reviewed, fixed or transplanted |
| Base64 blobs, minified bundles, lockfiles | A diff or patch to apply |
| Long file or directory listings | Short error text — a line or two naming the actual problem |

The test is **is this block the instruction, or evidence of a situation?** Evidence gets
summarised; the instruction never does. A 400-line test log is pasted so you can find the failure
in it, and once the commit exists the failure is what mattered — but a 400-line spec pasted from a
ticket *is the request*, and a commit body that replaces it with "[pasted: a spec]" has thrown away
the only record of what was agreed.

- **Leave anything under roughly twenty lines alone.** This is a rule about bulk, not tidiness
- **Mark every replacement** so a reader knows something was cut, and say what it was, how big it
  was, and what mattered in it:
  `[pasted: 340 lines of npm test output — 3 failures in auth.test.mjs, all ECONNREFUSED]`
- **When it could be either, keep it.** An over-long commit body is an annoyance; a commit body
  that has summarised away the actual instruction is a lie about what was asked, and nothing later
  can recover it

#### The Summary section

The full user-facing summary for this turn — the same explanation that is on screen, reproduced
faithfully as markdown. Under the hook that is the response you had already finished writing when
the turn tried to end; scroll back to it rather than composing a fresh one:

- Keep the whole thing: headings, tables, code references, the `★ Insight` blocks, and any
  assumptions, caveats or flagged concerns. Those caveats are the most valuable part to preserve —
  they are the context that is otherwise lost.
- Keep it verbatim rather than re-summarising. The point is that the commit and the terminal say
  the same thing.
- Drop only pure terminal decoration that carries no meaning (e.g. the long `─────` rule
  lines).
- Never invent content that was not in the summary, and never describe work that was not done.

### 6. Commit — onto the branch that is checked out

Write the message to a file and commit with `-F` — never build a multi-line markdown body with
`-m`, where backticks and quotes get mangled by the shell:

```bash
# Write the message under your session scratchpad directory, never into the repo.
MSG=<scratchpad>/commit-message.txt
cat > "$MSG" <<'EOF'
<subject line, ≤80 chars>

## Prompt

<the prompt, verbatim, bulk pasted data summarised>

## Summary

<full user-facing summary as markdown>
EOF

# --cleanup=whitespace keeps markdown '#' and '##' headings, which a
# 'strip' cleanup mode would delete as comments.
git commit --cleanup=whitespace -F "$MSG"
```

The quoted heredoc delimiter (`<<'EOF'`) is load-bearing: unquoted, the shell would expand
backticks and `$` inside the summary.

Do not write a `Co-Authored-By:` trailer by hand. The harness appends its own attribution, and a
hand-written one names whichever model the rule was written under — which is wrong the moment the
same skill runs under a different one.

**Commit onto whatever branch is currently checked out, whatever it is** — including the default
branch. Do not create a branch, switch branch or offer to, unless the user asked you to in this
prompt or earlier in the session. A branch made "to be safe" strands the work somewhere the user
did not expect and is not looking; if committing here seems wrong, say so and let them decide.

### 7. Verify

```bash
awk 'NR==1 { print length, $0 }' "$MSG"   # must be ≤ 80
git log -1 --format='%b' | grep -c '^## ' # must be 2: Prompt and Summary survived --cleanup
git log -1 --format='%s%n---%n%b'         # confirm subject and body landed intact
git status --short                        # confirm what, if anything, is still uncommitted
```

If the subject came out over 80 characters, shorten it and `git commit --amend -F` the corrected
file — this is the one amend this skill permits, and only for a commit it just created itself.

Then tell the user the commit was made, with its subject line and short SHA, and name anything
deliberately left uncommitted.

## Never

- **Never commit past a blocking problem.** Something majorly wrong with the change, or an open
  question whose answer decides whether the work is the right work at all, makes the question in
  step 3 mandatory. Nothing short of that does. (This bullet used to read "never commit past an
  open decision", which made any caveat or assumption in the summary a reason to ask, and before
  that "never commit unreviewed work the user has not seen"; see "Whether to ask at all" for why
  both were wrong.)
- **Never commit when the prompt said to hold off.** "Don't commit yet" outranks every other rule
  here, including "auto summary commit" appearing elsewhere in the same prompt.
- **Never change branch.** Commit onto the branch that is checked out, as-is — no new branch, no
  checkout, no rebase, no reset, unless the user asked for one.
- **Never push.** This skill commits locally and stops. Pushing is a separate, explicit request.
- **Never amend, reword, or squash a pre-existing commit** — only the one this skill just created,
  and only to fix an over-length subject.
- **Never commit secrets.** Credential files, `*.tfvars`, state files such as
  `terraform.tfstate` and anything else the project gitignores are gitignored for a reason; if one
  shows up staged, stop and tell the user rather than committing and fixing it afterwards — a
  secret in `git log` stays there after the file is deleted.

## Related

- `conventions` skill, in the sibling [`documentation-and-planning`
  plugin](../../../documentation-and-planning) — where a project records its own commit-message
  style, and why the project file wins over the default in step 4. It is not required: step 4 falls
  back to reading the style off `git log` when the skill is not installed
- `plan-of-action` skill, in that same sibling plugin — the
  `<Proposal Name> Proposal <stage>.<section>: ` prefix step 4 applies while a Plan of Action is
  being implemented, and what each part of it means
