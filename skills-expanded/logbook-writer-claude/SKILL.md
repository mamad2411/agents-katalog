# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Logbook Writer is a crew scheduling system that generates daily logbooks for retail stores. It ingests crew shifts, preferences, and store rules, then uses constraint solvers to produce optimal task assignments (register, product stocking, breaks, etc.) while respecting hard constraints and optimizing soft goals like preferences, continuity, and fairness.

## Tech Stack

- **Runtime**: Node.js + TypeScript, pnpm workspaces, Turborepo
- **API**: Fastify + Prisma ORM (PostgreSQL)
- **Web**: Next.js 13 (app router), React Query, Zustand
- **Testing**: Vitest
- **Solver**: Python-based CP-SAT solver (apps/solver-python)

## Common Commands

### Development

```bash
# Install dependencies (root)
pnpm install --frozen-lockfile

# Start API dev server (default port 4000)
cd apps/api
export DATABASE_URL="postgresql://user:pass@localhost:5432/logbook"
pnpm dev

# Start API on alternative port
cd apps/api
pnpm dev:4010

# Start web UI
cd apps/web
pnpm dev

# Build all packages
pnpm build

# Lint all packages
pnpm lint
```

### Database (Prisma)

```bash
cd apps/api

# Generate Prisma client (after schema changes)
pnpm db:generate

# Push schema to database (dev only, no migrations)
pnpm db:push

# Cleanup test data
pnpm db:cleanup-test-data
pnpm db:cleanup-tests
```

### Testing

```bash
# Run all tests (from root or any package)
pnpm test

# Run tests in apps/api
cd apps/api
pnpm test

# Run specific test file pattern
cd apps/api
pnpm test crud
pnpm test wizard
pnpm test fairness
```

### Utility Scripts (apps/api)

```bash
# Auto-tune preference weights
pnpm weights:auto-tune
pnpm weights:auto-tune:apply

# Mixed-mode tuning
pnpm weights:mixed-mode
pnpm weights:mixed-mode:apply

# Assign shifts to crew
pnpm assign:shifts
pnpm assign:shifts:store --store=768
pnpm assign:shifts:config scripts/shifts_prefs.sample.json
```

## Error Tracking & Learning

Before making any changes, check `LESSONS.md` in the project root for past mistakes and patterns to avoid. This file contains fixes and learnings from previous bugs.

When you make a mistake or I correct you:
1. Add an entry to `LESSONS.md` with what went wrong and the correct approach
2. Categorize it (UI bugs, misunderstandings, stack-specific, etc.)

## Frontend Context

- Stack: React 18, Next.js 13 (app router), Tailwind CSS
- Design system: AI glass components in `apps/web/components/ui/ai-glass/`
- "Responsive" = mobile-first, breakpoints at 640/768/1024px
- Use `gap` for spacing in flex/grid, not margin
- Always include `key` props when mapping

### Standard Spacing & Styling

- **Standard padding**: `1.5rem` (24px) for glass card content
- **Standard border radius**: `1rem` (16px) for cards, `0.75rem` (12px) for buttons, `9999px` for pills
- **Font**: `var(--font-open-sans)` for body text
- **Text colors**: `#2C2C2C` (primary), `#6B6B6B` (secondary), `#9A999E` (muted)

### Glass Component Defaults (Light Mode)

```typescript
// aiGlassLightContentStyle defaults:
backgroundOpacity: 0.1  // Very transparent
blur: 7px               // Backdrop blur

// aiGlassLightBorderStyle defaults:
borderOpacity: 0        // No visible border by default
borderWidth: 1px
borderBrightness: 1.85
borderFade: 50
```

## Communication

- If requirements are unclear, ask before implementing
- When I describe a visual bug, ask for a screenshot if needed
- Propose your approach briefly before large refactors

## Architecture

### Monorepo Structure

- **apps/api** – Fastify REST API with Prisma, route handlers, solver integration
- **apps/web** – Next.js frontend (WIP)
- **apps/solver-python** – Python CP-SAT solver using OR-Tools
- **packages/domain** – Core domain logic (normalize, validate, solve utilities)
- **packages/shared-types** – Shared TypeScript types

### API Architecture

The API is organized into route modules (registered in `apps/api/src/index.ts`):

- **Health**: `/health` – health checks
- **Crew**: `/crew` – CRUD for crew members
- **Roles**: `/roles` – CRUD for roles (REGISTER, PRODUCT, DEMO, etc.)
- **Role Rules**: `/role-rules` – constraints on roles (min/max consecutive, precedence, forbid, timing)
- **Shifts**: `/shifts` – crew shift data (date, startMin, endMin)
- **Coverage**: `/wizard/coverage` – role coverage windows (e.g., DEMO 10:00-14:00)
- **Requirements**: `/wizard/requirements` – daily role hour requirements
- **Schedule**: `/schedule/run` – build engine input, prepare solver data
- **Solver**: `/solver` and `/solver2` – invoke solver, generate logbooks
- **Tuning**: `/tuning` – preference weight recommendations
- **Constraints**: `/constraints` – constraint validation
- **Dashboard**: `/dashboard` – fairness metrics and analytics

