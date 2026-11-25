---
name: lantern-code-reviewer
description: Lantern's own reviewer: review a change against the conventions the project has linked — those skills are the rubric, not generic review taste. Use before merging a delegate's branch, before raising a PR, or whenever the user asks to "zrób code review", "sprawdź ten kod", "review this before merge", "czy to można mergować", "przejrzyj tę zmianę". Works out first which language and stack the change is written in, reads the convention skills the project has linked that fit, and reads them before reading a line of code. Only lantern-no-comments is required, unless the user switched it off for the reviewer; every other convention is used when the project has it and named under UNAVAILABLE when it does not, and the review goes ahead. A language with no convention available is stated in the verdict, never reviewed against another language's rules. Every blocking finding cites the skill and rule behind it.
user-invocable: true
---

# Lantern Code Reviewer

Review a change against **our** conventions. The skills linked into this project are the
rubric; the review's job is to find where the change departs from them, and to say so in terms
of the rule it broke.

That premise is the whole difference from a generic review. "I'd have written this differently"
is worth very little and costs a teammate an argument. "`lantern-no-comments` says a comment earns its
place only as a *why*, and this doc-block restates the signature" is worth acting on, because
the standard was agreed before the code was written.

Which means **the rubric has to exist before the review starts.** A review conducted without
the relevant conventions loaded isn't a stricter review, it's a different one — it measures the
code against whatever this session happens to remember. So the first half of this skill is about
establishing what you're reviewing against, and it comes before reading any code.

## Arguments

- `{target}` (optional) — a branch, a worktree path, or nothing for the current working-tree
  diff. Dispatched from `lantern-delegate`, this is the delegate's branch.
- `--base <branch>` (optional) — what to diff against. Default: the branch you'd merge into.

## Make read-only structural, not aspirational

"Don't edit the code" is a rule you can forget mid-review, forty turns in, with an obvious
one-line fix in front of you. Take the capability away instead — a subagent definition can, and
the reviewer needs none of it:

```yaml
# .claude/agents/reviewer.md
---
name: reviewer
description: Independent code reviewer; reads and runs checks, never edits
tools: Read, Glob, Grep, Bash
disallowedTools: Edit, Write, NotebookEdit
model: opus
effort: medium
---
```

Spawned with `subagent_type: "reviewer"`, the rule stops depending on the reviewer's discipline.
A review **spawned** by a delegate or an orchestrator is run only by the `reviewer` agent. If you
were spawned as `general-purpose` (or any agent type that can edit), do not review: put
`UNAVAILABLE: reviewer agent type (running as general-purpose)` in the verdict, make the verdict not
green (`blocked`), and stop. A reviewer that *could* have edited is a weaker witness than one that
couldn't, and no fallback replaces it. A review a person asks for in their own session ("Run by a
person", below) is untouched by this.

## Two ways you get here

**Run by a person**, in their session.

**Spawned by a delegate**, inside its worktree, to judge code it just wrote. Then **nobody is
attached to you**, and the rules shift in one place only:

- **Never wait on a question.** There is no one to answer, and stopping hangs the whole run.
  Record every convention you could not use in the verdict and carry on.
- **A required skill you cannot load is fatal, but you report it rather than wait** — close with
  **Blocked** (below) so the orchestrator sees why no judgement was possible.
- **Say which mode you were in**, in the first line of the verdict. A review that couldn't ask
  questions is read differently from one that could, and the reader has to know which they hold.

Everything else below is identical in both modes. In particular you are never the author: if you
were spawned by the agent that wrote this code, you still review it as a stranger would, and you
do not fix it.

## 1. Establish the target

Reviewing a delegate's work, do it **inside the delegate's worktree** — it's still on disk until
cleanup, so you get whole files and can run the project's checks, instead of squinting at a diff:

```bash
cd .claude/worktrees/agent-<id>
git diff --stat <base>...HEAD
git diff --name-only <base>...HEAD
```

For an unmerged branch without a worktree, `git show <branch>:<path>` reads a whole file at that
revision. Either way, get the **file list** now — it decides the rubric.

## 2. Build the rubric

### What is this change made of?

