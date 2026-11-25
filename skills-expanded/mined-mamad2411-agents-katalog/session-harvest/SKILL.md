---
name: session-harvest
description: "Use when invoked explicitly as /session-harvest, or when the user asks what's worth saving before compacting/ending a session, or says something like 'harvest this session', 'anything to remember here', 'anything dangling before I stop', or 'is it safe to compact'. Reviews the conversation for anything worth keeping and routes each item to a plain file every agent can read: plan-specific content to plans/*.md (per the plan-docs skill), repo-specific durable knowledge to that repo's AGENTS.md/docs/contributing, and cross-repo/personal preference to ~/AGENTS.md. Never a harness's own memory store, for any project or any reason — that vendor-locks the work. Then sweeps live state the conversation can't show: processes the session left running, unpushed commits in every repo it touched, CI on what it pushed, and work it promised but never verified. Ends with a report ordered least- to most-urgent and a safe-to-compact verdict. On-demand only — never installs hooks or runs automatically."
---

# Session harvest

Reviews a conversation for what's worth persisting before it's compacted or ends, and makes sure
each candidate lands in the _right_ place — not just memory by default because memory is the easiest
tool at hand. Primary invocation is explicit (`/session-harvest`); the description above also
matches natural-language phrasing, but explicit invocation is the one to rely on — description
matching for something this consequential (it writes files) has been reported unreliable by prior
art (see `references/rationale.md`).

On-demand only. Installing hooks, wiring `settings.json`, or running on any schedule is explicitly
out of scope — that's a different, heavier tool (see `references/rationale.md` for the prior art
considered and rejected).

## Procedure

0. **Check the copy you are running is the current one.** The running skill is a file copy dropped
   at install time, so a harvest can silently execute a version older than the source — skipping
   exactly the checks most recently added, and reporting a clean run because it never looked. Diff
   the installed copy against the checkout before starting
   (`diff -q ~/.agents/skills/session-harvest/SKILL.md <checkout>/skills/session-harvest/SKILL.md`),
   and do the same for any other skill this run leans on. If they differ, say so and offer to
   re-install first; a stale harvest is worse than no harvest, because its report reads identical.
   Added 2026-08-29 after the user asked for a harvest "with the latest versions" — behaviour the
   skill did not have, and could not have confirmed if asked.

