---
name: feature-tracking
description: Maintain portable Feature Track docs for project features. Use when designing, planning, implementing, reviewing, or finishing feature work; creating or updating PRD/API/design/implementation docs; adding a new feature; or validating docs/features.
---

# Feature Tracking

Use Feature Track as the current operational memory for feature work. The neutral spec is the source of truth; this Codex skill is only an adapter.

Read `references/spec.md` before changing feature docs.

## Default Workflow

Before feature work:

1. Read `docs/features/README.md` if it exists.
2. Identify the feature id from the request, code module, route, domain name, or existing docs.
3. Read `docs/features/<feature-id>/README.md` if it exists.
4. If no track exists, create one and add it to the index.

During work, update the feature track when behavior, decisions, endpoints, data models, dependencies, rollout constraints, tests, or source-of-truth links change.

Before completion:

1. Update the feature README for the actual outcome.
2. Update `docs/features/README.md` if status, source-of-truth links, dates, or notes changed.
3. Run validation when available:

```bash
python3 cli/feature_track.py validate --root .
```

If the project does not include this CLI, use `scripts/validate_feature_tracks.py` from this skill.

