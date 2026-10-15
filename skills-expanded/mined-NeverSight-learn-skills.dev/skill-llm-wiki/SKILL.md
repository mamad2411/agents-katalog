---
name: skill-llm-wiki
description: Use when the user explicitly asks to build, extend, validate, repair, rebuild, or merge an LLM-optimized knowledge wiki from markdown notes, documentation, source code, or mixed folders. Default output is a single stable sibling `<source>.wiki/` with full history in a private git repo under `.llmwiki/git/`; `--layout-mode in-place` transforms the source folder itself, and `--layout-mode hosted --target <path>` honours a user-provided `.llmwiki.layout.yaml` contract. SKILL.md is the entry point; detailed operation instructions are loaded on demand from `guide/` per the routing procedure below.
format_version: 1
---

# skill-llm-wiki

## ⚠ Read only SKILL.md and the specific `guide/` files it points to

**Hard rule:** SKILL.md is your entry point. You may additionally read files inside the `guide/` subdirectory of this skill, but **only** those the routing procedure explicitly names for the current operation. Never read anything else in this skill directory: never open `README.md`, never open files under `scripts/`, never open `LICENSE`, never open `guide/` files the routing did not activate, never open arbitrary files out of curiosity. Never `cat` / `head` / `tail` / `Read` a file just to see what's in it.

Scripts under `scripts/` are tools, not references. They are invoked via `node scripts/cli.mjs <subcommand>` exactly as documented in `guide/cli.md`. Never read their source. Never import from them. Never inspect their internals — everything a script does that you need to know is in `guide/cli.md`.

**Why this matters.** Every byte you read is a token spent. This skill is deliberately split so you read only the slice you need for the operation at hand. A typical Validate reads ~18 KB; a typical Build reads ~32 KB; a question about what this skill does reads just this file (~12 KB). Respect the budget.

## ⚠ Preflight: verify Node.js is installed

Before the first `node scripts/cli.mjs` invocation of any operation, run this via the Bash tool:

```bash
node --version 2>/dev/null || printf '%s\n' '__NODE_MISSING__'
```

**Interpret the single line of output:**

- **`__NODE_MISSING__`** — Node.js is not installed. Read `guide/ux/preflight.md`, pick the "Case A" message, and relay it verbatim to the user. **Stop the operation.** Do not attempt any `node scripts/cli.mjs` command. Do not try to install Node yourself.
- **`v<N>.x.x` where N < 18** — Node.js is too old. Read `guide/ux/preflight.md`, pick the "Case B" message, substitute the version string, and relay it verbatim. **Stop the operation.**
- **`v<N>.x.x` where N ≥ 18** — preflight passed. Proceed.

Preflight runs at the start of every operation. Never cache, never skip, never wrap in extra logic. `scripts/cli.mjs` also performs a runtime check and exits with code 4 if invoked on an unsupported Node — defense in depth only; always run the Bash preflight first so the user sees the detailed install/upgrade message from `guide/ux/preflight.md`.

## What this skill does

Builds and maintains **LLM wikis**: filesystem-based knowledge stores structured for deterministic, token-efficient retrieval by a language model. Six operations: **Build**, **Extend**, **Validate**, **Rebuild**, **Fix**, **Join**. Three layout modes:

- **`sibling` (default)** — writes to a stable sibling `<source>.wiki/`. One wiki, one sibling directory, forever. Prior states are reachable as git tags (`pre-op/<id>`, `op/<id>`) in the private repository at `<wiki>/.llmwiki/git/`. No `.llmwiki.v<N>` versioned directory proliferation.
- **`in-place`** — the source folder IS the wiki. `<source>/.llmwiki/git/` is created inside the source; the `pre-op/<first-op>` snapshot captures the user's original content byte-for-byte; rollback restores the original tree exactly. Runs only when the user passes `--layout-mode in-place` explicitly — never inferred, never substituted.
- **`hosted`** — writes to a user-chosen path that carries a `.llmwiki.layout.yaml` contract. The user passes `--layout-mode hosted --target <path>`.

