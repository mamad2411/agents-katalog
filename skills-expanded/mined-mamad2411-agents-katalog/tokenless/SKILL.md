---
name: tokenless
description: Optimize token consumption and prefix-cache hit rate for coding agents without sacrificing task quality. Use when the user asks to save tokens, cut API costs, trim an overgrown session, reduce tools/MCPs, or debug cache misses. Provider-agnostic; pasteable into any agent.
---

# Tokenless — Save Tokens & Win Cache Hits

A provider-agnostic strategy pack that reduces token spend and improves prefix-cache hit rate **without degrading task quality**. Inspired by the prefix-cache stability and cost-reduction techniques of DeepSeek-Reasonix.

## Guiding principle

Save tokens by sending *less duplicate/useless content*, not by doing *less work*. Never trade correctness, completeness, or verifiability for savings; when in doubt, do the job right. Claim success only with evidence; label anything unverified.

## A. Save tokens (without losing quality)

1. **Read precisely**: locate with search, then read only the needed excerpts — don't slurp whole files or whole batches into context.
2. **Long output → conclusions + key lines only**: trim logs/errors to the head, the error lines, and the conclusion. Keep full content only when it is small or genuinely required.
3. **Never re-send the same fact**: once a file or fact is already in this session, don't re-read or re-paste it in full.
4. **Don't summarize what isn't worth it**: drop low-information intermediates in one line or discard them; don't summarize tiny content just to look thorough.
5. **Recover across sessions via durable memory**: at wrap-up, persist key state (what changed, verification results, leftovers); resume from memory instead of re-importing the whole history.
6. **Reuse**: prefer existing tools/components/patterns over building new ones.

## B. Cache hits (prefix stability)

- **System prompt / rules are a fixed prefix — don't edit them mid-session**: any change invalidates the entire cache and the next request pays full price.
- **Grow the prefix append-only**: add new content at the end; never rebuild context for a small change.
- **Tool sets (MCP/plugins) are fixed prefix overhead**: every tool schema rides along on every request. Don't attach what the task doesn't need; don't toggle tools mid-session.
- **Compaction = a low-frequency cache-reset point**: compact only near the context limit (reference thresholds: 50% warn only, 60% trim stale tool output first, 80% actually compact). Do the free trims first — they often avoid a paid summary call. **Don't compact early**: compressing a warm cache throws away hits.
- **Local-only metadata changes** (decision records, message-preview rewrites) never reach the provider — they don't count as cache invalidation.

## C. Provider cache cheat-sheet

| Provider | Mechanism | Retention |
|---|---|---|
| DeepSeek | Automatic prefix caching (disk) | Hours–days, relaxed |
| Anthropic | `cache_control=ephemeral` breakpoints (auto via SDK) | ≈5 min; finish short sessions in one go |
| DashScope | Session cache | ≈5 min |
| Other OpenAI-compatible | Mostly automatic prefix caching | Vendor-dependent |

## D. Implementation checklist (agent-agnostic)

- Check context usage and usage stats; compare cache hit vs miss. Don't edit rules or system-prompt files mid-session.
- Review configured tools/MCP servers and disable unused ones — the most direct way to cut fixed prefix cost.
- For large logs: search-locate, then read only the relevant excerpt. Compress actively near the context ceiling; persist key state before closing the session.

## Cost ladder (cheapest first)

Trim stale output / drop useless history (0 API calls) < precise reading < cross-session memory < one summarization call (1 API call). **Always do the cheap ones first.**

---

*Inspired by DeepSeek-Reasonix (MIT, Copyright (c) 2026 Reasonix Contributors) · github.com/esengine/DeepSeek-Reasonix. Full attribution in the repo README.*
