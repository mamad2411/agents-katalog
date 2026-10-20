---
description: "Hard spec & doc sync gate. Verifies every scenario has a test, every business rule is enforced, and the spec / README / project profile match the implementation. Fixes any drift in-place — does not just report it."
agent: agent
tools: [read, edit, search, execute]
argument-hint: "Feature name or path to .feature file (e.g. specs/changes/add-user-login/delta.feature)"
---

Run the **Spec & Doc Sync hard gate** for:

${input}

This prompt does more than report — it **fixes drift in-place** so the spec, README, and
project profile match what the code now does. The cycle is not done until this gate passes.

## Steps

1. Read `specs/changes/<name>/delta.feature`.
2. Read `specs/changes/<name>/delta-rules.md` if it exists.
3. Find the test file(s) for this feature (search for the header comment
   `// Spec: specs/capabilities/<domain>/behavior.feature` or equivalent, or files named after the feature).
4. Find the implementation file(s) exercised by those tests.

---

### Sub-phase A — Spec Compliance Check

For every scenario in the feature file, determine:

- Does a test exist for this scenario?
- Does the test actually exercise the described behavior (not just named after it)?
- Would the test **fail** if the production code for that behavior were removed?

For every numbered business rule in the technical spec:

- Is the rule enforced in the production code?
- Is the rule covered by at least one scenario whose test would catch a violation?

For non-trivial logic in the production code:

- Is it exercised by a scenario?
- If not, treat it as **drift** (sub-phase B).

---

### Sub-phase B — Spec Drift Repair (mandatory if A fails)

**Classify each item before you touch a file.** "Update the spec to match the code" is safe in
one direction and dangerous in the other: a rule quietly relaxed during implementation, then
written back into the spec, makes the weakening invisible and permanently blessed.

| Class        | Meaning                                                             | Authority              |
| ------------ | ------------------------------------------------------------------- | ---------------------- |
| **ADDED**    | The spec gains a scenario or rule it did not have                   | Apply freely           |
| **MODIFIED** | An existing scenario or rule changes shape, keeping every guarantee | Apply freely           |
| **REMOVED**  | A guarantee the spec made is no longer promised                     | **Confirmation first** |

**The test for REMOVED:** _would a test written against the old spec still pass against the new
one?_ If no, it is a **spec weakening** — handle it under "Spec weakenings" below.

A **MODIFIED** repair must preserve every `Then` step the current spec has for that scenario.
Dropping one is a REMOVED, however the rest of the scenario is rewritten.

| Drift type                                                       | Class        | Repair action                                                               |
| ---------------------------------------------------------------- | ------------ | --------------------------------------------------------------------------- |
| Implementation supports inputs/outputs not in any scenario       | ADDED        | Add an `@edge-case` or `@happy-path` scenario, add a test, confirm it passes |
| New edge case handled but no `@edge-case` scenario               | ADDED        | Add the scenario and test                                                    |
| Scenario exists but no test                                      | ADDED        | Add the test, confirm it passes                                              |
| A business rule was **tightened** during implementation          | MODIFIED     | Update the rule, adjust the scenario, confirm the test catches a regression  |
| Validation message, status code, or error shape differs — same strictness | MODIFIED | Update the spec to match the code                                      |
| Test exists but is shallow (passes against a no-op)              | MODIFIED     | Strengthen the assertion so it would catch a regression                      |
| A business rule was **relaxed** during implementation            | **REMOVED**  | **Stop** — resolve as a spec weakening                                       |
| A validation was dropped, or an error case now succeeds          | **REMOVED**  | **Stop** — resolve as a spec weakening                                       |
| A scenario matches no current behavior and looks obsolete        | **REMOVED**  | **Stop** — resolve as a spec weakening                                       |

After each repair, re-run the affected tests. After all repairs, re-run the full test suite.

#### Spec weakenings

Never apply one silently under "match the code." Resolution depends on the autonomy mode chosen
at the Phase 1 spec approval gate:

- **Mode (b) — check first**: stop on that item and ask. Show what the spec promises today, what
  the code actually does, and which of the two you believe is the mistake. Apply only the answer
  given. Keep repairing other items while you wait.
- **Mode (a) — hands-off**: do not stop. Default to **preserving the spec** — change the
  implementation to honor what the spec promises, and record the item as
  _"code corrected to honor spec"_. Hands-off authorizes uninterrupted work; it never authorizes
  narrowing the spec. Stop only if honoring the spec is genuinely impossible.

Record every weakening twice: in the report below, and in `spec_weakenings` in the change's
`specs/changes/<name>/.atdd.yaml` (create it from
`docs/atdd/templates/atdd-metadata.template.yaml` if absent). The report is read once; the
metadata travels into the archive and outlives the conversation.

