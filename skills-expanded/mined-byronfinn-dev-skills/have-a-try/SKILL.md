---
name: have-a-try
description: "Settle a decision with conflicting options: build the minimal demo that exercises the contested point, verify the core conflict, then adjudicate — selecting the best option or eliminating wrong ones — and fix the evidence with rationale. Tactics: interactive logic probe, UI variants, benchmark comparison, concern-checking spike, or a synthesized experiment. Use when a divergence between options is cheaper to resolve by running code than by reasoning. Not for plain one-off measurements or lookups with no decision at stake (just run those directly). Trigger words: prototype, 原型, 试一下, spike, 验证一下, 看看效果, 跑起来看看, 有没有更简单的方式, 这个状态机对不对, 这个数据模型能表达吗, 有分歧, 帮我抉择, 选哪个, A还是B, 方案对比, 性能对比, benchmark, 基准测试, 哪个快, 可行性验证, 排除方案, 依次试试."
---

# Have-a-Try: Settle a Divergence with a Minimal Demo

🥷 The conflict decides the demo. The demo settles the conflict.

A divergence is **multiple mutually exclusive options, or one claim pitted against doubt about it**, that reasoning alone can't separate. This skill writes **disposable code** that produces the missing evidence: a minimal demo aimed at the contested point, run in one command, adjudicated on what it shows. A verdict that **eliminates** a wrong option is as valuable as one that **selects** the best.

This is the pipeline's adjudication-by-experiment service. `/think` generates options but writes no code; `/grill` challenges decisions by reasoning and reading; `/research` settles what documentation can settle. When the answer exists only in "run it and see" — on your machine, your load, your state machine, your eye — that's here.

## Outcome Contract

- **Outcome**: One settled divergence — a candidate selected, one or more eliminated, or a tie/all-fail verdict — with evidence and rationale captured durably.
- **Done when**: The verdict is recorded (PRD `## Traceability` / ADR / commit message / `NOTES.md` next to the demo) and the demo shell is disposed of (deleted, validated core absorbed, or archived).
- **Evidence**: The demo runs via one command; the verdict names what was selected or eliminated and why.
- **Output**: Divergence, tactic, verdict, evidence, where captured, disposition.

## The Pipeline

**Phase 1 — State the divergence.** Write down the decision, the conflicting positions (a candidate set, or "this design holds" vs "it breaks"), and what evidence would settle it. If you can't name the divergence, that's `/think`'s job, not this skill's.

**Phase 2 — Build the minimal demo.** Cover **only the contested surface** — anything in the demo that isn't disputed is scope creep. Pick the tactic from the table below; when none fits, synthesize one (CUSTOM, in [REFERENCE.md](REFERENCE.md)).

**Phase 3 — Verify the core conflict.** Run it (one command). Push each position toward its worst case: the awkward scenario, the realistic load, the concern list. Watch what the evidence says.

**Phase 4 — Adjudicate and fix the evidence.** Select, eliminate, or call a tie/all-fail — all three are valid verdicts. Record decision + evidence + one-line rationale where the divergence was born (see below). Then dispose of the shell.

### Divergence type → tactic

| The core conflict is… | Tactic | Adjudicator |
|---|---|---|
| "Does this logic / state model hold up?" | **LOGIC** interactive probe | The driver's feel |
| "What should this look like?" | **UI** side-by-side variants | A human's choice |
| "Is A or B faster / leaner?" | **BENCH** shared-harness comparison | Numbers, with environment |
| "Can option X survive concern C?" | **SPIKE** targeted demo + concern×option matrix | The checklist ✓/✗/△ |
| None of the above | **CUSTOM** synthesized experiment | Per synthesis |

The tactics are walked paths, not a closed enum — any decision that running code can settle belongs here, on one of these paths or a synthesized one.

### Route out (this is the wrong skill when…)

- The divergence hasn't formed — candidates can't be named, concerns can't be listed → `/think`.
- Documentation or an authoritative source settles it as-is (no my-machine / my-load factor) → `/research`.
- No divergence — behavior is already accepted and needs a proper implementation → `/tdd`.
- Open-ended performance tuning with no candidates to compare ("just make it faster") → `/debug`.

## Where This Skill Sits

Evidence flows back to where the divergence was born:

| Divergence born in | Enter | Verdict lands in | Then |
|---|---|---|---|
| `/think` converged but left A-vs-B | after the PRD, before `/grill` | PRD `Prototyped by` + the Open Question closed | `/grill` (back to `/think` if the verdict breaks the plan) |
| `/grill` hits a decision reasoning can't settle | grill parks the item, hands over | ADR with evidence | resume `/grill` |
| `/research` narrowed candidates by docs | after the INDEX record | research record cross-ref + ADR/PRD | `/think` or `/grill` |
| `/story` / `/implement` mid-build local doubt | a local mini try | issue comment / commit | continue the seam (production code via `/tdd`) |

## Rules

