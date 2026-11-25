# Context Optimization

## Purpose
Reduce token consumption of already-loaded context without losing task-critical information through deduplication, relevance pruning, lossless summarization of verbose payloads, and cache-directive annotations, measured as tokens per resolved goal.

## Use when
- A working set exceeds its token budget and must be compressed before the model call.
- Logs, traces, test output, or retrieved documents contain redundancy (repeated stack frames, duplicated headers, boilerplate).
- Deciding what survives compression: error signatures stay verbatim, verbose successes compress to counts.
- Auditing token spend per goal across runs to prove optimization pays off.

## Do not use when
- Deciding which files to load in the first place (use `lean-progressive-context`).
- Authoring prompts or eval sets (use `prompt-engineering`).
- The context already fits the budget; optimizing fitting context wastes the savings.

## Required context
- Loaded working set with measured token cost and the target budget (e.g. 24,000 tokens loaded, 12,000 target).
- Task acceptance criteria defining which facts are critical and must survive verbatim.
- Redundancy profile: which payloads are verbose (logs, dumps, retrieved chunks) and their compression ratios from prior runs.
- Cache topology if prompt caching applies (e.g. Anthropic extended cache with stable prefix blocks).

## Procedure
1. **Measure before cutting**: tokenize the working set and record cost per section (e.g. app.log excerpt 9,400 tokens, retrieved docs 7,100 tokens); optimize the largest sections first.
2. **Deduplicate mechanically**: collapse repeated stack frames, identical headers, and copy-pasted configs with dedup notes stating counts (e.g. "frame repeated 212 times, 1 kept"); never hand-edit what a script can collapse deterministically.
3. **Prune by relevance tier**: tag each section critical (error signatures, acceptance criteria), supporting (surrounding code), or noise (unrelated passing tests); drop noise entirely and compress supporting tiers first.
4. **Summarize verbose successes**: replace 400-line passing test output with counts (214 passed, 0 failed, 41s) while keeping failing assertions byte-identical; summaries must state what was removed.
5. **Annotate cache-stable prefixes**: mark immutable instruction and schema blocks as cache candidates and keep them byte-stable across runs so cache hit rates stay above 80%.
6. **Verify fidelity and run `scripts/verify.sh`**: re-check that every critical fact survives verbatim, record tokens before/after plus tokens per goal, and confirm the optimized set still addresses the acceptance criteria.

## Decision rules
- **Critical facts stay verbatim**: error messages, ids, acceptance criteria, and failing assertions are never paraphrased.
- **Summaries declare removals**: every summary states what was removed and where the original lives.
- **Scripts over hand-edits for dedup**: mechanical redundancy is collapsed by deterministic scripts, not by eyeballing.
- **Largest section first**: optimization effort targets sections by descending token share.
- **Cache stability**: prefix blocks marked cacheable must not be reworded between runs without invalidating the hit-rate record.

## Evidence required
- Token accounting before and after per section with total savings percentage.
- Fidelity checklist proving every critical fact survives verbatim.
- Tokens-per-resolved-goal metric for the run compared to the trailing mean.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Optimized working set within target budget with critical facts intact.
- Token accounting sheet with per-section savings.
- Cache annotations for stable prefix blocks.

## Stop conditions
- Working set fits the target budget with all critical facts verbatim.
- Further compression would touch critical facts; stop and request a larger budget instead.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the task owner if the set cannot fit the budget without cutting critical facts; scope or budget must change.
- Escalate to platform engineering if cache hit rates stay below 50% despite stable prefixes.