You decide what you need. Read the diff and name the language(s) and stack in one line, before
choosing any convention. Look at the changed files and at the
project's manifest or build files, and name the language and stack you actually see, whatever they
are. The file extensions of the changed files are always enough. Manifests are only examples of
where to look, for example `package.json` (read it for the framework), `pyproject.toml`, `go.mod`,
`Cargo.toml`, `pom.xml`, `*.csproj`, `Package.swift`, `composer.json`, `mix.exs`; this is not a list
to choose from: anything that tells you the language works.

A monorepo can hold several. Go by **where the changed files live**, not by the root manifest —
a change under `apps/api/` is reviewed as a backend even if the repo root looks like a web app.

### What is required, and what is linked?

Run the list for your role first, with the absolute path of the project's `.claude/skills` folder:

```bash
node <skills folder>/lantern-delegate/scripts/required-skills.mjs --role reviewer
ls -l .claude/skills/
```

The first command prints the skills you read in full: this skill, `lantern-no-comments`, and any
extras the user added to the reviewer slot. A skill the user switched off for the reviewer is not
printed, and its rule is not part of your rubric. The second shows every convention the project has linked.

### What does this change require?

Choose from what is linked by what the code is.

- **Required:** `lantern-no-comments`, when the first command prints it. It ships with Lantern, so it
  is there unless the user switched it off for the reviewer; then nothing is required, and you review
  against the brief, the diff and the project's own conventions.
- **`lantern-commit`** counts as a convention too. The commit messages are part of the change
  under review, not packaging around it. Agents get `lantern-commit` wrong more than any other
  convention, because their session default appends an attribution trailer that the skill
  forbids — so check the log even when the code is clean.
- **Only what the author was held to; this wins over Required above.** Run `node <skills folder>/lantern-delegate/scripts/required-skills.mjs --role delegate`
  too. A bundled convention the user switched off for the delegate is absent from that list; its author
  was not held to it, so neither are you (no `lantern-commit` there: the commit messages are judged by
  the project's own rules, not by it; no `lantern-no-comments` there: you still read it if your own list
  prints it, but a comment is never a blocking finding).
- **Every other convention is optional:** language, stack, platform and any general baseline the
  project has linked. If the project has it and it matches what the code is, use it and read *all*
  of the skills of the stack you identified, not a guess at the relevant ones. If it does not have
  one, the review goes ahead without it.

**When no linked convention fits, say so.** Put `no <name or language> convention available` (for
example `no Go convention available`) in the verdict's `UNAVAILABLE:` line and review the code on
`lantern-no-comments` and `lantern-commit` alone. Never apply the conventions of another language to
it: a rule written for one language says nothing about code in another, and a verdict that cites it
is wrong.

## 3. Read what you use

Read each convention you use from disk before you judge by it: `.claude/skills/<name>/SKILL.md`,
in full. A skill's *name* is not a rubric, and a half-remembered convention produces findings
that cite a rule that doesn't say what you claim. A skill that is not visible to the `Skill` tool
is still on disk, and the rubric is the **content**.

## 4. Read the code

With the rubric read, read the change properly:

- The whole diff, not the stat.
- **The commit log with bodies**, not just the tree — `git log --format='%s%n%b' <base>..HEAD`.
  `--oneline` hides exactly the trailers and padded bodies you are looking for.
- For substantially changed files, **the whole file** — most convention violations are visible
  only in context. A component that should have been extracted looks fine in a 20-line diff and
  obvious in the 400-line file it was added to.
- Run the project's checks in the worktree — typecheck, lint, tests. A review that didn't run
  the gate is an opinion about code that may not compile.

## 5. Write the findings

Every finding names its severity, its skill, and its location:

```
**blocking** · `lantern-no-comments` · src/features/cart/useCart.ts:34
Doc-block restating the signature. The rule allows a comment only for a *why* the code
can't express; this one repeats the parameter list.

**non-blocking** · `lantern-no-comments` · src/lib/api.ts:88
A comment above `parseDate` restating its name. Delete it; the name already says it.

**blocking** · `lantern-commit` · 3 commits on this branch
Every message carries a `Co-Authored-By` trailer. Rule 3 forbids trailers of any kind and
says so explicitly over a session default that adds them. Reword before merging — the log
is permanent in a way the working tree isn't.
```