Every operation is a git sequence: `preflight → pre-op snapshot → phase commits → validation → commit-finalize`. Rollback, diff, log, blame, reflog, history, and remote mirroring are first-class skill subcommands under `node scripts/cli.mjs <subcommand>`. Everything is explicit-invocation only — no hooks, no watchers, no automation.

**Ambiguous invocations refuse and prompt.** If the user's request could mean two things (a default sibling would stomp on a foreign directory, a hosted target has no contract, `--layout-mode in-place` is combined with `--target`, …), the CLI exits with code 2 and a structured `INT-NN` error rather than guessing. See `guide/ux/user-intent.md` for the full list.

## Integrating another skill or agent as a consumer

If the user is building a skill, agent, or CI job that calls this skill programmatically (rather than asking you to build a wiki for them in this session), route them to `guide/consumers/index.md`. That subtree answers: how to gate on `format_version`, how to `init` a topic wiki in one command, how to `heal` after every leaf write, how to detect the skill-absent case, how to write consumer tests against the shipped `scripts/testkit/` helpers. Every consumer recipe is dispatched from `guide/consumers/index.md`; do not re-derive the integration path from SKILL.md alone.

Quick probe summary: `skill-llm-wiki contract --json` returns `format_version` + the full CLI + frontmatter schema, and `skill-llm-wiki where --json` returns absolute install paths. Both are exempt from the runtime-dep preflight so consumers can probe before the skill is fully set up.

## Non-automation contract

This skill has **no hooks, no filesystem watchers, no PostToolUse listeners, no install-time wiring, no background processes**. Every action happens only in direct response to an explicit user request against an explicit target directory. If the user did not ask, do nothing. Do not propose automation. Do not create hooks. Do not schedule anything.

If the user hand-edits a wiki and indices go stale, nothing happens until they explicitly ask you to refresh it — at which point you run the operation they request.

## ⚠ Agent delegation contract

**Every wiki operation runs in a dedicated sub-agent, not inline in the current session.** This is a hard rule, not an optimisation.

When the user asks for any of the six operations (Build, Extend, Validate, Rebuild, Fix, Join), you do **not** execute `node scripts/cli.mjs <operation> ...` directly from the main chat. Instead:

1. **Resolve the ask** — pin down the operation, source, target, layout mode, and any constraints. Prompt the user to disambiguate where needed (see `guide/ux/user-intent.md`).
2. **Run the Node.js preflight** in the main session — this is cheap, produces a tiny output, and must happen before any agent is spawned so the user sees the detailed install/upgrade message on failure. Preflight failures stop the operation; do not spawn an agent.
3. **Spawn a dedicated "wiki-runner" sub-agent** via the host harness's sub-agent dispatch primitive (Claude Code: `Agent` tool; Codex CLI: equivalent; see the [`subagent-dispatch-v1`](https://github.com/ctxr-dev/kit/blob/main/docs/subagent-dispatch-v1.md) spec) with a self-contained prompt describing: the operation, the resolved CLI invocation, the activated `guide/` leaves by filename, any quality-mode / layout-mode flags, and the completion criterion. The sub-agent runs the CLI, handles Tier 2 sub-delegations, manages its own context, and reports back a summary when done.
4. **Relay the sub-agent's summary** to the user. The main session never loads the wiki's content into its own context window.

### Why

Wikis can be any size: a 10-entry notes folder or a 10,000-entry knowledge base. A Build that drafts frontmatter for a prose-heavy 10k corpus can run the host LLM against thousands of entries in Tier 2. Running all of that inline in the main session would consume the user's context budget on content they never asked to see, and would leave no room for continued conversation. The wiki-runner sub-agent has its own context window; the main session's budget stays lean for the user's ongoing chat.

### What the wiki-runner sub-agent is responsible for

