---
name: verify-stage-completeness
description: Use BEFORE marking a stage Done. Audits the stage's diff for new IUserOwned entities, new services, new resx templates, and new enum values, and verifies each lands in EVERY registry a downstream consumer iterates (DbSet + OnModelCreating + model-derived `UserOwnedModel.RlsTables` membership + RLS migration + DI + IgnoreQueryFilters allow-list + EN/ES resx pair + EmailTemplateKey enum + AuditLogAction documented-set test). Catches the class of bug where a Stage N feature ships entity #1 + service #2 + controller #3 but forgets registry #4, leaving a latent gap (no global query filter, no RLS policy, missing translation, untracked enum value) until a real user hits the wrong code path. HARD-enforced via a PreToolUse hook on the stage-close-out edit; this doc explains the rule so the hook is satisfied in advance.
---

# verify-stage-completeness

## 1 — Why this skill exists

The project has FIVE+ "single source of truth" registries that every new entity / service / template / enum value has to land in for end-to-end correctness:

| # | Registry | What iterates it |
|---|---|---|
| 1 | `AppDbContext.DbSet<T>` declaration | EF Core for query/save |
| 2 | `AppDbContext.OnModelCreating` configuration block | EF Core schema mapping |
| 3 | model-derived membership via `UserOwnedModel.RlsTables` (`ProjectCeres/Common/UserOwnedModel.cs`) — automatic for any concrete `IUserOwned` entity with a table; the hand-typed `UserOwnedTables.All` was deleted in Stage 9.5b | EF query-filter loop + RLS migration loop + ParityTests |
| 4 | RLS migration installing `CREATE POLICY user_isolation` | Postgres at runtime |
| 5 | `Program.cs` DI registration | ASP.NET DI container |
| 6 | `IgnoreQueryFilters()` allow-list (`ArchitectureTests.cs`) — IF the service calls `IgnoreQueryFilters()` | Architecture test |
| 7 | `EmailsResource.en.resx` + `EmailsResource.es.resx` — IF a new email template ships | `IEmailComposer` at runtime |
| 8 | `EmailTemplateKey` enum — IF a new email template ships | `IEmailComposer.Compose` |
| 9 | `AuditLogAction` documented-set architecture test — IF a new audit action ships | ParityTests-style enum guard |
| 10 | `FailedLoginReason` enum — IF a new failed-login surface ships | `FailedLoginRecorder` |

A spec-driven flow can copy a sibling entity at the file level (`EmailConfirmationToken` mirrors `PasswordResetToken`) but miss the registry level. Caught instance — 2026-05-23: `EmailConfirmationTokens` shipped with `rowsecurity = false` because it was added to #1 + #2 but not to #3, so the Stage 7.5 migration loop never installed a policy on it. Result: cross-user verification-token visibility under `ceres_app`. The full integration suite was green because `WafCollection.cs:75-76` routes through `ceres_admin` (BYPASSRLS) and never exercises the actual policy.

The existing `verify-backend` skill catches convention conflicts AT SPEC TIME (wrong status code, missing field). It does NOT enumerate cross-file registries AT STAGE-CLOSE TIME. The ParityTests catch the list→DB direction (entry exists but policy missing) but NOT the DB→list direction (table exists but entry missing). This skill closes both gaps as a pre-stage-close audit.

## 2 — When this skill fires

- **Auto (HARD) via the playbook Phase E′ gate** — PreToolUse on Edit/Write/MultiEdit against `docs/roadmap-phase-*.md` when the new_string flips a stage header from `[ ]` to `[x]` or adds `✅ Done`. Runs BEFORE the existing Phase E gate (`sync-docs` / `changelog-sync` / unchecked-items check). If E′ denies, E never runs.
- **Manual** — invoke `Skill name=verify-stage-completeness` to dry-run the audit against the current stage's diff without attempting a close-out.

## 3 — The audit procedure

The hook at `.claude/skills/verify-stage-completeness/hooks/stage-completeness-check.js` runs the checklist mechanically. **The audit reads the codebase as it stands right now — no git, no diff, no "what changed".** A broken cross-reference is a gap whether it was introduced this commit or two years ago. The trigger is a stage-close edit; the scope is the entire codebase. The rationale: if a Stage N close-out is allowed to pass a gap that pre-dated Stage N, the gap will never get caught — every later stage's close-out will also pass it.

### 3.1 — For every persisted entity under `ProjectCeres/Models/*.cs`

- Parse every `public class TypeName` declaration. Skip `abstract` classes (TPC roots like `Movement` are intentionally not tables).
- **Check D1 (HARD):** is there a `DbSet<TypeName>` declaration in `ProjectCeres/Data/AppDbContext.cs`? If no → not a persisted entity, skip the rest of the checks for this class.
- **Check D2 (advisory):** is there a `modelBuilder.Entity<TypeName>` block in `AppDbContext.cs`? Marked `n/a` if missing — many entities are configured by iteration over the model-derived user-owned set (`UserOwnedModel.RlsTables`) rather than per-entity blocks, so a missing explicit block is legitimate.
- **Conditional checks — only if the type implements `IUserOwned`:**
  - **Check U1 (HARD):** does the entity appear in the model-derived user-owned set (`UserOwnedModel.RlsTables`)? Since 9.5b this is automatic for any concrete `IUserOwned` entity with a table — so the real failure mode is an entity that should implement `IUserOwned` but doesn't. If the entity is user-owned-by-nature but the marker interface is missing → gap.
  - **Check U2 (HARD):** is there a `CREATE POLICY user_isolation` migration under `ProjectCeres/Migrations/` that covers the table — either by an explicit `ON "TableName"` reference, OR by iterating the model-derived user-owned set (covers entries present at migration time)? If no → gap.

