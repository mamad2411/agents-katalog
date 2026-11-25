---
name: brainstorm-debate
description: Read-only Map / Reason / Feasibility prompts with fail-closed debate parsing, Fable response rules, evidence, ledgers, and convergence.
---

# Brainstorm debate protocol (embed into Codex prompts)

Use the matching block in a fresh, read-only Astra session. Fable keeps the thesis and records the
analysis; Astra supplies an independent map, reasoning, and feasibility check.

## Standards block

### Map turn

```
Map turn (mandatory — you are Astra; the workspace is read-only):
- Apply the Map lens block from codex-flow:brainstorm-lenses.
- Read FRAME.md at the run-dir path given in the prompt header. Build your own system map from it;
  Fable's map is never shown to you.
- Name stocks, flows, feedback loops, delays, the fitting archetype or null, and leverage points.
  Do not introduce an option or recommendation.
- Read every cited file before citing it. Use run-dir paths from the prompt header.
- End with exactly ONE fenced json block and nothing after it. The block must have this shape:
{"kind":"map","stocks":[{"id":"S1","name":"stock"}],"loops":[{"id":"L1","type":"R","chain":"stock -> flow"}],"delays":[{"id":"D1","where":"measurement -> response"}],"archetype":"none fits","leverage":[{"id":"P1","level":1,"point":"change the paradigm"}]}
```

### Reason turn

```
Reason turn (mandatory — you are Astra; the workspace is read-only):
- Apply the Reason lens block from codex-flow:brainstorm-lenses.
- Apply the Debate block from codex-flow:brainstorm-argumentation verbatim.
- Read FRAME.md, MAP.md (Fable map, Astra map, Divergence), and REASON.md (current pyramid thesis
  and earlier rounds) at the run-dir paths. Attack the thesis; read cited files before citing them.
- Order the work: steelman → counter-thesis (round 1; later rounds keep or revise) → contributions
  → challenges (each names a Toulmin target, scheme, and cq) → violations (each names PD<k>) → json.
- In round 1, answer every Map conflict listed in the prompt. Add useful contributions as N<n>,
  then raise numbered C<n> challenges. Each challenge states Type (LOGIC, SYSTEM, ASSUMPTION, or
  EVIDENCE), Claim, Evidence, Severity (BLOCKER, MAJOR, or MINOR), and What would change my mind.
- Parsed json supplies ids, type, severity, status, target, scheme, cq, and short `evidence`; the
  parser drops a challenge without it. Prose under C<n> carries the full claim, evidence, and doubt.
- Reuse global ids. For earlier challenges, state HOLD with the evidence keeping them open or
  CONCEDE with the evidence that settled them. Do not re-raise a conceded challenge without new
  evidence. Use only NEW, HOLD, or CONCEDE for challenge status. Include dissent when needed.
- End with exactly ONE fenced json block and nothing after it. The block must have this shape:
{"round":<n>,"steelman":"the strongest version of the proposal","counterThesis":"the proposal should be tested against delayed effects","challenges":[{"id":"C1","type":"SYSTEM","severity":"MAJOR","status":"NEW","target":"claim","scheme":"cause-effect","cq":"CQ1","claim":"the proposed change misses a balancing loop","evidence":"REASON.md thesis S2"}],"contributions":[{"id":"N1","claim":"measure the delayed response before choosing an intervention"}],"violations":[{"id":"V1","rule":"PD2","claim":"the standpoint is not yet adequately defended"}],"dissent":null}
```

### Feasibility turn

```
Feasibility turn (mandatory — you are Astra; the workspace is read-only):
- Apply the Feasibility lens block from codex-flow:brainstorm-lenses.
- Assess only the surviving recommendation. When no recommendation survives Reason, the command
  skips this turn; record that absence under Open questions instead. If several survive, assess
  the top-ranked one and name the others.
- Read FRAME.md, MAP.md, and REASON.md (final thesis and surviving recommendation) at the run-dir
  paths before citing them. Record exactly one verdict, effort, reversibility, dependencies, risks,
  conditions, and firstStep.
- Do not include rollout, rollback, or task-list content.
- End with exactly ONE fenced json block and nothing after it. The block must have this shape:
{"kind":"feasibility","verdict":"FEASIBLE-WITH-CONDITIONS","effort":"M","reversible":"partly","dependencies":["approval"],"risks":[{"id":"K1","risk":"the delayed response obscures impact"}],"conditions":["measure the response"],"firstStep":"define the first read-only measurement"}
```

## Run files per turn

| Turn | Reads | Writes |
| --- | --- | --- |
| Map | FRAME.md | MAP.md `## Astra map`, MAP.md `## Map critique` |
| Reason | FRAME.md, MAP.md, REASON.md | REASON.md round |
| Feasibility | FRAME.md, MAP.md, REASON.md | REASON.md Feasibility turn, REASON.md `## Feasibility critique`; ANALYSIS.md `## Feasibility` |

## Parse every Astra output fail-closed

