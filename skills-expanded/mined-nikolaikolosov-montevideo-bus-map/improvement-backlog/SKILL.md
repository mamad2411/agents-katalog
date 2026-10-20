---
name: improvement-backlog
description: Produce the prioritized improvement proposals - each with evidence, effort class, impact, and the risk of NOT doing it. Adopt track phase A2; also used at Handover.
---

# /improvement-backlog

Owner: **adoption-lead** (adopt) or **product-director** (handover); inputs from
**lead-architect**, **security-lead**, **performance-engineer**, **qa-lead**, **cost-analyst**.

## Sequence
1. Source findings from the current-state report (adopt) or the phase reports (greenfield
   handover). A proposal without an evidence link back to a finding is opinion — cut it.
2. Per proposal (template: improvement-backlog.md): what, why now (evidence ref), effort class
   (S <1w / M 1-4w / L >1mo), impact (user/business/engineering — named metric where possible),
   risk of NOT doing it, dependencies on other proposals.
3. Categories forced for balance: security, correctness, performance, maintainability,
   cost, developer experience, product opportunities. Empty category = state why.
4. Prioritization by product-director: impact first, quick wins (S×high-impact) surfaced top;
   sequencing respects dependencies (build-health and test-safety-net items usually first).
5. The user reviews and re-ranks per operation_mode.

## Output
audit/improvement-backlog.md (or product/improvement-backlog.md at handover): ranked table +
one paragraph per proposal; top-5 summary for the user.
