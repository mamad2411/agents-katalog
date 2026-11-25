---
name: storozh
description: Advisory semantic guard over a changeset manifest before it lands in shared state. Use after a multi-repo session produces a changeset-manifest (mirabilis C1) and before the co-sign push gate — classify each unit's routing against the darwin routing-policy (C3) and NLI-check each unit against the shield corpus (claims + invariants + lessons + memory) for contradiction or duplication. Flags, never blocks — the owner and Claude co-review the flags and decide.
---

# Storozh: an advisory semantic guard, not a gatekeeper

BLUF: the cheapest moment to land a misrouted unit or a unit that contradicts an existing claim/invariant is the push — structural checks (shield `scripts/boot.py` + SHACL `ontology/shapes.ttl`) already catch *structural* contradictions (shape violations, malformed triples), but they cannot see that a new lesson *semantically* negates an existing one in prose. Storozh adds the SEMANTIC NLI layer on top of that structural layer — it is not a duplicate of boot.py/SHACL, it is the complement. It reads a changeset manifest, classifies routing, retrieves the nearest existing corpus items by embedding, and asks an NLI judge whether each unit contradicts / duplicates / is fine. Every result is a **flag appended to the manifest** for owner+Claude co-review. Storozh decides nothing; it surfaces.

This is a PROTOCOL the agent follows by hand (Read + the localllm tools), not a hook. There is no enforcement exit code — the gate is the co-sign markers (`auto-critic.sh`, C2); storozh only informs the co-signers.

## Stage 0 — BLUF and inputs

State up front, in one or two lines: how many units the manifest carries, and the headline flag count (`N misroute, N contra, N dup` or `all ok`). The co-reviewer reads this line first and decides whether to drill in.

Input is a **changeset manifest** (C1, produced by mirabilis, written to a host-visible `~/.claude` path both storozh and the gate can read):

```
{ sessionId, timestamp,
  repos: [ { name, dir, diff, files: [path] } ],
  session: { transcriptMinusTools } }
```

`transcriptMinusTools` is the session `.jsonl` with `tool_use`/`tool_result` entries stripped, keeping user prompts + assistant text. A **unit** is one logically-coherent changeset item derived from the manifest (a single lesson, invariant, skill, agent, hook, sandbox-mechanism, genome edit) — typically one per changed protocol artifact or one per coherent diff hunk. Read the manifest before classifying; do not infer units the diff does not contain.

## Stage 1 — routing-check (declarative, vs C3)

For each unit, classify its **type**, then compare the type's target repo against the darwin routing-policy (C3, the lane-map gene). This is **declarative only** — read the unit's type from what it is, do not infer routing from diff content cleverness.

| unit-type | target repo (C3) |
|---|---|
| `lesson`, `invariant` | shield (`alpha_S`) |
| `skill`, `agent`, `hook` | neuro-matrix (`alpha_N`) |
| `sandbox-mechanism`, `state` | mirabilis (`alpha_M`) |
| `genome`, `meta` | darwin (`alpha_Gamma`) |

If the unit's actual landing repo (`repos[].name` it appears under) differs from its type's target repo → flag `misroute` with `{unit, observed-repo, expected-repo}`. A misroute is the single most common composition failure across parallel slices (a lesson written into neuro-matrix instead of shield); catching it here is the point.

Repo→lane is also from C3 and frames the flag's urgency, not its truth: `mirabilis, neuro-matrix = code-lane` (PR+CI; CI green-gate BYPASSED this session); `darwin, shield = knowledge-lane` (push + storozh). A misroute that crosses lanes (a knowledge-lane unit sitting in a code-lane repo) is the higher-severity flag.

## Stage 2 — contra-check (semantic NLI over the shield corpus)

For each unit, run a three-step retrieve-then-judge:

1. **Embed** the unit's text via mirabilis localllm Embeddings (C5):
   `Embeddings(ctx, text string) ([]float32, error)` → `POST http://host.docker.internal:1234/v1/embeddings` (mirrors the existing `Complete()` adapter in `mirabilis/internal/engine/localllm/completer.go`). Embed the unit's normative content (the lesson/invariant/claim statement), not the surrounding diff noise.

