---
name: propose-workflow
description: Propose a reviewable multi-agent workflow as a blueprint — pick and name the pattern (map-reduce, pipeline, tournament, loop-until-dry, dag), emit its shape as an agentstack-blueprint JSON block, and WAIT for the user to approve / reject / edit before authoring and running it via agentstack more workflow run.
---

# Propose a reviewable workflow

Use when the user wants to **design or build a workflow and review it before it
runs** — "let's design a workflow for X", "build me a workflow but let me see it
first", "what shape would you use for X". You emit a **blueprint** (the shape:
pattern, phases, per-node role/model/effort/instruction, symbolic fan-out,
edges), the panel draws it as a graph, and the user approves / rejects / edits.
Only on approve do you author and run it.

The judgment worth reviewing is **which algorithm you chose** — fan-out
map→reduce for "audit this repo" vs a judge panel for "design an API". Emit the
shape; let the human check it.

## 1 — Propose, or just run?

Mode is the user's **intent**, not a setting — infer it:

- **"Just run a workflow" / "go" / "do X across the files"** → skip this gate.
  Author and run it the normal way — the declare → lock → trust → `agentstack
  workflow run` pipeline in §4. Same pipeline, gate auto-skips.
- **"Design / build / let me review / show me the shape first"** → propose a
  blueprint (below), then stop and wait. Do not author, do not run.

When unsure which the user meant, propose — a review gate is cheap to approve
and expensive to skip.

## 2 — Emit the blueprint, then stop

Pick the **best-fitting pattern for the task** and name it. One node per
role/step; give each a `model`/`effort`/`instruction`; edges carry a `kind`.
Emit it in a fenced block whose language tag is **exactly**
`agentstack-blueprint` — that tag is how the panel intercepts and renders it.

````
```agentstack-blueprint
{
  "workflow": "repo-audit",
  "pattern": "map-reduce",
  "goal": "Find and rank bugs across the changed files",
  "nodes": [
    { "id": "map", "phase": "Find", "role": "reviewer",
      "model": "gpt-5.5", "effort": "low",
      "instruction": "Scan ONE changed file for correctness bugs",
      "fanout": "1 per changed file" },
    { "id": "reduce", "phase": "Rank", "role": "synthesizer",
      "model": "opus", "effort": "high",
      "instruction": "Dedupe and rank all findings by severity",
      "fanout": null }
  ],
  "edges": [ { "from": "map", "to": "reduce", "kind": "fan-in" } ]
}
```
````

**Schema rules — follow exactly:**

- `pattern` ∈ `map-reduce | pipeline | tournament | loop-until-dry | dag |
  custom`. Name the one that actually fits; don't force map-reduce onto a chain.
- Each node: `id`, `phase` (human label), `role` (a role name you'll back with a
  profile), `model`, `effort`, `instruction` (one crisp sentence), `fanout`.
- **`fanout` is SYMBOLIC** — `"1 per changed file"`, `"3 attempts"`, or `null`
  for a single agent. **Never fabricate a concrete count** for data-dependent
  fan-out; the multiplicity is unknown before the run, and reviewing the
  *pattern* is the whole point.
- `edges`: `{ from, to, kind }`; `kind` is a short label —
  `fan-in`, `fan-out-then-score`, `chain`, `loop`, etc.
- `model`/`effort` are **declared intent** for review (advisory in v1, see §5).

Pattern → topology, at a glance:

| pattern | shape |
|---|---|
| map-reduce | fan-out one-per-item → single fan-in reducer |
| pipeline | linear chain, each stage feeds the next |
| tournament | N attempts → judge scores all → synthesizer builds the winner |
| loop-until-dry | a step repeats until it yields nothing new |
| dag | explicit multi-parent edges, no single spine |

