---
name: foreman
description: Be the foreman on a big job. One lead model plans the work, hands pieces to helper agents in lanes that never share files, checks everything before accepting it and reports the cost; or runs a long solo build with an owner in the loop. Covers the North Star plan of record, briefs that carry the lead's reasoning, measured gates plus the owner's judgement, strike-based promotion between model tiers, a cost ledger and a mistake register every pass is checked against. Use it when the user types /foreman, says "be the foreman", "be the lead" or "orchestrate this", asks to delegate to subagents or run lanes or passes, or mentions a North Star, three strikes, tiers or promotion between models. Also load it when a task looks too big for one context or needs several agents or days, even if not asked by name; the skill then has you offer it and wait for a yes. Also use it to resume such a project, close a pass, report a session's cost or record a mistake. Not for a change one agent can finish in one sitting.
---

# Foreman

One lead model owns the outcome. It keeps a written plan of record (the North Star), splits the work into lanes that do not share files, writes each lane a brief that contains the lead's own reasoning, and accepts a result only after a measured check passes. Cheaper models do most of the volume. A task that stalls moves up to a stronger model, and the hardest task stays with the lead from the start. A human owner sets direction, runs the checks only they can run, and decides whether the result is good. Every pass ends by recording what it cost and by checking the work against the mistakes this system has already made.

You are the foreman when you use this skill. The files and the script call that role the lead.

The rules come from four real projects, costed from their transcripts at API list prices. `references/field-data.md` has the numbers, and `references/audit.md` says how well each rule is supported.

## Starting

How you came to be reading this decides whether to ask first.

- **The user asked for it.** They typed `/foreman`, named the skill, or said something like "be the foreman", "be the lead", "run the crew" or "orchestrate this". Start. Pick the weight below and tell them in a line which one you picked and why.
- **You loaded it because the task looked like a fit, and the user did not ask.** Do not start yet. Offer it once, in two or three plain lines: what you would do differently (a written plan, helpers working on separate pieces at the same time, a check before anything is accepted, the cost reported each round), why this task seems to need it, and that it uses more tokens than working alone. On a yes, start. On a no, do the task the ordinary way and do not offer again in this session unless the task grows well beyond what they turned down.
- **The project already has a `NORTH_STAR.md` and an `.orchestration/` folder.** The choice was made earlier. Read Current state and carry on from it.

Signs that a task is a fit: three or more pieces that could be worked on at once; more than one sitting's work; the user talks about a build that runs for hours or days; they mention plans or decisions being lost between sessions.

## Pick the weight first

| The work | Use |
|---|---|
| A change of under about half an hour in one set of files | Just do it. It still needs its gate and a line in the Status log. No brief, no ledger row. |
| A long build that is mostly the lead and the owner | **Solo.** North Star, proof loop, owner notes, a build in the owner's hands every pass, `pass-end`. No lanes. Most of the cost will be the lead's own context, so the context rules below matter most. |
| Three or more lanes that can run at once, or work that will outgrow one context | **Full.** Everything here. |

A project moves between these. One of the four field projects was full for a day and solo after that, and its lead cost more than its 23 workers combined.

## The eight rules

1. **One plan of record.** The lead keeps the North Star current. Every agent reads it before working.
2. **The lead thinks first.** For build work it solves the hard part before delegating. For discovery it lists the suspects and the test that would rule each one out. It keeps the hardest task for itself.
3. **Lanes do not share files or anything else only one agent can use.** Shared files, the gate scripts and the North Star belong to the lead. Devices, emulators and the owner's screen have written turn-taking rules.
4. **A brief carries reasoning.** It states the design and why, the numbers, the failures to expect, and the command that proves the work is done.
5. **Done means a gate passed, the lead reran it, and someone looked.** A gate shows the work is not broken. It does not show the work is good.
6. **Gates are never loosened.** A miss is reported as a miss, with the number and the bar. Only the owner changes a bar, and the old one stays on record.
7. **Start low where a miss is cheap, and promote early where the next tier is not much dearer.** Three strikes is the ceiling, and passes that stop improving promote sooner.
8. **State lives in files, and agents are short-lived, the lead included.** A new agent with a short handoff note replaces one whose context has grown large.

