# AGENTS.md — docs/

Postmortems, ROI analyses, and multi-reviewer synthesis docs that live with the repo. NOT user-facing — these are operator references.

## Files

- **`kimi-search-roi-analysis.md`** — ROI breakdown for the Kimi search provider. Concludes that Kimi search is the slowest, least reliable, and most expensive provider with minimal unique-URL contribution; that's why `KIMI_API_KEY` is currently unset in production. The provider code is preserved (registry pattern) so it activates if the key is ever set. Kimi *fetch* is a separate path and remains active.
- **`mcp-empty-payload-anomaly.md`** — Postmortem for an open intermittent bug: under 3+ concurrent long-running `answer` calls, ~20% of MCP responses come back as empty JSON-RPC envelopes. Workaround: serial calls. Not fixed at time of writing.
- **`mcp-empty-payload-anomaly-v02.md`** — Follow-up investigation; refines the reproducer.
- **`skip_providers_review_synthesis.md`** — 9-reviewer hydra-heads synthesis of the fetch waterfall's `skip_providers` parameter. Canonical example of how reviews are run on this codebase.

## Conventions

- **Postmortems**: include reproduction steps, root cause (or "still investigating"), workaround, and a link to the relevant code path.
- **ROI / cost analyses**: include the data, the methodology, and the conclusion. Numbers should be reproducible from the raw R2 traces.
- **Synthesis docs**: name them `<feature_or_change>_review_synthesis.md`. Include the list of reviewers + their verdicts + the consensus action list.
- **Don't put user-facing docs here.** README.md is for users; this folder is for engineers debugging an incident.

## Related

- `../AGENTS.md` — repo root
- `../README.md` — user-facing docs
- `docs/skip_providers_review_synthesis.md` is referenced from `src/server/AGENTS.md` and the README's "Smoke tests" section
