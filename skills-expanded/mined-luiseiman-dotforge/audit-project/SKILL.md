---
name: audit-project
description: Audits the Claude Code configuration of a project against the dotforge template. Generates a report with score and gaps.
context: fork
---

# Audit Project

Run a full audit of the Claude Code configuration for the current project.

## Step 1: Detect stack

Use detection rules from `$DOTFORGE_DIR/stacks/detect.md`.

## Step 1b: Detect project tier

Auto-detect project tier based on signals:
- **simple** (<5K LOC, 1 stack, no CI config): recommended items are relaxed (items 8-10 don't penalize)
- **standard** (5K-50K LOC, 1-2 stacks): default behavior
- **complex** (>50K LOC, 3+ stacks, monorepo indicators like `packages/` or `apps/`): recommended items 8-10 become semi-obligatory (each worth 0-2 instead of 0-1)

Detection signals:
1. LOC: count non-empty lines in source files (`find . -name '*.py' -o -name '*.ts' -o -name '*.js' -o -name '*.go' -o -name '*.java' -o -name '*.swift' | xargs wc -l`)
2. Stack count: number of stacks detected in step 1
3. CI: presence of `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`
4. Monorepo: presence of `packages/`, `apps/`, `lerna.json`, `pnpm-workspace.yaml`, `turbo.json`

Save tier in registry entry.

## Step 1c: Config coherence check

Before scoring, validate internal coherence. Run `$DOTFORGE_DIR/tests/test-config.sh <project-dir>` or perform equivalent checks inline:

1. Hooks referenced in settings.json exist and are executable
2. Rules have valid `globs:` or `paths:` frontmatter (with `alwaysApply: false` for lazy loading)
3. Rule globs match at least 1 real file in the project
4. settings.json is valid JSON with deny list covering .env, *.key, *.pem
5. CLAUDE.md has minimum required sections (stack, build/test, architecture)
6. No contradictory allow+deny patterns in settings.json
7. No prompt injection patterns in rules or CLAUDE.md

If coherence check finds critical failures (missing hooks, invalid JSON), report them in a `── COHERENCE ──` section BEFORE the score. These are configuration bugs, not gaps.

## Step 2: Load checklist

Read `$DOTFORGE_DIR/audit/checklist.md` for evaluation criteria.
Read `$DOTFORGE_DIR/audit/scoring.md` for weights and caps.

## Step 3: Evaluate

For each checklist item, verify existence **and quality**:

### Obligatory (0-10 points)
1. **CLAUDE.md / AGENTS.md** — Does the instruction file Claude actually loads exist? `CLAUDE.md` if present (plus `AGENTS.md` when `CLAUDE.md` has an `@AGENTS.md` line); otherwise `AGENTS.md` alone (native since v2.1.277). Warn, without penalizing, when both exist with no import — `AGENTS.md` is then ignored and the copies drift. Verify it has key sections:
   - Stack/technologies mentioned explicitly
   - At least 1 exact build/test command
   - Project structure or architecture
   - Do NOT count only lines — a 50-line boilerplate file is score 1
2. **settings.json** — Does it exist in `.claude/`? Does it have explicit permissions? Does it have a deny list? Warn (do not fail) on: boolean `"attribution": false` in the shared file (older CLIs skip the whole file, v2.1.281), project-scope-inert keys (`defaultMode: auto|bypassPermissions`, `sandbox.credentials`, telemetry env — see `domain/permission-managed-settings.md`), allow rules with a wildcard before the subcommand (`Bash(git * main)`)
3. **Rules** — Is there at least 1 rule in `.claude/rules/`? Does it have frontmatter with `globs:` or `paths:`?
4. **Hook block-destructive** — Verify:
   - Does `.claude/hooks/block-destructive.sh` exist?
   - Is it executable? (`test -x` or check permissions)
   - Is it referenced in `.claude/settings.json` under hooks?
5. **Build/test commands** — Are they in CLAUDE.md? Do they match the detected stack?

### Dimension A — Native Health, Recommended (0-10 bonus points)
6. **.gitignore** — Does it protect .env, *.key, *.pem, credentials?
7. **Prompt injection scan** — Are rules/CLAUDE.md free of suspicious patterns?
8. **Auto mode safety** — Auto mode is active when `permissions.defaultMode` is `"auto"` OR absent (session default since Claude Code v2.1.284). In both cases, is the deny list complete? Pass only if deny covers secrets or `defaultMode` is explicitly non-auto. Missing settings.json → 0
9. **OS-level sandboxing** — `sandbox.enabled: true` with at least one restriction OR project demonstrably handles no secrets (auto-pass)
10. **Hook lint** — Does it exist? Is it executable? (verify `chmod +x`)
11. **Auto-memory well used (NEW)** — Is `MEMORY.md` a concise index (<200 lines AND <25KB), not a content dump? If errors are tracked, `CLAUDE_ERRORS.md` exists with table format (Type column). Penalize dumping content into the index — only first 200 lines / 25KB are injected per session.
12. **Permission cascade (NEW)** — Are machine-local overrides kept in `settings.local.json` rather than polluting versioned `settings.json`? Auto-pass if no local overrides needed.
13. **Attribution configured (NEW)** — `attribution.commit`/`attribution.pr` set (not the deprecated `includeCoAuthoredBy`)? Auto-pass if the default co-author is acceptable. For self-hosted forges, check `prUrlTemplate`.
14. **Custom commands** — Are there files in `.claude/commands/`?
15. **Agents** — Is there `.claude/agents/` + `agents.md` rule in rules?

**Tier adjustments (dimension A):**
- `simple`: items 14-15 score 0 don't penalize (treated as N/A)
- `complex`: items 14-15 become semi-obligatory (each 0-2 instead of 0-1)

### Dimension B — dotforge Adoption (informational, 0-4, does NOT affect native_health)
- **B1. v3 behaviors compiled** — `.claude/hooks/generated/*.sh` exist AND referenced in settings.json?
- **B2. Workflow availability (v4)** — `workflows/` with at least one `.js` containing `export const meta`?
- **B3. Domain rules** — at least one rule in `.claude/rules/domain/` with `last_verified` <90 days? Report stale count.
- **B4. Sync recency** — project `dotforge_version` == `$DOTFORGE_DIR/VERSION`?

A project scoring B=0 (native-first) is a valid, non-penalized outcome. Never recommend adopting dotforge machinery just to raise B.

## Step 4: Calculate scores (two dimensions)

Use weights from `$DOTFORGE_DIR/audit/scoring.md`:

**Dimension A — Native Health (the primary score):**
1. `native_health_obligatory = sum(items 1-5)` — maximum 10
2. `native_health_recommended = sum(items 6-15)` — maximum 10
3. `native_health = native_health_obligatory * 0.7 + native_health_recommended * 0.3` — max 10.0
4. Apply tier adjustments before calculating (see Step 1b)
5. `native_health = min(native_health, 10)`

**Security cap:** If item 2 (settings.json) or item 4 (block-destructive) is 0, `native_health` max = 6.0.

**Dimension B — dotforge Adoption (informational):**
6. `forge_adoption = sum(items B1-B4)` — 0 to 4. Does NOT enter native_health.
7. Label: 0=None, 1-2=Partial, 3=Most, 4=Full.

## Step 5: Generate report

Format:
```
═══ AUDIT dotforge: {{project}} ═══
Date: {{YYYY-MM-DD}}
Detected stack: {{stacks}}
Tier: {{simple|standard|complex}}
dotforge version: {{version from last bootstrap/sync if detectable}}
Native Health: {{X.X}}/10 {{level}}
dotforge Adoption: {{N}}/4 {{None|Partial|Most|Full}}  (informational — does not affect Native Health)

═ DIMENSION A — NATIVE HEALTH ═

── OBLIGATORY ──
{{✅|⚠️|❌}} CLAUDE.md ({{0-2}}) — {{detail: which sections exist/missing}}
{{✅|⚠️|❌}} settings.json ({{0-2}}) — {{detail: deny list yes/no, permissions}}
{{✅|⚠️|❌}} Rules ({{0-2}}) — {{detail: N rules, globs yes/no}}
{{✅|⚠️|❌}} Hook block-destructive ({{0-2}}) — {{detail: executable yes/no, wired yes/no}}
{{✅|⚠️|❌}} Build/test commands ({{0-2}}) — {{detail: which ones and whether they match the stack}}

── RECOMMENDED ──
{{✅|⚠️}} .gitignore — {{detail}}
{{✅|⚠️}} Prompt injection scan — {{detail}}
{{✅|⚠️}} Auto mode safety — {{detail: auto mode active/inactive, deny list complete/incomplete}}
{{✅|⚠️}} OS sandboxing — {{detail: enabled/disabled, secret indicators yes/no}}
{{✅|⚠️}} Hook lint — {{detail: executable yes/no}}
{{✅|⚠️}} Auto-memory well used — {{detail: MEMORY.md lines/KB, index vs dump, CLAUDE_ERRORS yes/no}}
{{✅|⚠️}} Permission cascade — {{detail: settings.local.json used / no local overrides}}
{{✅|⚠️}} Attribution configured — {{detail: attribution.* set / deprecated includeCoAuthoredBy / default ok}}
{{✅|⚠️}} Custom commands — {{detail: N commands}}
{{✅|⚠️}} Agents — {{detail}}

═ DIMENSION B — DOTFORGE ADOPTION ═ (informational)
{{✅|—}} B1 v3 behaviors compiled — {{detail: N generated hooks, settings reference yes/no}}
{{✅|—}} B2 v4 workflow availability — {{detail: N .js workflows OR "none"}}
{{✅|—}} B3 domain rules — {{detail: N rules, M stale >90d}}
{{✅|—}} B4 sync recency — {{detail: project version vs current VERSION}}

── DOMAIN KNOWLEDGE ──
Role defined:     {{✓ if ## Role exists in CLAUDE.md with content | ✗ otherwise}}
Domain rules:     {{N files in .claude/rules/domain/ | "none"}}
Stale (>90 days): {{N files with last_verified older than 90 days | "none"}}
Coverage:         {{list glob patterns from domain rules → cross-reference with git log --name-only -30 to estimate % of recent edits covered}}

Note: Domain knowledge is informational only — does not affect the audit score.
If no domain rules exist and the project has business logic, suggest: /forge domain extract

── CRITICAL GAPS ──
1. {{what is missing}} → {{recommended action}}
2. ...

── NEXT STEP ──
Run `/forge sync` to apply the dotforge template and close the gaps.
```

## Step 6: Cross-project error promotion

If the project has `CLAUDE_ERRORS.md`, scan it for recurring patterns:
1. Read `CLAUDE_ERRORS.md` and group errors by Area column
2. If any Area has 3+ entries with similar root causes, it's a candidate for promotion
3. Check `$DOTFORGE_DIR/practices/inbox/` and `active/` for existing practices covering that pattern
4. If no existing practice covers it, create a new practice in `practices/inbox/` using the capture format:
   - `source_type: cross-project`
   - `tags: [error-promotion, <area>]`
   - Description: the recurring pattern and derived rule
5. Report promotions in the audit output under `── ERROR PATTERNS ──`

This closes the Memory → Learning synergy: recurring project errors feed the practices pipeline.

## Step 7: Audit gaps as practices

For each obligatory item scored 0 or 1, and each recommended item scored 0:
1. Check if a practice already exists in `practices/inbox/` or `active/` for that gap
2. If not, create a practice in `practices/inbox/`:
   - `source_type: audit-gap`
   - `tags: [audit-gap, <item-name>]`
   - Description: what's missing and recommended fix
3. Only create practices for gaps that reflect a template/stack issue (not project-specific misconfigurations)
4. Report in audit output under `── CAPTURED GAPS ──`

This closes the Audit → Learning synergy: detected gaps feed back into the practices pipeline.

## Step 8: Update registry

Update the project entry in `$DOTFORGE_DIR/registry/projects.local.yml` (create it from the `projects.yml` header with `projects: []` if missing — never write to `projects.yml`, the shipped template):
- `score:` with `native_health` (the primary score — preserves trend continuity with prior audits)
- `forge_adoption:` with the dimension-B value (0-4)
- `last_audit:` with the current date
- `dotforge_version:` with the VERSION version if the project was bootstrapped
- `last_sync:` preserve the existing value (do not modify here)
- `notes:` brief summary of the audit
- `history:` append a new entry `{date: YYYY-MM-DD, score: X.X, adoption: N, version: <dotforge_version>}`. Never overwrite previous entries — this enables trending over time.

**Transition note:** the two-dimension model (v4.x) changes how scores compose vs the single-score model. Native-first projects (no behaviors/workflows) will show HIGHER `native_health` than their old single score because dimension-B items no longer penalize them. Expect a one-time step in the history trend at the first two-dimension audit; this is by design, not a regression.