### Solver Architecture

The system uses a two-layer solver architecture:

1. **Input Builder** (`apps/api/src/solver2/builder.ts`): Builds `SolverInputV2` from Prisma data
   - Fetches store, roles, crew, shifts, coverage, quotas, preferences, fairness history
   - Normalizes dates to UTC
   - Applies preference banking and fairness adjustments
   - Supports shift overrides

2. **Python Solver** (`apps/solver-python/logbook_solver_v2/cli.py`): CP-SAT solver using OR-Tools
   - Reads `SolverInputV2` JSON from stdin
   - Builds constraint programming model with slot variables
   - Applies hard constraints (role rules, coverage, breaks, quotas)
   - Optimizes objective (preferences, fairness, consecutive penalties)
   - Returns assignments as JSON to stdout

3. **Result Analyzer** (`apps/api/src/services/constraint-analyzer.ts`): Validates solver output
   - Checks all hard constraints
   - Computes preference satisfaction
   - Reports violations

4. **Logbook Manager** (`apps/api/src/services/logbook-manager.ts`): Persists results
   - Saves assignments to `Logbook` and `Assignment` tables
   - Updates fairness history (`CrewRoleFairnessHistory`)
   - Computes preference satisfaction metadata

### Data Model Highlights

**Key Enums**:
- `AssignmentModel`: HOURLY, WINDOW, DAILY, SOLVER (how roles are assigned)
- `ConsecutivePolicy`: REQUIRED, PREFERRED, NONE (for roles like DEMO)
- `RoleRuleType`: MIN_CONSECUTIVE_MINUTES, CANNOT_BE_ASSIGNED_BEFORE, FORBID_ROLE, etc.
- `PreferenceType`: FIRST_HOUR, FAVORITE, TIMING, CONSECUTIVE

**Important Tables**:
- `Store`: timezone, open/close minutes, regHoursStartMin/regHoursEndMin (register window)
- `Role`: displayName, taskLength, assignmentModel, consecutivePolicy, role rules
- `Crew`: 7-character ID (`@db.Char(7)`), e.g., TCRW001
- `Shift`: date, crewId, storeId, startMin, endMin (shift bounds)
- `RoleCoverageWindow`: role coverage (e.g., DEMO 10:00-14:00 with crewPerMinute demand)
- `CrewRoleQuota`: daily role hour requirements per crew
- `CrewPreference`: crew-specific preference weights
- `RolePreference`: store-level preference definitions (preferenceType, baseWeight)
- `BankedPreference`: unused preferences carried forward
- `RoleFairnessTracker`: tracks fairness for specific roles (lookbackDays, enabled)
- `CrewRoleFairnessHistory`: daily minutes assigned per crew per role
- `RoleFairnessSnapshot`: daily fairness metrics (giniCoefficient, fairnessIndex, grade)
- `Logbook`: DRAFT/PUBLISHED/SUPERSEDED status, stores solver output
- `Assignment`: individual task assignments (crewId, roleId, startTime, endTime, origin)
- `PreferenceSatisfaction`: per-preference satisfaction scores (met, weightApplied, adaptiveBoost)

### Segmentation and Register Windows

The system segments shifts into PRODUCT (outside register hours) and FLEX (inside register hours):

- `Store.regHoursStartMin` and `regHoursEndMin` define the register window (default 08:00–21:00, i.e., 480–1260 minutes)
- `segmentShiftByRegisterWindow` (in `apps/api/src/services/segmentation.ts`) splits a shift into segments
- PRODUCT segments are assigned automatically; FLEX time is allocated by the solver

### Preference System

Preferences are multi-layered:

1. **RolePreference**: Store-level definitions (preferenceType, baseWeight, allowBanking)
2. **CrewPreference**: Crew-specific overrides (crewWeight, intValue)
3. **BankedPreference**: Unused preferences carried forward (weight boost, expiration)
4. **Adaptive Boost**: Fairness-based adjustment (crews with lower satisfaction get higher weights)
5. **Fairness Adjustment**: Tiered rotation boost for tracked roles (based on lookback history)

The solver uses these to compute a weighted objective that balances preferences and fairness.

### Fairness System

Roles can opt into fairness tracking via `RoleFairnessTracker` (enabled, lookbackDays):

- **CrewRoleFairnessHistory**: Tracks daily minutes assigned per crew per role
- **RoleFairnessSnapshot**: Daily metrics (Gini coefficient, fairness index, grade)
- **Tiered Boost**: Crew with fewer minutes get higher preference weights in the solver objective
- **Dashboard**: `/dashboard` endpoint provides fairness charts and distribution data

## Domain Package (packages/domain)

Core domain logic is separated into:

