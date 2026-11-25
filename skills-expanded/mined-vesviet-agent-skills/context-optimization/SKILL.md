---
name: context-optimization
description: Use when optimizing LLM agent context windows, allocating token budgets, pruning semantic duplicates, scoring relevance density, and ordering context to mitigate lost-in-the-middle degradation.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter]
version: 2.0.0
---

# Context Optimization

Maximize effective reasoning density in agent context windows by allocating strict token budgets, eliminating redundant context via semantic deduplication, and structuring prompt sequences to eliminate lost-in-the-middle attention degradation.

## When to Use

- Constructing multi-turn agent execution loops with growing conversation histories
- Injecting multi-document retrieval-augmented generation (RAG) contexts into system prompts
- Compacting multi-agent message transcripts before dispatching downstream tasks
- Mitigating attention dilution and instruction forgetting in high-capacity LLMs
- Staying within hard token budget ceilings while preserving critical grounding facts

## Core Rules

- **Deterministic 6-Layer Prompt Prefix Caching**:
  To maximize KV cache hit rates (yielding up to 90% read latency and cost reductions), assemble prompts in strict static-to-dynamic volatility order:
  1. *Layer 1: Static System Invariants & Global Rules*: Fixed repository rules, safety constraints, action policies (100% KV cache hit rate across all agents).
  2. *Layer 2: Role Identity & Core Tool Contracts*: Role definition, instructions, and tool definitions deterministically sorted alphabetically by name (Anthropic Breakpoint 1).
  3. *Layer 3: Domain & Repository Architectural Cards*: Knowledge cards, domain boundaries, project layouts (Anthropic Breakpoint 2; shared across repo tasks).
  4. *Layer 4: Session Durable Working State*: Anchored 10-slot state (`compact-working-state.json`), verified decisions, and immutable entity IDs (Anthropic Breakpoint 3).
  5. *Layer 5: Dynamic Turn History with Head-Tail TOC*: Rolling dialogue history and tool outputs compacted via 20% Head / 80% Tail syntax-aware TOC (Anthropic Breakpoint 4 rolling).
  6. *Layer 6: Dynamic Ephemeral Payload*: Current turn user prompt, ephemeral context, and dynamic UTC timestamps (uncached).
- **Provider-Specific Cache Control Configurations**:
  - *Anthropic*: Explicit ephemeral breakpoints using `cache_control: {"type": "ephemeral", "ttl": "5m" | "1h"}`. Enforce hard ceiling of max 4 breakpoints per request; sequence across `tools` $\rightarrow$ `system` $\rightarrow$ `messages`; minimum 1,024 prefix tokens.
  - *OpenAI*: Automatic caching for prompts $\ge 1,024$ tokens quantized to 128-token boundaries. Use `prompt_cache_key` for sticky cluster routing; track cache telemetry in `usage.prompt_tokens_details.cached_tokens`.
  - *vLLM / SGLang*: Enable server-side prefix caching via `--enable-prefix-caching` and `--block-size 16|32`. Utilizes PagedAttention block alignment and RadixAttention Radix Tree LRU cache reuse.
- **Cache-Busting Anti-Pattern Mitigations**:
  - *Zero Dynamic Headers*: Never inject dynamic UTC timestamps, random UUIDs, or ephemeral session IDs into Layer 1–3 system headers. Keep dynamic values strictly in Layer 6.
  - *Deterministic Tool Ordering*: Always sort tool definitions alphabetically by name prior to serialization to prevent dictionary key shuffling between turns.
  - *Tenant Salt KV Isolation*: Partition shared cache trees cryptographically using $H_0 = \text{HMAC-SHA256}(\text{TenantID} \parallel \text{Domain}, \text{Salt})$ to prevent cross-tenant cache probing.
- **Five-Tier Token Budget Allocation**:
  Context capacity must be partitioned into strict deterministic slices:
  1. *System & Behavioral Invariants*: $15\%$ (fixed prompt, role constraints, tool contracts).
  2. *Dynamic Task Grounding*: $35\%$ (task objectives, retrieved references, verified facts).
  3. *Working Memory & Turn History*: $25\%$ (recent tool calls, observations, active state).
  4. *Scratchpad & Intermediate Reasoning*: $10\%$ (scratch notes, plan checklists).
  5. *Output Generation Reserve*: $15\%$ (completion buffer to prevent truncated generations).
- **Lost-in-the-Middle Priority Ordering**:
  Frontier LLMs demonstrate highest attention accuracy at prompt boundaries (primacy and recency). Place mandatory constraints at the top ($0\%-15\%$) and active turn triggers at the bottom ($85\%-100\%$). Confine secondary data to the middle zone ($15\%-85\%$).
