---
name: GeneXus MCP Mastery
description: Current MCP-first usage guide for the GeneXus gateway, with coordination for specialized skills.
---

# GeneXus MCP Mastery

Use this skill to interact with the GeneXus KB through the MCP server in this repository.

## Coordination with Specialized Skills

When working on complex GeneXus tasks, coordinate this "Transport" skill with "Knowledge" skills (imported from [`genexuslabs/genexus-skills`](https://github.com/genexuslabs/genexus-skills) — see [`.gemini/skills/NOTICE.md`](../NOTICE.md)):

- **[Nexa](../nexa/SKILL.md)**: Authoritative reference set for GeneXus 18 objects, commands, types, properties, and modeling rules (`object-*.md`, `common-*.md`, `properties-*.md`, `global-*.md`). Load on demand — keep context minimal.
- **[GeneXus 18 Guidelines](../genexus18-guidelines/SKILL.md)**: Local conventions and engineering rules layered on top of Nexa.
- **[Chameleon Controls Library](../frontend/chameleon-controls-library/SKILL.md)**: 58 web-component docs for Chameleon UI elements.
- **[Mercury Design System](../frontend/mercury-design-system/SKILL.md)**: Mercury tokens, bundles, icons, theming.
- **[Design System Builder](../frontend/design-system-builder/SKILL.md)**: Authoring custom design systems for KBs.
- **[UI Creator](../frontend/ui-creator/SKILL.md)**: Templates for generating GeneXus panels and screens.

## Preferred Workflow

1. **Search**: Use `genexus_query` to find entry points.
2. **Read**: Use `genexus_read` or `resources/read` to get source/metadata.
3. **Plan**: Apply rules from **GeneXus 18 Guidelines** or **Nexa** to design the solution.
4. **Edit**: Use `genexus_edit` for focused changes (singular `name` or `targets[]` for multi-object atomic edits).
5. **UI/UX**: If the task involves screens, apply **Frontend Skills** for modern aesthetics.
6. **Validate**: Use `genexus_lifecycle` to build and verify.

## Multi-KB (v2.3.0+)

The server can hold multiple KBs open at once (`Server.MaxOpenKbs`, default 3), each in its own Worker process. Cross-KB tool calls run in parallel — intra-KB calls remain serialized by the SDK's STA constraint.

- Every non-meta tool accepts an optional `kb` argument: an alias declared in `config.Environment.KBs[]` or an absolute path. When exactly one KB is open and no `kb` is given, that KB is used; with 2+ open the `kb` arg becomes required (`KB_AMBIGUOUS`).
- `genexus_kb action=list` returns open KBs with PID, working-set memory, and idle seconds — use it to decide when to free a slot before opening a new KB.
- `genexus_kb action=open` (alias and/or path) acquires a Worker on demand; `action=close` releases it; `action=set_default` persists `DefaultKb` to `config.json`.
- Legacy single-KB configs (`Environment.KBPath`) auto-migrate to `KBs[]` + `DefaultKb` at load time; existing flows keep working unchanged.

## Tool Best Practices

| Tool | Tip |
| --- | --- |
| `genexus_query` | Narrow down by `typeFilter` for faster results. |
| `genexus_read` | Always check the `Variables` part if adding logic. `PatternInstance` / `PatternVirtual` return the full pattern XML (WorkWithPlus). `Documentation` / `Help` are first-class write targets. |
| `genexus_edit` | Prefer `mode=patch` for surgical changes; use `targets[]` for atomic multi-object edits. For pattern parts see "Pattern editing" below. |
| `genexus_analyze` | One tool covers `linter`, `navigation`, `hierarchy`, `impact`, `data_context`, `ui_context`, `pattern_metadata`, and `summary`. `explain` is `compatibility-only` and returns `NotImplemented`; use `summary`, `context`, or `genexus_read` instead. |
| `genexus_sql` | `action=ddl` for Transaction/Table DDL, `action=navigation` for the SQL produced by a For Each (replaces `genexus_get_sql` and `genexus_get_sql_for_navigation`). |
| `genexus_kb` | List/open/close/set_default — multi-KB pool management (replaces `genexus_open_kb`). |
| `genexus_properties` | Essential for enabling "Business Component" or "Expose as Web Service". For WorkWithPlus also handles `SDPlus_Editor_Apply_On_Save` (toggle to keep pattern XML overrides). |
| `genexus_list_objects --typeFilter ThemeClass --nameFilter <Button\|TextBlock\|Title\|...>` | Discover real theme-class names in the KB before applying styling. |

## Pattern editing (WorkWithPlus PatternInstance / PatternVirtual)

The MCP edits the IDE's full pattern XML model — containers, controls, actions, grids, orders, filters, rules, event blocks. Both `mode: full` and `mode: patch` work on `part: 'PatternInstance'` (and `'PatternVirtual'`).

**Auto-reconcile `childrenOrderedList`** — don't manage it by hand. On every pattern write the MCP rebuilds (and creates if missing) every parent's `childrenOrderedList` from the actual child order in your XML, dropping orphans and adding new entries. The response carries a `childrenOrderedListReconciliation` block describing each rewrite (or skip with reason). The IDE only renders children listed there, so this matters.

**Transaction view vs Selection view** — they're separate XPath subtrees inside the same PatternInstance:
- `/instance/transaction/...` → form view (TableContent + TableActions, `<rule>`s).
- `/instance/level/selection/...` → list view (TableSearch + `<orders>` + `<grid>`).

Edit one without touching the other.

**Element kinds** (XML node → IDE control):
- **Custom buttons → `<userAction>`**, NOT `<standardAction>`. Only `Trn_Enter`/`Trn_Cancel`/`Trn_Delete` (transaction) and `Insert`/`Update`/`Delete`/`Export`/`ExportReport` (selection grid) are registered standard actions; the SDK rejects unknown standardAction names during validated ops.
- Sections → `<table isGroup="True" title="…" groupThemeClass="GroupTela|GroupTelaResp|GroupFiltro">…</table>`.
- Text → `<textBlock controlName="…" caption="…" themeClass="BigTitle|LinkText|…" format="HTML" />`.
- Buttons style via `buttonClass="btn ButtonGreen|ButtonBlue|ButtonRed|ButtonCinza"` (resolve real class names from the KB; see the `genexus_list_objects` tip above).

**Apply-on-save override** — when `SDPlus_Editor_Apply_On_Save` is enabled on the WorkWithPlus object, the pattern engine recomputes some attributes after every save (notably `title` bound to the underlying transaction). To keep hard overrides:

```jsonc
{ "tool": "genexus_properties",
  "arguments": { "action": "set", "name": "WorkWithPlus<Object>",
                 "propertyName": "SDPlus_Editor_Apply_On_Save", "value": "False" } }
```

Accepts `"True" | "False" | "Default"`.

**Workflow for a pattern redesign**:
1. `genexus_list_objects --typeFilter ThemeClass --nameFilter <kind>` — discover real class names.
2. `genexus_read --part PatternInstance` — current state.
3. Edit the XML in memory: add `<userAction>`/`<textBlock>`/group `<table isGroup="True">`/etc, apply theme classes. Don't worry about `childrenOrderedList`.
4. `genexus_edit --mode full|patch --part PatternInstance` — MCP reconciles ordering, validates via SDK, returns `persistedVerified: true` plus the reconciliation report.
5. Read back to confirm.

See `genexus://kb/tool-help/genexus_edit` resource for concrete pattern examples.

## Anti-patterns

- Do not attempt to guess object names; always query first.
- Do not use `genexus_edit` without reading the latest state of the object.
- Avoid large monolithic edits; prefer smaller, validable changes.
- Do not call removed tools (`genexus_batch_read`, `genexus_batch_edit`, `genexus_open_kb`, `genexus_get_sql`, `genexus_get_sql_for_navigation`, `genexus_summarize`, `genexus_explain_code`). They return JSON-RPC -32601 with `error.data.replacedBy` pointing at the current tool.