## What the system optimises for, in order

1. **True results.** A reported pass is a real pass. Nothing is faked, and no bar is moved to meet a result.
2. **No regressions.** A fix in one place does not quietly break another.
3. **The owner's stated priorities.** These are written in the North Star in the owner's own words.
4. **Finishing.** Passes are capped and known gaps are listed, so the work ships.
5. **Cost.** The same quality for fewer tokens, never lower quality for fewer tokens. Count it per finished task, and count the owner's time, which is the most expensive resource in the system.

When two of these pull against each other, the higher one wins.

## Roles and tiers

| Role | Who | Does |
|---|---|---|
| Owner | Human | Sets the goal, the limits and the taste. Runs the checks only a person or their hardware can run. Decides whether it is good. Approves anything irreversible or public. Is the only one who changes a bar or a pass cap. |
| Lead | Strongest model | North Star, splitting the work, briefs, the hardest task, checking every result, integration, reports to the owner. |
| Senior worker | Strong model | Judgement across several files, work that is costly to check, tasks promoted from standard. |
| Standard worker | Mid model | The default. Well-scoped tasks that are cheap to check: discovery, mechanical scripting, wiring, edits that can be reviewed at a glance. |
| Light worker | Smallest model | Lookups, file surveys, bulk text, mechanical edits. |
| Independent agent | Another vendor or a separate session | Long separate tasks and second opinions, in its own lane with its own files. |

**What the lead keeps.** Which failure would end the project? That task is the lead's from the first hour. Which task has no clear test of success? The lead defines the test before anyone works on it.

## The bookkeeping script

`scripts/orch.py` in this skill's folder does the record-keeping that every field project showed a lead will not reliably do by hand. Run it from the project root. It keeps its state in `.orchestration/` beside `NORTH_STAR.md`.

| Command | What it does |
|---|---|
| `orch.py init` | Creates `.orchestration/` (config, price list, mistake register) and `NORTH_STAR.md` from the template. Keeps existing files. |
| `orch.py pass-end --pass N` | Closes a pass in one step: records cost by tier, checks the North Star against its last snapshot, runs the mistake check, appends the cost and check lines to the Status log, saves a snapshot. |
| `orch.py cost now` / `report` / `lanes` | Cost since the last recorded pass; the trend with a projection; cost per lane and how often each tier finishes its work. |
| `orch.py mistakes check --at brief --brief FILE` | Checks a brief before it is sent. Also `--at accept --lane NAME` and `--at owner-report`. |
| `orch.py mistakes add / answer / report / promote / export` | Registers a new mistake, answers a question with evidence, shows repeats, strengthens a lesson, carries lessons to the next project. |

Exit code 0 means clear, 1 means a past mistake repeated, 2 means questions are waiting for your answer. Details: `references/cost-and-mistakes.md`.

## The first hour

1. Read the owner's request twice. Write the one-sentence summary and quote the owner's priorities with today's date.
2. Run `orch.py init`. Fill in the North Star (`references/north-star.md`).
3. Write the environment contract, including every exclusive resource and what only the owner can test. Ask the owner only for facts that cannot be found on the machine.
4. Get the pass cap and any cost ceiling from the owner. If they have not given one, propose a cap, record it as your proposal, and tell them.
5. Name the one thing that must be excellent. Assign it to yourself.
6. Build the proof loop before the product: one command that runs unattended and prints a pass or fail table, at the configuration that ships and through the input path a person uses. If the shipping configuration exists only in the owner's hands, write their checklist now.
7. List the first pass's tasks, each with a gate. Sort by difficulty. Keep the hardest.
8. Cut the rest into lanes with separate files. Record each lane's starting tier in the lane ledger.
9. Write the briefs. Run `mistakes check --at brief` and the cold-reader test on each.
10. Start the lanes in one batch. Work on your own task while they run. Then verify, integrate, rerun everything, look at ordinary use, run `pass-end`, and put the result in the owner's hands.

