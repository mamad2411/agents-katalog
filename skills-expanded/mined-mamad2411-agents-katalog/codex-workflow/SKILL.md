---
name: codex-workflow
description: >-
  Author and run a custom Workflow (the Workflow tool's agent()/pipeline()/parallel()
  orchestration, a.k.a. "ultracode") that BLENDS Codex headless (`codex exec`) nodes
  into otherwise-Claude orchestration — for cross-model adversarial verification, judge
  panels with a Codex juror, and second-opinion generation. This is "Pattern A": the
  orchestration logic stays in Claude's Workflow JS, and selected nodes shell out to a
  genuinely different model family (the Codex CLI / GPT) to catch correlated Claude
  failure modes. Use this skill whenever the user asks to run a task as a "custom workflow
  using codex", "a workflow that mixes in codex", "blend codex into a custom workflow",
  "cross-model verify while orchestrating", "have codex verify/double-check the findings",
  "use codex as a verifier/juror/second opinion in the workflow", "Claude and codex both
  in one workflow", or any equivalent phrasing. Trigger even when the user only implies it
  — if they want a Workflow AND a second model family in the loop, this is the skill. Do
  NOT use it for a pure single Codex handoff (use a dedicated codex handoff command/agent
  instead), for codex image generation, or for a plain Claude-only Workflow with no second
  model.
---

# Codex-in-Workflow (Pattern A)

Authoring custom Workflows with the **Workflow** tool (`agent()`, `pipeline()`,
`parallel()`, `phase()`, schemas, loop-until-dry, etc.) is assumed knowledge. This
skill is the know-how for **mixing Codex headless into one** so that the
orchestration stays Claude's but selected nodes run on a *different model family*.

## Mental model

A Workflow's `agent()` normally spawns a **Claude** subagent. Pattern A keeps
every orchestration primitive exactly as-is and only changes *who does the work
at chosen nodes*: a "codex node" is a normal `agent()` whose subagent does nothing
but shell out to `codex exec` and relay its output back.

```
Workflow (Claude JS orchestration)
 ├─ find / generate ............... Claude agent()  ← Claude is broad, fast, cache-warm
 └─ verify / judge / 2nd-opinion .. codex node      ← GPT, independent failure modes
```

The value is **diversity, not replacement.** Two model families disagree in
different places, so a Codex verifier catches Claude's *correlated* false
positives (and vice versa) in a way that N more Claude verifiers cannot. The
single highest-ROI use is **adversarial verification**: Claude finds, Codex
tries to refute.

## Prerequisites — preflight before trusting any codex node

This skill assumes the Codex CLI is installed and authenticated in the
environment running the Workflow. Do NOT assume a specific version or default
model — confirm them, because they change between installs. Run the **preflight**
(CLI present, auth live, structured-output path works) from
`references/codex-headless.md` once before relying on any node; if it errors on
auth, the user must `codex login` (interactive) — that cannot be done headlessly.

## Step 0 — should this task even use Codex?

Don't bolt Codex on for its own sake; each node costs a separate Codex/OpenAI run
plus a Claude wrapper turn. Route a node to Codex only when a *second, independent
model* materially de-risks the result:

- **Yes:** verifying findings/claims, judging candidates, an independent attempt
  in a diverse panel, sanity-checking a risky Claude conclusion.
- **No / don't blend when:**
  - it's bulk throughput work (Claude subagents are cheaper, faster, cache-warm);
  - it's a **correlated check** — Codex would only re-derive from the *same*
    evidence Claude already used, with no independent angle (an echo, not a
    second opinion);
  - it's a **blind check** — the node can't give Codex what it needs to verify
    independently (no files/tools in read-only, and the evidence isn't inline);
  - there's no verifiable/judgeable artifact (pure open-ended ideation) —
    diversity adds noise, not signal.

If none of the **Yes** cases apply, skip the skill and ship a plain Claude Workflow.

## The codex node (the core mechanism)

In `exec` mode the Codex CLI runs non-interactively with approvals disabled, and
`-s read-only` stops the *model* from writing to your workspace — so a verify/judge
node has no model-driven side effects on your files (Codex still writes its own
session files and the `-o` output file; that is expected). The node writes both
the task and the schema to temp files *inside the subagent*, runs Codex read-only,
and relays the clean `-o` output file.

> **Why self-contained:** a Workflow script's JS body has **no filesystem
> access** — it can't write the schema file itself. So the node embeds the
> schema as a string and the (Bash-capable) wrapper subagent writes it. One
> `schema` object is the single source of truth: `JSON.stringify` feeds Codex's
> `--output-schema`, and the same object is passed to `agent()` for re-validation.

The helper's **contract** (the full copy-paste implementation lives canonically at
the top of `references/workflow-templates.md` — paste it once near the top of your
script):

