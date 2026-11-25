---
name: clawhub-security-auditor-all
description: "Audit public skill or plugin bundles for ClawHub, Claude, Hermes, AgentSkill, AgentSkills.so, and GitHub release risks. Use when: checking Suspicious/upload flags, dangerous local behaviors, quality/security mismatches, legacy auth surface, or non-runtime files before publishing."
---

# Publish Security Auditor

Audit public skill and plugin bundles for patterns that commonly trigger `Suspicious` flags, marketplace rejection, quality-score collapse, or avoidable trust regressions during publishing.

## When to use

- When a skill or plugin was flagged `Suspicious` on ClawHub and you need the likely causes
- When preparing a release bundle for ClawHub, Claude, Hermes, AgentSkill, AgentSkills.so, or public GitHub distribution
- When comparing EN and ZH bundles to ensure they were trimmed consistently
- When checking whether a release bundle still contains risky helper scripts, legacy auth paths, or local credential access code
- When a package looks structurally correct but may still fail scanner, audit, or trust review

## When NOT to use

- When you only need metadata optimization or search wording; use `clawhub-skill-optimizer`
- When you need plugin manifests or marketplace wrappers; use `clawhub-plugin-packager`
- When the task is general product refactoring unrelated to publishing

## Scope boundary

This skill owns:

- suspicious-pattern detection
- upload-risk explanation
- smallest-safe cleanup recommendations
- EN/ZH consistency checks for shipped runtime scope
- frontmatter and registry mismatch detection
- quality/security trust-surface mismatch detection

This skill does not own:

- search-copy optimization
- plugin manifest generation
- broad feature redesign unless required to remove a concrete publish risk

## Core goal

Find and explain publish risks without breaking runtime behavior. Prefer:

- starting from the upstream `AIsa-team/agent-skills@agentskills` runtime when the skill already exists there
- removing non-runtime files from release bundles
- downgrading dangerous defaults to repo-local or explicit behavior
- shrinking credential surface area
- preserving the main shipped workflow

## Primary risk categories

1. Cookie extraction and local credential access
2. Dangerous external CLI invocation
3. Self-install or cache sync behavior
4. Default writes into user-home data locations
5. Legacy secret surface area
6. Version-switching or repo-mutation helpers
7. Non-runtime developer utilities in release bundles
8. Non-text files and generated artifacts
9. Aggressive persistence wording
10. Frontmatter or registry mismatch
11. Quality-score collapse from bundle drift
12. Relay / upload / OAuth side effects described too vaguely
13. Public prompt-injection or internal-scaffold wording in `SKILL.md`

### Quality-score collapse from bundle drift

Flag cases such as:

- the title promises a narrow expert workflow, but the bundle is generic or empty
- examples mention outputs the shipped files do not produce
- AgentSkill or marketplace metadata claims platform support the bundle does not actually ship
- AgentSkills.so listing signals such as weekly-download intent, repo trust, or security posture do not match the shipped bundle
- GitHub README, marketplace listing, and bundle contents disagree materially

Why this matters:

- a package can survive upload and still lose discovery because quality/security/rating reviewers see a trust mismatch

## Platform-specific review lenses

### ClawHub

- watch for `Suspicious`, source mismatch, capability/install incoherence, unsafe local side effects, and board-facing copy that would fail the downloads / installs / stars discovery surfaces
- verify that `Security Scan`, `VirusTotal`, `OpenClaw verdict`, `runtimeId`, compatibility, and README claims all agree

### Claude

- watch for runtime vs README drift, non-runtime helpers, overly broad install claims, and repo/listing mismatch that would weaken install trust

### Hermes

- watch for unsafe community wording, non-runtime references, and section/path/category mismatch that breaks atlas discovery

### AgentSkill

- watch for obvious security findings, weak implementation evidence, and copy that would depress discovery/structure/expertise scores
- watch for owner-page ladder drift where sibling bundles tell inconsistent trust stories
- quality and security pages effectively become part of the public product surface

### AgentSkills.so

- watch for repo-trust mismatch, vague task boundaries, and security-language drift
- weekly-download competition punishes generic titles and unproven workflows faster than upload scanners do
- verify that `Trust & Identity`, `Behavioral Monitoring`, `Vulnerability Exposure`, and distribution claims are backed by the shipped bundle
- if security posture is unclear, treat it as a trust regression even when upload technically succeeds

### GitHub

- watch for provenance gaps, stale README claims, and missing install proof

## Severity model

Classify every finding as exactly one of:

- `blocker`
  - high likelihood of upload rejection, `Suspicious`, or hidden trust regression
- `warning`
  - upload may succeed, but residual risk or trust fragility remains
- `note`
  - informational cleanup or polish item

## Output format

Prefer this structure:

1. Findings
   - grouped into `blocker`, `warning`, and `note`
   - include file paths, the suspicious pattern, and why the platform may care
2. Safe fixes
   - explain the smallest change that removes the risk
   - state whether runtime functionality is preserved, reduced, or unchanged
3. Final verdict
   - `ready to upload`
   - `uploadable with low residual risk`
   - `uploadable with residual risk`
   - `not ready`

## Practical rules

- do not recommend deleting core runtime code just because it looks noisy
- if the skill already exists in `AIsa-team/agent-skills`, treat that upstream runtime as the baseline and preserve its functionality unless the task explicitly asks for a behavior change
- prefer trimming publish bundles over rewriting the whole skill
- prefer API-key-only runtime auth for published bundles
- when a credential mismatch is reported, compare against a known-good uploaded bundle before touching runtime code
- if multiple invocation styles exist in docs, prefer declaring only the true shipped runtime path as required
- apply the same trimming to EN and ZH bundles; platforms may rescan them independently
- if AgentSkill or marketplace pages emphasize security or quality reviews, treat mismatched documentation as a trust issue, not just a style issue
- if AgentSkills.so positioning depends on security posture or repo trust, verify those claims against the shipped files, not just the source repo
- if a live page still shows scan output as pending or unresolved, do not collapse that into a clean/suspicious verdict

## 2026-04-20 live review lessons

### AgentSkill

- owner-page portfolios expose repeated trust mismatches quickly, so EN/ZH and sibling bundles must stay aligned
- quality-score collapse often comes from generic titles, thin examples, and bundles that feel smaller than the page claims
- large plugin families need especially strict runtime-only trimming because reviewers compare trust and scope across siblings

### AgentSkills.so

- reviewers and users infer demand from weekly-download positioning, so generic copy without proof feels suspicious even if safe
- repo-backed trust breaks when detail-page claims and bundle contents drift apart
- security posture must be described concretely: permissions, side effects, and persistence behavior all affect trust

## 2026-04-25 live suspicious lessons

- relay-based Twitter skills can be technically coherent yet still trigger `Suspicious` when key flow, media upload, or OAuth side effects are not explicit enough
- public `SKILL.md` text can trigger scanner concern even when code is fine if the copy looks like prompt injection or exposed internal prompt scaffolding
- a package can be `clean` while still carrying a trust bug when registry metadata omits a required env var already declared in the shipped bundle

## Example requests

- `Audit this skill bundle for ClawHub Suspicious risks`
- `Check whether this Claude, AgentSkill, or AgentSkills.so bundle still ships non-runtime files`
- `Compare the Hermes and ClawHub releases for the same skill and list publish risks`
- `Give me the smallest safe cleanup before uploading this package`