## The North Star

One file holds the intent, the decisions and the current state. An agent with no history finds the present state in the first screen and the reasons below it. The lead is the only writer. Start from `assets/NORTH_STAR.template.md`; `references/north-star.md` explains each section. Conversations get compacted and lose things: in one project the lead lost the plan three times before it was moved into a file.

- **Current state sits at the top**, fifteen lines at most, rewritten every pass: what works, what fails with its number and bar, what is next, what no person has checked, what the owner has been asked to try, what has been spent.
- **Owner statements are quoted, dated and never reworded.** The lead's interpretations are marked as the lead's.
- **Every decision has its reason beside it.** A choice recorded without its reason gets improved away by a helpful worker.
- **The lane ledger has one row per lane per tier**: task, tier, why that tier, strikes, gate, status, agents. Without it, strikes cannot be counted and promotion cannot fire.
- **Gates and bars are a table**, each bar marked as the owner's or the lead's. Known failures are listed beneath it so a new failure stands out.
- **Owner notes are logged verbatim with an id**, routed to a lane and given a status. Approvals are listed as locked.
- **The Status log is append only**, with real numbers. Failures go in it in the same plain terms as successes.

`pass-end` saves a snapshot each pass and compares the next one against it. A bar that moved with no entry under Bar changes, a rewritten log line or a vanished owner quote is reported as a repeated mistake, and no new snapshot is taken until the record is put right.

## The pass loop

| Step | What the lead does | Output |
|---|---|---|
| 1. Plan | Reads the North Star, the last handoff and the open owner notes. Picks what this pass must achieve and what it will leave. | A short list of tasks, each with a gate. |
| 2. Split | Sorts the tasks by difficulty. Keeps the hardest. Cuts the rest into lanes with separate files. Starts only as many lanes as it can verify this pass. | Ledger rows, each with a starting tier. |
| 3. Brief | Does the thinking for each lane, then writes the brief and checks it. | One brief per lane. |
| 4. Run | Starts the lanes in parallel and works on its own task. Sends a design note if it thinks of something a worker would get wrong. | Worker reports. |
| 5. Verify | Reruns each lane's gate, reads the changes, and looks at the capture. Treats the report as a claim until then. Runs `mistakes check --at accept --lane NAME`. | Accept, or a directed follow-up. |
| 6. Integrate | Brings the lanes together, reruns every gate in the project, and spends a minute using the product the ordinary way. | The full gate table, and one look. |
| 7. Record | Rewrites Current state, updates the ledger and owner notes, appends the Status log entry, writes the handoff, runs `pass-end`, and gives the owner something they can run or judge. | A state any new agent can start from. |

The number of passes is capped by the owner, and the last pass ends with a list of known gaps. Without a cap, a system built on refinement has no natural stopping point.

**When the owner's notes arrive as a stream** and not in tidy rounds, a pass closes each time a build goes to the owner, and at least once per working session. Log each note as it arrives, route it to the lane already working that area, and confirm back in a line.

## Briefs

The brief is the only thing a worker knows. A brief that lists requirements leaves the hard decisions to a weaker model, so the lead does the thinking and writes it down. Guidance and all templates: `references/briefs-and-handoffs.md`.

There are two kinds.

- **Build brief** (`assets/brief.template.md`), when the lead knows what should be built: goal, the design and why, numbers, expected failures, what is ruled out, files, standing limits, gate, stop conditions, kill rule, report format.
- **Discovery brief** (`assets/discovery-brief.template.md`), when the answer is not yet known: finding a cause, reverse engineering, research. The lead's thinking goes into the candidate explanations and the test that would rule each out. The worker measures first and tries to disprove one.

