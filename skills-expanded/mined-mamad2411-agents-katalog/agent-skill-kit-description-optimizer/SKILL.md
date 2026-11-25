---
name: agent-skill-kit-description-optimizer
description: Optimize a SKILL.md description for trigger quality — generate synthetic positive and negative queries, score the current description by hit-rate vs false-positive, and propose three ranked rewrites. Use when the user asks to auto-tune, improve, or rewrite a skill description, fix a skill that never fires, or measure description quality.
tier: app
license: Apache-2.0
compatibility: requires `skills-ref` CLI
---

# Agent Skill Description Optimizer

Wraps `skills-ref optimize`. Generates trigger queries, scores the current description against the F04 rubric, and proposes three deterministic rewrites. The `--apply N` flag commits the chosen variant back to disk with byte-preservation of every other line.

## When to use

- "Improve this description"
- "Why doesn't my skill ever fire?"
- "Optimize the SKILL.md descriptions in this tree"
- "Rewrite this description to score higher"
- "Measure description quality before shipping"

## Where LLM-quality variants come from

The CLI ships **deterministic** variants only — three template-based transforms, < 200 ms, no network, no API keys, no provider config. This is intentional: when the skill runs inside an AI harness (Claude Code, an SDK agent, etc.), the calling harness *is itself* an LLM with provider credentials already attached. Asking the CLI to hold a separate API key duplicates auth surface for no benefit.

When higher-quality rewrites are wanted, the harness does the work:

1. Run `skills-ref optimize <dir> --baseline-only --format json` to get the current score + breakdown.
2. The harness reads the SKILL.md and generates its own three improved descriptions, using whatever model/auth it already has.
3. The harness writes the chosen description directly into the YAML frontmatter (Edit / Write).
4. Run `skills-ref validate <dir>` to confirm the post-edit file passes (the same gate `--apply` uses internally).

`--apply N` remains useful for the deterministic case — it preserves bytes and auto-rolls back on validation failure.

## Invocation

```bash
# Score the current description only (no rewrites)
skills-ref optimize /path/to/skill-dir --baseline-only

# Score + propose three ranked variants (sorted by F04 score desc)
skills-ref optimize /path/to/skill-dir

# Apply variant 0 in-place (with re-validation safety + auto-rollback)
skills-ref optimize /path/to/skill-dir --apply 0

# Machine-readable output for the CI gate
skills-ref optimize /path/to/skill-dir --format json
```

## Output shape

Human format reports the baseline and each variant on its own block:

```
/abs/path/SKILL.md
  provider: none
  baseline: score=98/100 hit=6/8 false=1/8
  variants:
    [0] score=99/100 hit=5/8 false=1/8
        rationale: lead-with-verb + append trigger phrase
        text: <rewritten description>
```

JSON format is canonical sorted-key output containing `baseline`, `variants`, `queries`, `provider`, `path`. Both runtimes emit byte-identical JSON (parity-tested against the frozen `.agents/skills/agent-skill-kit-commons/fixtures/optimize/expected/low-score-vague.json` snapshot).

## Two scores per variant

- **`score`** — F04's description-quality score (0–100). The deterministic ranker sorts variants by this.
- **`hit_rate.score`** — `(positive_hits / positive_total - false_positives / false_total) * 100`, clamped to 0–100. Surfaced for CI gating without re-running F04's scorer.

## Safety contract for `--apply`

- The `description:` line in the YAML frontmatter is replaced; every other line is byte-preserved.
- A `.bak` file is created before write.
- After write, the validator runs against the same directory.
- On validation failure, the backup restores the original and the `.bak` is removed; the CLI exits 1.
- On success, the `.bak` is deleted; the CLI exits 0.

## Limits

- The deterministic rewriter is intentionally conservative — three template-based transforms, no LLM. For higher-quality variants, see "Where LLM-quality variants come from" above; the harness generates them, the CLI does not.
- The `chars / 4` token estimate from the prompt emitter is not used here; the optimizer's input is bounded by the body excerpt (first 1000 chars) and the query JSON.
- The trigger-phrase regex re-uses F04's; both share the same edge cases (e.g. "for " inside "helpful for" matches as a trigger). The lint pipeline is the canonical filter; this skill defers to it.

## Reference

Full specification: see the canonical spec at [../../../agentskills.io.md](../../../agentskills.io.md).