- **Executing the CLI subcommand** and streaming progress back periodically (don't spam every phase — one line per phase is plenty).
- **Its own context-window hygiene.** The sub-agent monitors its remaining budget and auto-compacts when it approaches the limit. See `guide/isolation/scale.md` "Context-window management in the wiki-runner" for the protocol — the short version is: phase commits in the private git are the durable checkpoint, so the sub-agent can safely drop its conversation history of prior phases and re-read only what the next phase needs.
- **Handling the Tier 2 exit-7 handshake.** The skill's CLI runs under Node and cannot spawn sub-agents directly. When the operator-convergence phase accumulates Tier 2 requests (cluster naming, mid-band merge decisions, `propose_structure` whole-directory asks, `nest_decision` gate decisions, …) the CLI writes them to `<wiki>/.work/tier2/pending-<batch-id>.json` and exits with code **7** (`NEEDS_TIER2`). Each pending request follows the [`subagent.dispatch.v1`](https://github.com/ctxr-dev/kit/blob/main/docs/subagent-dispatch-v1.md) shape (`prompt`, `inputs`, `effort`, optional `model`, `response_schema`, `outputs_path`) so any Agent Skills harness can service it. Exit 7 is **not a failure**, it is the suspend-and-resume signal. The wiki-runner must:
    1. Detect exit 7 from the CLI.
    2. Read every `pending-*.json` file under `<wiki>/.work/tier2/`.
    3. Service each request (see "Inline servicing vs fan-out" below).
    4. Collect each sub-agent's structured JSON response.
    5. Write the merged results to `<wiki>/.work/tier2/responses-<batch-id>.json` (one file per pending batch, matching batch ids).
    6. Re-invoke the CLI with the same positional args. The orchestrator seeds the responses into the tiered decision map at resume and continues from the last committed iteration.
    7. Loop if the re-invocation produces another exit 7 (deeper sub-clusters, remaining directories, or additional `propose_structure` asks generated after an early NEST). Terminate on exit 0 (complete) or any other non-zero code (real failure — surface to the main session).

#### Inline servicing vs. fan-out

The wiki-runner chooses **inline** or **fan-out** servicing based on the batch size. The skill CLI's wire protocol is identical either way — pending files in, response files out, exit 7 between — so the choice is entirely a context-budget and throughput call that the wiki-runner makes at runtime:

- **Inline (≤ ~50 requests per batch).** The wiki-runner answers every request directly, reasoning as the Tier 2 worker itself. No child sub-agent dispatch per request. Each request's `prompt`, `inputs`, `response_schema`, `effort` (with optional `model` override) are visible to the wiki-runner, which writes the JSON response inline. This is the right choice for a typical `build`/`rebuild` against a ~10-50 leaf corpus: batch sizes stay small, fan-out overhead would dwarf the work, and the wiki-runner's own context is plenty for a few dozen frontmatter-blob comparisons. Environment constraint: general-purpose sub-agents in current Agent Skills harnesses (Claude Code, Codex CLI) cannot spawn further sub-agents themselves, so inline servicing is actually the *only* option when the wiki-runner is itself a nested sub-agent, and the skill's design must not require fan-out.

- **Fan-out (> ~50 requests per batch, or mixed `effort`/`model` per request).** The wiki-runner reports the batch size back to the main session, which dispatches one narrowly-scoped sub-agent per request (or per small group of homogeneous requests) via the host harness's sub-agent primitive, passing the request's `prompt`, `inputs`, `response_schema`, `effort`, and optional `model`. The sub-agent sees ONLY those inputs (two frontmatter blobs for a `merge_decision`, a cluster's leaf metadata for a `cluster_name`, a directory's whole leaf list for a `propose_structure`, and so on). Never pass the whole wiki. Fan-out is the right choice for large corpora (thousands of leaves → thousands of draft-frontmatter and merge-decision requests) where inline would burn through the wiki-runner's context.

Either way the skill CLI doesn't change — it always emits pending files and exits 7, and the wiki-runner is free to decide how the actual reasoning happens before the response files appear.

#### Prompt templates per Tier 2 kind

For small-batch inline servicing the wiki-runner can use these ready-made shells. Each returns strict JSON matching the request's `response_schema`; commentary outside the JSON object is a test bug.

`propose_structure`:

````text
You are a Tier 2 sub-agent for skill-llm-wiki acting as a structural optimiser. Answer in STRICT JSON matching the response_schema. Return ONLY the JSON object, no commentary.

Directory: <inputs.directory>
Leaves:
```json
<inputs.leaves array>
```

Your task:
Propose the optimal nested structure for this directory. Group related leaves into named subcategories (slug + purpose + member ids). Leaves that genuinely stand alone should be reported as siblings. You SHOULD favour nesting over flatness whenever 2+ leaves share a defensible conceptual grouping — err on the side of nesting if in doubt.

Response schema:
{
  "subcategories": [ { "slug": "<kebab-case>", "purpose": "<one line>", "members": ["<leaf-id>", ...] }, ... ],
  "siblings": ["<leaf-id>", ...],
  "notes": "..."
}

Return your answer now as a single JSON object.
````

`nest_decision`:

````text
You are a Tier 2 sub-agent for skill-llm-wiki acting as a nesting gate. Answer in STRICT JSON.

Cluster candidates:
```json
<inputs.leaves array>
```

Should these N sibling leaves be grouped together under a new parent subcategory? Answer `nest` if they share a defensible conceptual grouping that would meaningfully improve routing, `keep_flat` if the overlap is incidental and nesting would add noise, or `undecidable` if you cannot tell from the frontmatter.

Response: { "decision": "nest"|"keep_flat"|"undecidable", "reason": "<one line>" }
````

`cluster_name`:

````text
You are a Tier 2 sub-agent for skill-llm-wiki naming a cluster. Answer in STRICT JSON.

Cluster members:
```json
<inputs.leaves array>
```

Return a short kebab-case slug (one or two words, e.g., `history` or `layout-modes`) and a one-line purpose. If the leaves are clearly unrelated, return decision `reject` with a reason.

Response: { "slug": "<kebab-case>", "purpose": "<one line>" } or { "decision": "reject", "reason": "<...>" }
````

- **Reporting completion** with a one-paragraph summary plus the op-id the orchestrator assigned.

### Default model and effort

Unless the user specifies otherwise, the wiki-runner and its Tier 2 fan-outs pick the **most suitable model for the task size** at their default effort level. Concretely:

- **Wiki-runner**: spawned at the sub-agent type that can orchestrate CLI subprocesses and hold the whole operation in its context. For very large corpora (>1k entries or >10 MB) prefer a 1M-context model with high effort (`effort: "heavy"`).
- **Tier 2 draft-frontmatter sub-agent**: picks whatever model the host maps to `effort: "light"`, cost-effective for writing a ~200-word `focus` + `covers[]` pair from a single source file.
- **Tier 2 operator-convergence sub-agent**: `effort: "light"` to `"balanced"` depending on pair ambiguity. The host's mapped model should be strong at structural judgment on frontmatter pairs.
- **Tier 2 rebuild plan review sub-agent**: `effort: "heavy"` because this is the "deep understanding" case.
- **HUMAN-class Fix sub-agent**: `effort: "balanced"` because the decision needs justification.

**User overrides.** If the user specifies a model (`"use sonnet"`, `"use gpt-5-codex"`, `"use opus 1M for the whole thing"`) or an effort level (`"light effort"`, `"maximum quality"`), pass it as the dispatch envelope's optional `model` field and the required `effort` field. The host harness honours the explicit `model` when set; otherwise it maps `effort` to its own model lineup. Honour the override on every sub-agent the operation spawns, not just the wiki-runner. If the user specifies conflicting overrides (e.g., a model that doesn't support the requested effort level), ask before proceeding.

