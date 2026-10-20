---
name: kendo-ui-migration
description: Use when upgrading Kendo UI versions, migrating between framework variants (jQuery to React/Angular/Vue), or planning a phased replacement with deprecation tracking and rollback controls.
---

# Kendo UI Migration

## Specialization

Plan and execute Kendo UI migrations covering version upgrades (breaking change triage, deprecated API removal, SASS variable renames), framework variant migrations (Kendo UI for jQuery → KendoReact, Kendo UI for Angular, Kendo UI for Vue), licensing model changes, and phased coexistence patterns — grounded in official Kendo UI release notes and migration guides.

## Trigger Conditions

- Upgrading Kendo UI to a new major or minor version.
- Migrating from Kendo UI for jQuery to KendoReact, Kendo UI for Angular, or Kendo UI for Vue.
- Deprecation warnings appear after a Kendo UI version bump.
- A security advisory requires upgrading the Kendo UI jQuery dependency.
- A project is moving from a free Kendo UI Core component to a commercial component.
- A licensing model change requires re-evaluating which Kendo UI distribution is in use.
- SASS variable renames or theme contract changes break the build after a version upgrade.
- A `kendo-ui-quality-gate` audit identifies a migration-related finding.

## Scope Boundaries

In scope:

- Version upgrade planning: breaking change inventory, deprecated API triage, test regression matrix.
- Framework variant migration: component equivalence maps, DataSource contract differences across frameworks, TypeScript typing differences.
- Theming migration: SASS variable renames across versions (coordinate with `kendo-ui-theming`).
- Licensing changes: Open Source (kendo-ui-core) vs. commercial (Kendo UI), distribution file differences.
- Phased coexistence: running old and new Kendo UI versions in parallel during migration.
- Rollback plan: version pinning, lock file strategy.

Out of scope:

- Server-side API changes required by a new Kendo UI version (coordinate with backend skills).
- Full theming re-implementation (see `kendo-ui-theming`).
- CI gate configuration for the migrated project (see `kendo-ui-ci-integration`).

## Inputs

- Current Kendo UI version and distribution (Core OSS or commercial).
- Target Kendo UI version and target framework variant (if changing).
- Current framework: jQuery, Angular, React, Vue.
- Number of widgets in use and their types.
- Existing test coverage (automated or manual) for Kendo UI-powered features.
- SASS customization depth.
- Evaluation date for release notes (`YYYY-MM-DD`).

## Required Outputs

- Breaking change inventory for the upgrade path with widget-level impact classification.
- Deprecated API usage scan result (list of deprecated methods/options in current codebase).
- Framework variant component equivalence map (if changing framework).
- SASS variable rename list for the version range.
- Migration sequencing plan: phased steps with rollback trigger criteria.
- Test regression matrix: which test cases must be re-run per breaking change.
- Rollback plan: version pin, lock file restore, and rollback owner.

## Version Upgrade Workflow

### Step 1: Breaking Change Inventory

- Read the What's New page and GitHub changelog for every version between current and target.
- For each breaking change, classify impact: None / Requires Code Change / Requires Theme Change / Requires Server Change.
- Capture the inventory table before writing any code.

### Step 2: Deprecated API Scan

```bash
# Search codebase for known deprecated Kendo UI jQuery APIs
grep -rn "\.kendoGrid\b" --include="*.js" . | grep -i "deprecated-option"
# Use project-specific grep patterns per the breaking change inventory
```

### Step 3: SASS Variable Audit

```bash
# Run SASS compilation targeting the new version
# Any `Undefined variable` error = breaking SASS rename
npm run build:styles 2>&1 | grep "Undefined variable"
```

### Step 4: Test Regression Scope

- Run the full Kendo UI widget test suite against the upgraded version.
- Flag any test failures as blocking before merging the version bump.

### Step 5: Rollback Plan

```json
// package.json — pin to known-good version if rollback is needed
{
  "dependencies": {
    "kendo-ui-license": "x.y.z",
    "@progress/kendo-theme-default": "x.y.z"
  }
}
```

## Framework Variant Migration Considerations

### Kendo UI for jQuery → KendoReact

| Concern | jQuery Approach | KendoReact Approach |
|---|---|---|
| Widget init | `$("#el").kendoGrid({})` | `<Grid data={data} />` JSX |
| DataSource | `kendo.data.DataSource` | `@progress/kendo-data-query` utilities + fetch |
| MVVM | `kendo.bind()` | React state / hooks |
| Theming | SASS variable override | `@progress/kendo-theme-default` CSS import + CSS variables |
| Events | `widget.bind("event", fn)` | JSX `onXxx` props |

### Kendo UI for jQuery → Kendo UI for Angular

| Concern | jQuery Approach | Angular Approach |
|---|---|---|
| Widget init | jQuery plugin | `<kendo-grid>` component |
| DataSource | `kendo.data.DataSource` | `GridDataResult` + Angular service |
| MVVM | `kendo.bind()` | Angular two-way binding `[(ngModel)]` |
| Theming | SASS `$kendo-` variable override | Angular CLI SCSS variable override |
| Module | Global `kendo` namespace | `@progress/kendo-angular-grid` `NgModule` imports |

## Rollback Criteria

Trigger rollback if any of the following occur after merging an upgrade:

- Production error rate exceeds baseline by > 1%.
- Any Kendo UI widget fails to initialize (console error during init).
- DataSource transport fails to serialize requests correctly.
- SASS build fails due to undefined variable.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Identify breaking changes for a patch or minor upgrade | Breaking change inventory complete; no surprises in build |
| L2 Practical | Major version upgrade with deprecated API remediation | All deprecated APIs replaced; tests pass on new version |
| L3 Hardening | SASS variable migration + theme rebuild + regression test | Theme builds cleanly; all widget tests pass |
| L4 Expert | Framework variant migration (jQuery → React/Angular) | Component equivalence map complete; migration phased with coexistence plan |