- Save the raw Astra answer at the run-dir path named in the prompt, then invoke the helper for
  its turn: `node "${CLAUDE_PLUGIN_ROOT}/scripts/debate-parse.mjs" --kind map --file <path>`,
  `node "${CLAUDE_PLUGIN_ROOT}/scripts/debate-parse.mjs" --kind round --round <n> --file <path>`,
  or `node "${CLAUDE_PLUGIN_ROOT}/scripts/debate-parse.mjs" --kind feasibility --file <path>`.
- If the helper is not found, STOP and tell the user to reinstall the codex-flow plugin.
- Exit 0 accepts the parsed fields only when no entry was dropped. Exit 1 means an unparsed answer
  or dropped entries: inspect `parseError` and `droppedReasons`, request one corrected JSON block
  with `mcp__codex__codex_continue`, and parse that answer again. If it still exits 1, record each
  dropped entry or wholly unparsed turn under `## Open questions` as
  `UNVERIFIED: <droppedReason or parseError>` with no reconstructed claim.
- Exit 2 is a usage or read failure: surface the error and STOP.
- Never reconstruct an entry from the prose. Keep the raw answer and tell the user when a turn is
  `UNVERIFIED`.

## Fable's response format

- Judge Astra's steelman as `FAITHFUL | UNFAITHFUL`. Mark challenges resting on an unfaithful reading
  `STRAW-MAN` and do not count them.
- Steelman the counter-thesis before answering it element by element, using the same Toulmin structure.
- For every counted challenge, name the Toulmin element defended or revised in the disposition.
- Answer every open `C<n>` in order with exactly one disposition: `C<n> ACCEPT`, `C<n> REBUT`,
  or `C<n> REFINE`, followed by the change or checkable evidence.
- Answer every `N<n>` with `ADOPT | DECLINE` and a reason. Rewrite the thesis after the
  dispositions and append `Changed this round:`.
- A changed recommendation is one flip. Do not add options through the response format.

## Map critique

- Write the critique in MAP.md under `## Map critique`; critique Astra's map and Fable's own map
  element by element in the Debate block's Toulmin format.
- Put every map conflict into the round-1 Reason prompt for Astra to answer.

## Feasibility critique

- Write the critique in REASON.md under `## Feasibility critique`. For each contested field—the
  verdict, effort, reversibility, and each risk `K<n>`—write one line as
  `<field> ACCEPT | REBUT | REFINE — <Toulmin element> — <evidence>`.
- Copy disagreements still open to ANALYSIS.md `## Open questions` at Decide.

## Violations

- Astra reports Fable's violations in the json `violations` array; Fable records Astra's violations
  as `V<n>` with `PD<k>` in its response.
- List both in REASON.md under the round; the affected standpoint's Evidence column cites the `V<n>`
  id. A sustained PD3 violation is the STRAW-MAN case.

## Evidence rules

- Cite a file as `file:line`, a read-only command, a measurement, or named prior art; mark it
  `prior-art:`. Read a file before citing it.
- A claim without checkable support is marked UNVERIFIED in the Evidence column and cannot make a
  standpoint MAINTAINED. A concession names the evidence that caused it. Fable never re-grades
  Astra's severity.

## Transcript budget

Estimate tokens as chars/4. When the transcript exceeds 6 000 estimated tokens, embed the standpoint
ledger, assumption register, and last round; point to the run-dir transcript for the rest; never raise
the budget.

## Standpoint ledger

Record one compact table with this exact header:

```markdown
| Id | Standpoint | Owner | Status | Crux | Evidence |
| SP1 | ... | astra or fable | UNRESOLVED | warrant or A<n> | path:line, command, measurement, or prior-art: |
```

- Record the main answer, every argument, and the counter-thesis as standpoints with ids `SP<n>`.
- End each standpoint at MAINTAINED | RETRACTED | UNRESOLVED. For UNRESOLVED, Crux is
  required and points to a Toulmin warrant or an `A<n>` assumption.
- Map dispositions to standpoints: a challenge Fable REBUTs and Astra later CONCEDEs leaves its
  standpoint MAINTAINED; a challenge Fable ACCEPTs retracts or revises the standpoint (RETRACTED,
  or a revised standpoint with a new SP id); a challenge still NEW or HOLD at the stop leaves the
  standpoint UNRESOLVED with a Crux; a STRAW-MAN challenge changes nothing; an ADOPTed contribution
  adds or revises a standpoint.

## Assumption register

Record one compact table with this exact header:

```markdown
| Id | Assumption | Held by | Importance | Certainty | Evidence |
| A1 | ... | astra or fable | high | low | path:line, command, measurement, or prior-art: |
```

- Record every root assumption as `A<n>`; set Importance and Certainty only to high | low.
- Trace every UNRESOLVED standpoint to its warrant or an assumption in this register.

## Stop rule

- A round is one Astra Reason turn plus Fable's response. Minimum 1 round, cap 3.
- Converged when no standpoint is UNRESOLVED without a Crux.
- Stop when converged or after round 3; severity only orders work. Record remaining standpoints and
  evidence gaps under `## Open questions`. Never run a fourth round.