- **normalize** (`src/normalize`): Date normalization, shift validation
- **validate** (`src/validate`): Constraint validators (slotAlignment, storeHours, hourlyCoverage, dailyHours, breakPolicy, etc.)
- **solve** (`src/solve`): Solver utilities
- **constraints** (`src/constraints`): Constraint definitions and scorers (firstHour, favorite, timing, consecutive)

## Important Conventions

### Date Handling

- Daily dates are stored as `@db.Date` (PostgreSQL DATE type) to avoid timezone drift
- Always supply dates as `YYYY-MM-DD` strings
- Use `startOfDay(date)` utility (in `apps/api/src/utils.ts`) to normalize to UTC midnight
- Wizard endpoints coerce dates and return `normalizedDate` in responses

### Crew IDs

- Crew IDs are exactly 7 characters (`@db.Char(7)`)
- Tests and seeds use IDs like `TCRW001`, `TCRW002`, etc.
- Prisma will error if you try to insert a crew ID of incorrect length

### Time Representation

- All times are stored as minutes since midnight (`startMin`, `endMin`)
- Range: [0, 1440) where 0 = 00:00, 1440 = 24:00 (exclusive)
- Use `hhmmToMin` and `minToHHMM` helpers in `segmentation.ts` for conversions

### Role Assignment Models

- **HOURLY**: Hourly coverage requirements
- **WINDOW**: Coverage window with start/end offsets
- **DAILY**: Daily hour requirements
- **SOLVER**: Pure solver-driven assignment
- **HOURLY_OR_WINDOW**: Either hourly or window
- **HOURLY_AND_SOLVER**: Combination

Use the correct `AssignmentModel` when creating roles to ensure the solver interprets requirements correctly.

### Consecutive Policies

- **REQUIRED**: Role must be assigned in consecutive blocks (hard constraint)
- **PREFERRED**: Role should be consecutive if possible (soft penalty for splits)
- **NONE**: No consecutive requirement

DEMO roles typically use `REQUIRED` to avoid fragmenting demo time.

## Testing

- Tests are in `apps/api/test/` and `packages/domain/test/`
- Use `vitest run` to run tests
- Tests create and clean up their own test data (see `cleanup-test-stores.ts`)
- Integration tests (`solver.integration.test.ts`, `e2e.api.test.ts`) cover full solver flow
- Constraint tests (`packages/domain/test/constraints/`) validate individual constraint logic

## Solver Python Environment

The Python solver lives in `apps/solver-python/`:

- Python module: `logbook_solver_v2.cli` (invoked by Node.js API)
- Virtual environment: `PROJECT_ROOT/.venv/bin/python`
- Fallback: `python3`
- Requirements: OR-Tools, NumPy, etc.

The API spawns the Python process, pipes JSON input, and reads JSON output.

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (required)
- `PORT`: API server port (default: 4000)
- `BANKING_WEIGHT_DIVISOR`: Weight divisor for banked preferences (default: 10)
- `BANKING_MAX_WEIGHT_BOOST`: Max weight boost for banked preferences (default: 3)
- `BANKING_AGE_BOOST_FACTOR`: Age boost factor (default: 0.5)
- `BANKING_CARRYOVER_DAYS`: Days to carry forward unused preferences (default: 30)

## Key Files to Know

- `apps/api/src/index.ts`: API entry point, route registration
- `apps/api/prisma/schema.prisma`: Database schema
- `apps/api/src/solver2/builder.ts`: Builds solver input from Prisma data
- `apps/api/src/solver2/types.ts`: TypeScript types for solver input/output
- `apps/api/src/routes/solver2.ts`: Solver endpoint handlers
- `apps/api/src/services/logbook-manager.ts`: Persists solver output
- `apps/api/src/services/constraint-analyzer.ts`: Validates solver results
- `apps/api/src/services/segmentation.ts`: Shift segmentation logic
- `apps/api/src/config/solver.config.ts`: Solver tuning parameters
- `packages/domain/src/constraints/`: Constraint validators and scorers
- `apps/solver-python/logbook_solver_v2/cli.py`: Python solver CLI

## Workflow Example

1. **Setup Store**: Create store, roles, crew, role families
2. **Assign Shifts**: POST to `/shifts` with crew shift data
3. **Define Coverage**: POST to `/wizard/coverage` with role coverage windows
4. **Set Requirements**: POST to `/wizard/requirements` with daily role hour requirements
5. **Run Solver**: POST to `/solver2/solve` with storeId, date, timeLimitSeconds
6. **Fetch Logbook**: GET `/schedule/logbook` to retrieve assignments

## Recent Changes (ml-schedule-learning branch)

The current branch (`ml-schedule-learning`) includes:

- ML-based schedule tuning engine integration
- Fairness dashboard with tiered rotation boost
- Distribution charts (histogram-style min/hr buckets)
- AI glass styling with gradient borders

Refer to recent commits for details on these features.