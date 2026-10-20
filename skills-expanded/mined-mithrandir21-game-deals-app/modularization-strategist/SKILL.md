---
name: modularization-strategist
description: Plan or refactor Android/KMP module boundaries — feature/data/domain/core splits, API/impl modules, build-time impact, Gradle convention plugins (`build-logic`), and version catalog hygiene. Use whenever the user asks about "modularization", "splitting modules", "module structure", "API vs impl", "convention plugins", "slow Gradle builds because of modules", or wants to break up a monolithic `:app`. Also use when adding a new module type and wanting it to fit the existing graph.
---

# Modularization Strategist

Modularization is leverage when done well and tax when done wrong. The right structure depends on team size, feature count, and what you're optimizing for (build speed, ownership, reuse). This skill helps think through it.

## When to use

Triggers: "modularize", "split into modules", "too many modules", "feature module", "API/impl", "convention plugin", "build-logic", "slow Gradle".

Don't use for a 5-person app with 10k LOC — premature modularization is real and expensive.

## Process

### Phase 1: Clarify the goal

Modularization optimizes for different things. Get the dev to pick one or two:

- **Build speed** — incremental builds skip untouched modules.
- **Ownership** — different teams own different modules.
- **Reuse** — the same logic ships in multiple apps.
- **Encapsulation** — features can't reach into each other.
- **Dynamic features / on-demand delivery** — modules ship separately.

Without a goal, you'll end up with modules that don't pay off.

### Phase 2: Assess the current state

Run:

```
./gradlew projects                 # see the module tree
./gradlew :app:dependencies | wc -l
find . -name "build.gradle.kts" | wc -l
```

Note:
- Number of modules.
- Whether convention plugins exist (`build-logic` or `buildSrc`).
- Version catalog presence (`gradle/libs.versions.toml`).
- Any module that depends on more than ~10 others (likely a god module).
- Cyclic dependencies (Gradle would reject them, but visual cycles in DI or via `Context` are real).

### Phase 3: Pick a topology

Common shapes — choose one and apply consistently:

**Three-layer (small/medium apps)**
```
:app
:feature:* → depends on :data and :core
:data
:core (utilities, design system)
```
Good when one team owns everything. Simple, works up to maybe 30 features.

**Feature × Layer (medium/large apps)**
```
:app
:feature:onboarding (UI only)
:feature:home
:domain:onboarding (use cases, models)
:data:onboarding (repos, network, db)
:core:ui (design system)
:core:network
:core:database
```
Better for parallel work. Each feature has its own data + domain.

**API/Impl split (large apps, multi-team)**
```
:feature:onboarding:api  ← public surface other features depend on
:feature:onboarding:impl ← implementation, only :app depends on it
```
Lets features expose just navigation entry points without leaking internals. Doubles module count — only worth it when team sizes justify it.

**KMP-aware**
```
:shared:core
:shared:feature:onboarding
:androidApp
:iosApp (Xcode project consuming the KMP framework)
```
Common code lives in `:shared:*` with `commonMain` source sets. Platform-specific UI stays in `:androidApp` / `:iosApp`.

### Phase 4: Set up the foundations

Before splitting modules, make sure these exist or land first:

**Version catalog** (`gradle/libs.versions.toml`)
- Single source of truth for versions.
- Reduces drift across modules.

**Convention plugins** (`build-logic` composite build)
- Plugins like `app.feature`, `app.android.library`, `app.kmp.library` that encode common Gradle config.
- Replace the repetitive 50-line `build.gradle.kts` in every module with `plugins { id("app.android.library") }` + 5 lines.

Without these, every new module is a copy-paste headache and a maintenance hazard.

### Phase 5: Plan the split

If splitting an existing module, do it in this order:

1. **Identify the seam.** A package that has few inbound references is a good candidate to extract. Use the IDE: right-click package → Find Usages.
2. **Extract a `:core` first.** Pull out the bits that have no Android dependencies and that other code uses heavily (utilities, models). This unblocks later splits.
3. **Extract one feature.** Start with the smallest, most independent one. Note pain points; refine the convention plugin if needed.
4. **Repeat per feature.** Don't try to split everything at once.

For each extracted module:
- Tests move with the code.
- DI bindings move to a module-local Hilt/Koin module.
- Navigation entries: keep route definitions in the feature module, register them in `:app`.

### Phase 6: Verify the payoff

After splitting, measure:

- `./gradlew :feature:foo:assembleDebug --profile` — incremental build time for that feature only.
- `./gradlew --scan` — look at task execution graph and what reran.
- Run a clean build, then change one line in a feature, rebuild — should be substantially faster than before.

If it isn't faster and that was the goal, the split was wrong. Likely causes:
- Too many modules depend on a common one (changes ripple).
- The `:app` module imports everything (everything reruns when `:app` changes).

## Output

A modularization plan with:

1. **Current shape** — short diagram or list.
2. **Target shape** — diagram with module names and dependency directions.
3. **Foundations needed** — version catalog, convention plugins, etc.
4. **Migration sequence** — ordered list, smallest first.
5. **Success metrics** — what gets measured to confirm the win.

## Common pitfalls

- **Modularizing for its own sake.** Modules have overhead (Gradle config, cross-module APIs, friction). Only split when it pays for itself.
- **Too granular too soon.** 80 modules in a 5-person team is misery. Aim for ~1–3 modules per developer max.
- **No convention plugin.** Every new module is a 30-minute copy-paste. Build the convention plugin first.
- **`:app` knowing everything.** If `:app` depends on every feature, you've achieved nothing — `:app` changes still trigger full rebuilds. Use API/impl or runtime-discovered features.
- **Ignoring KMP source-set hierarchy.** `commonMain` source sets share across `androidMain` and `iosMain` — model the module tree to match.