A REMOVED repair may not be applied without an entry there.

---

### Sub-phase C — Documentation Sync (mandatory)

Read `docs/project-profile.md` and walk the **`Sources consulted`** list. For every doc listed
there that could describe the changed behavior, either update it or mark it ⏭️ with reason.
Do not create new doc files unless the user explicitly asks.

Work through them in this order:

1. **`README.md`** — if the feature is user-visible, confirm the feature list, usage examples,
   configuration table, environment variables, or CLI flags are accurate. Update them now if not.
2. **`CONTRIBUTING.md`** — if the change affects how contributors build, test, or submit work
   (new commands, new gates, changed conventions), update it.
3. **`ARCHITECTURE.md` / `docs/architecture.md`** — if a new module, layer, or integration
   pattern was introduced, record it here.
4. **`docs/adr/` or `docs/decisions/`** — if an architectural decision was made that isn't
   already captured, add a new ADR. Never silently diverge from an existing ADR.
5. **Style guides, coding standards, or runbooks** — if a new pattern was established that
   future contributors should follow, record it in whichever doc the project uses.
6. **`docs/project-profile.md`** — update the `Conventions`, `Reference Files`, or
   `Anti-patterns to avoid in this repo` sections if Phase 3 introduced anything new.
7. **Any other doc in `Sources consulted`** that describes the changed behavior — review it;
   update if stale.

For each source: confirm it is accurate, update it, or record N/A with a reason. Do not skip
sources silently. If the feature has no user-visible surface (internal refactor, infra change),
README sync is ⏭️ — note the reason in the report.

---

### Sub-phase D — Final Verification

After every repair and doc update:

1. Re-run the full test suite — must be green.
2. Re-run all available quality gates — must pass.

---

### Report Format

Return a structured **Spec & Doc Sync** report. The cycle is not done until every row is ✅
or has an explicit ⏭️ with a reason.

```markdown
## Spec & Doc Sync: <Feature Name>

**Result**: ✅ In sync | ❌ Repairs needed (still failing)

### Sub-phase A — Spec Compliance

| Scenario | Tag    | Test Exists | Tests Behavior | Would Catch Regression |
| -------- | ------ | ----------- | -------------- | ---------------------- |
| "..."    | @smoke | ✅          | ✅             | ✅                     |

| Rule    | Enforced | Tested |
| ------- | -------- | ------ |
| 1. ...  | ✅       | ✅     |

### Sub-phase B — Spec Drift Repaired

| Drift item | Class    | Repair action taken | Files changed               |
| ---------- | -------- | ------------------- | --------------------------- |
| ...        | ADDED    | ...                 | `specs/changes/.../delta.feature` |

(or "⏭️ no drift found")

### Spec Weakenings

| Guarantee at risk | Spec promised | Code does | Resolution | Authority |
| ----------------- | ------------- | --------- | ---------- | --------- |
| Rule 3 — due dates future-dated | rejects same-day | accepts same-day | Code corrected to honor spec | mode (a) default |

(or "⏭️ none — no repair removed a guarantee")

**The gate does not pass while any row here lacks a resolution.**

### Sub-phase C — Documentation Sync

| Doc                       | Status                                    |
| ------------------------- | ----------------------------------------- |
| `README.md`               | ✅ Updated / ⏭️ not user-visible          |
| `CONTRIBUTING.md`         | ✅ Updated / ⏭️ no contributor impact     |
| `ARCHITECTURE.md`         | ✅ Updated / ⏭️ no structural change      |
| ADRs                      | ✅ Added ADR-N / ⏭️ no new decision       |
| Style guides / runbooks   | ✅ Updated / ⏭️ none                      |
| `docs/project-profile.md` | ✅ Updated / ⏭️ no changes                |
| Other consulted docs      | ✅ \<files\> / ⏭️ none                    |

### Sub-phase D — Final Verification

- Tests: ✅ N/N passing
- Quality gates: ✅ all passing

### Remaining Issues

(empty — gate must not pass with remaining issues)
```

---

## Rules

- **Repair, don't just report.** If you find drift, fix it before producing the report.
- **Classify before repairing.** ADDED and MODIFIED apply freely; REMOVED never does.
- **Update the spec to match the code** only when doing so keeps every guarantee the spec made.
  The moment a repair would remove one, it is a spec weakening — resolve it under the rules
  above, never under "match the code."
- **Never modify tests** to mask drift — adjust the spec and the implementation, then add a
  test that would catch a regression.
- **Don't create new doc files** unless explicitly asked — only update what exists.
- The cycle is **not** done while any row in the report is unresolved.
