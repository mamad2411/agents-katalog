---
name: repository-memory-curator
description: Curate a single GitHub repository's stored agent "memories" from a pool of NEW mined candidates (produced by `repository-memory-miner`) plus the repo's existing memories. Verifies each fact against its citations, dedups and merges, rewords, and ranks by criticality, producing a JSONL file of repository-scoped memory records that can replace the repo's memory set.
user-invocable: true
---

# Repository Memory Curator

You **curate** a single repository's stored agent "memories" — the short facts injected into future agent prompts for that repo. You take a pool of **NEW candidate memories** (mined by the companion `repository-memory-miner` skill) plus the repo's **existing memories**, and produce a JSONL file of **repository-scoped** memory records — verified, deduplicated, merged, reworded, and **ranked by criticality**.

This is the **second of two skills**. The miner proposes candidates; you decide what survives. Curate for **signal**: the memories that survive should be the ones most likely to save a future agent many turns, prevent a costly mistake, or unblock cross-repo work. Everything else is noise that wastes prompt budget. This version ranks by your editorial judgment of **criticality**, not a backend popularity/vote signal. It does not read memory scores, votes, or timestamps, and does not preserve memory `id`s across rewords. Existing memories are fetched as **reference text** (via the `read_memories` MCP tool) and used to dedup/merge — not as a structured, id-bearing export. The apply step (writing back to the memory DB) remains out of scope (§10).

**Model requirements (mandatory).** Run all **clustering, curation, and holistic-ordering** subagents, plus the **first refinement pass (§8)**, on **Claude Opus 4.8 or later**. Run the **per-bucket verification review** and the **mandatory second refinement pass (§8)** on **GPT‑5.5 or later** — a *different* model family, for a genuine second pair of eyes. Always use the **strongest-reasoning configuration** available, and run every review, holistic, and refinement subagent in a **clean context** (a fresh subagent with no access to the generation conversation).

## Contents