### Inline execution is the escape hatch, not the norm

The only time you run `node scripts/cli.mjs` directly from the main session is for **one-shot read-only probes** that produce tiny output: `--version`, `--help`, `validate <small-wiki>`, `log <wiki>`, `diff <wiki> --op <id> --stat`, `resolve-wiki`. If the probe might return more than a few hundred lines, or if it's a mutation, spawn a sub-agent.

## Layout mode detection

The default is `sibling`. The skill's `intent.mjs` resolver decides the effective mode from the invocation and refuses to guess. Summary of how detection flows for each operation:

- **Build.** If the user passed `--layout-mode <mode>` explicitly, honour it. Otherwise default to `sibling`. If the source already contains `.llmwiki/git/`, the skill refuses with `INT-02` ("this is already a wiki — did you mean extend/rebuild/fix?"). If the default sibling `<source>.wiki/` would land on a foreign non-empty directory, the skill refuses with `INT-01`.
- **Extend / Rebuild / Fix.** Operate on an existing wiki; the layout mode is whichever one the wiki was built under. The resolver reads `<wiki>/.llmwiki/git/` for sibling/in-place and `<target>/.llmwiki.layout.yaml` for hosted.
- **Join.** User-specified `<target>` is hosted if it has a contract, otherwise sibling. Multi-source joins require explicit canonical designation (`INT-07` otherwise).
- **Hosted.** User passes `--layout-mode hosted --target <path>`. If `<target>/.llmwiki.layout.yaml` is missing, the skill refuses with `INT-01b` and asks whether to create the contract or pick a different target.