```
codexNode(taskText, { schema, sandbox='read-only', model, cwd, effort, revalidate=true, phase, label, timeoutMs=1200000 })
  → Promise<parsedObject>
```

- **taskText** — the verify / judge / generate prompt for Codex.
- **schema** — a JS JSON-Schema object, the single source of truth: feeds Codex's
  `--output-schema` AND (when `revalidate`) re-validates the result in `agent()`.
- **cwd** — optional working root (`-C`) so Codex can read files itself (variant
  below). **effort** — optional reasoning-effort knob (`-c model_reasoning_effort`;
  ladder `low`→`xhigh`, plus `max` on all GPT-5.6 tiers and `ultra` on
  Sol/Terra). **model** — optional model override (`-m`; use fully-qualified tier
  IDs like `gpt-5.6-sol`/`-terra`/`-luna`). Both are open, per-node choices — see
  "Picking tier & effort per node" below.
- **timeoutMs** — watchdog deadline for the codex run: default 1200000 ms
  (20 min), and `ultra` nodes default to 1800000 (30 min); non-finite or
  non-positive values fall back to the default. The helper always launches
  codex as a **background** Bash call with an in-snippet watchdog (TERM to
  codex and its children at the deadline, KILL 10 s later, plus an exit trap
  that repeats the escalation if the Bash task is cancelled mid-run)
  — the foreground Bash cap is 10 min (default 2 min, which kills anything
  beyond a routine verify and fabricates `_codex_error`), while measured
  real-task runs reach ~8–17 min at high efforts.
- **returns** a parsed object matching `schema`, or `{ _codex_error: true }` on
  failure (always filter that out before aggregating — see codex-headless.md).
  Internally re-validation uses a `{ result: anyOf[schema, sentinel] }`
  envelope, unwrapped before return: the sentinel must survive
  `revalidate: true`, and Anthropic's tool input_schema rejects top-level
  `anyOf`/`oneOf`/`allOf` (400), so the union nests one level down.
- **invariant** — self-contained: the Bash-capable subagent writes schema + task
  to temp files because Workflow JS has no filesystem.

Three rules are load-bearing (they are the actual teaching — keep them in any copy
of the helper):

1. **"Relay, not solver."** The wrapping Claude subagent is smart and will be
   tempted to just answer the question itself — which silently turns the
   "cross-model" node back into a Claude node. The prompt forbids this
   explicitly; keep that instruction at full strength.
2. **Extract from the `-o` file, not stdout.** Codex prints its final message to
   stdout but also writes session headers/logs around it; `-o "$OUT"` is the one
   reliable clean-JSON path. Redirect codex's own stdout/stderr to `/dev/null`
   and `cat "$OUT"`.
3. **Pass the prompt via stdin (`- < "$TASK"`), not as a shell argument.** Task
   text contains quotes, `$`, and backticks that would break or expand inside a
   double-quoted arg. The helper writes the task to a temp file via a single-quoted
   heredoc with a collision-proof delimiter, then pipes it via stdin — quoting- and
   injection-proof even for untrusted task text.

