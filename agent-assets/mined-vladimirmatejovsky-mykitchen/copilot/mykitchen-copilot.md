# MyKitchen – Project Instructions

These instructions apply to all Copilot interactions in this workspace.

---

## Product

MyKitchen is a household meal planning application.

Goal: simplify household meal planning while preserving full user control.

The application assists users. It never controls them.

Algorithms may suggest, optimize, recommend.
Algorithms must never block, enforce, or reject.

**Main goals:** manage ingredients, manage recipes, create meal plans, generate shopping lists, reduce food waste, preserve cooking knowledge, remember history.

**Target users:** single household (initial scope).

**Devices:** desktop browser (primary), mobile read-only (secondary).

**Product workflow:** Ingredient → Recipe → Weekly Plan → Shopping → Cooking → History

---

## Architecture

Optimize for: simplicity, readability, maintainability, testability, local development.
Avoid overengineering.

### Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Blazor WebAssembly |
| UI components | DevExpress Blazor |
| Backend | ASP.NET Core minimal API |
| ORM | EF Core |
| Database | SQLite |
| Tests | xUnit |

### Solution Structure

```
src/
  MyKitchen.Web          – Blazor WebAssembly frontend (rendering, navigation, localization, validation, API communication; NO business logic)
  MyKitchen.Api          – HTTP endpoints, request validation, orchestration (NO domain rules)
  MyKitchen.Application  – use cases, workflows, business orchestration (NO infrastructure)
  MyKitchen.Domain       – entities, value objects, business rules (NO UI, NO persistence)
  MyKitchen.Infrastructure – EF Core, SQLite, external integrations (NO business logic)
  MyKitchen.Contracts    – DTOs, request/response models (NO logic)
tests/
  MyKitchen.Tests        – xUnit tests
```

### Dependency Flow

`Web → Api → Application → Domain ← Infrastructure`

### Forbidden Patterns

- No CQRS
- No MediatR
- No Repository Pattern
- No Microservices
- No Event Sourcing

### API Rules

REST, JSON. Minimal API style.

### UI Rules

Use DevExpress Blazor components. Avoid custom components unless justified.

### Persistence Rules

SQLite for local development. Application must not depend directly on SQLite – abstraction required for future provider replacement. Always use migrations.

### Localization

- Code language: **English only**
- UI: **localized** (sk-SK default, en-US supported)
- Resources in `Resources/` folder of `MyKitchen.Web`
- No hardcoded UI text

---

## Domain Model

Ingredients are the foundation. Recipes are composed from ingredients. Planning is composed from recipes. Shopping is composed from plans. History preserves outcomes.

### Aggregate Roots

`Ingredient`, `Recipe`, `WeeklyPlan`, `ShoppingList`

### Core Entities

**Ingredient** – canonical identity, categorization, unit support, shelf life. Exists independently. Must not depend on recipes.
- Relations: `IngredientAlias`, `IngredientCategory`, `IngredientUnit`

**IngredientAlias** – alternative names for import matching and normalization. Never replaces canonical ingredient.

**Recipe** – structured cooking instruction preserving ingredients, instructions, nutrition, notes, source.
- Relations: `RecipeIngredient`, `RecipeInstruction`, `RecipeNote`, `RecipeSource`

**RecipeIngredient** – ingredient usage with quantity, unit, optionality. Always references Ingredient.

**WeeklyPlan** – planned week with meal assignments.
- Relations: `WeeklySlot` (types: Breakfast, Lunch, Dinner, Leftovers, EatOutside, Empty)
- User can always override.

**ShoppingList** – aggregated purchase requirements with manual confirmation.
- Relations: `ShoppingItem` (states: Buy, AlreadyHave, Skip). Inventory is manual.

**HistoryEntry** – immutable planning history. History cannot be edited. Recipe notes remain editable.

---

## Workflow

Human remains responsible. Agents assist.

### Feature Lifecycle

Idea → Backlog → Task → Architecture → Implementation → Testing → Review → Commit

### Task Execution

1. Create task in `tasks/`
2. **Architect**: read docs, design only, save to `work/{task-id}_architect.md` → **ArchitectReviewer** reviews → wait for human approval
3. **Developer**: read docs + task + architect handoff, implement approved scope only → **DeveloperReviewer** reviews → wait for human approval
4. **QA**: read task + implementation, write tests, produce findings report → **QAReviewer** reviews → wait for human approval
5. **Human**: final review, approve or request changes

### Living Documents

Decisions are recorded in `docs/decisions.md` (append-only, never rewrite history).
Backlog is tracked in `docs/backlog.md`.
