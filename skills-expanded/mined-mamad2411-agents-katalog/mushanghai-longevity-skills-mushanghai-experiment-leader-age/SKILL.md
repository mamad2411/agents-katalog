# mushanghai-experiment-leader/AGENTS.md

> Five modes for the proposal lifecycle: Proposal Bootstrap to TL Review to SOP to Consent to Mid-experiment Status. See `../AGENTS.md` for family-level conventions.

## Modes

| Letter | Name | Trigger | Primary Output Path |
|---|---|---|---|
| A | Experiment Leader - Proposal Bootstrap | draft, propose, build, seed hypothesis | `experiments/<track>/<seed-name>.md` |
| B | Track Leader - Proposal Review | review, approve, Track Leader review | chat review or proposal-adjacent note |
| C | Participant SOP | SOP, participant script, approved proposal | `experiments/<track>/<seed-name>-sop.md` |
| D | Consent + Disclaimer | consent, disclaimer | `experiments/<track>/<seed-name>-consent.md` |
| E | Mid-experiment Status | mid-experiment, status, blocker, revision ask | completed TL handoff note |

## Local Layout

- `SKILL.md` - five-mode router and step order.
- `references/biobloom-variant.md` - BioBloom overrides for the short sprint.
- `references/mid-experiment-status.md` - Mode E timing and scope.
- `assets/proposal-template.md` - Mode A proposal scaffold.
- `assets/review-checklist.md` - Mode B TL review checklist.
- `assets/sop-template.md` - Mode C participant SOP scaffold.
- `assets/consent-template.md` - Mode D consent and disclaimer scaffold.
- `assets/preflight-checklist.md` - Mode C launch-readiness checks.
- `assets/mid-experiment-status.md` - Mode E TL handoff template.

## Where to Look

| Task | Location | Notes |
|---|---|---|
| Draft a proposal | `assets/proposal-template.md` | Filled in by Mode A. |
| Review a proposal | `assets/review-checklist.md` | Walk every item, no shortcut. |
| Compress for BioBloom | `references/biobloom-variant.md` | Load when cohort is BioBloom. |
| Generate launch SOP | `assets/sop-template.md` | Requires TL approval first. |
| Prepare status handoff | `assets/mid-experiment-status.md` | Pair with `references/mid-experiment-status.md`. |

## Local Conventions

- For Proof of Living, Interaction must follow `../mushanghai-canon/references/proof-of-living.md`.
- Proof of Living Interaction needs four hashtags, platform handles, and weekly cadence.
- Mode B decisions use APPROVE, REVISE, or REJECT only.

## Anti-Patterns (this skill)

- Filling Proof of Living Interaction without all four required hashtags.
- Using an old placeholder name instead of Proof of Living.
- Approving health-risky proposals without escalation.
- Generating SOP or consent before TL approval exists.

## Hand-Offs

- Mode A hands to Mode B after the Track Leader receives the proposal.
- Mode B hands to Mode C and Mode D after approval.
- Mode E coordinates with `mushanghai-track-leader` Mode D.