Never hand-parse the target to guess the mode. Always invoke the CLI with the user's explicit flags and trust the resolver's decision; surface `INT-NN` errors to the user verbatim.

Mode is determined **once per operation**. Never switch modes partway through.

## How to invoke the skill

When the user asks for an operation:

0. **Run the Node.js preflight.** See above. Stop and relay the user-facing message from `guide/ux/preflight.md` if it fails.
1. **Read the ask carefully.** Which operation? What's the source? What's the target? Confirm uncertain details before mutating anything. If the ask is ambiguous (e.g. "migrate my notes", "do it in place", "put it in my memory folder"), prompt the user to resolve the ambiguity before invoking the CLI — see `guide/ux/user-intent.md` for the scenarios that require this.
2. **Identify the exact target.** Never infer a target. Ask if unclear. The default sibling location for `build ./docs` is `./docs.wiki/`.
3. **Decide the layout mode.** See "Layout mode detection" above. Sibling is the default; `in-place` and `hosted` require an explicit `--layout-mode` flag.
4. **Route into `guide/` via its own indices** — see the Routing section below. Read `guide/index.md`, compute the activation set from the user's ask, then read only the activated leaves. Never hand-pick `guide/` files from outside the wiki.
5. **Plan the phases.** Use TodoWrite for long operations so the user can see progress and interrupt if needed.
6. **Start with the lowest-risk phase.** For anything touching an existing wiki, run Validate first and report findings before proceeding to structural changes.
7. **Use the CLI for deterministic phases.** Every subcommand is documented in `guide/cli.md`.
8. **Handle AI-intensive work in your own context.** Drafting `focus` and `covers[]` from prose, classifying with no taxonomy, semantic DECOMPOSE partitioning, AI-ASSIST Fix repairs — these are yours. Read the source files with `Read`, write the frontmatter with `Write`, verify it roundtrips.
9. **Verify before commit.** Always run Validate on the new state before commit. Never leave a wiki in a broken state.
10. **Stop after the requested operation completes.** Do not chain into Rebuild or Fix unless asked. Do not run `shape-check` on wikis the user didn't mention. Do not open sibling wikis for comparison.

## Routing into `guide/`

`guide/` is a real LLM wiki — the same kind of structure this skill builds for users. Claude routes into it via the methodology's standard **semantic routing procedure**, not via a hand-maintained table. This teaches you the routing discipline once so it generalises to any wiki you later operate on.