Tournament example — same schema, different shape: nodes `attempt` (phase
Generate, role designer, opus/high, "Design the API from a distinct angle",
fanout `"3 attempts"`), `judge` (phase Score, role judge, fable/high, "Score
every attempt on clarity, safety, ergonomics", fanout `"1 per attempt"`),
`synth` (phase Synthesize, role synthesizer, opus/high, "Build the final design
from the winner + best grafts", fanout `null`); edges `attempt→judge`
kind `fan-out-then-score`, `judge→synth` kind `fan-in`.

After the block, add **one or two sentences** naming the pattern and why that
shape fits — then **STOP**. Do not author the workflow, do not run anything, do
not keep talking past that framing. Wait for the user.

## 3 — The review loop

The panel's three buttons arrive as plain user messages (recognize the exact
templates **and** natural-language equivalents), where `<workflow>` is the
blueprint's `workflow` field. These strings are the interlock with the t3code
panel — they must stay byte-for-byte identical to the builders in t3code's
`workflow-blueprint.ts`; changing one side without the other breaks the button
actions.

- **Approve** — `Approved: run workflow blueprint "<workflow>" exactly as
  shown.` → go to §4.
- **Reject** — `Rejected: cancel workflow blueprint "<workflow>". Do not run
  it.` → acknowledge briefly and stop. Author nothing.
- **Edit** — `Edit workflow blueprint "<workflow>": <change request>` → apply
  the change and **re-emit the FULL blueprint** in a new `agentstack-blueprint`
  block (never a partial diff or prose-only description), then stop and wait
  again. Keep looping until approve or reject.

## 4 — Compile on approve (you are the compiler)

On approve, author a runnable workflow **faithful to the approved blueprint**,
then declare / lock / trust / run it through the governed pipeline
`docs/workflows.md` documents (inlined below) — this is `agentstack`'s own
`workflow run`, not an external executor.

Map the blueprint onto the engine's authoring model — verify every mapping
against the prelude's real semantics (`pipeline(items, ...stages)` runs **each
item through all stages independently** — per-item, no barrier, no fan-in;
`parallel(thunks)` runs the thunks concurrently):

- **Topology → control flow.**
  - **map-reduce** → a `pipeline` (or `parallel`) map over the items, **then a
    single, separate `agent()` call** fed the collected results. The reduce is
    one fan-in step, not a pipeline stage: a reducer *inside* `pipeline(items,
    map, reduce)` would run once **per item** (N reducers), which is not a
    fan-in. Mirror `docs/workflows.md`: `const found = await pipeline(files, f
    => agent(…, { role: 'reader' }))`, then `const report = await
    agent(\`…${found.join('\n')}\`, { role: 'writer' })`.
  - **tournament** → `parallel` attempts, then a **single** judge `agent()` over
    all of them, then a **single** synth `agent()`.
  - **chain** → sequential `agent()` calls (or a `pipeline` when the same
    per-item stage chain applies to every input).
  - Each node's `instruction` becomes that `agent()` call's prompt; `phase` → a
    `phase(title)` / `meta.phases` entry.
- **Node role → profile; model/effort reconciled through the profile.** The
  engine's source of truth is the **role's profile**, not the script — `agent()`
  names a `role`, and the harness/model come from that profile. For each node,
  choose or create a `[profiles.<role>]` whose bound model resolves to the
  node's declared `model` (and effort where the role supports it). This is how
  declared intent becomes real.
- **Roles — set BOTH; script ⊆ manifest.** `[workflows.<name>].roles` in the
  MANIFEST is the admitted authority set; the script's `meta.roles` must be a
  **subset** of it. Set both to the distinct node roles. Construction
  **refuses** the workflow if `meta.roles` names a role the manifest does not
  declare (the per-`agent()` role-in-`meta.roles` check is a bridge check, not
  the authority gate — the manifest `roles` is). Size `[workflows.<name>]`
  `max_agents` / `max_wall_seconds` to the fan-out (a per-file map needs
  headroom for many children); ceilings only narrow the machine ceiling,
  requests never widen it.
- Symbolic `fanout` becomes a data-dependent loop over the real inputs at
  author time (e.g. the changed-file list) — never a hardcoded count.

### Authoring primitives that make a wide workflow actually work

Use these when the fan-out is more than a handful of nodes. They are the
difference between a workflow that demos and one that survives width.

