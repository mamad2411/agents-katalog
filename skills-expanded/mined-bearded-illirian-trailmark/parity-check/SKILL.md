---
name: parity-check
description: |
  Guides a fixture run end to end and reports whether the framework behaved the
  same on this runtime as on the reference one. Picks a fixture, hands its task
  statement to the agent under test, waits, locates the log directory the run
  produced, then calls bin/parity-run and explains the result.

  The stop in the middle is the point: an agent cannot hand a task to itself and
  wait for its own answer. A human runs the chain; this skill frames it.

  Use when: "/parity-check", "run a fixture", "check parity", "does it behave the
  same on Codex", verifying an adapter after installing it.
---

# Parity-Check Protocol

Answers one question: **did the framework produce the same shape of work on this
runtime as it does on the reference one?**

Not "is the output identical" — it never is. Two agents word an artifact
differently, and so does the same agent twice. What must match is the shape: the
artifact exists, carries its sections, registers its row, offers its gate.

## When to invoke

- After installing an adapter on a new runtime, to see whether anything works at all
- After changing a protocol, to see whether the change holds on both runtimes
- Before claiming a runtime is supported

## Input

A fixture directory under `fixtures/{skill}/{case}/` and a runtime to test.

## Output

A per-assertion report from `bin/parity-run`, plus a plain reading of what a
failure means — a broken framework, a fixture that expects the wrong thing, or a
genuine divergence between runtimes.

## Hands off to

— (terminal). A failure is a finding, not a next step: it goes to the person
running the check, who decides whether to fix the framework or the fixture.

---

## Step 0 — Locate the workspace root

```bash
test -d fixtures && test -d bin && echo "root ok" || echo "not the workspace root"
```

Not the root → walk up until `fixtures/` and `bin/` sit side by side. Nothing
found → stop and say so. Everything below assumes paths relative to that root.

---

## Step 1 — Choose the fixture

List what exists:

```bash
find fixtures -mindepth 2 -maxdepth 2 -type d | sort
```

Show the list numbered. Accept either a number or a path.

No fixtures at all → say so and point at `/fixture-new`. Do not invent one on the
spot: a fixture written to be passed is worth nothing.

---

## Step 2 — Hand the task to the agent, then stop

Read `{fixture}/input.md` and show it **in full**, not summarised. It is the exact
statement the agent under test must receive; paraphrasing it changes the test.

Then stop:

```
Hand the statement above to the agent you are testing, let the chain run to the
end, and come back when it has finished. Say "done" and I will pick it up.
```

**This stop is not optional and it is not politeness.** A shell script cannot make
Codex or Claude Code execute a protocol, and neither can this skill. Skipping the
stop means checking a directory some earlier run produced — which passes, proves
nothing, and hides that nothing was tested.

Wait for an explicit answer. Do not proceed on silence.

---

## Step 3 — Locate the run

Offer the freshest task log directory:

```bash
ls -td tasks/log/*/ | head -3
```

Show the three most recent with their modification times and propose the newest.
Let the answer override it — the run may have gone elsewhere, and guessing wrong
means checking someone else's work.

Confirm the directory holds something from the last few minutes:

```bash
find {log_dir} -type f -newermt '-30 minutes' | head -5
```

Nothing recent → say so and ask whether the run actually completed. An empty or
stale directory produces a confident red report about the wrong thing.

---

## Step 4 — Run the checks

```bash
bash bin/parity-run {fixture} {log_dir}
```

The runner prints one line per assertion and exits non-zero if any failed.

---

## Step 5 — Read the result

Exit zero → the shape matches. Say so plainly and name what was checked, so the
claim is inspectable rather than a bare "passed".

Exit non-zero → a failure is one of three things, and they are not the same:

| What failed | Likely meaning | What to do |
|---|---|---|
| `artifact_exists` | The chain never reached the skill, or wrote elsewhere | Check the run actually completed and the directory is right |
| A `section` assertion | The skill ran but produced a different shape | A real divergence — this is what the fixture exists to catch |
| `db_row` | The artifact was written but never registered | The runtime executed the protocol but skipped its bookkeeping step |
| `approval_gate` | The skill did not stop where it must | The discipline broke, which matters more than a missing section |

State which of the three it is. "It failed" is not a report.

A fixture can also simply be wrong — expecting a section the skill no longer
writes. Say so when it looks that way rather than blaming the runtime; a fixture
nobody trusts is worse than no fixture.

---

## Anti-patterns

### ❌ Skipping the stop in Step 2

The skill runs `parity-run` against whatever directory is newest, without anyone
handing the fixture to an agent. Green report, nothing tested.

**Rule:** Step 2 waits for an explicit answer. Silence is not consent.

### ❌ Summarising `input.md`

The statement is the test input. Paraphrased, it is a different test.

**Rule:** show it in full, verbatim.

### ❌ Reporting "failed" without saying which kind

A missing section and a missing database row mean different things — one is a
divergence in behaviour, the other a skipped bookkeeping step.

**Rule:** name the kind, per the table in Step 5.

### ❌ Editing the fixture until it passes

The fastest way to a green run, and it destroys the only thing a fixture is for.

**Rule:** change a fixture when it demonstrably expects the wrong shape, and say
that is what you are doing.

---

## Step 99 — Log invocation (auto)

Before exiting, log this skill invocation to routing.db:

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'parity-check', datetime('now'))" 2>/dev/null || true
```

If `{slug}` / `{N}` are unknown the row is written with empty values; `|| true`
keeps a logging failure from aborting the skill.
