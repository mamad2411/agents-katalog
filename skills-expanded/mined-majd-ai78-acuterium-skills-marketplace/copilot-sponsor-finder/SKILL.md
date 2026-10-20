---
name: copilot-sponsor-finder
display_name: Sponsor Finder
skill_id: ACU-SKILL-1987
version: 1.0.0
category: code-review
thread: T04
domain: cognitive
shard_affinity:
  - AcuTect-CODEX
layer_access:
  - L5
  - L6
  - L7
  - L8
sovereignty_score: 10
governance_level: mandatory
source_repo: github/awesome-copilot
triggers:

---

# Sponsor Finder

## Description
Find which of a GitHub repository's dependencies are sponsorable via GitHub Sponsors. Uses deps.dev API for dependency resolution across npm, PyPI, Cargo, Go, RubyGems, Maven, and NuGet. Checks npm funding metadata, FUNDING.yml files, and web search. Verifies every link. Shows direct and transitive dependencies with OSSF Scorecard health data. Invoke with /sponsor followed by a GitHub owner/repo (e.g. "/sponsor expressjs/express").

## Acuterium Integration
- **Thread:** T04 — ACIW
- **Shard:** AcuTect-CODEX
- **Layers:** L5, L6, L7, L8
- **Governance:** mandatory
- **Sovereignty Score:** 10/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/sponsor-finder/SKILL.md
- **Author:** GitHub Copilot Community