- **`schema` on any map node whose output a later stage reads.**
  `agent(prompt, { role, schema })` resolves with a **parsed value**, so the
  reduce stage indexes fields instead of parsing prose. At width 5 prose is
  survivable; at width 100 the chance that *every* mapper emits parseable
  output collapses, and a reduce that string-matches its inputs is the most
  common way a wide workflow fails. Supported subset: `type`, `properties`,
  `required`, `items`, `enum`, `additionalProperties: false` — anything else in
  the schema document is **ignored**, so do not rely on it.

  A step whose output fails the schema fails **closed** — the script sees
  `null`, and there is **no automatic re-ask** (a retry would spend an agent
  slot the ceiling never granted). Write the script to tolerate `null`:
  `.filter(Boolean)` before the reduce, every time.

  Tell the user plainly if they ask: schema validation constrains **shape, not
  content**. A prompt-injected step can return perfectly schema-valid lies, so
  it is a parsing convenience, never a trust boundary.

- **`partition(items, r, keyFn)` when one reducer cannot hold the map output.**
  A single reduce node is the default and is right for small fan-out. Past
  roughly a hundred map results, one reduce prompt stops fitting in any context
  window and the run fails on the last step **after paying for every mapper**.
  Split it: `partition` returns exactly `r` buckets (empty ones included, so
  your reducer count never varies with the data) and always routes the same key
  to the same bucket. Then `parallel` one reducer per bucket, and — if the
  blueprint calls for a single answer — one final fan-in over the R results.

  If you do this, the blueprint must show it: R reducer nodes plus the final
  fan-in, not one reduce node. The shape the user approved has to be the shape
  that runs.

- **`shard(items, { per })`** to batch small inputs into fewer children. 200
  files as 200 children is usually worse than 20 children of 10 files: same
  tokens, a tenth of the process and admission overhead.

- **`result: 'handle'`** on stages returning kilobytes each. The promise
  resolves with `{ digest, bytes, preview }` instead of the full text, keeping
  a wide run under the machine's resident-result ceiling. A handle costs ~620
  bytes, so it is pointless on short results. If a run fails with
  `resident_cap`, this is the remedy the error names.

- **`agentstack more workflow explain <name>`** after step 2 and before step 4. It
  reports the effective ceilings, which roles launch serially, and the
  `agent()` call sites — statically, spawning nothing. Cheap way to catch "this
  fans out wider than `max_agents` allows" before paying for the first N
  children.

**Serial roles are a real cliff.** A role whose harness takes no per-child MCP
config runs its children **one at a time**, whatever the concurrency cap says.
`workflow explain` and `workflow list` mark those roles. Do not design a
20-wide map onto one.

**Do not write `[workflows.<n>.scheduling]`.** `effect_free`, `retry`, and
`speculative` all parse and are all **refused by validation** — nothing in the
current authority model can prove a role is side-effect free, so the claim is
not accepted. Adding the table only produces a validation error.

Then run the governed pipeline `docs/workflows.md` specifies:

1. **Declare — ONE command, one rollback.** Write the script and the approved
   blueprint to temp files, then:

   ```
   agentstack more workflow declare --name <name> \
     --script /tmp/<name>.js --blueprint /tmp/<name>.blueprint.json \
     --role <role> [--role <role> …] \
     --max-agents <n> --max-wall-seconds <n> --write
   ```

   It stages both files under `.agentstack/workflows/`, adds the
   `[workflows.<name>]` entry, validates, and re-locks — **or rolls every one
   of those back and tells you which step failed.** Do NOT hand-write the
   manifest entry and lock separately: that was six independent writes, and a
   failure partway left a half-declared workflow behind a button the user had
   already approved (F14). Omit `--write` first to see the plan.

   Pass `--blueprint` whenever the workflow came from an approved graph. It
   pins the blueprint beside the script, so the trust review below shows the
   shape the user signed off on — see the F13 note after this list.
2. *(folded into step 1 — `declare` re-locks for you.)* Run `agentstack lock --write`
   by hand only when you edited a declared workflow afterwards.
3. **Trust** the pinned bytes with `agentstack trust .` — review the declared
   roles/ceilings, then pin. Untrusted, the workflow never parses and its name
   is not invocable; a one-byte change re-gates.
4. **Check the cost statically** with `agentstack more workflow explain <name>` —
   ceilings, serial roles, call sites. Spawns nothing.
