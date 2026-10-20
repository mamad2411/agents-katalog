---
name: seed-from-web
description: Bootstrap-time skill that web-researches the latest popular security certifications per domain and drafts JSON stubs for any missing ones, as one PR per domain.
---

# seed-from-web

## When to use

- Right after the initial hand-curated seed PR has been merged, to expand
  coverage from ~30 to ~100+ certs.
- Periodically (e.g. quarterly), to catch certifications introduced since
  the last sweep.

## Process

For each domain in `data/domains.json`:

1. **WebSearch** with queries shaped like:
   - `"top security certifications 2026 <domain label> ranked"`
   - `"<domain label> certification ANSI accredited 2026"`
   - `"<domain label> certification DoD 8140 baseline 2026"`
   - For Japan-specific domains, add: `"<domain label> 認定資格 IPA OR JPCERT 2026"`
2. **Collect candidate cert names**, deduplicating against the existing
   manifest. Skip courses, training programs, and non-proctored "badges".
3. For each surviving candidate, call the `add-cert` skill workflow
   (fetch official + 2 third-party, write JSON, leave evaluation null).
   **Populate `prerequisites.recommended_certs[]`** when the official page
   identifies prerequisites — these power the roadmap UI's arrow overlay
   and are easy to harvest at this step.
4. **Group results by domain** into one PR per domain. PR title:
   `seed: <domain> (<n> new certs)`. PR body lists each cert with its
   official URL.
5. **Run `make validate` and `make manifest`** before opening the PR. Run
   `make evaluate` locally if the maintainer wants tier outputs in the same
   PR; otherwise leave `evaluation.computed_tier = null` and let the
   maintainer trigger evaluation on review.
6. **Run `python3 scripts/infer_relationships.py --dry-run`** so the
   per-domain PR also surfaces any prereq edges the new certs should
   acquire. Apply the accepted edges before merge so the roadmap arrows
   reflect the new certs immediately.

## Refusal conditions

- A candidate cert lacks any third-party evaluation: skip it, list it in
  the PR body under "deferred candidates" with the reason.
- A candidate's official site is unreachable: skip it, add a TODO in the
  PR body.

## Anti-goal

This skill must **not** simply scrape Paul Jerimy's or CyberDudeKZ's lists
and convert them to JSON. The list of candidates must come from web search
(or government / accreditation bodies). The two reference roadmaps may be
linked in `sources[]` with `"use": "inspiration_only"` but never as the
primary discovery mechanism.