1. **Significance test first.** Re-read the conversation for candidates. For each one, before
   anything else: _if this were lost, would a future session go wrong?_ Anything that fails this is
   dropped (optionally noted in the report as "considered, not worth persisting"), not proposed.
   This is the actual noise filter — apply it upstream of routing, not after.

   **Then, for anything shaped like a convention — "always do X", "never do Y" — check it is
   actually true before proposing it.** Every filter below assumes the candidate is correct and only
   decides where it goes. A convention inferred from what this session happened to do, or from a
   sample of one or two sibling repos, is a hypothesis: check it against the tool's own
   documentation and real community practice first, and say which you checked. Losing a candidate
   costs one rediscovery; writing a wrong one into a shared doc costs every future reader, and the
   shared doc is exactly where nobody re-derives it. Confirmed 2026-08-27: a harvest proposed
   recording "don't make `tests/` a package" from two sibling repos that happen not to — pytest's
   own docs say the opposite for the default `prepend` import mode ("highly recommended to arrange
   your test modules as packages"), and the session had actually backed out of `__init__.py` to
   satisfy a shared type-checker config. The true finding was a different claim with a different
   destination, and only the user pushing back surfaced it.

2. **Routing filters**, for what survives the significance test:
   - **Plan-specific content → `plans/*.md`, never memory.** If the session touched or produced work
     that the `plan-docs` skill would track — a design, an idea, in-progress implementation — it
     does not get a memory entry. Check whether the relevant `plans/YYYY-MM-DD-*.md` already
     captures it; if the repo uses `plan-docs` and it doesn't, say so and offer to create/update the
     plan file instead of saving to memory. Memory has no retirement mechanism, so a plan snapshot
     parked there would just rot silently — `plans/` already owns that lifecycle. **If a plan file
     already exists but its `status` is now stale** (e.g. `planned`/`in-progress` when the session
     just finished landing and verifying the work), invoke the `plan-docs` skill directly to apply
     its own status-bump/retirement procedure — don't improvise an `AskUserQuestion` about whether
     to retire it. Confirmed as friction 2026-08-23: asked the user a retirement judgment call that
     `plan-docs`'s own "Retiring a plan" section already answers (default: preserve unless the
     rationale is already covered elsewhere in the repo); the user's correction was "why isn't the
     plan docs skill kicking in?"
   - **Repo-specific durable knowledge → `AGENTS.md`/`docs/`/`contributing/`, never memory.** Use
     this split, not a flat "put it in AGENTS.md":
     - `AGENTS.md` (or equivalent instructions file) — only operating instructions an agent needs on
       _every_ task in that repo (commands, conventions, gotchas that change behavior). Keep it
       minimal: it's loaded into every session unconditionally, so this is the actual
       bloat-avoidance lever, not a place to write everything learned.
     - `docs/*.md` — usage-facing reference material, linked from `AGENTS.md`, read on demand.
     - `contributing/*.md` (or a skill's own `references/*.md`, if the knowledge is about a skill
       itself rather than the repo) — design rationale, prior art, implementation gotchas, also on
       demand.
   - **Cross-repo/personal preference (not tied to one project) → `~/AGENTS.md`, never memory
     either.** Same logic as the repo-specific split above, one level up — version-controlled via
     its real source. If `~/AGENTS.md` is generated (assembled from fragments, deployed by a dotfile
     manager, symlinked out of a repo), find and edit that source; a deployed file is silently
     overwritten on the next run, so an edit there is lost and reaches no other machine. On this
     author's machine it is assembled from fragments under
     `power-user-linux-setup/config/agents-md/`, whose `README.md` says which fragment owns what.
     **Read the canonical source before drafting an addition — the deployed copy loaded into a
     session's context can be structurally stale against it.** Confirmed 2026-08-24: a session held
     a ~20 flat-section `~/AGENTS.md` while the source had been restructured to 7 clustered ones, so
     an addition drafted against the section names in context would have targeted headings that no
     longer existed. `grep -n '^## ' <source>` first. Loaded into every session regardless of repo,
     so it's the actual bloat-avoidance-and-reviewability lever for content that isn't tied to one
     project, the same way a repo's own `AGENTS.md` is for that repo. Confirmed as a real gap
     2026-08-22: a session found ~30 `feedback`-type memories accumulated across multiple projects'
     memory folders — each project's memory is invisible to every other project's sessions, so a
     genuinely cross-repo preference saved there never actually reaches a session in a different
     repo. Most had simply never been promoted because nothing routed them anywhere else. **A
     candidate that's a _variant_ of a rule already in `~/AGENTS.md` extends that rule's existing
     section — it doesn't get a new one.** "Already covered → skip" (below) is for an exact
     duplicate; this is the near-miss case, where the principle is written down but this particular
     shape of it isn't. Default to appending a short paragraph to the section that already frames
     it, because that file is loaded into every session in every repo, so a new heading costs
     context everywhere and a reader who sees three instances under one principle generalizes better
     than one holding three unrelated rules. Reach for a new section only when the trigger and the
     detection signal are both genuinely different from anything already there. Resolved 2026-08-23:
     "don't characterize a multi-file diff from one sampled file" was folded into "Verify what
     actually happened, not what output looks like" — which already covered
     clean-stdout-vs-exit-code and test-suite-vs-throwaway-script, both the same "the convenient
     surface signal isn't the real signal" shape.
   - **A skill that already owns the topic beats a new always-loaded rule.** `~/AGENTS.md` is not
     the default home for every cross-repo finding. Whatever document states that file's admission
     criteria is the gate (on this author's machine,
     `power-user-linux-setup/contributing/global-agents-md.md`'s "Admitting a new rule"); where no
     such document exists, the tier test below still applies — a rule whose miss is _silent and
     expensive_ belongs in the always-loaded file, while one with a sharp trigger whose miss is
     _cheap and recoverable_ belongs in a skill. Check the file's current size against its own
     reference points (`grep -c '^### '`, `wc -l`; ≤15 rules / ≤200 lines) before proposing, and say
     the numbers out loud when asking — admission is a real cost once it is over them, and the user
     should decide with that in view. Resolved 2026-08-25: `pgrep -f` matching the harness's own
     `zsh -c … eval` wrapper (a false positive that reads as a real process) went to
     `session-bash-audit` — which already invites newly noticed Bash anti-patterns and can _measure_
     the rate — rather than becoming a 34th rule in a file already at 33 rules / 390 lines. A
     finding that a topic-owning skill can act on is usually better there than restated globally.
     Counter-example, resolved 2026-08-28 the other way: a non-terminating CI-poll loop went to the
     always-loaded file _despite_ it standing at 37 rules / 446 lines, because the tier test is
     decided by the miss, not by the budget — this miss is silent by construction (a loop that
     cannot fail emits nothing, so "still waiting" and "will never finish" look identical) and it
     had already made a session report a result it could never observe. Size pressure argues for a
     skill; it does not overrule "silent and expensive". Two levers keep the cost honest when the
     always-loaded file wins: extend an existing section instead of adding a heading (rule count
     unchanged), and end the rule on the command that replaces the habit rather than on the warning.
     Report the before/after line count either way.
   - **Destination mid-restructure → the plan reshaping it, not the file.** When a candidate's
     correct home is currently the subject of an open `plans/*.md` that is reshaping it — especially
     one that defines its own criteria for what may be added — record the candidate _in that plan_,
     as a `[NEEDS CLARIFICATION: ...]` item stating its trigger, rather than appending to the file.
     Appending bypasses the criteria that plan exists to enforce, risks the addition being
     restructured away unread, and conflicts with whatever session is doing the restructuring.
     Applies to any destination with an open plan owning its shape, not just `~/AGENTS.md`. Resolved
     2026-08-23: two cross-repo rules routed to `~/AGENTS.md` while the (since retired) leanness
     pass was actively cutting it from 30 sections and adding admission rules of its own — now
     permanent in `contributing/global-agents-md.md` ("Admitting a new rule"); both candidates were
     parked in that plan instead of appended, and were decided at its close. **When the destination
     is a _different repo_ that is mid-restructure, the queue is a plan in the current repo carrying
     `depends_on: [<that-repo>]`** — you cannot park a `[NEEDS CLARIFICATION: ...]` in a plan you
     are not in, and holding the candidate in the session is how it is lost. Confirmed 2026-08-29: a
     session produced nine evidence-backed edits owed to two skills in `agent-skills` while that
     repo was undergoing surgery; they went to a `depends_on`-tagged plan in the project that found
     them, with the evidence attached, so the edits can be made in one pass later.
   - **A candidate belonging to another repo is _filed_ there, not queued here.** As of 2026-08-29
     `plan-docs` has `plans.py new <topic> --for <repo>`, which writes the plan into that repo's
     store mirror outside every working tree: no commit crosses, and the session that next works in
     that repo is offered it by `plans.py absorb`. Prefer it over a `depends_on` plan in the current
     repo, which was the workaround before the mechanism existed and leaves the candidate somewhere
     the owning repo never looks. Commit the filed plan in the store immediately — a dirty store
     forces every other session into the add-a-new-file fallback for as long as it lasts.
     `depends_on` keeps its own, different meaning: **this** work cannot land until that repo
     changes, which is a dependency rather than a delivery. Used this way on the run that added it,
     to route two `~/AGENTS.md` corrections to the repo that owns the fragments.
   - **Already covered → skip.** If an existing doc already says this, don't write a duplicate —
     check first.
   - **Meta-conventions about how to build things in this ecosystem (e.g. "skills should do X by
     default") → the relevant existing skill's own docs, not a feedback memory** — even though on
     the surface "how to approach work" sounds like the `feedback` bucket. Resolved via
     `AskUserQuestion` during this skill's own design: a preference about how _new skills_ should be
     authored belongs in `mcp-skill-shipping` (durable, version-controlled, visible to every
     contributor/tool), not this harness's private memory store. Use that as the default for similar
     cases rather than re-asking each time.

3. **There is no memory tier. Every survivor lands in a plain file, and step 2 is the whole of the
   routing.** A harness's own memory store is never a destination — not for durable content, not for
   perishable content, not as a staging area, not "just this once".

   [DECISION: stated by the user 2026-08-29 — no memories, for any harness, for any project, for any
   reason, because project data and user-wide practices must not be vendor-locked. The carve-out is
   harness **configuration** (`settings.json`, hooks, keybindings), which is expected to differ per
   harness because it describes the tool rather than the work. The sorting rule: configuration
   describes the harness; anything describing the work is a plain file any agent can open.]

   **State the ban, not the mechanism.** Earlier versions of this step sent "genuinely temporary"
   survivors to the harness's memory store, and explaining _why_ that store is a poor home is
   precisely what let a session reason its way to an exception — see
   [`references/rationale.md`](references/rationale.md), "Why no memory tier at all".

   If a candidate fits no filter in step 2, that is a signal to add a filter there (step 6's
   self-update) — never a reason to reach for a harness feature. The gap is usually smaller than it
   looks: an `in-progress` plan is already sorted above everything else by `plans.py list`.

4. **Loose-ends pass**, separate from the memory scan: is there in-progress state in _this_
   conversation that isn't memory-worthy (failed step 1) and isn't covered by a plan file either,
   that compaction would still lose track of? Surface it explicitly — recommend a `plans/*.md` entry
   if it's real design/idea work worth resuming, or say plainly that it's fine to let go if it's
   genuinely ephemeral task state.

   **Read the conversation, not only the summary.** A compacted session hands you someone else's
   précis: intermediate summaries drop exactly the loose ends this step exists to catch, and their
   confident tone reads as completeness. Extract the real user turns from the session transcript
   (`~/.claude/projects/<slugged-cwd>/<session-id>.jsonl`, `type == "user"` entries with real text
   content — a few dozen lines of Python, and typically under ten turns even in a long session) and
   re-read the original instructions rather than the recap of them. Confirmed 2026-08-28: the
   brief's own "this needs a full tier run afterwards, only one common cause was established"
   survived into no summary, and neither did an explicitly-declined consumer sweep.

5. **Live-state sweep** — the parts of "dangling" that are not in the conversation at all. The
   transcript says what was _intended_; these say what is actually true now. Run them even when the
   session felt tidy, because every one of them has been wrong at least once:
   - **Processes this session started.** Backgrounded polls and watchers outlive the turn that
     spawned them. Check for live children (`ps -o pid,stat,etimes,args`, and whether a `sleep`
     child was respawned seconds ago — that is the difference between hung and still-working).
     Confirmed 2026-08-28: four CI-poll loops, 36 hours old, still polling, whose exit condition
     could never be true; the harvest was the only thing that would ever have found them.
   - **Git state, every repo the session touched** — not just the primary one. Dirty tree, unpushed
     commits (`git log origin/<branch>..HEAD`), and whether the remote moved under you. An unpushed
     commit is the most common real loose end, and a session that ends with one usually believes it
     pushed. **Check that the `git fetch` actually succeeded before trusting either answer**: on
     this machine a fetch needs the Zenity SSH-passphrase dialog, which fails with
     `Permission denied (publickey)` when nobody is at the keyboard — and a failed fetch leaves
     `origin/<branch>` exactly where it was, so the ahead-count still prints a plausible number
     computed against a stale ref. Same silent-by-construction shape as the CI loop above: the wrong
     answer and the right one are indistinguishable. Read the fetch's exit code, and when it failed
     say how old the ref is (`git log -1 --format=%cr origin/<branch>`) rather than reporting the
     count flat. Run the fetch on its own, unpiped: `git fetch origin 2>&1 | tail -3; echo $?`
     reports `tail`'s exit, not git's, so the very check meant to catch a stale ref reads clean
     while the fetch is failing. Confirmed 2026-08-28, and again 2026-08-29 by this bullet failing
     to prevent it. When it is the empty-agent case, the machine's own diagnostic names the fix
     (`inv ssh.check` on this machine) — do not reach for `ssh-add`, and apply that fix as a
     per-call environment prefix rather than an `export`, which does not survive to the next Bash
     call. **Then check who wrote the unpushed commits before recommending a push.** Where sessions
     run in parallel the ahead-count is not necessarily this session's work, and "you have two
     unpushed commits, push them" publishes another session's unfinished history under a
     recommendation that reads as routine. Name which are this session's and which are not, and let
     the user decide. Confirmed 2026-08-29: two commits from a parallel session appeared in the
     ahead-count between one push and the next, and asking rather than pushing was the only thing
     that surfaced them.
   - **Sibling repos this skill itself wrote to.** A skill self-update (step 6) commits locally and
     reaches nothing until it is pushed and re-installed, so `agent-skills` is a repo the session
     touched and it is the one most likely to be forgotten — the edit felt done when it was
     committed. Check its ahead-count too, and report it with the rest.
   - **Paths this session told other sessions to run.** A rule written into an always-loaded
     instructions file, or a `SKILL.md` command block, names a path on this machine — usually an
     installed copy, not the checkout the session was editing. Run one of them. Confirmed
     2026-08-29: a session deployed a `~/AGENTS.md` rule pointing at
     `~/.agents/skills/<name>/scripts/<file>` while the installed skill still had no `scripts/`
     directory, so a machine-wide rule instructed every future session to run a file that did not
     exist. The checkout worked perfectly throughout, which is why nothing surfaced it.
   - **CI, for anything this session pushed.** A green local gate is not a green CI run. Use a
     bounded waiter (`gh run watch <id> --exit-status`), never a hand-rolled `until` loop. **Do not
     pipe it.** `gh run watch <id> --exit-status | tail -5; echo $?` reports `tail`'s exit, so the
     `--exit-status` flag that exists to turn a red run into a non-zero exit is discarded by the
     very command reading it, and a failed run prints `0`. Run it bare, or read the conclusion as
     data (`gh run view <id> --json status,conclusion`). Same shape as the `git fetch` bullet above,
     and confirmed the same way, 2026-08-29: a harvest reported `WATCH_EXIT=0` from `tail` while
     executing this very checklist. Both bullets now exist because the pipe defeated the check.
   - **Shared stores outside any repo.** `$RESEARCH_HOME` clones, caches, anything the session added
     to a location no `git status` covers. The failure is a half-finished convention rather than a
     missing file — a clone without its `SOURCE.md`, or one that failed partway — and it is
     invisible to every other check here precisely because the store is not version-controlled.
     Cheap to verify (does each new entry exist, and does it carry whatever metadata that store's
     convention requires), and nothing else will.
   - **Work the session promised but never verified** — a test tier it added to but never ran, a
     consumer it changed but never swept. "I'll report when it lands" in the last message is a
     promise the harvest has to either keep or retract.
   - **`depends_on` plans whose blocker may have lifted.** The routing filter above parks work owed
     to a mid-restructure repo in a `depends_on`-tagged plan — which stores it safely and gives it
     no trigger. Nothing watches the named repo, so the queue is discovered only when someone thinks
     to look, and a plan waiting on a repo that has been ready for days is indistinguishable from
     one waiting on a repo that is still busy. Cheap to close: for each `depends_on` plan the
     current repo has, check that repo's tree and recent commits, and report the ones whose blocker
     is gone as ready rather than blocked. Anchor the match — `rg -l '^depends_on:' plans/`, not a
     bare `rg -l 'depends_on'`, which also hits a plan whose body tabulates a data schema having a
     field of that name, and a false positive here reads exactly like a real queue entry. That was
     caught by the "run one of them" rule above, applied to this bullet on the run that added it.
     Confirmed 2026-08-29: nine skill edits parked five hours earlier were already unblocked, and
     were found only because the user asked what plans needed other repos — the harvest that created
     the queue had not scheduled anything to drain it. Verify against the working tree, not the
     plan's prose: the same check that day read "surgery finished" from a clean `git status` and a
     landed plan, then found two modified files a few minutes later. **A clean tree only answers the
     queue case.** The tag carries two meanings — work parked because that repo was mid-restructure
     (this bullet's case, and a deprecated one now that `new --for <repo>` exists), and `plan-docs`'
     own documented meaning, "sibling repos this plan can't fully land without". For the second, the
     named repo being idle says nothing: the blocker is a change that repo has not made yet, and
     only reading the plan answers whether it has. Sort the tagged plans into the two kinds before
     reporting any of them, and report readiness only for the first — "seven plans ready" assembled
     from clean `git status` output is a claim the check never made. Confirmed 2026-08-29: eight
     tagged plans, three sibling repos all clean, and exactly one of the eight was queue-shaped.
   - **Work handed off to another session, and what it blocks here.** This user runs parallel
     sessions, so "another session is doing X, don't touch it" is a routine instruction — and it
     creates state no other check finds: not a process, not git state, not CI, not an unkept
     promise, but a dependency this session is stopped on and deliberately not solving. Name it in
     the report with what it blocks, so the handoff cannot fall between the two sessions. Do **not**
     re-probe the handed-off thing to report its status; that is the instruction being violated one
     call at a time. Confirmed 2026-08-28: a session finished its work, could not push because the
     ssh agent was empty after a reboot, was told another session owned that — and the only
     remaining record of the blocked push was the harvest report.
   - **Whether a finding is already owned, before reporting it as new.** A sweep that reaches back
     through history or across repos surfaces things this session did not cause, and on a machine
     running parallel sessions the likeliest explanation for a real finding is that someone else
     already found it. Check before escalating: the sibling repos' recent commits
     (`git log --oneline -10`) and their open plans. Report an already-owned finding as _confirmed
     still open_ and name the plan that owns it — never as a discovery, and never by acting on it.
     Confirmed 2026-08-29: a confidentiality scan returned 55 hits in published history and was
     minutes from being reported as urgent, when another session had already rewritten both
     histories, force-pushed, opened a support request for the residue, and written all of it into a
     plan. Several probing calls, and nearly a duplicate alarm, for work that was done.

6. **Improve the skill on every run — this is not optional, and not only for friction.** The skill
   is actively dogfooded: each invocation is also a test of it, and the author has said catching and
   fixing issues immediately is the point. So before writing the report, ask explicitly: _did this
   run show the skill to be wrong, incomplete, or unhelpful anywhere?_ Signals, in rough order of
   how often they are missed:
   - The user's invocation supplied behavior the skill lacks (see the third trigger below).
   - A step ran and produced nothing of value, or the run's best finding came from something no step
     asked for. Both mean the procedure is mis-aimed, and the second is the easier to overlook
     because the finding still got made.
   - A step was skipped as inapplicable — was that judgment right, or is the step written too
     narrowly?
   - Anything the user had to say twice, or ask about after the fact.
   - The skill contradicted itself, or an instruction turned out ambiguous when applied.

   Default to editing the source now, not filing it for later; a deferred skill fix is a skill fix
   that does not happen. Keep the change small and additive. If a run genuinely surfaces nothing,
   say so in the report in one line — an explicit "no skill changes needed this run" is the evidence
   the check happened, and it should be the exception rather than the norm while the skill is young.

   **Committing and deploying the skill edit.** Commit it locally without asking — it is reversible,
   reviewable as a diff, and pausing for approval mid-run is what makes the fix get dropped. Pushing
   and re-installing is outward-facing and always asked, because that is the step that changes what
   other sessions and machines load. Confirmed 2026-08-28: `Bash(git commit:*)` and
   `Bash(git push:*)` are both allowlisted on this machine, so no permission prompt guards either —
   the discipline is entirely instruction-side, deliberately (see `~/AGENTS.md`, "Proposing an
   enforcement mechanism for agent behavior"). Do not read the absence of a prompt as permission.

7. **On friction, ask — then self-update the skill, not just this session.** Three triggers:
   - A candidate doesn't clearly fit any routing filter in step 2 (e.g. arguably both plan-specific
     _and_ a durable cross-repo preference), or the significance test itself is a genuine toss-up.
   - The user corrects a routing decision this skill just made.
   - **The user's own invocation asks for behavior this skill doesn't have.** Arguments like "make
     sure you also check X, not sure the skill does that today" are a spec, not a one-off request.
     Applying them to the current run and stopping there is the failure this step exists to prevent
     — and it is easy to miss, because the run itself goes well. Confirmed 2026-08-28: every
     live-state check in step 5 arrived that way, was executed, produced the session's most valuable
     findings, and was nearly lost because nothing prompted writing it down. If the user has to ask
     "did you update the skill?", this trigger already fired and was missed.

   In the first two cases use `AskUserQuestion` to resolve it for _this_ item — never silently pick
   a side on a real ambiguity. In the third the user has already told you what they want; just fold
   it in. Either way the resolution goes back into this skill's source (see below) so the same
   friction doesn't recur. Resolving it for one session only defeats the point of a shared
   convention skill.

   **Do the fold-back before the final report**, not after — which is why both skill steps sit ahead
   of it — and say in that report which destination was updated (this skill's source, or the
   always-loaded instructions file). A harvest whose whole subject is "what would be lost" should
   not end by losing its own lesson.

8. **Harvest report**, last, and ordered so the reader can stop early only at their own risk: least
   urgent first, most urgent last, because the final lines are what a skimmed report actually
   retains.
   - **Settled** — verified green/clean, no action. Say what was checked, so "fine" is a measurement
     and not an impression.
   - **Persisted this pass** — routine routings as one-liners (memory / plan / docs / dropped), plus
     any cost worth naming, e.g. what an addition did to an always-loaded file's size.
   - **Skill changes** — what step 6 changed, or one line saying it found nothing.
   - **Decisions waiting** — documented, not urgent. Name plans that must be decided _together_.
   - **Risks carried** — known and written down. For each, the falsifier: what observation would
     show the reasoning was wrong.
   - **Needs action now** — dangling state, and anything the user alone can decide (a push, a
     re-install, a destructive cleanup). Last, and specific.
   - Ends with a one-line verdict: "safe to compact" or "not yet — needs a decision on X."

   Fix what is cheap and unambiguous rather than only reporting it — kill the orphaned loops, write
   the lost measurement into the plan that owns it — and report it as done. Reserve the report's
   last zone for what genuinely needs the user. Anything outward-facing (a push) still gets asked.

Everything this harvest writes into a repo — a `plans/*.md` entry, an `AGENTS.md` addition, a
`docs/`/`contributing/` page, a skill's own source — goes through that repo's quality gate
(`inv quality.precommit`, or the repo's equivalent) before committing, same as code. Markdown is not
exempt: dprint reformats prose line-wrapping, and doc-only commits that skipped the gate were the
one recurring CI-failure cause across these repos (confirmed 2026-08-23).

## Self-update mechanics

Resolving friction (steps 6–7) means editing the skill's _source_, not whatever copy is in front of
the current session:

- The running copy — `~/.agents/skills/session-harvest/` (or a project-local
  `.agents/skills/session-harvest/`) — is a plain file copy dropped there at install time.
  Hand-editing it is silently clobbered by the next install and never reaches any other project or
  machine anyway. Never edit it directly.
- Find the canonical source: the [`agent-skills`](https://github.com/TheodoreAD/agent-skills) repo,
  normally at `~/projects/github.com-personal/agent-skills`. If that isn't obviously reachable from
  the current session (invoked from an unrelated project), locate it (e.g.
  `fd -td agent-skills ~/projects -d 4`), clone it, or ask the user for its path — don't guess or
  silently skip the update.
- Edit `skills/session-harvest/SKILL.md` there: a small, additive change — a new bullet under the
  relevant routing filter, or a note under "On friction, ask" if the friction was about the
  escalation process itself. Not a rewrite. Rationale for _why_ a resolution was made a particular
  way goes in `references/rationale.md` instead, matching the split already used for the rest of
  this skill.
- Run that repo's quality gate, then commit — locally, without asking, per step 7. Its own
  `tests/unit/test_skill_layout.py` is part of that gate and enforces real limits (the description
  cap among them), so run it rather than eyeballing the frontmatter. Then tell the user what
  changed.
- **Say plainly that a committed edit still reaches nothing.** The installer clones from the remote,
  so the change takes effect only once it is pushed _and_ re-installed
  (`npx skills add TheodoreAD/agent-skills --skill session-harvest`) — including for other projects
  on the same machine, whose `~/.agents/skills/` copy is now stale against the source. Ask before
  that step, and verify afterwards by diffing the installed copy against the source rather than
  trusting the installer's output.

## Full rationale

[`references/rationale.md`](references/rationale.md) has the prior-art survey (why this isn't a
`PreCompact` hook, what was borrowed from `learning-loop-skill` and what was deliberately left out,
why plan-specific content is excluded from memory even though it's tempting mid-session) and the
reasoning behind the self-update mechanism.