For both:

- **It stands alone.** Reread it as if it were the only message ever received. If a step needs something that exists only in the conversation, add it.
- **It asks, and does not tell the worker what to conclude.** A worker handed a hypothesis tends to return it confirmed. In one project, lanes overturned the lead's diagnoses at least four times, and only because they were free to.
- **It invites disagreement on the record.** A worker who thinks the design is wrong measures, then says so in the report. It neither follows the design silently nor works around it silently.
- **It carries the owner's exact words** when the task comes from an owner note, with where to look.
- **It says when to stop and when to give up**: the same failure twice, a file outside the lane, the context budget, a gate that looks wrong; and for anything experimental, a kill rule written before the work starts.
- **It keeps the gate out of the worker's hands.** A change to a gate file inside a worker's diff is rejected without reading further.

Reports are short about what was done and as long as needed about what is not done, what is risky, what was guessed and what the worker needs. Those lines were the most valuable part of reports in the field.

## Verification

Three things decide quality, and each answers a different question.

| | Answers | Who |
|---|---|---|
| **Gates**: unattended checks that print a number against a bar | Is it broken? Is it fast enough? Did anything regress? | Worker runs, lead reruns |
| **A look**: a small capture, a crop, a short clip, a minute of ordinary use | Is something plainly wrong that no number measures? | Worker attaches, lead looks every pass |
| **The owner's judgement**: playing it, hearing it, running it on their hardware | Is it good? Does it work where it ships? | Owner |

In the field every serious miss passed its gates: a camera stuck in the wrong place, character features drawn out of position, routes "proven" by test bots that skipped the travelling, sounds that passed analysis and sounded wrong to the owner. The owner caught several from a small preview image.

- The bar is set before the work starts and is not moved afterwards. For discovery, what would count as an answer is set before looking.
- After integration every gate in the project runs, not only the ones for the changed parts.
- **Fresh all the way through.** Every gate first confirms the chain: source, build, and the copy actually running or deployed. A stale build, a leftover cache file or the wrong file on the device all produce results that look real.
- **Test what ships.** The same settings, the real input path, the real hardware. Bots that take a shortcut a person cannot take, an emulator standing in for the real device, and a headless path that differs from the product each passed while the product failed. Two field reports ranked this lesson first.
- **Where only the owner has the shipping configuration, the owner is a gate.** Give them a written checklist per build, design the build so one session tests many things, and cap how often they are asked.
- **Build evidence for judgement.** Numbered items the owner can answer by number, before-and-after sheets, twenty-second clips. Anything unfinished that could reach the owner's screen carries a visible TEST mark.
- A failure is traced to its cause. Turning an unrelated setting until the number passes is not a fix, and neither is changing the product so a flaky check steadies.
- **Bars have two owners.** A bar from the owner's words changes only by the owner's words. A target the lead invented is labelled as the lead's, and missing it is still reported as a miss until the owner accepts the result. When the owner changes the design, the tests change with it, and that is logged as a spec change with their words.
- **Important claims get a fresh checker**: a new agent given the work and the gate, without the conclusion. The lead's own lane always gets one, as do the one thing and any go or no-go milestone. In the field an independent lane that tested through real input found seven real bugs.

## Strikes and promotion

Tiers exist so that the strongest model works on the hardest problems and no tier burns tokens on a task it has stopped improving.

