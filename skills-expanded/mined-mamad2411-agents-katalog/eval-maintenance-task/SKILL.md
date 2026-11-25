---
name: eval-maintenance-task
description: >
  Post-maintenance evaluation skill for production readiness tasks (registry cleanup, DB imports, live listings freshness, etc.).
  Uses the 8 stages AI engineering maturity lens: moves "standards" (success criteria, protection of active data, freshness) out of heads and into the system as first-class evals (Stage 5/8). Always run after one-off or recurring maintenance to produce auditable reports.
user-invocable: true
disable-model-instruction: false
---

# Eval: Maintenance Task (AI Engineering Maturity)

**Primary source**: https://upsun.com/blog/8-stages-ai-engineering-maturity/

**When to invoke**:
- After running registry cleanup (to confirm untagged space reclaimed, active tags protected, GC success).
- After full prod DB import from backup (to verify row counts, data freshness, live listings last_seen_at).
- After daily/periodic jobs (live listings import, house price ingest, etc.).
- As part of production path reviews or before promoting code that touches maintenance flows.
- In daily-standup-with-cache synthesis when tracking "production ease" items.

**Mandatory start**: Always begin by loading shared context (this skill cross-references `.github/prompts/load-project-cache-first.prompt.md` and the maturity skill itself).

**Core principles (from maturity framework)**:
- AI amplifies good practices: Our existing DDEV-only, test-safety, security-before-scale, cache-first, and guardrails must be reflected in every eval.
- Eval becomes the product (Stage 8 target): Success criteria for maintenance now live in this skill + referenced queries/scripts, not just in operator heads. Reports should be logged/committed where appropriate (e.g. .tmp/ or docs/ for audit).
- Don't skip stages: This eval assumes Stage 4+ (shared .github/ context + governance) and Stage 5 (spec-first via TODOs + risk-based checks).
- Shared context over drift: Use the project's doctl_scripts, import scripts, and Python importers. Never hardcode prod secrets or bypass .env sourcing.
- Cost/observability: Note any external calls (doctl, mysql) and their impact.

**How to use (one-liner friendly)**:
After a maintenance one-liner or script (see doctl_scripts/README.txt for exact registry/DB examples):

```bash
# Example post-registry-cleanup (with low KEEP_RECENT to address oversize/untagged)
KEEP_RECENT=3 APPLY=true RUN_GC=true FORCE=true ./doctl_scripts/cleanup_registry_tags_safe.sh
# Then invoke eval (via this skill or direct):
.github/skills/eval/maintenance-task/SKILL.md --task=registry-cleanup --apply-run=true
```

The skill will:
1. Load cache + TODO + current branch context.
2. Run targeted checks (see below).
3. Output a structured report (JSON + human summary) suitable for logging or .tmp/maintenance-eval-$(date).json.
4. Reference maturity stage and suggest advancement (e.g. "Move this eval into scheduled agent job per Stage 8").

**Specific checks (project-tailored, update as data evolves)**:

**For registry cleanup (to confirm untagged deletion + protection)**:
- Run `doctl registry repository list-tags ndestates-io-app -o json` (or the safer script's plan).
- Verify: Active production tags (from app spec via DO_APP_ID) are still present.
- Count total tags pre/post.
- Confirm GC was triggered (if RUN_GC).
- Check for recent "untagged" reduction via doctl registry get (storage usage) if available.
- Fail if active tag was deleted or tag count increased unexpectedly.

**For DB import / full prod DB refresh (clean state after import_backup or similar)**:
- Use connection from doctl_scripts (or env-sourced TARGET_*).
- Run key freshness queries (from runbooks + prior DB work):
  ```sql
  SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE();
  SELECT MAX(year) FROM house_price_index_annuals;
  SELECT MAX(quarter_start_date) FROM house_price_index_quarters;
  SELECT COUNT(*) FROM house_price_transaction_counts;
  SELECT COUNT(*) FROM live_listings;
  SELECT COUNT(*) FROM agent_live_listings;
  SELECT MAX(last_seen_at) FROM live_listings;
  ```
- Compare against expected from the backup (or local DDEV after ingest).
- Verify no regression in core tables (properties, valuations, credits, etc.).
- Check last import timestamps if columns exist.

**For live listings / daily ingest jobs**:
- Confirm recent last_seen_at within expected window (e.g. last 24-48h for active listings).
- Row counts for live_listings and agent_live_listings vs. historical baseline.
- Spot-check a few sources from the adapters.

**General output format** (for consistency and "standards in the system"):
```json
{
  "task": "registry-cleanup|db-import|live-listings",
  "timestamp": "...",
  "stage_assessment": "Current project center of gravity: Stage 4-5 (see .github/skills/ai-engineering-maturity/SKILL.md)",
  "checks": { ... },
  "status": "PASS | WARN | FAIL",
  "recommendations": ["Lower KEEP_RECENT next time", "Add to scheduled agent job"],
  "maturity_advance": "This moves recurring maintenance toward Stage 6/8 (infrastructure + evals as product)"
}
```

**Security & governance (non-negotiable, Stage 4)**:
- All DB/registry access must go through existing doctl_scripts or .env-sourced vars (never hardcode).
- This skill itself triggers full security checklist + MCP threat scan if extended.
- Reports must not contain secrets.

**Cost note (Stage 6)**: External calls (doctl, mysql) should be noted in the report. Prefer cached/ local checks where possible.

**Cross-references** (always load these first):
- `.github/prompts/load-project-cache-first.prompt.md`
- `.github/skills/ai-engineering-maturity/SKILL.md`
- `.github/prompts/daily-standup-with-cache.prompt.md` (include maturity indicators)
- copilot-instructions (DDEV, security on agent changes, data safety)
- git-workflow-guardrails (for any resulting commits)
- doctl_scripts/README.txt and the specific maintenance scripts
- docs/codebase/CONCERNS.md (AI Engineering Maturity item)
- TODO carry for production path items

**Advancement using this skill**:
- After successful eval, consider promoting the task to a scheduled/audited agent job (see Stage 8: recurring jobs as first-class, central logs).
- Update this skill with new project-specific checks as data models or maintenance needs evolve.
- Reference the report in branch context or PR descriptions when the maintenance enables a production push.

When extending or invoking: Re-run full security checklist. Do not skip governance.

**Grok note**: Surface current maturity stage + one advancement step when this skill is used in a briefing. Cite https://upsun.com/blog/8-stages-ai-engineering-maturity/

This skill turns manual "run the script and hope" into auditable, repeatable, standards-living-in-system maintenance — directly easing the path to production by making clean registry state, clean DB data, and fresh listings verifiable and low-friction.