### The procedure

1. **Build a context profile** from the user's ask. A profile is a small structured object with three fields Claude constructs in its head. These fields shape the *query you formulate semantically* against the wiki — they are no longer used for literal keyword/tag matching against aggregated routing tables.

    - **`keywords`** — tokens from the ask. Include operation names (`build`, `extend`, `validate`, `rebuild`, `fix`, `join`), their common synonyms (`create wiki`, `check wiki`, `repair`, `optimise`, `merge wikis`), subcommand names (`ingest`, `shape-check`), and any other concrete terms the user used. Use these to form the semantic intent you'll match against each entry's `focus`.
    - **`tags`** — short categorical labels Claude derives from the ask:
        - `operation` — set whenever the user is requesting any of the six operations.
        - `hosted-mode` — set when the target is hosted (the mode-detection step decided this).
        - `mutation` — set for any operation except Validate (structural change may happen).
        - `preflight-failure` — set only when the Node.js preflight check actually failed; never by default.
    - **`operation`** — the one operation id the ask is about (`build` / `extend` / `validate` / `rebuild` / `fix` / `join`), or `null` for informational queries. Signals that the operations subtree is in scope.

2. **Read `guide/index.md`.** Parse its frontmatter. The `entries[]` field lists every direct child with `id`, `file`, `type`, `focus`, and any authored `tags`. The parent index also carries an authored `shared_covers` list describing what every child in the subtree has in common — use that as extra context when deciding whether to descend.

3. **Decide which entries are relevant to the current ask.** For each entry, read its `focus` (and lean on the parent's `shared_covers` as shared-subtree context) and make a **semantic** relevance decision: does this entry's purpose overlap with what the user is asking for? A keyword or phrase from the ask appearing in the entry's `focus` is a strong positive signal; semantic similarity to the ask's intent is an equally strong signal even without literal overlap — synonyms and paraphrases count. Be inclusive but not indiscriminate: if an entry's focus is clearly unrelated to the current ask, skip it. There is no literal keyword/tag lookup table to consult; your judgment is the gate.

4. **Descend matched subcategories.** When a matched entry has `type: index`, `Read` its `index.md` and repeat from step 2 at that level. No AND-filter, no cascading activation set — the semantic relevance decision at step 3 is the only gate. For `guide/`, informational queries typically leave the `operations/` subtree unvisited because its `focus` ("the six CLI operations and their phases") doesn't match a question about what the skill does — which is exactly the short-circuit you want.

5. **Load matched leaves.** For each matched leaf entry, `Read` the full leaf file. Once a leaf is open, its own `activation.{keyword_matches,tag_matches,escalation_from}` block (if present) is **supplementary hint data**, not a routing rule: it tells you *why* the author thought this leaf is relevant in certain situations, and can inform follow-up decisions (e.g. "this leaf lists `fix` in its `escalation_from`, so if I'm working on a Fix operation I should probably check whether the neighboring `correctness/invariants.md` is also in scope"). But it is never matched literally to decide whether to load the leaf — that decision was already made at step 3 against the parent's `focus` description.

6. **Preflight failures take a dedicated path.** If the Node.js preflight fails, your context profile is just `tags: [preflight-failure]` with no operation intent. Walk the wiki semantically for the preflight concept: the `ux/preflight.md` leaf's `focus` will be an obvious match (and its parent subcategory `ux/` carries shared covers about user-facing messaging, which reinforces the match). Load exactly that one leaf, relay the appropriate Case message verbatim, stop. Do not load operation leaves.

7. **Informational queries.** When the user asks "what does this skill do?", "explain hosted mode", "what operations exist?", or any other question that does not demand an operation against a target, the semantic decision at step 3 should produce **zero matches** against the root entries[] — their `focus` strings describe "how to do X" subjects, not "what X is" subjects, so they don't overlap with informational intent. **Read nothing from `guide/`.** Answer from SKILL.md alone. The exception is when the user's ask specifically targets a wiki topic ("explain hosted mode", "how does layout contract work") — then descend to that one leaf semantically and read only it.

### Why this is better than a hand-maintained table

- **Self-maintaining.** Adding a new leaf to `guide/` only requires writing its `focus` clearly and placing it under the right subcategory. The routing picks it up on the next `index-rebuild`. No SKILL.md edit required.
- **Each keyword is written once.** The author writes each routing-relevant word exactly once — in the leaf's own `focus` (or optionally in an `activation` hint block, or in the parent's `shared_covers`). The old substrate duplicated every keyword up the narrowing chain into every ancestor's `activation_defaults`, so a single leaf's keyword ended up on three or four indices. The new substrate eliminates that duplication.
- **Semantic matching handles synonyms, paraphrases, and new vocabulary.** The old literal router only matched keywords the author had enumerated. With semantic matching, "blame a line" will reach a leaf whose focus says "inspect per-line authorship" even though the two share no literal tokens. This is how Claude already reasons about everything else in this skill — the router is now consistent with it.
- **Routing aligns with the rest of the skill.** Tier 2 decisions are already semantic (cluster naming, nest gating, `propose_structure`). The router was the last deterministic layer and the aggregation tax it imposed on every index file was the price of that determinism. Semantic routing brings the substrate in line and erases the tax.
- **Teaches a transferable skill.** The procedure you apply to `guide/` is the same one you apply to any LLM wiki — e.g., the user's own `./memory.wiki/` or `./docs.wiki/`. One procedure, infinite wikis.
- **Short-circuits informational queries.** A "what does this skill do?" question produces zero semantic matches at the root and answers from SKILL.md alone. That's still the cheapest path.

