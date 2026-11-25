---
name: laravel-filament
description: Version-aware best practices for Filament (the Laravel admin-panel / TALL-stack framework by filamentphp), covering v1 through v5. Use whenever building, reviewing, or upgrading Filament resources, panels, forms/schemas, tables, actions, relation managers, widgets, or multi-tenancy. ALWAYS detects the installed Filament major version first, because the API differs significantly between majors (especially v3 -> v4), then applies the rules for that exact version. Also covers every upgrade path (v1->v2, v2->v3, v3->v4, v4->v5).
---

# Laravel Filament (v1 - v5)

Filament is a collection of TALL-stack (Tailwind, Alpine, Laravel, Livewire) packages for building admin panels and app UIs. Its API has changed substantially across major versions, so **the same code is right on one version and wrong on another**. This skill's core discipline: **find out which version is installed, then apply only that version's rules.**

## Step 1 - Detect the installed version FIRST (do not skip)

Never write or review Filament code before you know the major version. Determine it, in order of preference:

```bash
# Most reliable - the resolved installed version:
composer show filament/filament | grep -i '^versions'
# or
php artisan about | grep -i filament

# From the constraint (tells you the intended major):
grep '"filament/filament"' composer.json          # e.g. "^3.2", "^4.0", "^5.0"

# Fallback - read the locked version directly:
grep -A2 '"name": "filament/filament"' composer.lock | grep version
```

Map the result to a major: `1.x`, `2.x`, `3.x`, `4.x`, or `5.x`. If Filament is not yet installed and the user is starting fresh, default to the **latest stable** and confirm with them. If you truly cannot determine the version, ask - do not guess.

## Step 2 - Load the matching reference

Read the reference file for the detected major before giving version-specific syntax. Each file has that version's real namespaces, class names, method signatures, patterns, and gotchas.

| Version | Era (one-liner) | Reference |
|---|---|---|
| **v1** | Earliest release, pre-panel | `references/filament-v1.md` |
| **v2** | The TALL-stack admin panel (Livewire 2) | `references/filament-v2.md` |
| **v3** | Unified "panels", split packages (forms/tables/etc.) | `references/filament-v3.md` |
| **v4** | Schema unification + performance rewrite; the big break from v3 | `references/filament-v4.md` |
| **v5** | v4 API + Livewire v4 support (no new Filament features vs v4) | `references/filament-v5.md` |

**Key mental model:** the real API divide is **v3 vs v4**. v4 and v5 share almost the entire API surface - v5 is a major bump *only* to support Livewire v4, with no breaking changes to forms/tables/actions/resources. So v4/v5 guidance is nearly identical; when on v5, apply v4 rules plus the Livewire-4 notes.

## Step 3 - For upgrades, load the matching upgrade guide

| Path | Guide |
|---|---|
| v1 -> v2 | `references/upgrades/v1-to-v2.md` |
| v2 -> v3 | `references/upgrades/v2-to-v3.md` |
| v3 -> v4 | `references/upgrades/v3-to-v4.md` (the big one - schema unification, namespace moves) |
| v4 -> v5 | `references/upgrades/v4-to-v5.md` (mostly Livewire v4; run the automated script) |

Each upgrade guide lists the automated upgrade tooling (`filament/upgrade` + the `vendor/bin/filament-vN` script) and the manual breaking changes. Always run the automated script first, then work the manual list.

## Version-independent best practices (apply on every version)

These hold regardless of major - the *syntax* to express them lives in the version reference, but the *principle* is stable:

- **Authorization is not optional.** Back every Resource with a Laravel Policy; don't rely on hiding UI. Filament calls policy methods (`viewAny`, `create`, `update`, `delete`) - implement them.
- **Kill N+1 in tables.** Eager-load relationships used by columns/filters via the table's base query (`modifyQueryUsing` / `->query()`), and prefer counts over loading collections for badges.
- **Validate on the server.** Field-level rules in the schema are real validation, not decoration; never trust client state. Watch mass-assignment - Filament fills models from form state, so guard `$fillable`/`$guarded` deliberately.
- **Keep resources thin.** Push non-trivial logic into the model, actions, or dedicated service classes; a Resource should read as configuration, not business logic.
- **Prefer relation managers** over hand-rolled nested forms for one-to-many/many-to-many editing.
- **Test panels.** Filament pages are Livewire components - test them with Pest + Livewire (`livewire()->set()->call()->assertHasNoErrors()`), assert table records, and cover authorization paths.
- **Don't hardcode volatile API from memory.** Method signatures and namespaces move between majors. When unsure of an exact signature for the detected version, verify against `https://filamentphp.com/docs/<major>.x` (or via the context7 docs tool) rather than guessing.
- **Match the ecosystem versions.** Each Filament major pins specific Laravel / Livewire / Tailwind / PHP ranges (see each reference's compatibility box). Mismatched Livewire or Tailwind majors are a common source of "it doesn't render" bugs.

## Output expectations

- State the detected version up front ("Detected Filament v3.2").
- Give code in that version's exact syntax, labeled with the version.
- On an upgrade task, produce the ordered steps from the relevant upgrade guide (automated script first), and call out the breaking changes that affect the user's actual code.
