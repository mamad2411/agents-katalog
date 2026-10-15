---
name: blutui-project-guidelines
description: Blutui project guidelines from the Blutui Engineering team. Use this skill whenever working on ANY Blutui project — writing or editing templates, layouts, components, or partials; creating or querying Collections; building or handling forms; configuring routing or Courier; working with Canopy or Cassettes; using the Blutui MCP; or setting up a new Blutui project from scratch. If the user mentions Blutui, Canopy, Cassettes, Courier, or any Blutui-specific concept, always load and follow this skill before writing any code or configuration.
license: MIT
metadata:
  author: Blutui
  version: '1.0.0'
---

# Blutui Project Guidelines

Load the rule files that match your task. Always load ALL that apply — multiple rules often overlap.

## Rule Index

| Task                                                      | Load                                                            |
| --------------------------------------------------------- | --------------------------------------------------------------- |
| Creating/editing any template, layout, or component       | `rules/foundation-templates-and-layouts.md`                     |
| Writing Canvas template syntax (tags, filters, functions) | `rules/templating-canvas.md`                                    |
| Including/embedding other templates                       | `rules/templating-including-templates.md`                       |
| Working with Collections (querying, displaying data)      | `rules/collections.md`                                          |
| Building a blog listing or post page                      | `rules/blog.md`                                                 |
| Building or processing forms                              | `rules/forms.md`                                                |
| Building site navigation (header, footer, dropdowns)      | `rules/menus.md`                                                |
| Setting up routing or URL patterns                        | `rules/route-patterns.md`                                       |
| Configuring Courier                                       | `rules/courier.md`, `rules/foundation-courier-configuration.md` |
| Project file structure / starting a new project           | `rules/foundation-file-structure.md`                            |
| Version control / switching cassettes                     | `rules/cassettes.md`                                            |
| Calling the Blutui MCP or writing MCP integrations        | `rules/mcp.md`                                                  |
| Using Canopy (in-page editor)                             | `rules/canopy.md`                                               |

Rule files live at: `rules/<rule-name>.md`

## Core Rules (Always Apply)

1. **Templates are the HTML shell; layouts are page types editors choose.** Templates (`views/templates/`) define the outer structure that wraps every page — developers own them, editors never touch them. Layouts (`views/layouts/`) extend templates and represent individual page designs that editors pick when creating pages in the dashboard. See `rules/foundation-templates-and-layouts.md`.
2. **Use Canvas for all templating logic.** See `rules/templating-canvas.md`.
3. **Store structured content in Collections**, not hardcoded in templates. See `rules/collections.md`.
4. **Never build raw HTML forms** — use Blutui's form tags. See `rules/forms.md`.
5. **Don't invent new top-level directories.** See `rules/foundation-file-structure.md`.
6. **Search documentation first.** Use `search_blutui_documentation` via Blutui MCP before making code changes. See `rules/mcp.md`.

## Full Reference

For all rules in one document: `AGENTS.md`

Use `AGENTS.md` when you need a comprehensive reference or are unsure which rules apply.