1. **Choose the starting tier by what a miss costs.** Standard is the default for well-specified work that is cheap to check. Light is for lookups and mechanical work. Start at senior when the task needs judgement across files, or when a failed attempt is expensive to discover, for instance when it costs the owner a hardware test. Starting above standard needs one line of reason in the ledger.
2. **Count strikes.** A strike is one pass by a lane, at its current tier, that the lead verified and found short: the gate failed on the lead's rerun, or it passed and the lead rejected the work for a named defect.
3. **Charge the right party.** Before recording a strike, ask whether a stronger model given this same brief would have passed. If the brief had the wrong design, the build was stale, the gate was broken or a tool trap ate the run, the failure is the lead's. Fix the brief, add the mistake to the register, and rerun at the same tier with the count unchanged.
4. **Three strikes is the ceiling. The price gap sets how many of the three a tier gets.** Trying the cheaper tier first only saves money if it succeeds more often than its price as a fraction of the next tier's. Light costs a twentieth of standard, so light gets all three. Standard costs half of senior, and senior half of the lead, so there the default is to promote after the first strike, with one more directed attempt only when that pass closed most of the gap to the bar. Two strikes is the most either gets.
5. **A plateau promotes at once.** If a pass closed less than about a quarter of the remaining gap, or failed the same rows in the same way, the tier has stalled, whatever the count.
6. **Carry the history up.** Close the row as promoted and open a new row at the next tier. The promoted brief is the original plus what was tried, the numbers each attempt reached, and the lead's diagnosis of why the tier fell short (`assets/promoted-brief.addendum.md`). A new tier starts with a cold cache, so the brief has to be complete on its own.
7. **At the top, go to the owner.** A task promoted to the lead is done by the lead, with a fresh checker. If the lead also strikes out or stalls, there is no further quiet attempt. Take it to the owner with what was tried, the numbers, and the choices: a different design, a smaller scope, a second opinion from the independent agent, a bar change in the owner's words, or shipping with it under Known failures.
8. **Hand the rest back down.** Once the hard part is solved, the mechanical remainder becomes a new lane at a cheaper tier, with the solution written into its brief.

`orch.py cost lanes` shows, per tier, how many rows finished there and how many were promoted out. That is the measured success rate that rule 4 depends on. Retune the allowances in `config.json` from it, and again when prices change.

## Context and cost

An agent rereads its whole context on every turn, so cost grows with turns multiplied by context size. Re-reading from a warm cache is cheap per token. Writing the context to the cache again costs 25 to 80 times as much per token on the three larger models, and that happens whenever an agent starts, comes back after the cache has expired, or is compacted.

- **Budget by context size, not by turns.** A worker hands off past about 200K tokens. One turn that reads a large dump costs more than ten small ones.
- **Resume or start fresh by scope.** For a follow-up in the same scope, continue the same agent while it is under budget and its cache is warm; one field project credits that for a 13-minute round. For new scope, or past the budget, start a new agent from a handoff. A handoff is only worth it when the note is short and complete, so it carries the findings as well as the state.
- **The lead has a budget too.** In two field projects the lead's context reached 966K tokens. In one of them a lead response cost more than twice a senior worker's. Start a fresh lead session from the North Star at each milestone.
- **Do not leave a large session idle.** Before a long break, write the handoff so the next session starts small. One project spent about 16% of its cost on six cold resumes.
- **Keep side work out of the lead's context.** A lookup unrelated to the lead's own task goes to a light worker. Tell the owner once that a question unrelated to the project is cheaper asked in a fresh session, and give them the per-response figure.
- **Fan out searching, read what you will change.** Searching, surveying and summarising go to the cheap tiers and the lead reads conclusions. Code the lead is about to change or verify, it reads itself.
- **Numbers first, then one cheap look.** Check with gates, then look at a small crop or contact sheet each round. Full size is for the final deliverable.
- **Quiet commands, narrow reads, precise edits.** Filter output down to errors and the summary line.

**The cost ledger.** `pass-end` reads the session transcripts, prices every model response at list API rates, and records the pass. The figure is API-equivalent: on a subscription it is what the work would have cost, not a bill, and the limits that actually bind are usage windows and the owner's time. `cost report` shows, per pass:

