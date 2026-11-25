---
name: guard-verification
description: "Use when code adds a guard. Prove tests catch its loss."
version: 1.1.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [testing, verification, sabotage, guards, quality, mutation-testing]
---

# Guard Verification

A green suite proves the code passes the tests. It does **not** prove the tests would
catch the code being wrong. When the deliverable is guarded behaviour — a refusal, a
safety check, a branch that changes where data goes — the only evidence that a guard is
protected is: delete it, and watch the test that owns it fail.

Use this whenever a change adds a rule the system must obey, a check that refuses
something, or a branch that changes an outcome. Skip it for purely additive code with no
guard in it — there is nothing whose absence would be silent.

## Before building a refusal: measure its blast radius

A guard that refuses an input class (skip an input with 2+ subjects, reject a file over N)
can throw away inputs that work today. Before writing it, run a throwaway read-only
script over the REAL data the guard will see and print two numbers:

- **how many inputs it would refuse**: if that is near zero, the simple rule is safe.
  If it is large, the rule needs a sharper condition, for example counting only
  items above the existing quality floor so a blurred bystander does not trigger it.
- **how many of those were actually WRONG under the old behaviour**: check against
  ground truth that is already there (the same entity's other, unambiguous inputs). This
  turns "it might be wrong" into "it was wrong in 2 of 3". The same pass also finds
  bad records that already exist, and those need to be reported to the owner separately.

Run it against a scratch copy of the database or with `mode=ro`, never the live store.

**When the owner dictates the rule, still measure its blast radius and lead with it.** Build
it exactly as specified, then report the effect in one line ("237 of 331 groups now
refuse"), with what still happens to the refused items. Do not soften the rule with a
fallback to shrink that number: the number is the owner's input for the decision, not a defect
for you to engineer away.
Then explain to the owner, with the result in hand, why the guard exists even though the
rule already tells users not to do it: a rule is for the person, a guard is for when
the rule gets broken.

**A refusal must not leave a half-made record behind.** When an input loop can refuse
every item, create the parent row (the entity, the run) at the FIRST accepted item,
never before the loop, or an all-refused run leaves an empty entity that looks valid.
Give this its own test and its own sabotage (move the create back above the loop).

**Count from what the write DID, never from the loop that attempted it.** Behind an
idempotent insert (`INSERT OR IGNORE`, an upsert), a loop counter reports every
already-stored item as added on a re-run, and the user reads "+20" as 20 new records.
Increment on the write's result (`rowcount == 1`, a returned id) and test a second run
over the same input reports zero added.

**Every new refusal reason needs its own counter, in BOTH the human output and the
machine output (`--json`).** If an existing tally (added / rejected / missing) has no
slot for it, the refused item disappears silently, which is the failure the guard
exists to prevent. Update any contract test that pins the exact dict, plus any agent
docs that name its keys.

## Red before green must be per test

When the new tests import a name that does not exist yet (a new constant), the red run
is one collection ERROR, which proves nothing about each test. Add just the bare name
first (the constant with no behaviour change), then run: every test must fail on its
own assertion. Any test that passes before the build should be an invariant that the
change must keep (e.g. "3 inputs must still map to one record"). Say so in the report
rather than leaving it as an unexplained pass.

**A new FILE gets a stub with the final API first** (a function returning the empty
result, plus the export line), so the red run fails per assertion instead of on
"file not found". The tests that stay green against the stub are the "must NOT match"
rules, which an empty answer obeys by definition: name them in the report as proved
only by the sabotage pass, and make sure that pass has a case loosening each of them
(threshold lowered, matcher made greedy).

**Read your own sabotage list before the first run and tighten the tests it would
miss.** Writing the cases often shows a constant or branch with no test on its
boundary (a minimum length with no query just under it). Add that test first, then run
the pass; a first-run miss costs a full extra cycle.

**A gap found by eye mid-build follows the same order.** When a screenshot shows a
miss (a locked control that still looks live), extend the test first and watch it go
red, then fix the code, then add a sabotage that reverts only that fix. A fix made
straight from the picture leaves nothing to stop the gap coming back.

**A threshold change needs a test on each side of every boundary**: below the minimum
(refused), in the warn band (accepted plus flag), at the recommended value (accepted, no
flag). Also cover each surface that repeats the number: CLI flag refusal, JSON flag,
text output, window Api, page constant. Sabotage each one separately: the number back,
the flag forced off, the flag forced on, the refusal widened, a quiet clamp restored,
and the page constant drifting.

**Raising a floor (a minimum count) breaks every old fixture that sat under it.**
Run the whole suite once after the gate lands and triage all failures together,
then fix file by file:

- A test whose subject IS the guarded flow gets the smallest real fix: add
  qualifying items (more matching inputs) and update counts it pins. Never weaken
  an assertion to get green.
- A test whose subject is something else (dedupe, filenames) and needs 1-2 items
  on purpose gets an autouse fixture that lowers the floor
  (`monkeypatch.setattr(mod, "MIN", 1)`), with a docstring naming the test file
  that owns the gate. Count these in the report so the reviewer sees each one.
- A test pinning the OLD behaviour at the boundary ("20 or fewer: all learned")
  is rewritten to the new rule with both decisions in its docstring, not deleted.
- Adding a journalled run to a flow changes contract tests too: the output gains
  a `run_id` key and "list runs" gains the new kind. Expect these in the triage.

**One gate for many entry points: a pure function plus a test per door.** When
several commands must apply the same selection rule (folder import, by-id learn,
the window's button, the picker), implement it once as a pure function returning
`(chosen, over_cap, outside, too_few)` and give EACH door a test with the same
fixtures: the same too-few input refused with the same sentence, the same odd item
left out. A door whose test is missing is the one that drifts.

## The procedure

1. **List each guard separately and name the test that owns it**, before running
   anything. Writing the owner down first is what turns "a test failed" into "the right
   test failed" — without it, an unrelated failure reads as success.
2. **Write the pass as a script with a `finally` that restores from an in-memory copy of
   the original file.** Never restore from git (it cannot distinguish the sabotage from
   the work in progress) and never drive it from a long-lived interpreter session.
3. **Run the whole suite for each sabotage, never with `-x`.** Stopping at the first
   failure lets an unrelated earlier test mask the owner, and the pass then cannot tell
   "the wrong test failed" from "the right test never ran".
4. **Check the tree afterwards regardless of what the script reported** — `git status`
   plus a grep for the sabotage strings (`if False`, the replaced literal). A restore
   that did not run looks identical to one that did until something greps.
5. **Report the score** as `N/N fired the test that owns them`, naming any owner that had
   to be relabelled and why.

**A clean first pass is a result worth stating, not a step to skip.** When every sabotage
fires its owner immediately, say so explicitly — it is the evidence that the fixture was
built right, and it is the only thing that distinguishes a verified guard set from one
nobody sabotaged. Silence reads as the latter.


## Promote the scratch pass into the permanent gate

**For a consistency checker, make the sabotages permanent tests by construction.**
Write it as a pure function of its inputs (`problems(parser, table, source_text) ->
[messages]`) and have one test call it on the real inputs (must be empty) and one test
per failure mode feed it a broken copy (dropped entry, extra dummy subcommand on a live
parser, blank reason, stripped source text) and assert a message NAMING the item.
No file is edited, so no restore can fail; still do one scratch pass on the real files
before reporting, since that proves the checker reads what the code really has.

A scratch sabotage script proves the guards once, on the day they were written. When
those guards protect SHIPPED behaviour, move the cases into the project's permanent
sabotage gate in the same step that closes the feature. Otherwise the next refactor
can drop a guard, and every gate stays green.

- **Give a test-owned guard its own case shape:** `(label, file, find, replace,
  pytest node)`, kept beside the checker-owned cases. The proof is that the NAMED node
  fails. Any failure somewhere in the suite does not count.
- **When a new test closes a miss, re-point the case at that test.** The case
  still names the old owner, which cannot see the gap, so the rerun reports the same
  miss and looks like the new test failed too.
- **Run the node clean first, and report `RED BEFORE` if it already fails.** A test
  that is red before the sabotage proves nothing when it is red after it.
- **Run the node alone**, `-B` and `-p no:cacheprovider` included. One node per case
  keeps a full pass to minutes, where a full suite per case would take hours.
- Share one `originals` snapshot and one `finally` across both case kinds, so a
  crash in the test-owned half still restores the files the checker half touched.

## A changed decision rule: measure the transition table

When a rule is meant to change answers (largest item wins -> the known match wins),
report before vs after as `old outcome -> new outcome: count` on scratch copies of the
dev store and the benchmark store. Do this in the shape, and again with the built code.
Get the "before" from the base commit, not from a hand-written copy: run
`git show <base>:src/pkg/mod.py`, `exec` it into a `types.ModuleType` named
`pkg._mod_<base>` with `__package__ = "pkg"` (relative imports then resolve), and
re-make the inputs with the OLD module's classes (enum by `.value`). Where ground-truth
labels exist, split the newly changed items into right / wrong-known / not-registered.
The post-build numbers must equal the shape's numbers, and they are what the report
quotes.

## A speed-up must prove the answers did not move

A performance rewrite of a decision function (vectorising a loop, caching, batching)
is a guard on "same answers". Procedure:

1. **Freeze the old implementation inside the test file** (`_old_rank(...)`, copied
   verbatim) and compare old vs new EXACTLY — names, order and float scores with `==`,
   never `approx` — on generated inputs at production dimensions. Include ties (two
   classes at the same score), one class, one reference, and no references at all.
   **Exception: a change that alters the arithmetic itself (batching many items into
   one matrix product).** BLAS rounding then depends on the matrix shape AND the item's
   row position in the block, so exact equality is unreachable even against itself
   (float64 does not fix it either). Do not loosen the old test silently: replace `==`
   with same names, same order, same VERDICT on every item, scores within a stated
   tolerance derived from a measured max difference (with headroom), and exclude only
   items whose score sits within that tolerance of a threshold, COUNTED out loud in the
   test. Route every caller through the batched function (single item = batch of one)
   so there is one code path, and tell the user that one path still is not
   bit-identical numbers across callers.
2. **Red first with a structural test** that only the new shape passes (e.g. the
   function must not iterate the reference names: spy or count calls), so the run
   proves the test file is wired before the build.
3. **Sabotage the ways a vectorisation goes subtly wrong**, each must fire the
   equivalence test: classes in sorted order instead of first-seen, unstable tie sort,
   average instead of max, rows not grouped by class, a dtype change (float64 matmul
   moves the last digits). Once a tolerance is accepted, float64 lands INSIDE it by
   design: replace that case with a coarser dtype (float16, ~1e-3 off) so the pass
   still proves the tolerance has teeth, and say why in the case's comment.
   **For batching, sabotage ALIGNMENT too:** rotate the batch's answers by one
   (`a[1:] + a[:1]`), never pad with `None` (a crash is not a catch). The owning test
   monkeypatches the batch and block sizes tiny (4 items, 3 rows) so boundaries split
   inside groups, then compares every output item against the one-by-one decision of
   its OWN inputs. Add a spy test counting calls (one batched call, zero per-item) so
   a regression to the old loop goes red even when answers stay right.
4. **Real-data proof in scratch, never in the repo** (real user data may be personal):
   on a read-only backup copy of the live store, run old vs new on every item and
   report the count that differ (must be 0), at the current size AND at a grown size.
   If the real teaching path cannot reach the requested size (too few qualifying
   items), grow the copy by direct inserts under test names and say so in the report.
5. **Time in one process, old vs new, per user-visible command** (listing, sort in
   plan-only mode), not only the inner function: the user feels the command, and the
   unchanged parts (I/O, parsing) explain why speedups differ per command. Report a
   table: size / command before -> after / answers differing. A size where nothing
   changes is reported too, not hidden.
   Run "before" without stash or worktree: `git archive HEAD src | tar -x -C
   <scratch>/head`, then `PYTHONPATH=<scratch>/head/src` for the before runs. The
   bench script prints `pkg.__file__` on every line, so no number can be credited to
   the wrong version. Save each run's `--json` output and diff before vs after field
   by field (verdict, match, destination folder, rounded score; groups as item
   sets); "same answers" is that diff at 0, not the test suite.
   A planner bench needs a PRE-FILLED target too, not only an empty one: build it
   from the empty run's plan (per move: 1/4 same bytes, 1/4 same size other bytes,
   1/4 other file under the name, 1/4 nothing), so every branch costs its real
   share. Run benches and pytest from `terminal`, not a subprocess inside
   execute_code: its environment leaks into the venv child (numpy import fails).
   Every figure written into code comments, constants' docs or the plan file comes
   from a run in this session or a cited record. A handoff's numbers (a drift, a
   reference count) are claims to re-measure: report the measured value and the
   mismatch.
   The same holds for a CAUSAL claim you are asked to write down ("the next
   bottleneck is db reads + planning"): profile the real command once before writing
   it (`cProfile` around `cli.main(argv)` on a scratch copy, list project functions
   above ~1% by cumulative time, with call counts). Briefs guess; a profile often
   shows half the guess wrong (here: a folder walked twice, not the db). Write the
 measured table and name the part of the claim that did not hold.
 Profile WITH the flags the real caller sets (the window always passes
 `--progress`): a progress bar that pre-counts its total re-walks the input,
 so a dry-run profile without it hides half the cost of a repeated walk.
   **Before shaping the fix, grep every call of the slow primitive inside the
   command, not just the ones the profile showed.** A profile run without
   `--progress` misses the extra passes that only the window's mode adds (a
   count-the-files helper that walks the same folder again). Here, "walked
   twice" was really four times under the window. Then split the primitive's
   cost in a scratch test (listing vs sort vs per-entry stat) so the shape
   promises a measured saving. Cheap reorderings with no effect on the result,
   like checking a filename suffix before calling the stat, come out of the
   same test.

## Removing a value creates a guard

When a shipped value is removed (an answer kind, a flag, a mode), the removal itself is
guarded behaviour and needs owners:

- **Turn every catch-all `else` that the removed value used to share into an explicit
  branch.** Once the value's own branch is gone, the `else` is where it lands. Then a
  stale caller silently does the default action, for example filing an input when it
  should have been refused. An unknown value must do nothing, and a test must assert
  that nothing happened.
- **Pin the removal from outside:** the entry point refuses the value, and the module
  no longer exposes the old function or constant (`not hasattr`). Sabotage it by adding
  the value back.
- **Prove that old persisted artefacts still work.** A journal, row or config written
  by the old version must still be read correctly, for example an old run must still
  undo. The absence of the code path must not break the history.
- **A changed normaliser with a legacy fallback needs four owners.** When a function
  that turns names into keys changes (a folder-name sanitiser, a slug, a case fold),
  its old outputs already live on disk and in databases. The shape: keep the old rule
  as a separate read-only helper, used ONLY on a lookup miss and in both directions,
  never to create anything new; grep every caller first, including private tools,
  since some work around the old behaviour and must be relaxed in the same change.
  The four owners: an old stored name finds the new-style folder, a new name finds the
  old-style folder, the exact match wins when both exist, and two fallback hits raise
  instead of picking. Sabotage by replacing the fallback with an empty result; the
  first, second and fourth must fire.
- **When a decision rule changes, grep the CONCEPT it retired, not only the enum.**
  Consumers often re-derive the old concept themselves (a review card that asks about
  the `is_primary`/largest item's match). Those items now carry the new outcome and are
  still treated the old way, so no enum grep finds them. Give each one a test under
  the new outcome, plus a sabotage that reverts only that consumer.
- **Removing a UI control: pin the count, the leftovers, and the remaining route.**
  Assert the container holds exactly the controls that stay (count the `<button`s in
  that bar, not just "the old label is absent"). Assert the old id appears nowhere in
  the JS or the CSS, so a dead click handler or style rule cannot linger. Assert the
  feature is still reachable from where it now lives (that panel's button calls the same
  `show(...)`). Run the count test red before you edit the markup.
- **After a mechanical rename in the tests (OLD→NEW), re-read what each test asserts.**
  Tests that still pass may be asserting the old meaning, or nothing about the new one.
  Add the assertion that tells the two apart, for example that a learn did NOT move the
  file.

## Sabotage the ORDER, not only the presence

A guard that runs in the wrong order is a guard that is absent for the inputs that matter,
and deleting it tests neither. Where a check must happen BEFORE a write — a validation
ahead of the row it protects, a refusal ahead of the side effect it prevents — add a
sabotage that disables the check while leaving the write in place (`if False and <cond>:`)
and name the test that must fail. The owning test has to assert the side effect did not
happen, not merely that an error came back: a refusal that returns the right message while
still writing is the defect this sabotage exists to catch.

**A docstring saying a test "owns" an ordering is a claim.** Re-run that sabotage
whenever the rule the order feeds changes. Under the new rule the fixture's order may
no longer decide anything, or it may never have decided anything, for example when the
item is already first in storage order. Build a fixture where the stored order and the
wanted order disagree AND the rule still uses order (two ask-band items, the larger one
stored second). Then move the case's owner to that test.

## Run it in the background, not in a foreground call

A full pass is `guards × full suite` and outgrows a foreground tool timeout. When the
call is killed the `finally` never runs and a sabotage is left sitting in the source —
silently, because the next test run is green with the guard gone.

Run the pass as a **background process** writing to a log file, then poll it; a tool
timeout cannot then kill the interpreter. Have the script append `git status` to its own
log as its last line, so the tree state is captured by the run itself.

Restore from an on-disk copy of the original and confirm with `git diff --numstat` that
only the intended lines remain. Do this whether or not the run reported success.

**Edit nothing in the repo while the pass runs.** Each case rewrites a source file and
its `finally` writes the snapshot back, so an edit made meanwhile to a file the pass
touches is silently reverted, and an edit to any other file can change what the
remaining cases see. Do the docs, wiki and log edits before starting the pass, or wait
for its exit. `_private/` notes that no case reads are the only safe exception.

## Exercise the guard; do not grep for it

A structural checker written as `"<token>" in source` is the default shape and it is
usually vacuous, because the token appears in places that are not the guard:

- **The docstring that EXPLAINS the guard contains its name.** A file documenting why it
  uses `samefile`, or why `PRAGMA foreign_keys` matters, keeps the check green with the
  call itself deleted — the prose is the match.
- **A second code path holds its own copy of the same comparison.** Matching a threshold
  test that exists in both the decision function and the near-miss/preview function
  proves neither, since deleting one leaves the other's identical line behind.
- **A flag or name occurring many times survives one rename.** `--apply` appearing
  seventeen times means renaming the one that matters changes no substring result.

Replace each with something that RUNS: open a real temp database and read the pragma
back, build a real file and ask the predicate about its own path, feed embeddings at
known scores through the real matcher and assert the verdicts, drive the real argument
parser and ask it for the flag. A behavioural check also survives refactors that a
string check turns into false alarms.

**A substring check survives a dead condition.** `'x.textContent = ' in src` stays
green when the line becomes `if (0) x.textContent = ...`. When the rule is "runs
every time", anchor the regex on the line start with its indentation
(`\n  x\.textContent = `) and sabotage by prefixing a false condition.

**Help text is prose too.** Checking a flag with `"--apply" in parse_args([cmd,
"--help"])` output stays green with the flag deleted as soon as the command's
description says "nothing happens until --apply". Walk the parser instead: find the
subparsers action (`dest == "command"`), take `choices[cmd]`, and test the flag against
the union of its actions' `option_strings`. Sabotage by deleting the `add_argument` line
only, leaving the description intact.

**Target the sabotage at the OCCURRENCE that matters and confirm which one it hit.** A
naive replace-first edits occurrence #1, which is frequently the docstring or the
sibling code path — the guard stays intact, the run goes green, and it reads as a
redundant check. Anchor on enough surrounding lines to be unique, and give every
duplicated guard its own case so each copy is separately proved.

**Match the sabotage's BREADTH to the check's breadth.** The rule above assumes a guard
that lives at one place; a check searching a WHOLE FILE for a string is the opposite
shape, and narrowing the anchor there makes the case permanently unprovable. Break the
first of two occurrences and the substring is still present, so the check stays green,
the text-differs assertion passes, and the harness reports a working guard as not
caught. Ask what the checker actually reads before writing the case: a line-specific
guard needs one precise occurrence, a file-wide search needs EVERY occurrence. Give the
harness an explicit opt-in (a `replace_all` field defaulting to false, so one edit /
one guard stays the norm) rather than widening every case to match the one that needed
it.

**When a rebuilt check fails, decide whether the CODE or the CHECK is wrong before
editing either.** A checker written from a rule's wording encodes an assumption about
scope that the code may deliberately not share — a plan-before-write flag belongs on the
commands that move data, not on one that only writes a reversible database row, nor on
the command that IS the reversal. Read the design intent, then fix the check to match
the code and write the exemption and its reason into the check. Silently widening the
code to satisfy a guess is how a checker starts dictating architecture.

## Harness requirements

- **Count errors and non-standard exit codes as failures, not only the word FAILED.** A
  sabotage that is a syntax error makes every test ERROR; a harness grepping for FAILED
  reports zero failures, and the guard looks tested when nothing ran.
- **Run the suite clean BEFORE the first sabotage and abort if it is not green.** A
  pass started from a red tree scores every sabotage against pre-existing failures, and
  "the owner fired" can no longer be told from "it was already failing".
- **Copy each sabotage anchor from the current source, never from memory.** Grep the
  exact line before writing the case: a line remembered as `if (x) return;` that is
  really `if (x) { ...; return; }` never applies, and the pass reports a working guard
  as missed.
- **Assert the sabotage applied at all.** If the target string is not found, report
  `SABOTAGE DID NOT APPLY` rather than counting the clean run as a pass. Assert the
  patched text differs from the original too: a replacement whose new text happens to
  equal the old is found, applied, and changes nothing.
- **Normalise line endings in the editor, and re-encode on write.** Repos mix CRLF
  and LF files; a multi-line target typed with `\n` is "not found" in a CRLF file and
  the sabotage silently never lands. Decode, `replace("\r\n", "\n")`, match, then put
  the original endings back before writing. Use
  `open(path, "r", encoding="utf-8", newline="")` to do it:
  `Path.read_text(newline=...)` and `write_text(newline=...)` are 3.13+ and raise
  `TypeError` on 3.11, killing the harness before the first sabotage lands. Expect this
  to hit most targets at once when it hits — a pass reporting one owner fired and every
  other target "not found" is an encoding bug in the harness, not a set of missing
  guards.
- **A scripted edit must keep the file's line endings.** On Windows,
  `Path.write_text` turns every `\n` into CRLF. A whole-file rewrite then makes the
  next exact-match sabotage "not found" and leaves a diff full of line-ending noise.
  Rewrite with `write_bytes(text.encode())` (or `newline=""`). After any scripted
  edit, run `git ls-files --eol <files>` and expect `i/lf w/lf`. A file shown as
  `i/lf w/crlf` (checked out CRLF by autocrlf, stored LF) is LF in git: read it with
  `.replace("\r\n", "\n")` before matching (a `\n` anchor is "not found" otherwise,
  and a multi-edit cell then stops halfway with only the earlier edits in memory),
  and write it back as LF. Only a file stored CRLF (`i/crlf`) keeps CRLF; inserting
  `\n` lines there makes it mixed, so normalise back to its own ending. `git ls-files` prints nothing for an UNTRACKED
  file, and a file-writing tool can save a new file as CRLF. Check new files with
  `file <path>` (no "CRLF" in the output) before the final gate. To count CRLF across
  many files, use Python bytes (`Path(f).read_bytes().count(b"\r\n")`): `grep -c $'\r'`
  under git-bash reported a count on every LF file. The agent's own
  find-and-replace tool can flip a whole LF file to CRLF too, and `git diff` hides it
  (it reports only the real lines). The tell is `git status`/`diff` warning "CRLF will
  be replaced by LF". Before the stop-before-commit report, loop over every touched
  file, compare against `git show HEAD:<file>` and rewrite to LF with `write_bytes`
  where HEAD is LF.
- **Run every child Python with `-B` (or clear `__pycache__`) in a finally-restore
  pass.** Python trusts a `.pyc` whose source has the same SIZE and the same mtime to
  the second. Most sabotages are same-size edits (`0.55` -> `0.40`), so a sabotage plus
  restore inside one second leaves the sabotaged bytecode valid: the next case runs
  against the previous case's code and fires the WRONG rule, and every later run of the
  real gate reports a value the source file does not contain. Measured, not theorised.
  If a gate reports something the source contradicts, delete `__pycache__` before
  suspecting the code.
- **Sabotage the REGISTRATION as well as the check.** With a real violation in place,
  remove the checker's call from `main()` (or the test from the suite's collection) and
  confirm the run goes green — that is the proof the call is load-bearing, and it
  catches a check that was written and never wired.
- **For a docs or consistency checker, require its own claim to be named in the output**,
  not merely a non-zero exit — otherwise one detector firing covers for another that
  never did.

## A sabotage anchored on prose rots when the project moves on

Cases that anchor on a document's STATUS — a phase heading, a section title, a
"— open" / "— closed" marker — stop matching the day that status legitimately changes,
and the harness then reports the anchor as stale rather than the check as broken. That
is the right message, but nothing generates it until someone runs the pass, so the rot
is discovered by a session that did not cause it.

- **Re-point such cases as part of closing the thing they name**, in the same step that
  changes the status. A case anchored on `## <phase> — open` is a dependent of that
  heading exactly like any other reference to it.
- **Prefer anchoring on a structural invariant over a transient one.** The rule being
  proved ("the roadmap never numbers a phase") is true of whichever phase is currently
  open, so anchor on the open one and expect to move it, rather than pretending the
  anchor is permanent.
- **After a refactor of guarded code, triage the permanent gate's anchors BEFORE the
  full pass.** Moving or reindenting a guarded line stales every case anchored on it.
  Run `scripts/stale_anchors.py` (loads the harness's case lists, checks each `find`
  against the working tree AND `git show HEAD:<file>`): "broken by me" cases are
  re-pointed at the new line in the same change; "stale at HEAD too" cases are
  reported as pre-existing, not fixed silently. Same split for NOT CAUGHT cases: say
  whether they touch files the change touched.
- **Date a pre-existing defect with `git log -S'<the line that defeats the case>'`**
  (the fallback, the earlier occurrence the find now hits), and write "since <hash>
  (from git history; not re-run there)" unless you actually ran the harness at that
  commit. "Every run since then showed it" is a claim about runs you never saw.
- **When a pass comes back below its known score, check the last-known-good copy before
  assuming you broke it.** A backup, the remote, or the previous tag either carries the
  same stale anchor — proving the rot predates this session — or does not, which points
  straight at the edit that caused it. One grep settles it and stops a hunt through work
  that was never involved.

## When a sabotage changes nothing

**Fire the guard by hand, both ways, BEFORE editing either the case or the check.**
Apply the sabotage manually at full breadth and confirm the check goes red; then apply
the narrow version and confirm it stays green. Two runs separate "the guard is broken"
from "the sabotage is too narrow", and they cost a minute against an afternoon of
rewriting a guard that was working the whole time. Restore from a copy taken before the
first edit and confirm the tree is clean afterwards, since this bisect is done outside
the harness and therefore outside its `finally`.

The question is **not** "is this test redundant". In order, the suspects are:

1. **The sabotage itself.** Did it compile? Did it land somewhere reachable? An injected
   statement ordered after the rows it selects from matches nothing and changes no
   behaviour.
2. **The fixture.** Values coinciding by accident — two id counters running in step, a
   subject's name also appearing in a path an assertion reads, or the setup having
   already produced the exact state the assertion looks for. Force the values apart and
   ASSERT they differ.
3. **The layer.** Only once the first two are clean: is this guard independently
   reachable at all? If it is, push the fixture into the state that reaches it. If it is
   not, it is error handling rather than a layer — test it where it IS reachable (call
   the helper directly) and write that reason into the test, rather than building a
   fixture that pretends an unreachable path can be driven. If the layer below already
   guarantees the outcome by construction (read the source lines that do it), the
   new guard is dead code: delete it, keep the test that pins the behaviour, and name
   the lines that make it redundant in the report.

**The same minimum checked twice is one gate too many.** When a count is gated before a
step that can only shrink the set (single-subject inputs >= MIN, then their subset core >= MIN),
breaking the first check changes nothing: the second catches it. Delete the earlier
check, keep the last one, and re-point the sabotage there. Confirm the step it
guarded copes with tiny inputs (0, 1, 2 items) first.

**An equivalent change is not a miss.** When the sabotaged step is redone a few lines
later by construction (ids deduped, then gathered into a dict keyed by the same id),
the sabotage cannot change behaviour. Name the line that redoes it, drop the case
from the gate, and report it as "dropped, equivalent". Same for "create the parent
before the check" inside a write path that rolls back on any refusal: the rollback
erases the early create, so replace the case with one that breaks the check's INPUT
(wrong item index, wrong key) instead. Do not write a test for a
behaviour that cannot change, and do not count it as a gap.

## Fixture rules that stop a vacuous pass

- **Keep the names out of the paths.** If an assertion about a name can pass on a
  filename or a folder name, it is not testing the name. Assert inside the fixture that
  no subject's name appears in any path it builds — it catches the agent's own careless
  filenames too.
- **Delete what the SETUP produced before asserting the SUBJECT produced it.** When the
  setup step already wrote the file, row or folder the assertion looks for, the assertion
  passes with the feature entirely disabled.
- **A refusal test's input must be valid in every respect except the guarded one.**
  This holds for each entry of a refused-values list too. When a key is renamed, the
  old key's test value must be one the NEW key's range accepts (`name_size 3`, not
  `name_size 300`), or the range check refuses it and deleting the key check stays
  green. A path that does not exist is the same trap: an "only listed items" check
  stays green with the allow-list deleted when the item behind it fails `is_file()`
  anyway, so point every listed item at a real file in that test. A fake file (`b"x"` named `.jpg`) makes a thumbnail/path guard test return None
  whether or not the guard exists, because decoding fails first. Use a real decodable
  input (e.g. `cv2.imwrite` of a small array) and assert the SAME input succeeds from an
  allowed location, so only the guard can explain the refusal.
- **A hazard test must assert that the hazard was actually set up.** Write the
  precondition as an assertion before the act (`assert reused_id == shown_id`), or a
  wrong setup produces a green test that never met the trap. Example: SQLite hands out
  `max(rowid)+1`, so only the LAST deleted row's id comes back. Deleting an earlier
  row never recreates the collision.
- **Give every fake file unique bytes once anything dedupes by content.** A helper
  writing one identical image for every "input" turns all of them into copies of each
  other. A sha256 dedupe then correctly drops them, and old tests fail for a reason
  that has nothing to do with what they test. Derive a few pixels from the path
  (`sha256(str(path))`) so each file stands for a different input. When a NEW content
  rule turns old tests red, read each one's intent before touching code: a test that
  meant "another item" gets its own bytes (fixture fix, named in the report); a test
  that meant "the same item arrives again" is a behaviour the new rule really changes,
  so report it to the owner as a decision instead of quietly re-pointing it.
- **A "this command only reads" assertion on a SQLite file's size and mtime needs the
  earlier writers closed first.** A connection that is never closed gets closed
  whenever Python collects it, and that close checkpoints the WAL into the main file.
  It can land in the middle of the read-only command, and the test then blames it.
  Call `gc.collect()` (or close the setup's connection) before measuring "before",
  and open the read-only side with `?mode=ro` and close it explicitly.
  Even a `mode=ro` reader on a WAL database creates EMPTY `-wal` / `-shm` side files.
  Snapshot the WAL as its bytes with missing == `b""`, and leave the two side-file
  names out of the data-dir file list; content written into the WAL still shows up.
  Otherwise the test goes red only in a full-suite run, where file order decides
  whether the side files already existed.
- **Prove "the plan only reads" on an OLDER-version store, not a current one.**
  Swapping the read-only open for the normal writable connect is silent on a current
  database: a no-op writable open writes no bytes, so the file hash and mtime stay
  equal and the sabotage is missed. On a store stamped one version back, a writable
  open runs the upgrade (version bump, backup file beside it), so the owner asserts
  the stamp unchanged and no backup file. Stamp it back with a raw `UPDATE meta` in the
  fixture.
- **Feed `True` and a float to any "must be an integer id" guard.** `int(True) == 1`
  and `int(0.9) == 0` both hit real ids, while text like `"0; x"` already fails inside
  `int()`, so a test using only junk text stays green with the type check deleted.
- **Add one extra entity nobody acts on**, so "it picked the right two" cannot pass by
  there being only two.
- **For a capped selection (best N), place the outsider FIRST in the order the
  selection walks** (file order, path sort). Otherwise the cap fills with good items
  before it reaches the outsider, and deleting the "never an outsider" rule stays
  green. Add a test with fewer qualifying items than N plus non-qualifying ones
  present, asserting the result is short rather than padded, and one under the
  minimum asserting nothing is written even with `--apply`.
  At the cap itself (exactly N), a fixture of N identical good items makes `<= N`
  and `< N` equivalent: both branches return the same N. Put one item the
  over-cap branch would DROP (an outsider) among the N and assert it is kept, so
  the off-by-one sabotage goes red.
- **An edge case is only a test if the wrong code answers it differently.** For a
  picked case (a rounding pair, a tie, a boundary count), freeze the WRONG variant
  in the test too and select the case where wrong != right, else
  `pytest.fail("test is blind")`. The first case a search finds usually does not
  separate them, and only a sabotage pass shows it.
- **Put an excluded item where excluding it changes the answer.** If the skipped folder
  comes LAST, numbering over all folders and numbering over the scanned ones both give
  "1 of 1" for the first, and a sabotage of the numbering stays green. Place the skipped
  item first (or in the middle), so every later index shifts when the exclusion is lost.
- **Assert the ids or counters differ** wherever two of them must not be confused.
- **A scan that finds nothing must fail.** A test that collects items from a document
  or tree with a regex (`every command the doc names exists`) passes vacuously when the
  regex matches zero items — the set is empty and `empty <= real` is true. Assert the
  collection is non-empty first; the wrong regex is then a red test instead of a green
  lie. The same applies to a leak-shape ban: prove it fires on a planted violation.
- **Feed a normaliser input that is NOT already in its normal form.** A test for a
  case-blind lookup that folds with `lower()`/`normcase` passes with the fold deleted
  when the query is already in folded form. Use a query that differs from BOTH the
  stored value and the fold's output (`ALICE` against a folder `Alice`), and branch the
  expectation on the platform's own rule (`os.path.normcase("A") == os.path.normcase("a")`).
- **A typed-number ban needs a leading anchor.** Banning a hand-typed limit in UI
  source with `[<>]=? ?3\b` matches unrelated text (`<h3`, ids); anchor it on
  whitespace (`\s[<>]=? ?3\b`). Pair the ban with the positive test: every
  `LIM.x` / `data-lim="x"` the page reads exists in the bridge's `limits()`
  (non-empty set, subset check), and sabotage by restoring one old constant.
- **Word boundaries after a digit leak alphanumeric suffixes.** `gpt-?\d\b` does not
  match `gpt-4o`, `phi-3.5` or `v2b` — there is no boundary between `4` and `o`. End
  such shapes with `\d[\w.-]*` and plant the suffixed form in the sabotage.
- **When a fixture encodes an identity into media that passes through a lossy codec**
  (frame index as a pixel value, a marker in audio), use a step wide enough that codec
  noise cannot flip it — a step of 4 came back off by three through mp4v; 8 held — and
  decode the value from the real output, so "frame N was sampled" is asserted against
  the decoded bytes and not against the sampler's own counter.

## One conjunct, one test

A guard of the form `A and B` (same size AND same mtime, right owner AND not expired)
needs a test per conjunct, each changing ONLY that one input. A test that changes both
at once passes with either half deleted — sabotaging `B` alone is silent because `A`
still catches the fixture. Build the second fixture by restoring the other input to its
old value (`os.utime` back, same bytes with a bumped mtime) and assert the inputs really
differ in only one dimension.

## Wording is a guard too

When a change fixes words that users see, the old word coming back is a real
regression, and nothing else will catch it. Give each surface its own test, and have
that test assert the new word is present AND the old one is absent: the new word alone
can pass while the old one is still printed next to it. To sabotage, revert only that
one surface's wording and check that only its own test fails.

**A banned-words guard must read what the user sees, with exceptions listed by
name.** Filtering source literals by shape ("has a space", "starts uppercase")
hides single lowercase words the UI really shows. List the known non-visible
literals explicitly instead; recipe in skill `product-consistency-review`,
`references/wording-sweep.md`.

**A "leave it as it is" decision by the owner is a guard too.** When the owner decides one part
stays out of a change (e.g. it stays bright when everything else greys), the next
broad edit will sweep it in, and nothing fails. Give the exclusion its own negative
assertion beside the positive one. Sabotage it by applying the change to the
excluded part, and the test must go red.

**When the owner reverses a decision a test pins, rewrite the test to pin the new one.**
Don't delete the test. Keep the part of the old decision that still holds as a
refusal (other flags still refused), add the newly allowed case, and give both
decisions in the docstring. That way the next change has to cross both decisions.

**A guard spanning layers must stay green on a one-layer commit.** When a feature
lands as separate commits (CLI, back end, page), a cross-layer guard (every background
job has a page handler) goes red on the back-end commit. Add the smallest real stub in
the next layer, in the exact form the guard's pattern reads (one `onTask.x = handler`
line each, not a loop the regex can't see), and report that the next step replaces it.

**A constant defined before anything uses it** (an answer kind that the gate will only
accept a few steps later) has no behaviour yet to exercise. Add it to the checker's
list of required names, and add a sabotage that renames it, in the same step. Otherwise
the later steps of the phase can rename or drop it and every gate stays green.

## A negative assertion must name a string the passing output cannot contain

`assert "looks like" not in label` fails on the correct output when the correct
wording is "nothing registered looks like this item" — the banned phrase is a substring
of the allowed one. Ban the SPECIFIC leak (the exact name + score the bug would print)
and pair it with a positive assertion on the wording that must appear instead. When a
new negative test goes red on unsabotaged code, suspect the assertion's substring
before the code.

## Filter an enum by the good list, not a blacklist

A guard written as `verdict is not UNKNOWN` lets every OTHER member through, including
ones nobody thought about — a second low-confidence member leaks past it. Write the rule
as the named set of members that ARE allowed (`in {CONFIDENT, REVIEW}`), sabotage it by
turning it back into a blacklist (`set(Enum) - {X}`), and have the owning test feed a
member the blacklist would have missed.

## An absence needs a ban, not a claim

A positive-pattern claim in a consistency checker (`this regex must be present`) can
prove that code exists; it cannot prove that something never happens (a frame is never
written, a secret is never logged). Sabotaging by ADDING the forbidden call leaves the
positive pattern intact and the checker green. Encode absences as a forbidden-pattern
ban over the source tree, then sabotage by inserting the banned call and watch the ban's
own message fire.

The same holds for "only when" rules (load only when on screen, ask only after a click).
A test that checks the call sits in the right handler stays green when an EAGER copy is
added beside it. Also assert the call is absent where it must not be (the loop that
builds the items), and sabotage by adding the eager call there.

## Freeze time-derived ids in the fixture

An id built from the clock (a run id accurate to the second) collides only when two
operations land in the same tick — which tests never do by accident and a scripted real
run does every time. Monkeypatch the id source to a constant in the test that owns the
uniqueness guard, drive both operations, then assert the first one's record still
exists. Without the frozen clock the guard's absence is silent and the test is
decoration.

## Two commands, one filter

When a second command must accept exactly what an existing one accepts (a picker
choosing inputs a later command will consume), extract the existing inline rule into
one pure function returning `(reason, item)` and make BOTH call it, before writing the
new command. Two copies drift, and the picker then produces inputs the consumer refuses.
One sabotage on the shared function must fire an owner in each command's tests; give
each consumer-specific use (which reasons it accepts) its own case.

**A data rule found on one write path applies to every path that writes that record.**
When an experiment shows one entry point writing a bad record (a folder import assigning
record B an item that is A's), grep every writer of that table before building (CLI
batch, CLI by-id, the window's action) and expect at least one with NO check at all.
Put the rule in one function they all call, give each path its own refusal test plus a
test for the case the rule must still allow (the OTHER item of a multi-item input), and add
a structural test that counts the definition (1) and its call sites (N), so a new path
that skips it, or a second copy, goes red. Define "same thing" by content plus position
(`sha256` + `item_index`), never by row id: a byte copy at another path has a new id.

**A plan over several groups must remember what the run itself will create.** The plan
writes nothing, so when group 1 will learn an item that group 2 then duplicates, a
database lookup in group 2's plan sees nothing and promises what `--apply` will refuse.
Keep an in-run map (key -> first owner) checked after the database, and test that the
plan's lists equal the apply's lists on that exact two-group input.

**"Choose the way X chooses" means X's predicate, unwidened.** A new selection (best N
of a group) that reuses an existing rule must not add a fallback or top-up that admits
items the original rule refuses, even when the original leaves the set short or empty.
A short set stays short; an empty one surfaces X's own refusal (same status code, same
wording, reused from X's constant, never copied). Keep ONE definition of "an input
that qualifies" across every entry point, because two rules drift and nobody can say
which one a record was made under. If the measured result looks bad, report it; do not
widen.

## Two layers over one thing

Where two guards both protect one outcome, a single end-to-end test passes with either
one deleted. That is the intent of defence in depth, and it makes the headline test
useless as proof. Each layer needs its own test, and which test owns which layer goes in
the test's docstring. A sabotage on the second layer that changes nothing is a
reachability question, not a redundancy verdict.

**When one sabotage is MISSED and two safeguards block the same outcome, sabotage each
alone and then both together, in a small throwaway script restoring in a `finally`.**
Example: a validated reader that loops only over known keys AND rejects unknown keys in
the value check. Alone each stays green; together the owner must go red. Report it as
"doubly covered: either alone green, both red", never as a miss and never as a
redundant test. If both-together is also green, the owner is the problem.
To make it permanent, give the harness's test-owned cases an opt-in extra-edits
field (more (find, replace) pairs in the same file, all applied, each checked as
found) so ONE case breaks both layers; one edit per case stays the default.

**For a wrapper in front of a guarded command (a UI Api over a CLI), assert the wrapper
refused BEFORE calling through.** "Nothing moved" and "ok is False" both stay true when
the wrapper's check is deleted, because the command below refuses the same input, so a
first sabotage pass comes back mostly MISSED. Spy on the one function the wrapper uses
to reach the lower layer (monkeypatch it to record calls, then delegate), clear the
record before the refused call, and assert it is empty. Add one input only the wrapper
refuses (an item that appeared after the wrapper listed its queue) so the test cannot
pass on the lower layer at all.

**Undoing a create that also made the parent needs a different path, plus a check.**
Removing the new children one by one gets refused when the store won't leave a parent
empty (a record with no reference). So undo then deletes the parent, but only while it
holds exactly the ids just created. If it gained anything since, refuse, or the undo
deletes work it never made. The owners: the known-parent path, the new-parent path,
the grown-parent refusal (nothing removed), the plan removes nothing, undo runs once.

**A new reversible action can reuse the existing journal format.** When an action
that moves nothing (learning a reference) must become undoable like one that
moves files, write the same journal file with a `kind` field and an empty `moves`
list. Old readers (list runs, history) then keep working unchanged, and the undo
command dispatches on `kind`. Owners: the undo restores the count, runs once
(`undone_at` refusal), refuses when the target gained work since, and the plan
without `--apply` changes nothing.

**A two-step confirm across a UI must re-identify the target by content, not by id.**
Between the first click and the second, the id the page shows can be reused (rowids)
or its content changed (an upsert on the same id). Have the page send back what it
SHOWED (names, owner), re-read the lower layer's own plan at confirm time, and refuse
unless they still match. Give three tests: the id reused for other content, the content
changed on the same id, and the target already gone. Each must assert that nothing was
removed.

## A moving check count is not evidence

When a project has a mechanical consistency checker with a claim count, the count rising
is not proof a detector was added — most checkers run several markers per file, so
adding a test file moves the number on its own. State how many of the delta were real
detectors, and verify each new one by breaking the code and watching **its own claim**
named in the failure output.

A mechanical checker proves **consistency, not coverage**: it can be fully green while a
decision page sits two phases out of date. When closing a step, ask which document
*should* mention this, not only which one contradicts it.

## Spikes that feed a guard

**A defect known only by a vague line is hunted, never guessed.** When no record holds
the details, say so, then (if the owner chooses the experiment) write one throwaway script
per item in scratch on the project's fake data, never real data or the live store:

- **Reach the suspect branch and count it in the output.** An entity filtered out
  early (too few items) gives "same answer" for a reason that proves nothing.
- **Measure harm with altered inputs** (mirrored, cropped, darkened copies). The
  reference inputs themselves match at a trivial 1.0 and hide any effect.
- **Check the roadmap for a known, accepted behaviour** before calling something new;
  if listed, name it as out of scope.
- **Write each item as newly found** (today's behaviour, repro, wanted behaviour, fix
  shape); an item that does not break gets one line so it can be closed. Stop before
  coding.

**A sibling defect found mid-fix stays outside the fix.** When building an approved fix
shows the same flaw on a path the go did not name (sort fixed, a manual-filing command
with the same hole), do not widen the change: name it in the report and the findings
file as a later decision.

When a spike measures the behaviour a guard will rely on, give **each question its own
fixture, built by the same function** — two questions sharing one database or server
means question two can pass on state question one just mutated, and the spike then
certifies a fact it manufactured itself.

Drive the pieces through the **real entry point**, not by hand-feeding the values you
expect. A spike that passes ids straight into a lookup proves the lookup; one that goes
through the function the production path calls proves the chain, which is where the
wrong assumption lives. Write down the design calls the spike is testing before it runs,
and say out loud which ones it killed — a spike that confirms the plan every time is
being read to agree rather than to measure.

**A guard built to catch a measured failure must be run on that exact measured case**,
with real inputs, before it counts as done. Synthetic tests written from the shape do
not count. The shape's threshold can sit right on the property that caused the failure,
for example "5+ inputs" when the trap happened because the other record had 4. If the
guard misses, change the number, pin the measured case as its own test, and report the
change and its reason for approval.