- **Context Engineering 2026 (Anthropic-aligned)**:
  - *Context rot is real*: performance degrades as the window fills with low-value tokens — treat context as a scarce runtime resource, not free capacity.
  - *Compaction over overflow*: near the window limit, summarize the conversation and reinitialize a fresh context; keep raw records with stable identifiers so compaction is recoverable.
  - *just-in-time retrieval over pre-loading*: fetch context at the moment of need via tools instead of stuffing everything upfront.
  - *Durable notes over transcript replay*: persist structured notes/memory files outside the window; hydrate new sessions from notes, never full raw transcripts.
  - *Sub-agent isolation*: dispatch heavy reading to fresh-context sub-agents; return only distilled results to orchestrator.

## Suggested Process

1. **Assemble Prefix Layers 1–3**: Concatenate Static System Invariants, deterministically sorted Role Tools, and Domain Knowledge Cards. Set Provider Cache Breakpoints 1 and 2.
2. **Hydrate Layer 4 Durable Working State**: Load anchored `compact-working-state.json` notes and set Breakpoint 3.
3. **Compress Layer 5 History with Head-Tail TOC**: Apply 20% Head / 80% Tail syntax-aware TOC to tool outputs and set Breakpoint 4.
4. **Append Layer 6 Ephemeral Turn**: Append current user prompt and dynamic UTC timestamp.
5. **Prune and Deduplicate Ingested Content**: Strip n-gram overlaps ($>70\%$) and apply vector cosine thresholding ($\ge 0.88$).
6. **Verify Context Integrity**: Confirm critical entity IDs, schema fields, and safety boundaries survived optimization.

## Checklist

- [ ] 6-layer prefix caching sequence enforced (System -> Role -> Domain -> State -> History -> Ephemeral).
- [ ] Anthropic ephemeral breakpoints configured (at most 4 breakpoints, ordered tools -> system -> messages).
- [ ] OpenAI prompts aligned to 128-token boundaries with `prompt_cache_key` sticky routing.
- [ ] vLLM / SGLang prefix caching enabled with PagedAttention Radix Tree block alignment.
- [ ] Dynamic UTC timestamps and UUIDs confined strictly to Layer 6 ephemeral payload.
- [ ] Tool definitions deterministically sorted alphabetically by name.
- [ ] Token budget partitions configured with $\ge 15\%$ output generation reserve.
- [ ] Compaction with recoverable raw records replaces blind truncation near window limits.
- [ ] just-in-time retrieval preferred over pre-loading; durable notes hydrate new sessions.
- [ ] Essential entity IDs, contracts, and schema requirements verified intact.

## Output Contracts

When context optimization produces structured task dispatches or plans, emit:

- **`contracts/schemas/coordination-plan.json`**: Sliced execution stages respecting token budget allocations and prefix cache boundaries.
- **`contracts/schemas/compact-working-state.json`**: Anchored 10-slot durable working state preserving verified facts across turns.

## Failure Modes

- **Cache-Busting Prefix Invalidation**: Line-1 dynamic timestamp invalidates KV cache for all downstream tokens. Mitigation: Relocate all volatile timestamps to Layer 6.
- **Tool Shuffling Invalidation**: Unsorted tool maps yield different token streams each turn. Mitigation: Enforce deterministic alphabetical sorting of tools by name.
- **Breakpoint Overflow**: Setting $> 4$ Anthropic cache breakpoints causes API rejection. Mitigation: Strict limiter capping breakpoints at 4.
- **Lost-in-the-Middle Forgetting**: Safety rules placed in center of large context. Mitigation: Anchor rules in Layer 1 and repeat active trigger in Layer 6.
- **Aggressive Over-Pruning**: Truncating necessary contract schema fields. Mitigation: Keep JSON schemas intact; prune only prose.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: Reordering promotes untrusted content to prefix boundary. Mitigation: Keep untrusted inputs confined to Layer 6 inside boundary delimiters.
- **ASI04 Supply Chain**: Token count mismatch across tokenizer versions. Mitigation: Pin target tokenizer version (cl100k/o200k) and embedding models.
- **ASI06 Context & Memory Poisoning**: Density scoring strips provenance tags and trust delimiters. Mitigation: Exclude trust wrappers from density pruning.
- **ASI07 Inter-Agent Communication**: Summarized handoffs passing unverified claims. Mitigation: `coordination-plan.json` must carry only verified facts.
- **ASI09 Human-Agent Trust Exploitation**: Reporting token savings while truncating schema fields. Mitigation: Complete integrity verification before reporting savings.

## Related Skills

- **agent-tool-orchestration**: Coordinating tool executions within token-bounded contexts.
- **agent-graph-orchestration**: Orchestrating multi-agent state machines across bounded context nodes.
- **agent-evaluation**: Evaluating agent reasoning performance under varying context lengths.
- **prompt-injection-defense**: Sanitizing and delimiting untrusted inputs within optimized context boundaries.
- **systematic-debugging**: Diagnosing context leakage and token exhaustion failures.
- Companion reference: `references/token-budgeting-and-attention-allocation.md`
- Companion example: `examples/context-pruner-and-reorderer.py`
