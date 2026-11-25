---
name: deep-research
description: |
  Deep Research (8-step methodology) — Transform vague topics into high-quality, deliverable research reports.
  Systematic fact extraction, source tiering (L1>L2>L3>L4), time-sensitivity assessment, and verifiable "Fact→Conclusion" chains.
  Use when: deep research, comprehensive report, thorough investigation, concept comparison, decision support, trend analysis.
  Inspired by wshuyi/deep-research + OpenAI Deep Research + HKUDS.
---

# Deep Research Skill

8-step methodology: problem decomposition → source tiering → fact extraction → comparison framework → derivation chain → validation → final report.

## Usage

```bash
python3 _scripts/deep_research.py "REST API vs GraphQL" --methodology --sources --debate --save
python3 _scripts/deep_research.py "What are the tradeoffs of AI agents?" --save
```

## Options

- `query` — Research question or topic (required)
- `--methodology` — Full 8-step flow with intermediate artifacts saved to `Sources/Deep Research/<topic>/`
- `--sources` — Include external source recommendations
- `--debate` — Include steelmanned opposing views
- `--top-k N` — Max notes to retrieve (default: 15)
- `--depth N` — Graph expansion depth (default: 2)
- `--save` — Save final report to vault

## Source Tiering

L1 (official docs/papers) > L2 (official blogs) > L3 (media/tutorials) > L4 (community/forums). Conclusions must trace to L1/L2.

## Output

`Sources/Deep Research - YYYY-MM-DD.md` (or full artifact folder with `--methodology`)
