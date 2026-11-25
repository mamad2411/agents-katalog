---
name: moonshine-v4
description: Use when working on any MoonShine v4 admin panel task — setup, resources, fields, components, appearance, frontend, security, or advanced patterns. This is the single entry point that routes to specialized sub-skills.
---

# MoonShine v4 — Skill Router

MoonShine v4 is a Laravel admin panel framework (PHP 8.2+, Laravel 10.48+) for building back-office applications. It provides:

- **ModelResource** — CRUD scaffolding with page-centric architecture (IndexPage, FormPage, DetailPage)
- **Fields** — 40+ field types including relationships, files, JSON, and custom fields
- **Components** — FormBuilder, TableBuilder, 70+ layout/display/overlay components
- **Layouts & Theming** — Menu system, palette-based colors, icons, dark mode, custom assets
- **Frontend** — API mode with JWT, SDUI, OpenAPI generator, Alpine.js integration, AsyncCallback
- **Security** — Authentication, authorization, policies, 2FA, Socialite, custom auth responses

## How to Use This Skill

Based on what the task involves, read **1–3 relevant sub-skills** from the table below. Each sub-skill is a self-contained `SKILL.md` with code examples and references to deeper documentation.

## Routing Table

| Task involves... | Read this sub-skill |
|---|---|
| Installation, configuration, bootstrapping, routing, middleware, localization, artisan commands, project structure, IDE setup, starter kit, v3→v4 migration | `moonshine-setup-v4/SKILL.md` |
| ModelResource, CrudResource, CRUD operations, pages (IndexPage/FormPage/DetailPage), tables, forms, detail views, filters, search, pagination, query tags, events lifecycle, buttons, query modification, import/export, metrics, modal CRUD, redirects, active actions, response modifiers | `moonshine-resources-v4/SKILL.md` |
| Field types, relationship fields (BelongsTo, HasMany, BelongsToMany, Morph*), field validation, field lifecycle, apply logic, field modes (default/preview/raw), Fieldset, RelationRepeater, creating custom fields, reactivity, showWhen | `moonshine-fields-v4/SKILL.md` |
| FormBuilder, TableBuilder, ActionButton, layout components (Grid, Column, Box, Flex, Fragment), navigation (TopBar, Sidebar), modals, tabs, cards, CardsBuilder, metrics components, overlays, display components, JS events, component combinations | `moonshine-components-v4/SKILL.md` |
| Layouts, custom layouts, AppLayout, menus (MenuItem new parameter order), color palettes (PurplePalette), icons, assets, custom pages, dark mode, branding, Blade templates, admin panel design | `moonshine-appearance-v4/SKILL.md` |
| API mode/backend, JWT authentication for API, OpenAPI generator (moonshine/oag), SDUI (Server-Driven UI), Alpine.js events, JavaScript helpers, reactive fields, async UI updates, AsyncCallback, fragment-based partial updates, custom Alpine.js components, MoonShine JS global class | `moonshine-frontend-v4/SKILL.md` |
| Authentication, authorization, login, guards, custom user models, Socialite, 2FA, JWT, role-based access, Laravel policies, auth pipelines, authenticateUsing/logoutUsing, middleware, IP restrictions | `moonshine-security-v4/SKILL.md` |
| Custom controllers, handlers (Handler), custom routes, type casts, notifications, toasts, testing, package development, CrudResource (non-Eloquent data), JsonResponse, #[AsyncMethod] attribute, recipe patterns | `moonshine-advanced-v4/SKILL.md` |

## Instructions

1. **Identify** which areas the task touches (usually 1–3 from the table above)
2. **Read** the corresponding `SKILL.md` file(s) using the Read tool — resolve paths relative to this file's directory
3. **Follow** the patterns and examples in those sub-skills
4. If deeper detail is needed, each sub-skill cross-references files in its `references/` folder

## Quick Reference: Common Task Mappings

**"Create a new resource"** → setup + resources + fields

**"Add a custom page"** → resources + components

**"Build a dashboard"** → components + appearance + advanced (recipes)

**"Set up auth/permissions"** → security + setup

**"Add API endpoints"** → frontend + resources

**"Customize the theme"** → appearance

**"Add a custom field"** → fields + components

**"Write tests"** → advanced

**"Migrate from v3"** → setup (migration section)