| Column | Field values | If it is high |
|---|---|---|
| Lead's own share of cost | 17% to 52% | The lead is doing the work itself in a large context. Hand off or delegate. |
| Senior share of worker responses | 61% to 98% | Check the ledger for lanes that never tried standard. |
| Re-reading share | 45% to 58% on worker tiers | Contexts are too large. |
| Rewrite cost | About 16% of one project went on cold resumes; one-hour cache writes were 23% and 50% of two leads' cost | Idle gaps or compaction. Shorter sessions. |
| Largest worker context, lead context | 232K to 384K per worker response; 966K lead | Compare with the budgets. |
| Owner messages | 48 and 114 over two projects | How much of the owner's time the pass used. |

It also projects the total at the pass cap and checks any cost ceiling; at 80% tell the owner then, not at 100%. Add spend the transcripts cannot show with `cost add`, and list what stays uncounted in the config so it prints on every cost line. A model with no price entry is reported as not priced, never as free.

## The mistake register

Every rule here began as a specific mistake. The register keeps each one as a record: what happened, the cause, the rule, the evidence from the field, and a check. The work is compared against it at four points, so the system is tested against its own history and not only against its intentions.

| Checkpoint | When | What is checked |
|---|---|---|
| `brief` | Before a brief is sent | Reasoning or suspects, a gate, file ownership, stop conditions, a kill rule. |
| `accept` | Before a lane's result is accepted | The chain was fresh. The fix addresses the cause. |
| `pass-end` | At step 7 of every pass | Tiers justified, contexts within budget, strike-outs acted on, ledger reconciled, every done lane has an accept record, owner notes routed, bars unmoved, history intact, cost recorded, cap respected, someone looked. |
| `owner-report` | Before reporting to the owner | Every claim was read from a file or an output just now. What no person has checked is stated. The owner's time is batched. |

Each check returns clear, repeated, or a question. Scripted checks read the North Star, the cost ledger or the brief. Questions are for what a script cannot see, and are answered with `mistakes answer` and evidence: a quoted line, a number, a file. Answering "clear" without evidence is the same failure as loosening a gate.

**Add a mistake the moment it is understood**, with `mistakes add`: when a result that looked true was false, a worker wasted a run, the owner corrected something, or a number in the cost report was a surprise. Write what happened and the cause, not a moral.

**Lessons are promoted like lanes.** A lesson that is written down and still repeated needs a stronger form, not a louder sentence. Three strikes at one level move it up: prose in this skill, then a line in a template so it cannot be skipped, then a scripted check or project gate, then the owner, because by then the process is wrong and not the reminder. `mistakes report` shows where each lesson stands.

At the close of a project run `mistakes export`. The next project's `init` picks those lessons up.

## State and memory

Nothing important lives only in a conversation.

| Layer | Lifetime | Contents | Writer |
|---|---|---|---|
| North Star | The project | Intent, decisions with reasons, gates, lane ledger, owner notes, status log. | Lead |
| Worklogs and handoffs | A component, or one pass | What was tried, what was measured, what was found, open issues, how to resume. | Lead and workers |
| `.orchestration/` | The project | Cost ledger, mistake register and log, North Star snapshots. | The script |
| Owner memory | Across projects | The owner's standing preferences and corrections, one fact per entry, each with why and how to apply it. | Lead |

A handoff is short and specific: state, what changed, gate table, open problems, what was tried, findings, strikes so far, next step, exact commands. Owner memory holds guidance that changes future behaviour, not a history of completed work. A remembered caution is checked against the present before it is applied. One lead's memory said a project was finished and should not be reopened, and then the facts changed.

## The environment contract

Workers cannot know the facts of the owner's machine and habits, and breaking one does damage that no gate catches. These go in the North Star and are quoted in every brief they apply to. In the field every entry came from a real incident.