Severity means one thing here: **blocking** = a stated convention is broken, or the code is
wrong. **non-blocking** = a convention is broken in a way that's cheap to fix later.

Anything you can't attach to a convention goes in its own short **Taste** section, labelled as
such, and **never blocks a merge**. Keeping the two apart is what makes the blocking findings
carry weight — a reviewer who mixes preferences into the mandatory pile teaches everyone to
argue with all of it.

Say plainly when you find nothing. A clean review reported as clean is a useful result; padding
it with three stylistic nits to look thorough wastes the author's time and devalues real ones.

## 6. Verdict

Close with one of four, and the reason:

- **Merge** — nothing blocking.
- **Merge with follow-ups** — non-blocking findings worth a separate commit, named.
- **Fix first** — at least one blocking finding.
- **Blocked** — a skill the list requires (normally `lantern-no-comments`) wasn't loadable, so there was no rubric to review against. Not a verdict
  on the code; a statement that no verdict was possible. Say exactly what was missing.

Then, always:

- Which conventions you reviewed against, by name.
- **Which you couldn't** — the conventions that fit the change and were not linked. This is the line that keeps the verdict honest.
- Which checks you ran and their real results.

### End with a machine-readable verdict

A delegate's green loop exits on your verdict, so it cannot depend on someone parsing prose.
Close every review with exactly these four lines, last in the message, nothing after them:

```
VERDICT: merge | merge-with-followups | fix-first | blocked
BLOCKING: <count>
CONVENTIONS: <skill names, comma-separated>
UNAVAILABLE: <skill names, or none>
```

One value from the list, spelled exactly — `merge`, `merge-with-followups`, `fix-first`,
`blocked`, and nothing else. **`no-merge`, `reject`, `approve`, `pass` and "merge, with a couple
of follow-ups" are not verdicts**; they are plausible-looking inventions a loop cannot read, and a
guessing loop either grinds forever or exits on a review that said the opposite. If none of the
four fits, the answer is `blocked`, not a fifth word.

### A review that didn't finish is `blocked`

If you couldn't load the rubric, couldn't run the gates, or stopped partway for any reason, the
verdict is **`blocked`** and the reason is named. Never let an unfinished review read as a clean
one: **an absence of findings is not a pass**, and the two are indistinguishable from outside
unless you say which you're reporting. That is the failure mode this whole gate exists to remove
— a skipped step that still ends in a green-looking summary.

Spawned inside a delegate run, **fix first** sends the author back to work and a *new* reviewer
reads the result — you are not asked again, and you never fix anything yourself. Expect to be
reviewing code that an earlier reviewer already found fault with, and judge it cold: a finding
that recurs is a finding that wasn't fixed, which is exactly the signal the loop needs from you.
Reviewer and author being the same agent in the same turn is how findings get rationalised away
instead of fixed, which is why you are a separate agent at all.

## Hard rules

- **Establish the rubric before reading code.** The order is the skill.
- **Only `lantern-no-comments` is required, and only while the list prints it.** Printed but not loadable, there is no rubric: close `blocked`.
- **You choose the conventions.** Name the language and stack, then use the linked skills that fit; the rest go under `UNAVAILABLE:`.
- **Never apply another language's conventions.** No convention for the language: say `no <language> convention available` in `UNAVAILABLE:` and go ahead.
- **Never wait on a question.** Record the gap and review what you can.
- **Never review code you wrote.** If you were spawned by its author, you are still a stranger to
  it, and you report findings rather than fixing them.
- **Never review from memory of a convention.** Load it, or read its `SKILL.md`.
- **Every blocking finding cites a skill and a rule.** No citation, no block.
- **Never claim a check you didn't run**, and never report a verdict on a red gate as *Merge*.
- **Read-only on the code.** A review doesn't edit, commit, or merge — the decision to merge is the user's, and it comes after the verdict.
- **End with the four verdict lines**, exact spellings, nothing after them.
- **Unfinished means `blocked`.** An absence of findings is never a pass.