`revalidate: true` (the default) re-validates Codex's JSON and returns a parsed
object — best for small structured payloads (verdicts, scores), immune to schema
drift. For large structured outputs, set `revalidate: false` and `JSON.parse` the
relayed string yourself (Codex's own `--output-schema` still enforces shape) —
concrete snippet in `references/workflow-templates.md`.

### Variant: let Codex read the files itself

The embedded-prompt node above is right for **self-contained** claims. When the
thing to verify *is* large — a big diff, several source files, a long doc — don't
paste their contents into `taskText`. Instead point Codex at them: set `cwd` so
Codex's working root (`-C`) is the target tree, and name the files in the prompt
("Verify the auth check in `src/auth.ts` and `src/session.ts`"). `-s read-only`
blocks writes, **not reads**, so Codex opens and reasons over the tree under the
same no-write guarantee — and the wrapper prompt stays tiny regardless of file
size. This is the biggest generality unlock: it extends Pattern A to large-context,
multi-file verification with no new machinery.

## Routing: Codex node vs Claude node

| Node's job | Run it on | Why |
| --- | --- | --- |
| Find / generate / explore breadth | **Claude** | fast, cache-warm, cheap fan-out |
| Adversarially verify a finding | **Codex** | independent family kills correlated false positives |
| Judge / score candidates | **Codex** (or mixed panel) | a juror that didn't write the candidate |
| One attempt in a diverse panel | **mix** | genuine solution diversity, not reworded Claude |
| Synthesize / decide / write-up | **Claude** | holds the orchestration context |

### Picking tier & effort per node

Once a node routes to Codex, *which* Codex is a second, per-node decision — and
it is deliberately left open: match the tier and effort to what the node is for.
The GPT-5.6 generation names its tiers (`gpt-5.6-sol` flagship / `gpt-5.6-terra`
balanced / `gpt-5.6-luna` fast-cheap), and the effort ladder runs
`low`→`xhigh` plus `max` (all tiers) and `ultra` (Sol/Terra only — maximum
reasoning with automatic sub-agent delegation). A structured verify is a few K
tokens — cents even at flagship rates — so the high end is a real option, not
an emergency lever. Typical shape:

- wide verify/judge fan-outs → `gpt-5.6-luna`/`gpt-5.6-terra` at `low`/`medium`
  (compounds across the fan-out);
- a load-bearing verdict — deep judge, risky-conclusion cross-check →
  `gpt-5.6-sol` at `high`/`xhigh`, or `max` when it matters most;
- `ultra` → the strongest, longest option: at most one deliberate cross-check
  per run — a knowing exception to "keep Codex nodes SHORT" (below), trading one
  held slot for the strongest verdict — or a Pattern B worker; never a wide
  fan-out (it holds a slot and burns quota fast).

Mind the clock as much as the cost: runtime scales with tier × effort as
steeply as depth does. Measured on real tasks, sol runs ~8 min at `max` and
~14–17 min at `xhigh`/`ultra` — which is why the helper runs every codex node
as a background Bash call with a generous watchdog deadline (20 min default,
30 at `ultra`; see the `timeoutMs` bullet above), and why a held slot at
`ultra` is a real price.

Tier table, caveats (fully-qualified IDs on ChatGPT auth, ~372K effective
context), and the full ladder: `references/codex-headless.md` → "Model tiers &
reasoning effort".

## Concurrency & cost — keep Codex nodes SHORT

Each codex node **holds a Workflow concurrency slot** (cap = min(16, cores−2))
for Codex's *entire* runtime, with the Claude wrapper sitting idle on a blocking
Bash call. So:

- Use Codex nodes for **short** work — verify, judge, small generation
  (read-only). A routine structured verify at `low`/`medium` returns in seconds
  to a couple of minutes; at flagship tier × high effort it is minutes-to-tens-
  of-minutes (measured: sol@`max` ~8 min, sol@`xhigh`/`ultra` ~14–17 min).
- **Set real timeouts.** A foreground Bash call defaults to a 2-minute timeout
  and caps at 10 — enough only for routine verifies; a timeout kill surfaces as
  a fake `_codex_error`. The helper therefore runs every codex node as a
  background Bash call with a watchdog deadline (`timeoutMs`, default 20 min;
  30 at `ultra`).
- **Never** put a long multi-minute Codex *implementation* inside a Workflow
  node — it starves the slot pool while idling. That is Pattern B (below).
- Many short codex nodes simply queue at the cap; that is fine.
- Billing is on two surfaces (the Anthropic wrapper turn + the Codex/OpenAI run).
  The wrapper only relays, but it still pays a subagent's fixed overhead, so don't
  fan out hundreds of codex nodes casually.
- Verifying/judging **many small items**? Use the **batch codex node** (one Codex
  run for N items, keyed by id) in `references/workflow-templates.md` to amortize
  the slot + run; fan out (Template 1) only when each item needs a fresh context.

## Sandbox tiers

- `read-only` (default): verify, judge, read-and-reason. No writes, no approvals.
  Note it still grants disk **reads** — that is what makes the `cwd`/`-C` variant
  cheap for large-context verification.
- `workspace-write`: Codex may edit files in cwd. Use for generation that emits
  files; combine with `isolation: 'worktree'` on the node if several run in
  parallel and could collide.
- `--dangerously-bypass-approvals-and-sandbox`: full, unsandboxed. Only for
  trusted headless harnesses (this is what the background pool in Pattern B
  uses). Avoid inside Workflow nodes unless genuinely required.

## Worked patterns

Brief shapes below; full copy-paste scripts (and the canonical `codexNode` helper)
are in `references/workflow-templates.md` (read it before writing the script).

**Find → Codex-verify (pipeline, the default):** Claude finders fan out, each
finding is verified by a Codex node as soon as it is found — no barrier.

```js
const results = await pipeline(
  DIMENSIONS,
  d => agent(d.findPrompt, { phase: 'Find', schema: FINDINGS }),         // Claude
  review => parallel((review.findings ?? []).map(f => () =>
    codexNode(`Adversarially verify, defaulting to refuted=true if uncertain:\n${f.title}\n${f.detail}`,
      { schema: VERDICT, phase: 'Verify', label: `codex:${f.id}` })
      .then(v => ({ ...f, verdict: v })))),
)
const confirmed = results.flat().filter(Boolean)
  .filter(f => f.verdict && !f.verdict._codex_error && !f.verdict.refuted)
```

**Judge panel with a Codex juror:** generate N attempts (some Claude, optionally
one Codex), then score each with a mixed jury so no model only judges itself.

**Cross-check a single risky conclusion:** one Codex node that tries to refute
Claude's headline finding before reporting it.

**Loop-until-dry with a Codex gate:** iterate find → Codex-verify until a round
adds no new *confirmed* findings (Template 4) — for thorough audits.

## When it's NOT Pattern A — escalate

- **Long / parallel Codex *workers* (minutes–hours, resumable)** → do not force
  them through Workflow. Use a background process pool: launch
  `codex exec … --dangerously-bypass-approvals-and-sandbox &`, cap a few at a
  time, poll, and `codex exec resume --last`. See the "Pattern B" section of
  `references/codex-headless.md` for a self-contained reference implementation.
- **One autonomous Codex objective** (implement this whole thing) → hand it to a
  dedicated single-shot Codex handoff command or agent if one is installed (for
  example a `codex-rescue`-style agentType that forwards to the Codex runtime),
  rather than wrapping a long run in a Workflow node.

## codex exec flags (the load-bearing few)

`-s/--sandbox <read-only|workspace-write|danger-full-access>` · `--output-schema
<FILE>` · `-o/--output-last-message <FILE>` (clean final JSON — use this) ·
`--skip-git-repo-check` · `-m/--model` (fully-qualified tier IDs, e.g.
`gpt-5.6-sol`/`-terra`/`-luna`) · `-C/--cd <DIR>` (let Codex read a tree) ·
`-c model_reasoning_effort="…"` (`low`→`xhigh`, plus `max` on all GPT-5.6 tiers
and `ultra` on Sol/Terra — trade depth for speed, per node). Full annotated table (plus `--json`,
`resume`, image, gotchas, **troubleshooting**, the tier table) in
`references/codex-headless.md`.

## Verify your blend before trusting it

Beyond the preflight, sanity-check a *real* verdict-shaped command once before
relying on a codex node in a run (cheap, de-risks quoting/auth/sandbox):

```bash
OUT=$(mktemp); SCH=$(mktemp)
printf '%s' '{"type":"object","additionalProperties":false,"required":["refuted","reasoning"],"properties":{"refuted":{"type":"boolean"},"reasoning":{"type":"string"}}}' > "$SCH"
codex exec --skip-git-repo-check -s read-only \
  --output-schema "$SCH" -o "$OUT" \
  "Adversarially verify, defaulting to refuted=true if uncertain: 2+2=5" </dev/null >/dev/null
cat "$OUT"   # expect schema-valid JSON, e.g. {"refuted":true,...}
# </dev/null: with a positional prompt, codex still reads stdin — closing it
# stops the snippet from hanging on "Reading additional input from stdin" in
# non-interactive shells (CI, pipes). The codexNode helper avoids this by
# passing the prompt via stdin (- < "$TASK") instead.
```

If that returns clean JSON, the node will too. Then run the Workflow.

## Additional resources

- **`references/codex-headless.md`** — `codex exec` flags, sandbox tiers, output
  extraction, blending gotchas, the preflight, troubleshooting, the `_codex_error`
  discipline, and escalation patterns (B/C).
- **`references/workflow-templates.md`** — the canonical `codexNode` helper plus
  complete copy-paste Workflow scripts: cross-model review, mixed judge panel,
  single-conclusion cross-check, and loop-until-dry; with batch-node and
  large-payload variants.