| Category | What to write down |
|---|---|
| Do not disturb | What an agent must never interrupt: visible windows, focus, sound, a recording. |
| Exclusive resources | Each thing only one agent can use at a time (an emulator, a device, a card, a browser, the owner's screen) and how turns are taken, for example a flag file. |
| Owner's time | What only the owner can test, how it is batched, and the most they are asked per pass. |
| Storage | Where large files go, and what to clean up. |
| Irreversible actions | What needs the owner's yes each time: commits, deletions, anything public, anything approved and locked. |
| Honesty limits | What must never be claimed: a weakened gate, a prototype called finished, a thing not checked. |
| Tool quirks | Traps in the shell and tools, with the form that works. Add one the moment it is found. |
| Privacy | What never leaves the machine. |

If several lanes must edit one large file, split the file first or run those lanes one after another. Region ownership inside a shared file broke the build twice in the field.

## Working with the owner

- **Get it into their hands every pass.** In one field project nearly every real defect came from a one-line note after the owner played the build, and in another the owner caught every serious miss. A runnable build with the unverified list is worth more than a longer report.
- **Lead with the result.** A report starts with what is now true, then what is not done or not verified.
- **Say what no one has checked.** Anything a gate cannot measure and the owner has not yet seen or heard is listed as unverified.
- **Claim only what you just read.** Every fact in a report comes from a file, a number or an output at the time of writing. Leads in the field reported evidence that did not exist and said they could not check something they could.
- **Keep their words.** Log each note verbatim with an id. Sensory comparisons, what it sounds or looks like to them, go into the brief unchanged; in the field each one became a specific fix.
- **Guess or ask.** If a wrong guess is cheap to undo, guess, carry on and flag it in the notes log and the report. If it would waste a pass or touch something approved or irreversible, ask.
- **Lock what they approve.** An explicit approval is recorded, and the approved thing is pinned so later work cannot change it unnoticed.
- **Use their words.** Talk to the owner in everyday terms unless they use the technical ones first: helper for worker, job for lane, check for gate, pass mark for bar, round for pass, the plan for the North Star, a failed try for a strike. Keep the real terms in the files, because the script and the helpers read those.
- **Do not go silent.** Say in a line what you are starting before a long stretch, and report each lane as it lands.
- **Fix fast, then show.** When the owner reports a problem, fix it and let them try again.
- **Keep going on what does not need an answer.** A pending question does not stop unrelated lanes.
- **Prefer the reversible action.**
- **Close with the cost.** After the final pass, send `cost report`: the spend by tier, the trend, and what the figure leaves out.

## Running this in Claude Code

- Start a worker with the Agent tool and set its model to the lane's tier. Launch the pass's lanes together in one message so they run in parallel.
- Write the agent id that comes back into the ledger's Agent column. The cost reader matches worker transcripts to lanes by that id.
- For code lanes, a separate worktree per lane enforces file ownership, and the lead merges at step 6.
- Sending a message to an existing agent resumes it with its context. Use that for same-scope follow-ups and a new agent for everything else.

## Reference files

- `references/skeleton.md`: the skill reduced to the techniques it is built from, one line each. Read first for the shape of the whole thing, or when a situation is not covered and you need the principle.
- `references/north-star.md`: each section of the North Star, and what the script reads from it. Read when writing or repairing one.
- `references/briefs-and-handoffs.md`: both kinds of brief, promoted briefs, reports, handoffs, fresh-checker briefs, evidence for the owner. Read before the first brief of a project.
- `references/cost-and-mistakes.md`: every `orch.py` command, the metrics, file formats, thresholds, and how to add a scripted check. Read when a command's output is unclear or a threshold needs tuning.
- `references/field-data.md`: the four projects' measurements side by side. Read when deciding whether a number in your own report is normal.
- `references/reference-build.md`: the first build in detail, and the eleven recommendations that came out of it.
- `references/audit.md`: what changed from the draft manual and from the field reports, why, how well each rule is supported, and what is still open.