2. **Retrieve top-k** nearest items from the shield corpus by cosine similarity over the embeddings. The corpus is:
   - `SolitaryEquilibriumShield/claims/claims.ttl` (RDF claims),
   - `SolitaryEquilibriumShield/invariants` (invariant statements),
   - `SolitaryEquilibriumShield/lessons` (distilled lessons),
   - `SolitaryEquilibriumShield/memory` (persisted memory).
   k is small (3–5); the goal is the few items most likely to clash, not a full scan.

3. **NLI-judge** each (unit, retrieved-item) pair via localllm completion (`Complete()`, `POST .../v1/completions`). Prompt the judge for a single label per pair:
   - `contra` — the unit semantically negates / reverses the retrieved item (entailment of the negation).
   - `dup` — the unit restates an item already in the corpus (no new information; candidate for drop-or-merge).
   - `ok` — neither; the unit is novel and consistent.

   The unit's flag is the strongest label across its pairs: any `contra` → `contra`; else any `dup` → `dup`; else `ok`.

Why this is not a duplicate of the structural layer: shield boot.py + SHACL validate that triples are well-formed and satisfy the shapes graph — a structural contradiction is a shape violation. They do NOT read prose for *meaning*. «Always prefer fresh session on persistent misconception» vs a new lesson «patch in-session rather than reset» are both structurally valid triples; only an NLI pass sees they conflict. Storozh is that NLI pass, layered ON TOP of the structural checks, not instead of them.

## Stage 3 — output: flags appended to the manifest

Append a `storozh` block to the manifest (do not mutate the existing fields — storozh is additive):

```
storozh: {
  ranAt, k,
  flags: [ { unit, routing: ok|misroute, observed-repo, expected-repo,
             semantic: ok|contra|dup, against: [corpus-item-id], judge-note } ],
  summary: { units, misroute, contra, dup, ok }
}
```

Every flag is advisory. The manifest then goes to the **owner + Claude co-review** — the two co-signers of the C2 gate. A `contra` or cross-lane `misroute` is a reason for a co-signer to withhold their cosign marker until resolved; storozh itself withholds nothing and emits no blocking exit code. The decision (land / fix / accept-with-rationale / drop-as-dup) is the co-reviewers', recorded by whether they write their cosign markers.

## Output contract

1. Stage-0 BLUF line (units + headline flag counts). 2. Per-unit routing classification vs C3 with misroute flags. 3. Per-unit semantic label (`contra`/`dup`/`ok`) with the retrieved corpus item(s) and the judge's one-line note. 4. The appended `storozh` manifest block. No verdict, no gate — flags only.

Counter: storozh is skipped when there is no shield-corpus-relevant unit in the manifest — a manifest whose units are all pure code-lane changes (mirabilis sandbox-mechanism, neuro-matrix skill/agent/hook with no knowledge-lane claim) has nothing to NLI-check against the claims/invariants/lessons corpus; run only the Stage-1 routing-check and record `contra-check: skipped (no knowledge-lane unit)`. Storozh is also skipped when localllm is unreachable (`host.docker.internal:1234` down) — record `contra-check: skipped (localllm unreachable)` rather than fabricating labels; the routing-check still runs (it needs no model). In both cases the co-sign gate is unaffected — storozh is advisory, its absence degrades information available to the co-signers, it does not change whether the push unlocks.

---
Provenance: implements shared frozen contracts C4 (storozh I/O — advisory, flags-never-blocks) over C1 (changeset-manifest, mirabilis-produced), C3 (darwin routing-policy + lane-map gene), and C5 (localllm Embeddings). The structural-vs-semantic split is anchored to shield `scripts/boot.py` + `ontology/shapes.ttl` (structural) which storozh complements with the NLI layer. Routing-check mirrors the declarative lane-map; contra-check mirrors the existing localllm `Complete()` adapter for both embedding and judging.