5. **Run** with `agentstack more workflow run <name>` (invoker input via
   `--args-json '<json>'`); read the evidence tree with `agentstack more workflow
   report <run-id>`.

### The second gate shows the graph now — but it is still yours to frame (F13)

Approving the blueprint and trusting the script are two consents, and the
second one is the one that actually authorizes execution. They are no longer
independent: passing `--blueprint` to `declare` pins the approved graph beside
the script, so `agentstack trust .` renders the pattern and every node's
role/model/effort right above the roles and ceilings, and changing **either**
artifact re-gates the project. Admission verifies the blueprint pin too — a
graph swapped after consent refuses the run, it does not warn.

What that binding does NOT do, and you must not imply otherwise: **nothing
checks that the script implements the graph.** That is still your faithfulness.
So before `agentstack trust .`, tell the user in one short message:

- that this is the script you compiled **from the blueprint they approved**,
  and the review will show that graph back to them;
- what the graph could not show — the actual prompts, and any place you had to
  deviate (if you deviated at all, you should have re-emitted the blueprint
  instead, per the faithfulness rule);
- that the gate reviews **the bytes as well as the shape**, so skimming the
  script is not the same as having approved the graph.

Never present it as "just confirm again". A consent gate that reads as
redundant gets clicked through, and then it protects nothing.

### If a step fails, leave nothing behind (F14)

`declare` is a transaction: on any failure it rolls back the script, the
blueprint, and the manifest entry, and its error names the step that failed.
Report that message; do not attempt your own cleanup, and do not retry blindly
— a rolled-back declare means the project is already as it was.

`trust` and `run` come after, and neither writes project files, so a refusal
there leaves nothing to undo. If you need to remove a *successful* declare,
`agentstack more restore --last --write` reverts it as one entry.
3. Offer the next move: fix and retry, or re-open the blueprint for editing.

A half-written manifest plus an orphan script is worse than a clean refusal —
it leaves the project in a state the user never approved and cannot easily
name.

A minimal end-to-end anchor:

```toml
# .agentstack/agentstack.toml
[workflows.repo-audit]
path = "./workflows/repo-audit.js"
roles = ["reviewer", "synthesizer"]   # MANIFEST = admitted authority set
max_agents = 25
max_wall_seconds = 1800
```

```js
// .agentstack/workflows/repo-audit.js
export const meta = {
  name: 'repo-audit',
  roles: ['reviewer', 'synthesizer'],  // must be a SUBSET of the manifest roles
}
const found = await pipeline(
  args.files,
  f => agent(`Scan ${f} for correctness bugs. Findings only.`, { role: 'reviewer' }),
)
return await agent(`Dedupe and rank by severity:\n${found.filter(Boolean).join('\n')}`,
                   { role: 'synthesizer' })
```

Provision each role's `[profiles.<role>]` first — see `orchestrate-workflow`
§1–2 for **defining `[profiles.<role>]` only**; ignore its executor/Docker
framing. Here agentstack's own `workflow run` is the executor, not an external
loop.

**Faithfulness rule.** If compilation forces any deviation from the approved
shape (a pattern that won't express cleanly, a role you can't back with the
declared model, a ceiling that won't fit), **do not silently diverge** — say
what changed and why, re-emit a corrected `agentstack-blueprint` block, and wait
for re-approval.

## 5 — Honesty notes (say these, don't hide them)

- The graph is your **declared intent**, not an engine-verified plan. A truly
  dynamic script could diverge from the drawn shape; v1 scopes review to
  blueprint-declared workflows.
- `model`/`effort` are **advisory in v1** — reconciled via the profile you pick,
  not yet enforced per node by the engine.
- There is **no integrity binding** in v1 between the drawn blueprint and the
  executed script beyond your faithfulness. Keep the run true to what was
  approved.

## Rules

- One blueprint, then silence — never author or run before an explicit approve.
- Re-emit the **whole** blueprint on every edit; the graph re-renders from it.
- Symbolic fan-out only; a fabricated concrete count is a bug, not a detail.
- Never let the workflow agents edit the manifest or library — provision the
  role profiles before the run (`orchestrate-workflow` §1–2, profile definition
  only).