- [Helper scripts](#helper-scripts)

1. [Inputs](#1-inputs)
2. [Fetching the existing repo memories](#2-fetching-the-existing-repo-memories)
3. [Memory record schema](#3-memory-record-schema)
4. [How your output is used](#4-how-your-output-is-used)
5. [The curation procedure](#5-the-curation-procedure)
6. [Independent review pass](#6-independent-review-pass)
7. [Curation rules](#7-curation-rules)
8. [Refinement & ordering](#8-refinement--ordering)
9. [Sanitization](#9-sanitization)
10. [Future apply step](#10-future-apply-step)

## Helper scripts

This skill ships helper scripts in its own `scripts/` directory — **use them, don't reinvent them**. They live with the installed skill, **not** in the target repo, so every command invokes them by absolute path as `"$SKILL_DIR/scripts/…"`, where `SKILL_DIR` is this skill's own directory (e.g. `~/.copilot/skills/repository-memory-curator`). Set `SKILL_DIR` once at the start of a run.

- `scripts/run-workspace.sh` — sets up the run's output dir outside the target checkout and polices checkout cleanliness. `init` guards the target and creates a parent-dir-sibling run dir; `check` (after every wave) fails closed if the pinned worktree or invocation checkout gained leaked files.
- `scripts/render-briefs.py` — resolves each thin brief's `{{include: prompt-fragments/…}}` directives and `{OWNER}`/`{REPO}`/`{REPO_ROOT}` placeholders into ready-to-dispatch prompts under `$RUN_DIR/prompts/`, **failing closed** if any prompt is incomplete.
- `scripts/bucket-pool.py` — the deterministic front/back end for the LLM bucket-clustering subagent. `--emit-cluster-input` writes the compact `{i, subject, fact, citations}` view the subagent reads. `--from-assignments --stage curate|review` materializes its `{label: [indices]}` output into bucket files, a ready-to-dispatch `<safeName>.context.md` per bucket, plus `bucket-manifest.json`. Fails closed unless the indices are an exact partition of the pool; splits over-cap buckets and coalesces tiny ones.
- `scripts/order-spec.py` — the deterministic front/back end shared by the two §8 ordering passes. `--stage holistic` orders the whole list from a compact `{i, subject, fact, citations, rank}` view; `--stage refine` polishes the top `--window` (default 200) records and carries everything below verbatim. `--emit-input` writes the in-scope view (plus a `<stage>.context.md`); `--from-spec` materializes the subagent's `{merge, reword, drop, order}` spec over stable indices into `review/holistic-ordered.jsonl` / `review/refine-ordered.jsonl`. Fails closed on a malformed spec, a bad index, drift, or any window record left unplaced.
- `scripts/assemble-final.py` — concatenates the per-bucket curated/reviewed slices and merges exact-normalized duplicate facts (unioning citations). Assigns `rank`: intermediate assemblies get a coarse, possibly-tied rank from the curation tiers; the final list gets a unique total-ordering rank (1 = most critical, no ties) from the §8 passes via `--explicit-order` (`--manifest-stage holistic`, then `refine`). Fails closed on missing/stale slices or non-`repository` records.
- `scripts/validate-output.py` — validates the final JSONL (required fields, ≥1 citation, all `repository` scope; best-effort on-disk citation check with `--repo-root`).
- `scripts/citation_paths.py` — shared helper for citation path handling.
- `scripts/prompt/subagent-templates/` — `cluster-brief` (groups the pool into topic buckets), `curate-brief` (curation), `review-brief` (the §6 review), `holistic-brief` (final ordering/dedup), `refine-brief` (head polish).
- `scripts/prompt/prompt-fragments/` — shared **fragments** (`curation-rules`, `criticality`, `memory-schema`, `output-usage`, `bucket-discipline`, `curation-verification`, `ordering-spec`, `full-replacement-output`, `sanitization`, `injection`, `no-side-effects`, `completeness`): the single source for guidance multiple briefs share and this SKILL.md references.

---

## 1. Inputs

When invoked, establish these inputs (ask the user only if something is unclear):

- **Candidate pool** — path to the miner's `candidates.merged.jsonl` (NEW candidate records). Required. If the user hasn't run the miner yet, point them at the `repository-memory-miner` skill first.
- **Target repo NWO** — e.g. `github/copilot-agent-runtime`. Required, so you can verify candidate citations against the shipped code.
- **Output directory** (optional) — where to write all run artifacts. Default: a fresh per-run directory **outside the target checkout**, a sibling in its parent dir, named `memory-curation-<owner>-<repo>-<timestamp>/`. The curated deliverable, its `.summary.md`, the fetched existing-memory reference, and every interim artifact live inside it.

**Verify against `origin/main` HEAD.** Citations describe the shipped default branch, so verify against the current **`origin/main` HEAD** — §5 step 1 fetches and pins a clean detached worktree at that commit. **User-scoped memories are out of scope** — never fetch or emit them; work only at repository scope.

---

## 2. Fetching the existing repo memories

Fetch the repo's current **repository-scoped** memories with the **`read_memories` MCP tool** and save the returned text to `$RUN_DIR/existing.memories.txt`. In v0 this is **reference text** — a prose snapshot of what the repo already remembers, **without** per-memory `id`s, scores, votes, or timestamps.
Use it to **dedup and merge**, not to rank:

- Drop a candidate an existing memory already covers well (unless the candidate is materially clearer or more complete — then keep the better wording).
- Merge a candidate that extends or sharpens an existing memory into a single, stronger record.
- Re-author a worthwhile existing memory into the curated set when it should survive (it becomes a fresh record — see §3/§4).

Pass this reference text into the curation, review, and holistic briefs (each has an "existing memories (reference)" slot). If `read_memories` returns nothing, proceed with the candidates alone and note it in the summary.

---

## 3. Memory record schema

Each curated **output** record has these fields (the canonical definition is `scripts/prompt/prompt-fragments/memory-schema.md`, rendered into every record-authoring subagent prompt):

```json
{
  "subject": "short topic, 1-2 words",
  "fact": "the memory text injected into prompts",
  "citations": ["file.ts:123", "User input: \"...\"", "..."],
  "reason": "why this fact is worth remembering / when it helps",
  "source": { "interactionId": "...", "agent": "memory-mining", "baseModel": "..." },
  "scope": "repository",
  "rank": 1
}
```

- **`citations` ≥1 non-empty entry**, verified against its artifact (see §5).
- **`scope` is always `"repository"`.**
- `rank` carries a coarse criticality **tier** (1 = most critical … 5 = minor) while subagents work on buckets; the **final** deliverable uses a **unique total-ordering** `rank` (`1` = most critical, ascending, **no ties**) authored by the §8 holistic pass, so the future apply/injection step (top ~20–50) is deterministic. `assemble-final.py` turns the coarse tiers into tied ranks for intermediate assemblies and applies the final unique order with `--explicit-order`.
- **Never emit server-managed fields** (`id`, `score`, `votes`, `totalVoteCount`, `createdAt`, `updatedAt`, `expiresAt`). In v0 there is no structured existing export to carry an `id` from, so every curated record applies as new (§10).

---

## 4. How your output is used

You produce a **ranked set** that is the **complete desired list** of the repo's repository-scoped memories — you control prominence via `rank`, ordered most-critical first. A memory you curate away is dropped by **omission**; a merge or reword is a **single resulting record**; verified candidates become records. The per-record rules subagents apply are the fragments `scripts/prompt/prompt-fragments/output-usage.md` and `full-replacement-output.md`, rendered into the curation, review, and holistic prompts.

Also write a sibling **human-readable change summary** (`<owner>-<repo>.summary.md`) — NOT part of the insertable JSONL — listing what was dropped, merged, reworded, and added, each with a one-line rationale citing the verifying artifact. This is what human reviewers read before applying the curated set.

Validate before finishing: every output line parses as JSON; every record has the required fields; every `citations` array has ≥1 non-empty entry; `scope` is `"repository"` everywhere.
---

## 5. The curation procedure

Curating the whole pool in one context degrades quality past many hundreds of records — semantic dedup needs focused attention. So **bucket, then fan out.** Like the miner, this is a multi-wave orchestration over **fresh isolated subagents** under the environment's concurrency cap (manage the budget **per wave**; finished agents drop to `idle` and free their slot; a subagent's model is fixed at creation; never reuse an agent to free capacity or for an independent review/holistic pass).
1. **Pin a clean `origin/main` worktree + set up the run dir.** Note the target checkout's absolute path as `TARGET` (the one you cloned/`cd`'d into). Set `SKILL_DIR` to this skill's directory. Then:

   ```bash
   RUN_DIR="$(bash "$SKILL_DIR/scripts/run-workspace.sh" init --target "$TARGET" --owner <owner> --repo <repo>)"
   git -C "$TARGET" fetch origin
   MAIN="$RUN_DIR/main"   # find $DEFAULT_BRANCH via the GitHub MCP server
   git -C "$TARGET" worktree add --detach "$MAIN" "origin/$DEFAULT_BRANCH"
   git -C "$MAIN" rev-parse HEAD
   ```

   Use **`$MAIN` as the repo root** for citation verification (`validate-output.py --repo-root`, opening cited files). Remove the worktree at the end. **Clean-checkout assertion (after every wave):** `bash "$SKILL_DIR/scripts/run-workspace.sh" check --run-dir "$RUN_DIR" --target "$TARGET"` — if it trips, stop, move strays under `$RUN_DIR`, and tighten the offending dispatch's prompt; never auto-delete from `TARGET`.

   Fetch the existing memories (§2) into `$RUN_DIR/existing.memories.txt`. Then **render the briefs once**:

   ```bash
   python3 "$SKILL_DIR/scripts/render-briefs.py" --owner <owner> --repo <repo> --repo-root "$MAIN" --out-dir "$RUN_DIR/prompts"
   ```

2. **Cluster the candidate pool into topic-cohesive buckets** with one clustering subagent, so each curation subagent sees related memories (co-locating duplicates and path-less/cross-repo facts so overlaps get merged within a bucket):

   ```bash
   # (a) emit the compact clustering input:
   python3 "$SKILL_DIR/scripts/bucket-pool.py" \
       --candidates "$RUN_DIR/candidates.merged.jsonl" \
       --emit-cluster-input "$RUN_DIR/curate/cluster-input.jsonl"
   # (b) dispatch ONE clustering subagent (rendered cluster-brief.md, Opus 4.8+, clean context)
   #     given that input, a scratch dir, and an output path for its {label:[indices]} JSON
   #     (e.g. "$RUN_DIR/curate/assignments.json"); this tiny dispatch is composed inline.
   # (c) materialize buckets + manifest (pass the SAME --candidates as (a) so indices line up):
   python3 "$SKILL_DIR/scripts/bucket-pool.py" \
       --candidates "$RUN_DIR/candidates.merged.jsonl" \
       --from-assignments "$RUN_DIR/curate/assignments.json" --stage curate \
       --cluster-input "$RUN_DIR/curate/cluster-input.jsonl" --out-dir "$RUN_DIR/curate"
   ```

   `--from-assignments` writes `bucket-manifest.json`, a ready-to-dispatch `<safeName>.context.md` per bucket, and **fails closed** unless the agent assigned every record exactly once (so a clusterer can't silently decimate the set); it **splits** any bucket over `--max-bucket` (default 100) and **coalesces** buckets too small to be worth a subagent. If it fails or warns heavily (most records in one bucket), **re-cluster** (re-run b–c). A small pool (fewer records than `--max-bucket`) producing a **single bucket is normal**. For a pool too large to cluster in one context (~150K tokens ≈ ~2.5k records), use a **1M-context variant** or a **shard-and-merge** pass (note it in the summary).

3. **Dispatch one curation subagent per bucket, in parallel** (each on **Claude Opus 4.8+**). Dispatch each with the rendered `$RUN_DIR/prompts/curate-brief.md` **plus its written `$RUN_DIR/curate/<safeName>.context.md`** and the existing-memory reference text (§2). Each subagent:
   - **Verifies each candidate against its citations** — opens cited repo files at the cited lines under `$MAIN` for repo-local facts; looks up non-repo / cross-repo sources (other repos, PRs, CI, releases, docs, live endpoints) via `gh`/the artifact. A cross-repo or external fact is **discredited only by a contradiction from its real source**, never merely because the pinned checkout can't confirm it (the carve-out in `curation-rules.md`). Narrow a record to its verified kernel; fix or drop a citation whose target is gone or contradicted.
   - **Dedups/merges against existing memories** (the §2 reference) and within the bucket.
   - **Applies the curation rules** (§7 / `curation-rules.md`) and assigns a coarse criticality **tier** in `rank`.
   - Writes its `curated_<bucket>.jsonl` slice and a **findings note** recording in→out counts, merges, and **every dropped memory with its specific reason**.

   When the wave finishes, run the clean-checkout assertion. You can validate a slice early — `validate-output.py --pre-assembly --repo-root "$MAIN" <slice>` — to catch bad citations before review.

4. **Assemble + global dedup + coarse ranks:**

   ```bash
   python3 "$SKILL_DIR/scripts/assemble-final.py" --in-dir "$RUN_DIR/curate" \
       --manifest "$RUN_DIR/curate/bucket-manifest.json" --manifest-stage curate \
       --default-interaction-id "<this session's interaction id>" --default-agent "memory-mining" \
       --default-base-model "<the model used, e.g. claude-opus-4.8>" \
       --out "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl"
   ```

   Assembly uses only manifest-listed slices (fails closed on missing/stale slices), strips any stray DB-only fields, exact-dedups facts, assigns provisional coarse ranks, stamps each record's `source` from the defaults, and aborts on malformed/non-`repository` records or an empty result.
5. **Audit the curation drop log** (anti-decimation guard): read each findings note's dropped-memory list and **reinstate any memory dropped for a non-substantive reason** — especially poor bucket-fit. A record should be dropped only for the reasons in `curation-rules.md` or `sanitization.md`. **Treat a drop logged "unverifiable" for a cross-repo, external, or operational fact as suspect** — the pinned checkout is the wrong oracle — so reinstate it unless its **actual source contradicts** it or an independent valid drop reason (trivial, mis-scoped, unsafe) applies; consider `/research` to validate or debunk the fact. When you reinstate, **re-read the original line from the bucket's `bucketFile`, re-verify its citations**, narrow to the verified kernel, and append it to that bucket's `curated_<name>.jsonl` slice.

---

## 6. Independent review pass

After assembly and **before** writing the final deliverables, the set gets a **mandatory independent review** — a second pair of eyes that did **not** generate it, catching errors, low-value injections, duplicates, and ranking mistakes the authoring model is blind to.

**Hard rules:**

- **Models.** The bucket-clustering pass that precedes review runs on **Claude Opus 4.8+** (it only groups records, judging nothing). The per-bucket verification review runs on **GPT‑5.5 or later** — a *different* model family is the point. Always use the strongest-reasoning variant available.
- **Clean context.** Every reviewer is a **fresh subagent** with no access to this conversation — it sees only the candidate JSONL + the repo/artifacts it verifies against.
- **Verify against sources, matched to the fact** — open cited repo files for repo-local facts; look up cross-repo/external sources via `gh`/the artifact. A cross-repo or external fact is **discredited only by a contradiction from its real source**.

**Recipe (mirrors the curation fan-out):**

1. **Re-bucket** the assembled set by re-clustering it into fresh topic buckets (the curated set has dropped/merged/reworded records, so a fresh classification is cleaner than re-packing curation-time labels):

   ```bash
   python3 "$SKILL_DIR/scripts/bucket-pool.py" \
       --candidates "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl" \
       --emit-cluster-input "$RUN_DIR/review/cluster-input.jsonl"
   # dispatch ONE cluster-brief.md subagent (Opus 4.8+, clean context), then:
   python3 "$SKILL_DIR/scripts/bucket-pool.py" \
       --candidates "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl" \
       --from-assignments "$RUN_DIR/review/assignments.json" --stage review \
       --cluster-input "$RUN_DIR/review/cluster-input.jsonl" --out-dir "$RUN_DIR/review"
   ```

   Use the resulting `$RUN_DIR/review/bucket-manifest.json` for the per-bucket review assembly and the holistic/refine assemblies. Same extreme-scale fallback as §5 step 2 if the pool is too large to cluster at once.

2. **Dispatch one review subagent per bucket, in parallel** (GPT‑5.5+, clean context) — a **fresh** cross-family fleet; the finished curation agents are idle and have freed their slots (dispatch in successive sub-waves if there are more buckets than the cap). Each gets the rendered `$RUN_DIR/prompts/review-brief.md` **plus its written `$RUN_DIR/review/<safeName>.context.md`** and the existing-memory reference. Each writes its `reviewed_<bucket>.jsonl` slice plus a findings note listing **every removed memory with its verified reason** (plus merges, corrections, re-tierings). After the wave, run the clean-checkout assertion.

3. **Audit the drop log** (MANDATORY anti-decimation guard): run the **same anti-decimation + citation re-verify guard as §5 step 5** over each review bucket's removed-list. Reinstate any memory removed for a non-substantive reason, re-reading each from the bucket's `bucketFile` and **re-verifying/fixing its citations before appending** to that bucket's `reviewed_<name>.jsonl` slice. The holistic and refinement passes re-rank, dedup, and reword but do **not** re-cite, so **this is the last chance to fix citations.**

4. **Re-assemble + coarse ranks** (merges exact-normalized duplicates; the unique total order is authored by the holistic pass below):

   ```bash
   python3 "$SKILL_DIR/scripts/assemble-final.py" --in-dir "$RUN_DIR/review" \
       --manifest "$RUN_DIR/review/bucket-manifest.json" --manifest-stage review \
       --default-interaction-id "<this session's interaction id>" --default-agent "memory-mining" \
       --default-base-model "<the model used, e.g. claude-opus-4.8>" \
       --out "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl"
   ```

The review **may shrink** the set (cutting **contradicted** or low-value memories and merging related ones is the goal), but the anti-decimation guard still applies: removing a *distinct, verified, useful* fact — or a cross-repo/external fact merely because the pinned checkout can't confirm it — is a regression.

---

## 7. Curation rules

Apply these to turn raw candidates + existing-memory reference into the final set.

> **Curate, don't decimate.** The output is the repo's desired memory set, so dropping a valid memory deletes it, and collapsing a large set to a tiny handful is almost always a curation failure, not good taste. Default to **verify-and-keep**; the volume check below backstops it.

The per-record curation rules subagents apply are `scripts/prompt/prompt-fragments/curation-rules.md`, rendered into the curation, review, and holistic prompts. The orchestrator-level checks stay here:

- **Output-volume sanity check (anti-over-pruning).** Before finalizing, compare the output to what was mined and to the existing-memory reference. If the curated set is a **small fraction** of a non-trivial input (e.g. hundreds of legitimate memories collapsing to a few dozen), **stop and re-examine** — you have probably dropped valid memories. Distinguish genuine noise (mass-generated facts about test/benchmark data, which *should* be cut wholesale) from real conventions (naming, components, testing, error handling) that must be **kept**. A healthy run **adds** durable facts on top of the verified survivors; it does not mostly delete.
- **What to rank highest.** Rank by **criticality** (defined in `scripts/prompt/prompt-fragments/criticality.md`, rendered into the curation, review, and holistic prompts). Curation and review subagents assign a coarse **tier** (1 = most critical … 5 = minor) in `rank`, since each sees only a subset. `assemble-final.py` turns tiers into coarse, possibly-tied ranks; the **final** unique `1..N` order is authored by the §8 holistic reviewer and applied with `--explicit-order`. Never leave the *final* ranks tied.

---

## 8. Refinement & ordering

After the review pass re-assembles the set, author the global order and polish the head. All passes run in a **clean context**.

1. **Holistic ordering + dedup** — one reviewer on **Claude Opus 4.8+** (clean context) authors the most→least-critical order and full-list cross-bucket merges/drops over the **whole** list: it **prunes the clearly-low-value tail** and **ranks the kept set globally** (records it leaves unranked keep their incoming order). The subagent reads a compact view and emits a compact spec; `order-spec.py` is the deterministic front/back end.

   ```bash
   # (a) emit the compact {i, subject, fact, citations, rank} holistic input:
   python3 "$SKILL_DIR/scripts/order-spec.py" --stage holistic \
       --reviewed "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl" \
       --emit-input "$RUN_DIR/scratch/holistic/holistic-input.jsonl"
   # (b) dispatch ONE Opus 4.8+ reviewer (clean context) with holistic-brief.md + its
   #     written holistic.context.md; it writes the {merge, reword, drop, order} spec.
   #     Run the clean-checkout assertion after it finishes.
   # (c) materialize the ordered list (fails closed on a malformed spec / bad index / drift):
   python3 "$SKILL_DIR/scripts/order-spec.py" --stage holistic \
       --reviewed "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl" \
       --from-spec "$RUN_DIR/scratch/holistic/holistic-spec.json" \
       --input "$RUN_DIR/scratch/holistic/holistic-input.jsonl" \
       --out "$RUN_DIR/review/holistic-ordered.jsonl"
   # (d) number it positionally and write the holistic-ordered deliverable:
   python3 "$SKILL_DIR/scripts/assemble-final.py" --in-dir "$RUN_DIR/review" \
       --explicit-order --manifest "$RUN_DIR/review/bucket-manifest.json" --manifest-stage holistic \
       --default-interaction-id "<this session's interaction id>" --default-agent "memory-mining" \
       --default-base-model "<the model used, e.g. claude-opus-4.8>" \
       --out "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl"
   ```

   `--explicit-order` trusts the holistic pass's record line order and assigns unique ranks `1..N`; the manifest gate requires it so the authored order isn't assembled in coarse-rank mode. `order-spec.py --emit-input` **WARNs** if the compact input exceeds the single-context budget (~600 KB ≈ 150K tokens); above that, use the shard-and-merge tier and note it in the summary.

2. **Refine the head (two passes).** A final, full-fidelity editorial polish of the top-ranked memories (most likely to be injected). It reads the holistic-ordered deliverable, polishes the top `--window` (default 200) records, and carries everything below the window verbatim. It does **no** source re-verification (facts were verified by curation/review). It dedups/merges near-duplicates, rewords for clarity, removes low-value records, and refines the order — O(1) attention in repo size, a scale-independent quality floor on the injected records.

   ```bash
   # (a) emit the full-fidelity {i, subject, fact, reason, citations} refine input (top --window):
   python3 "$SKILL_DIR/scripts/order-spec.py" --stage refine \
       --reviewed "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl" \
       --emit-input "$RUN_DIR/scratch/refine/refine-input.jsonl"
   # (b) dispatch ONE Claude Opus 4.8+ subagent (clean context) with refine-brief.md + its
   #     refine.context.md; it writes the {merge, reword, drop, order} spec. Clean-checkout assert.
   # (c) materialize the refined list (fails closed on a malformed/drifted spec, a changed tail,
   #     or any window record left unranked/undropped/unmerged — refine has no implicit tail):
   python3 "$SKILL_DIR/scripts/order-spec.py" --stage refine \
       --reviewed "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl" \
       --from-spec "$RUN_DIR/scratch/refine/refine-spec.json" \
       --input "$RUN_DIR/scratch/refine/refine-input.jsonl" \
       --out "$RUN_DIR/review/refine-ordered.jsonl"
   # (d) number positionally and write the deliverable (same flags as 1(d), --manifest-stage refine):
   python3 "$SKILL_DIR/scripts/assemble-final.py" --in-dir "$RUN_DIR/review" \
       --explicit-order --manifest "$RUN_DIR/review/bucket-manifest.json" --manifest-stage refine \
       --default-interaction-id "<this session's interaction id>" --default-agent "memory-mining" \
       --default-base-model "<the model used, e.g. claude-opus-4.8>" \
       --out "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl"
   ```

   Pass the **same** `--window` to the emit (a) and from-spec (c) commands (a mismatch fails closed via the tail sidecar). The materialize summary reports how much changed and WARNs on a no-op; treat a near-no-op as a **red flag to weigh, not a hard error**.

   **(e) Second refinement pass (mandatory) — cross-family second opinion.** Repeat (a)–(d) once with a fresh **GPT‑5.5+** subagent. `--reviewed` stays the canonical `$RUN_DIR/<owner>-<repo>.memories.curated.jsonl` — step (d) already overwrote it with the first pass's renumbered deliverable, so the second pass reads the first pass's result. The only per-pass changes are the **model family** and a **fresh scratch dir** (`$RUN_DIR/scratch/refine2/`). The passes hand off **only** through the step-(d) deliverable.

3. **Validate + report.** Run `validate-output.py` **once, after the final pass**:

   ```bash
   python3 "$SKILL_DIR/scripts/validate-output.py" \
       "$RUN_DIR/<owner>-<repo>.memories.curated.jsonl" --repo-root "$MAIN"
   ```

   Fix every error, then write the `.summary.md` change log (§4) recording the review's net effect (removed / merged / corrected / re-ranked / reinstated counts) and the staged funnel: candidates **in** → kept → reworded → newly-surfaced → **final out**.
---

## 9. Sanitization

When writing the change summary or any saved output, **redact** sensitive content from sessions/chat/telemetry (message bodies, internal-only URLs, personal data); memory `fact`s and `citations` must reference durable, shareable artifacts, not raw private transcripts. The per-record rules are `scripts/prompt/prompt-fragments/sanitization.md`.

---

## 10. Future apply step

_Out of scope for now._

This skill emits the desired ranked memory list; it does **not** write to the DB. A later step will apply it against the memory API, inserting records and removing memories no longer present. In v0 the curated records carry **no `id`**, so every record applies as new — there is no vote/score continuity for memories that already existed. Restoring `id`/score continuity requires the structured, scored existing-memory export that v0 deliberately does not consume; it is deferred to that future step, along with the choice of how many top-ranked records (on the order of several hundred) to insert so the stored set stays bounded.