### 3.2 — For every `Service.cs` under `ProjectCeres/Common/Authentication/` or `ProjectCeres/Services/`

- Parse the class name.
- **Check S1:** is there an `AddScoped<ClassName>()` or `AddSingleton<ClassName>()` in `Program.cs`? If no → gap.
- **Check S2:** does the service file contain `IgnoreQueryFilters(`? If yes:
  - is the relative file path in the `allowed` set inside `ArchitectureTests.cs § IgnoreQueryFilters_only_appears_in_documented_exception_paths`? If no → gap.

### 3.3 — For every resx key matching `<KeyName>.Subject` in `EmailsResource.en.resx`

- **Check R1:** are matching `KeyName.BodyText` and `KeyName.BodyHtml` entries also present in `en.resx`? If no → gap (3-key contract).
- **Check R2:** are all three keys (`Subject` / `BodyText` / `BodyHtml`) also present in `EmailsResource.es.resx`? If no → gap.
- **Check R3:** is the key name added as a value in the `EmailTemplateKey` enum at `ProjectCeres/Common/Email/EmailTemplateKey.cs`? If no → gap.

### 3.4 — For every value in the `AuditLogAction` enum in `ProjectCeres/Models/AuditLog.cs`

- **Check A1:** is the value listed in the `expected` array of `ArchitectureTests.cs § AuditLogAction_enum_values_match_documented_set`? If no → gap.

### 3.5 — For every value in the `FailedLoginReason` enum in `ProjectCeres/Models/FailedLoginAttempt.cs`

- **Check F1:** is the value referenced in at least one `FailedLoginReason.<Name>` call site across `ProjectCeres/`? If no → gap. (Unused enum values are a code smell that indicates a half-wired surface.)

## 4 — Output shape

The hook only reports items that have at least one ✗ gap (a healthy item is silent). On a clean codebase the hook returns `permissionDecision: "allow"` with no message; on a codebase with gaps it denies the close-out with a structured report. Example output that the Stage 9.3 close-out would have produced **before** the 9db67df fix:

```
verify-stage-completeness — codebase audit (live state):

Entities with gaps (1):
  EmailConfirmationToken:
    ✗ U1: typeof(EmailConfirmationToken) in UserOwnedTables.All
    ✗ U2: CREATE POLICY user_isolation migration covers "EmailConfirmationTokens"

Summary: 2 gap(s) found across the codebase. Stage close-out blocked.
```

The audit reports gaps in *any* entity / service / template / enum value, not just ones added during the current stage. A pre-existing gap that no prior close-out caught is exactly the class of bug this gate is designed to surface.

The gap on U1 + U2 is the exact pair the Stage 9.3 close-out shipped silently. With this skill in place, the Phase E′ gate would have denied the roadmap edit until both were closed.

## 5 — Bypass + escalation

- **Per-session bypass:** `CERES_SKIP_STAGE_COMPLETENESS_HOOK=1`. Use when the audit fires a false positive on a deliberately-incomplete stage (e.g. one that legitimately splits across two roadmap entries).
- **Initial enforcement level: HARD.** The class of bug it catches is security-sensitive (RLS gaps, missing translations, untracked enums). Advisory-first was rejected because the existing parity test already covers the easy half — the gaps that slip through are exactly the ones a HARD gate would catch.

## 6 — What this skill does NOT do

- Does not check spec / plan content against project conventions. That's `verify-backend` / `verify-frontend`.
- Does not enforce TDD discipline. That's `superpowers:test-driven-development`.
- Does not detect bugs inside the entity's own code (RLS-aware service implementation correctness). The Stage 9.10 RLS-pre-auth-write audit covers that.
- Does not block code commits — only roadmap close-out edits. The implementation can ship gappy and tests can pass against `ceres_admin`; the gate fires only when someone tries to call the stage done.

## 7 — Auxiliary tool: turn-shape.json generator

`lib/turn-shape-generator.js` is a standalone Node script (no npm deps) that emits a `turn-shape.json` evidence-bundle slot. It scans the assistant's text in the latest turn of the Claude Code JSONL transcript for three claim types — **fix mentions** (verbal-promise gap), **confidence claims** (research-before-confidence gap), and **runtime assertions** (Field=value claims) — and records whether each one has a co-located tool call (Edit/Write/MultiEdit for fixes; WebFetch/WebSearch/Agent for confidence; Bash with psql/curl/cat/etc. or a matching Read for runtime). False-positive avoidance follows the `discussion-frame-strip` precedent: code blocks, blockquotes, diagnosis-template headings, and quote-introducing prefixes are stripped before pattern matching.

Manual invocation (once `tools/agent-env/finalize.sh` lands, this becomes one line of that script):

```bash
node .claude/skills/verify-stage-completeness/lib/turn-shape-generator.js \
  --transcript "$CLAUDE_TRANSCRIPT_PATH" \
  --stage-id "9.5a" \
  --output ".claude/state/evidence/stage-9.5a/turn-shape.json"
```

The consumer is the evidence-bundle Stop hook (sibling sub-task #33).

## 8 — Linked memory

- `feedback_iuserowned_requires_five_registries` — the underlying rule this skill enforces.
- `feedback_finished_stages_have_no_unchecked_items` — sibling gate at Phase E (this skill is the structural-completeness sibling of the unchecked-items completeness check).
- `feedback_deferral_requires_receiving_stage_checkbox` — Phase D sibling.
- `reference_playbook_skill` — Phase E′ is documented in the playbook constitution alongside the other phases.