1. **Throwaway from day one.** Locate the demo close to its target code; name it to signal prototype, not production. Follow project routing conventions. State the demo's file location explicitly (anti-pattern #13 — no unsolicited or unannounced files).
2. **One command to run.** Use the project's existing task runner. *(anti-pattern #29 — run command is the success contract.)*
3. **No persistence by default.** In-memory state. If persistence IS the contested point, use a scratch store with a clear "PROTOTYPE" name.
4. **Minimal — cover only the contested surface.** Skip the polish: no tests, no error handling beyond runnability, no abstractions. Anything uncontested inside the demo is scope creep. *(Prototype-scoped; the opposite of `/tdd` discipline — don't let it leak.)*
5. **Surface the evidence.** State panel (LOGIC), variant switch (UI), numbers with environment (BENCH), concern matrix (SPIKE) — after every action, show what changed or what was measured.
6. **Adjudicate, then dispose.** Capture verdict + evidence + rationale; delete the shell or absorb the validated core into real code. Only when the verdict is contested or the losing samples have archive value: commit the demo to a throwaway branch off main and leave a pointer at the verdict record. Don't leave it rotting on main.

## Process Summary

**Step 0 — Bootstrap.** Apply the [Skill Entry Protocol](../rules/entry-protocol.md) — it reads `CONTEXT.md` and `docs/adr/` and reports what's missing.

**Step 1 — State the divergence.** Decision, conflicting positions, deciding evidence, acceptable outcomes — including elimination. A demo answering the wrong divergence is pure waste.

**Step 2 — Pick the tactic.** From the table above, or CUSTOM. If ambiguous and the user isn't reachable, default by matching surrounding code (backend module → LOGIC/BENCH/SPIKE; page/component → UI) and **state the assumption** at the top of the demo.

**Step 3 — Build the minimal demo.** Follow the tactic chapter in [REFERENCE.md](REFERENCE.md). Match the project's existing language, tooling, conventions — don't add new runtimes or structures. *(anti-pattern #19)*

**Step 4 — Hand it over.** Give the user the run command (LOGIC/BENCH/SPIKE) or URL + `?variant=` keys (UI). They drive it. The interesting moments are "wait, that shouldn't be possible" — those are bugs in the *idea*, which is the point.

**Step 5 — Adjudicate, fix the evidence, dispose.** Record verdict + evidence + rationale where the divergence was born (PRD `Prototyped by` / ADR / commit / `NOTES.md`). Then delete the shell, absorb its validated core, or archive it per Rule 6.

See [REFERENCE.md](REFERENCE.md) for the full LOGIC / UI / BENCH / SPIKE processes and the CUSTOM synthesis rules.

## Gotchas

| What happened | Rule |
|---|---|
| Wrong tactic — built a UI variant for a "which is faster" question | Phase 1: name the deciding evidence first; the tactic follows from it, not from habit |
| Demo includes uncontested parts (full feature, walking skeleton) | Phase 2 / Rule 4: minimal = only the contested surface; everything else is scope creep |
| Verdict recorded as a selection; what was eliminated and why went unrecorded | Phase 4: elimination is half the value of the run — record it with the same care |
| Benchmark reported without environment (machine, versions, data size, rounds) | BENCH: numbers without environment are not reproducible — they aren't evidence |
| Spike grew into a real implementation (tests, abstractions, polish) | SPIKE: the knowledge is the product, not the code; the production rewrite goes through `/tdd` |
| Divergence never written down before coding | Step 1: make the divergence explicit and checkable |
| Logic module references `console.log`/prompts/escape codes | LOGIC: keep the logic in a pure portable module; the shell is thin — nothing flows back |
| Variants differ only in colour or copy | UI: that's a tweak, not a divergence. Real variants disagree about structure |
| Demo left rotting in repo after the verdict | Step 5: capture, then delete / absorb / archive per Rule 6 |
| Wired the demo to the real database by default | Rule 3: in-memory by default; scratch store only if persistence IS the contested point |
| Files created without telling the user where | Rule 1: state the demo's file location explicitly (anti-pattern #13) |

## Output

```
Have-a-try complete.

Divergence: <the decision and its conflicting positions, one sentence>
Tactic:     LOGIC | UI | BENCH | SPIKE | CUSTOM
Run:        <the one command, URL + ?variant= keys, or results location>

Verdict:    Selected <X> because <evidence-based reason>
            | Eliminated <Y> because <evidence-based reason>
            | Tie / all failed — <what this means for the plan>

Evidence:   <what was observed: state transitions, chosen variant,
             numbers + environment, concern×option matrix>

Captured at: <PRD-NNNN ## Traceability Prototyped by | ADR <NNNN> (see docs/adr/) | commit | NOTES.md>

Demo disposition:
- Deleted (shell only, nothing worth keeping)
- Absorbed core into <real module/route> (shell deleted)
- Archived to throwaway branch <name> (pointer left at <verdict record>)

Next (route by where the divergence was born):
- /think → close the PRD Open Question; /grill (or /think if the plan broke)
- /grill → fold the verdict into an ADR; resume /grill
- /research → cross-ref the research record; /think or /grill
- mid-build → record on the issue/commit; continue the seam via /implement
```

**PRD Traceability:** If a PRD exists for the feature, fill the `Prototyped by` field in its `## Traceability` section so downstream skills know a demo adjudicated (selected or eliminated) a design option:

```markdown
- **Prototyped by**: `/have-a-try` (<YYYY-MM-DD>) — <divergence> → <selected X / eliminated Y>, because <evidence>
```