### Forbidden shortcuts

- Do not read `guide/` files by hardcoded path from SKILL.md. Always walk the routing procedure.
- Do not read leaves without first reading `guide/index.md` to see their `focus`.
- Do not peek into leaf frontmatter before deciding to match — the root index's entries[] already carries the leaf's `focus` string, which is all you need to decide relevance.
- Do not skip the informational-query short-circuit and preemptively read everything. Every byte costs tokens.

## Common mistakes to avoid

- **Reading `guide/` files by hardcoded path.** Always walk the routing procedure. The routing is the methodology — don't bypass it.
- **Reading any `guide/` file for an informational query.** A "what does this skill do?" ask produces zero semantic matches against the root entries — answer from SKILL.md alone.
- **Peeking at leaf frontmatter before deciding to match.** `guide/index.md`'s `entries[]` already carries each child's `focus` string — that's what you match against. Opening a leaf to read its own frontmatter is a waste: the relevance decision is made at the parent level.
- **Reading scripts as source.** Never. Use them via the CLI subcommands documented in `guide/cli.md` (reached via the routing procedure).
- **Skipping the Node.js preflight.** Runs before every operation, no exceptions.
- **Attempting to install or upgrade Node.js yourself.** Never. On preflight failure, walk the wiki semantically for the preflight concept — `guide/ux/preflight.md`'s `focus` matches — read it and relay verbatim.
- **Writing inside the user's source folder in `sibling` mode.** Never. The source is immutable in sibling mode; all writes go to `<source>.wiki/`.
- **Writing outside the layout contract in `hosted` mode.** The contract is authoritative.
- **Inferring `in-place` mode.** Never. The user must pass `--layout-mode in-place` explicitly; any ambiguity refuses with `INT-02` or `INT-09a`.
- **Writing leaf content into `index.md`.** Index bodies are navigation only. Leaf content belongs in leaf files.
- **Proposing automation.** No hooks, no watchers, no schedules. Every action is an explicit user request.
- **Running operations the user didn't ask for.** Don't chain Rebuild after Validate unless asked.
- **Mixing layout modes in one operation.** Resolved once by `intent.mjs`, honored for the whole operation.
- **Re-reading the same `guide/` file mid-operation.** Once per operation is enough.
