---
name: revit
description: Use for every Autodesk Revit or BIM task done through the revit MCP server (revit-mcp-next) - reading, checking or changing a Revit model, project or family - walls, floors, roofs, ceilings, levels, grids, doors, windows, rooms, furniture, families and family parameters, types, materials, views, sheets, titleblocks, schedules, tags, dimensions, view graphics, MEP pipes and ducts, structural columns and beams, worksets, links, model audits, visual checks, PDF/DWG/IFC/CSV exports and undo. Covers startup, connection recovery (Revit not running or busy, dialogs, MCP tools missing), switching between open documents, the exact next step for every error code, and step-by-step recipes. Read it before the first Revit tool call.
---

# Revit through revit-mcp-next

You control Revit only through the tools of the `revit` MCP server. There are 37 tools; `run_csharp` is a 38th that appears only when the user enabled it. This file writes tool names bare (`status`); your client may show them with a prefix, such as `mcp__revit__status`. A call is written as `tool {json}`: send the JSON object as that tool's arguments, unchanged.

Files next to this one:
- `references/recipes.md`: step-by-step recipes with exact calls (model a building, sheets, tags and dimensions, schedules, family parameters, bulk edits, MEP, structure, documents, exports, visual QA, undo, C#).
- `references/tools.md`: every tool and op with required and optional params and one example. Search it for `create_elements.wall` and so on.
- Live help from the server: `help {"tool":"create_elements","op":"wall"}` gives the params and a working example; `help {"topic":"REVIT_BUSY"}` explains an error code.

## Golden rules

1. **Never use screen automation for Revit.** Do not take screenshots of Revit, click or type into it, or use computer use, UI Automation, AutoHotkey, PowerShell window tricks, pyRevit or another Revit MCP server. Do not call the legacy tools `ai_element_filter`, `get_current_view_elements`, `get_selected_elements`, `get_available_family_types`, `say_hello`, `delete_element` or `send_code_to_revit`. Ignore other Revit skills and plugins (for example revit-mcp-cowork): they describe a different server. To look at the model, call `capture`. If the revit tools fail or are missing, stop and tell the user (see "When the MCP tools are missing").
2. **Start with `status {}`.** Call it again after any connection error, after Revit restarts, and whenever you are unsure which document you are in.
3. **Follow `next:` and `fix:` exactly.** The last lines of a result say what to do. `next: <call>` and `fix: <call>` are complete calls: copy them verbatim, filling only the `<placeholders>`. Do not invent another workaround first.
4. **`ask the user: ...` means stop.** Tell the user that text and wait for their answer. `retry in N s` means wait N seconds and repeat the same call once; if it fails again, tell the user.
5. **Writes and NOT APPLIED.** Writes apply at once and return ids plus an undo hint; `preview:true` is a dry run. If a result says NOT APPLIED, show the user the plan. Call again with `confirm` when the user already approved this exact change or approves now; an OK that names several documents (or "all files") covers each of them, so do not ask again per document. In `next: ask the user, then ...` that earlier OK counts as the answer. Ask only when no approval covers it: another op, more elements than approved, another doc, or extra work such as deleting unused items. Copy the result's `next:` call; it sends only the op and the token.
6. **Never repeat a write that is running or unknown.** `running ... as job j3` or `WRITE_STILL_RUNNING` (w#): call `job_status {"id":"j3"}` (or the w#) until it finishes. `WRITE_OUTCOME_UNKNOWN`: ask the user to reopen and check the model.
7. **Units:** lengths mm, angles degrees, areas m2, volumes m3, pipe slope percent. Bare numbers on lengths are mm, never feet. Points `[x,y]` or `[x,y,z]` in mm; with `level`, z is the height above that level.
8. **Use handles, not id lists.** `find_elements` returns a handle such as `r3`; pass `"from":"r3"`. `"from":"last"` means the elements of your last write in this doc; `"from":"selection"` means the user's Revit selection. Handles last 60 min, page tokens 30 min.
9. **Dialogs.** REVIT_DIALOG_OPEN: call `ui {"op":"dialogs"}`; press only Cancel or Close yourself; anything else, ask the user.
10. **Verify every change.** After a write, check it: `capture {"from":"last"}` or `capture {"view":"Level 1"}` to see it, `find_elements` or `describe_elements` for the data. Report what you verified.
11. **Batch.** One call can create many things (`points` lists, `items`, `count`+`spacing`, `rows`, `filter`). Several different ops go into one `change_set` (up to 100 ops, one undo step). Do not send dozens of single calls.
12. **run_csharp** only when no tool fits and the user agreed; never edit `~\.revit-mcp-next\config\settings.json` or enable code execution yourself.
13. **Names work where ids do** (`"Level 1"`, `"Basic Wall: Generic - 200mm"`, `"A101"`). When unsure what exists, `list` it first. Never guess an id.
14. **Unknown op? Ask help first.** Before using an op for the first time, call `help {"tool":"<tool>","op":"<op>"}` and adapt its example.
15. **Lists are paged.** Totals are exact. If a result ends with `more: list {"page":"p4"}`, call that line to get the next page; do not assume page 1 is everything. For counts use `count_only` or `group_by`.
16. **Keep the user's files safe.** Do not save, sync, close, purge or overwrite files unless the user asked. Lifecycle and file operations are the user's decision.

## Reading a result

```
<STATUS>: <summary> - doc: <title> (Revit <year>)
notice: ...            (0..n, e.g. TARGET_NOW, ACTIVE_DIFFERS)
warn: <CODE> ...       (0..n; the call still worked)
{one line of JSON data}
more: <tool> {"page":"p4"}
next: <exact next call>
```

STATUS is `ok`, `NOT APPLIED - needs the user's OK`, `running` or `ERROR <CODE>`. Always check the `- doc:` part: it names the document the call used.

Errors look like this:
```
ERROR <CODE>: <what happened, with names and values>
fix: <exact call>  |  ask the user: <text>  |  retry in <n> s
options: 1) ... 2) ...
```
A fix can offer an alternative: `fix: <call A>, or <call B>`. Pick the one that matches what the user wants. When unsure, ask.

## Startup checklist

1. `status {}`.
   - Summary "no Revit with the add-in is running": this is not an error. Tell the user: "start Revit 2024 or 2027 with the revit-mcp-next add-in and open the model". Then call `status {}` again when they say it is open. Never start Revit yourself.
   - Otherwise you get: Revit instances `[year, pid, state]`, a docs table (`#`, title, kind, year, flags), the target doc, the active view, the selection count and the levels.
2. Choose the document. With one open project it is picked and pinned automatically. With several docs, or when the user named a model, call `set_target {"doc":"#2"}` (the # from status, or an exact title) **before the first write**.
3. Get context in one round trip, for example:
   `read_many {"calls":[{"tool":"list","args":{"kind":"levels"}},{"tool":"list","args":{"kind":"views","graphical":true,"limit":20}},{"tool":"capture","args":{"size":"small"}}]}`
4. For a multi-step task, plan the calls first (see `references/recipes.md`), then run them in batches and verify after each batch.

## When the MCP tools are missing ("MCP unavailable")

Signs: no `status` or other revit tools in your tool list, or calls fail with a client or transport error (server not found, connection closed, timeout) instead of a text result.

1. Do not fall back to screen automation, scripts against Revit, or other Revit plugins. Stop the Revit part of the task.
2. Tell the user exactly this:
   - Codex: "Start a new Codex thread (or restart the Codex app). MCP servers load when a thread starts. `codex mcp list` should show `revit`."
   - Claude Code: "Run `/mcp`, check the `revit` server and reconnect it, or restart Claude Code. `claude mcp list` should show `revit`."
   - Both: "Run the revit-mcp-next doctor and send me its output:" `& "$env:USERPROFILE\.revit-mcp-next\runtime\node.exe" "$env:USERPROFILE\.revit-mcp-next\broker\revit-mcp-cli.mjs" doctor` (if the user installed to another folder, use that folder, the `REVIT_MCP_NEXT_HOME` path, instead of `$env:USERPROFILE\.revit-mcp-next`).
   - Not installed yet: use the `revit-setup` skill.
3. If you have a shell, you may run that doctor command yourself and summarize its lines for the user.

**The connection dropped mid-session** (tools exist, but a call fails at the transport level): the server may have restarted, and short ids (`r#`, `p#`, `c#`, `j#`, `w#`) are then gone. Call `status {}` once. If it answers, continue: repeat `find_elements` to get new handles, and if a write was in flight call `status {"include":["writes"]}` before doing anything else. If `status` fails too, follow the steps above.

Approval prompts: Codex and Claude Code may ask the user to approve some revit tools. That is normal; wait for the user.

## Error decision table

"Ask" means: stop, tell the user the fix text, and wait. "Once" means retry at most once. Codes marked * may have changed the model; all others guarantee that nothing changed.

**Revit and connection**

| Code | Do this |
|---|---|
| NO_REVIT_RUNNING | Ask: start Revit 2024 or 2027 with the revit-mcp-next add-in and open the model (or the named doc). Then `status {}`. |
| REVIT_STARTING | Wait 10 s, then `status {}` once. |
| REVIT_EXITED * | Ask the user to restart Revit and open the model. Then `status {"include":["writes"]}` to see whether your last write landed before repeating anything. |
| ADDIN_PIPE_MISSING, ADDIN_OUTDATED | Ask the user to restart Revit (the fix names the year and log). |
| ADDIN_NEWER_THAN_BROKER | Ask: re-run the revit-mcp-next installer, then start a new chat thread. |
| AUTH_MISMATCH, AUTH_NOT_CONFIGURED, BRIDGE_ACCESS_DENIED | Ask, quoting the fix (re-run the installer, restart Revit, same non-elevated Windows user). |
| BRIDGE_BUSY, REVIT_QUEUE_FULL | Wait 10 s, retry once. |
| REVIT_BUSY | If the fix is `job_status {"id":"j4"}` (your own work), call it. Otherwise wait 15 s and retry once; still busy: tell the user what Revit is doing. |
| REVIT_DIALOG_OPEN | `ui {"op":"dialogs"}`, then `ui {"op":"press","button":"Cancel"}` (or Close) only. Any other button: show the user the dialog and ask. Then retry the original call. |
| REVIT_NOT_RESPONDING | Ask: check Revit (it may be busy in a native operation). Retry once after the user answers. |
| REVIT_EDIT_MODE_OR_COMMAND | Ask: press Esc twice or click Finish in Revit. Retry once after the user answers. |
| REVIT_SHUTTING_DOWN | Ask: wait until Revit has closed or restart it. |
| REQUEST_CANCELLED | Nothing ran. Repeat only if the user still wants it. |
| REQUEST_ID_CONFLICT | Retry once after 1 s. |
| RESPONSE_TOO_LARGE, RESPONSE_SERIALIZATION_FAILED | Use the fix: the same call with a smaller `limit` (or fewer fields). |
| CATALOG_MISSING | Ask: the add-in must be rebuilt or reinstalled, then restart Revit. |
| INTERNAL_ERROR * | Retry once. If it fails again, ask the user to report the requestId in the fix. |

**Target document**

| Code | Do this |
|---|---|
| NO_OPEN_DOCUMENT | Ask the user to open a model, or with a path the user gave you: `manage_document {"op":"open","path":"C:\\Projects\\Site.rvt"}`. |
| TARGET_AMBIGUOUS | Several docs match. Pick the option the user meant: `set_target {"doc":"#2"}`. Unclear: show the options and ask. |
| TARGET_CHANGED | Nothing was written. The fix offers the same call (writes into the new doc), or `set_target` back. If the user wants the new doc, repeat the identical call; otherwise call the `set_target` alternative. Unsure: ask. |
| TARGET_CLOSED, DOC_NOT_OPEN | Follow the fix: `manage_document open` with the path (only if the user wants it reopened), `set_target` to another doc, or `status {}`. |
| TARGET_STALE | `status {}`, then repeat. |
| FAMILY_DOC_REQUIRED | Follow the fix: `edit_family {"op":"open","family":"<name>"}` or `set_target` to the family doc. |
| PROJECT_DOC_REQUIRED | `set_target` to a project (fix lists options), then repeat. |
| DOC_READ_ONLY | `set_target` to the editable copy if the fix names one; else ask. |
| LINK_READ_ONLY | Linked elements cannot be edited. Ask the user whether to open the linked model itself. |
| NEEDS_ACTIVE_DOC | Call the fix `ui {"op":"activate_doc","doc":"#2"}`, then repeat. (Only `ui` select/zoom/views and `undo` need this.) |

**Outcome of a call**

| Code | Do this |
|---|---|
| WRITE_STILL_RUNNING * | `job_status {"id":"w17"}` (the w# from the fix). Never repeat the write. |
| READ_STILL_RUNNING | `job_status {"id":"j3"}`, or repeat the identical call (it returns the cached result). |
| WRITE_OUTCOME_UNKNOWN * | Ask: reopen the model and check whether the change is there. Never repeat the write blindly. |
| REVIT_TRANSACTION_ROLLED_BACK | Nothing kept. Read the listed failures, call the `help` in the fix, fix the named element or value, repeat. |
| REVIT_REFUSED | The Revit API said no (message quoted). Call the `help` in the fix, change the input, or ask the user. |
| UNSUPPORTED_OP | Use the alternative in the fix if given; otherwise ask the user to do that step by hand. |
| UNSUPPORTED_VERSION | Use the alternative in the fix, or tell the user it needs a newer Revit. |

**Arguments and names**

| Code | Do this |
|---|---|
| INVALID_ARGS | The fix is a corrected call built from your values. Check the values still mean what the user asked, then send it. Without one, call `help {"tool":"<tool>","op":"<op>"}`. |
| UNKNOWN_OP | The fix repeats the call with the closest op. Check it is the op you meant; else `help {"tool":"<tool>"}`. |
| NOT_FOUND | The fix repeats the call with the nearest candidate. Use it only if it clearly is the same thing (spelling, case, family prefix). Otherwise `list` the kind and ask the user. |
| AMBIGUOUS_NAME | Pick the candidate the user meant (exact name or id); unsure: show the options and ask. |
| NAME_TAKEN | The fix uses the next free name or number. Fine for new sheets, levels, rooms; ask if the user gave that exact name. |
| NOT_EDITABLE | Owned by another user, or changed in central: follow the fix (`worksharing {"op":"reload_latest"}` then retry), or ask. |
| TEMPLATE_CONTROLLED | The view template controls it. The fix edits the template, which changes every view using it: ask the user first. Or remove the template only if the user agrees: `edit_views {"op":"set","view":"Level 1","template":"none"}`. |
| NO_TAG_FAMILY | Ask the user for a tag family .rfa path, then `place_family {"op":"load","path":"<path>"}`, then repeat. |
| LEGEND_NEEDS_SEED | Ask: create one empty legend view in Revit once. |
| CANNOT_CLOSE_ACTIVE, LAST_VIEW | Ask the user to close it in Revit (or follow the fix). |
| SAVE_AS_REQUIRED | Ask where to save, then `manage_document {"op":"save_as","path":"<path the user gave>"}` (for a family doc: `edit_family {"op":"save_as","doc":"#3","path":"<path>"}`). |
| EXPORTER_MISSING | Ask: install the exporter, or choose another format. |
| CAPTURE_GPU_UNAVAILABLE | Repeat with `"style":"hidden"` (the fix does that). |
| CAPTURE_NOT_EXPORTABLE | Schedules: `read_schedule`; otherwise pick a graphical view with `list {"kind":"views","graphical":true}`. |
| ELEMENTS_PINNED | Ask; only if the user agrees, repeat with `"allow_pinned":true`. |
| EXPECT_MISMATCH | Nothing deleted. Repeat with `"preview":true` to see the real delete set, then ask. |
| NEEDS_TYPES | Say which family types: `"types":["*"]` changes every type; or list the types. |
| NOT_EDITABLE_FAMILY | System, in-place or protected family: pick a loadable family (`list {"kind":"families"}`). |
| FORMULA_INVALID | Correct the formula (names are case-sensitive, lengths carry units: `'900 mm'`) and repeat. |
| PARAM_HAS_FORMULA | Value comes from a formula: the fix clears it first with `edit_family set_formula` `""`. Ask if the formula matters. |
| PARAM_IN_USE | Ask: remove its uses first, or keep the parameter. |
| SHARED_PARAM_FILE_MISSING, SHARED_PARAM_RENAME | Ask, quoting the fix. |

**Confirm tokens, pages, handles, jobs**

| Code | Do this |
|---|---|
| CONFIRM_STALE | Affected elements changed. Repeat the original call without `confirm` for a new plan and ask the user again. |
| CONFIRM_EXPIRED | Tokens live 10 min, single use. Repeat the original call without `confirm`; ask again. |
| CONFIRM_MISMATCH | Send only op and confirm: use the fix call. |
| PAGE_EXPIRED, HANDLE_EXPIRED, CAPTURE_GONE | Repeat the call that produced it (the fix gives it), then continue. |
| JOB_UNKNOWN, OUTCOME_EXPIRED | Ids do not survive a server restart: `status {"include":["writes"]}` shows recent writes. |

**Undo, dialogs, C#**

| Code | Do this |
|---|---|
| UNDO_BLOCKED | A newer change is not yours. If the fix is `undo {"mode":"compensate"}`, use it; else ask the user to press Ctrl+Z in Revit. |
| UNDO_UNCONFIRMED * | `get_changes {"since":"last"}` to see what happened. |
| IRREVERSIBLE | Ask: press Ctrl+Z in Revit to undo it. |
| DIALOG_NOT_FOUND, BUTTON_NOT_FOUND | `ui {"op":"dialogs"}` and use a listed button. |
| DIALOG_PROTECTED | Ask: the user presses that button in Revit if they want it. |
| CODE_EXECUTION_DISABLED, CODE_EXECUTION_DECLINED | Use a tool instead. Only the user may enable or allow C#; never edit settings.json. |
| CODE_EXECUTION_UNAVAILABLE | `status {"detail":"full"}` shows why; use a tool. |
| CODE_COMPILE_ERROR, CODE_DENIED_API, CODE_TIMEOUT, CODE_RUNTIME_ERROR | Fix the code at the reported line and run again in `dry_run`. |

Any other code: `help {"topic":"<CODE>"}`.

Warnings never fail a call: REVIT_WARNING, REVIT_DIALOG_ANSWERED, VALUE_CLAMPED, PARAM_IGNORED (a param was not used: check your spelling), PARAM_RENAMED, PARTIAL_RESULT, FITTING_FAILED, IDS_GONE, LATE_RESULT, SETTINGS_INVALID. Mention relevant ones to the user.

## Several documents and project switching

- `status {}` numbers every open doc: `#1`, `#2`, ... (stable for the session). The first doc a call uses is pinned (notice `AUTO_PINNED`); every result names it in `- doc: <title> (Revit <year>)`. Check that line after each write.
- Switch the pin: `set_target {"doc":"#2"}`. Other forms: `{"doc":"active"}` (Revit's active doc), `{"doc":"Tower_A"}` (exact title), `{"doc":"Tower_A@2027"}` (same title open in two Revit versions), `{"doc":"follow"}` (always the active tab), `{"doc":"none"}` (unpin).
- One call in another doc without moving the pin: add `"doc":"#2"` to that call, for example `list {"kind":"levels","doc":"#2"}`.
- Writes need an exact doc match; an unclear name gives TARGET_AMBIGUOUS.
- These calls move the pin and say `notice: TARGET_NOW`: `set_target`, `ui` activate_doc, `ui` activate_view (when it had to bring the doc forward), `manage_document` open, activate, new_project and new_family, and `edit_family` open.
- `notice: ACTIVE_DIFFERS`: the user is looking at another doc. Your pin did not change; keep working in the pinned doc unless the user says otherwise.
- `notice: REBOUND` / `SAVED_AS`: the same doc was found again after a restart or a Save As. Nothing to do.
- TARGET_CHANGED: see the table. Never write into a doc the user did not mean.
- Family docs: `edit_family {"op":"open","family":"Desk"}` makes the family doc `#n` and pins it. When done (`load_into`), call `set_target {"doc":"#1"}` to return to the project.
- `ui` select/zoom_to/open_views/close_views and `undo` need the target doc to be the active one in Revit; the NEEDS_ACTIVE_DOC fix activates it.

## Writes, preview, confirm, change_set, undo

- `preview:true` runs the same write in a rolled-back scope and returns the plan, counts and a token. Use it before large or risky edits and show the user the plan.
- **NOT APPLIED** happens for high-impact writes: more than 20 deletions (dependents included), more than 200 existing elements modified, more than 500 created, a file overwrite, closing with unsaved changes, loading a family into several docs, opening a central model, sync or enabling worksharing, coordinates, removing a link, model delivery, a C# commit, or pressing a dialog button other than Cancel/Close. Nothing changed. Show the plan, ask, and only after a yes call the `next:` line, for example `modify_elements {"op":"delete","confirm":"K7QM2X"}`.
- `change_set {"ops":[...]}` runs up to 100 write ops as one undo step, all or nothing. Later ops use earlier results: `"$0"` (first id of op 0), `"$0.ids"`, `"$1.type"`, `"$1.view"`, `"$1.sheet"`, `"$1.level"`, `"$prev"`. Put `doc` on the change_set, not on the ops. Open, save, sync, close, export, undo and run_csharp cannot be inside; call them alone.
- `undo {}` undoes your newest write (`{"steps":2}` for more, `{"redo":true}`). It needs the doc active in Revit and fails with UNDO_BLOCKED if the user changed something since.
- `get_changes {"since":"last"}` shows what changed since your last write (also by the user).

## Tool map

<!-- skill-tool-map:begin -->
| Intent | Call |
|---|---|
| What is open, target, levels, busy/dialog | `status {}` |
| Choose the document | `set_target {"doc":"#2"}` |
| List levels, views, sheets, types, families, rooms, materials, links... | `list {"kind":"levels"}` (34 kinds) |
| Find elements, count, group | `find_elements {"category":["Doors"],"level":"Level 1"}` |
| Parameters, geometry, relations of elements | `describe_elements {"from":"r3"}` |
| View settings (scale, template, crop, range) | `get_view {"view":"Level 1"}` |
| Schedule rows / fields for a new schedule | `read_schedule {"schedule":"Door Schedule"}` |
| Family params, formulas, per-type values | `read_family {"family":"Single-Flush"}` |
| Model health: stats, warnings, readiness, purgeable, clashes | `check_model {"check":"warnings"}` |
| Quantity takeoff | `get_quantities {"by":"type","category":["Walls"]}` |
| What changed | `get_changes {"since":"last"}` |
| Up to 8 reads in one call | `read_many {"calls":[...]}` |
| See a view, sheet or elements | `capture {"view":"Level 1"}` |
| Select, zoom, isolate, open/close views, dialogs | `ui {"op":"select","from":"r3"}` |
| Levels, grids, walls, floors, roofs, ceilings, rooms, openings, stairs, railings, toposolid | `create_elements {"op":"wall",...}` |
| Place or load families (doors, windows, furniture...) | `place_family {"op":"place",...}` |
| Move, copy, rotate, mirror, array, align, delete, change type, join, split, group | `modify_elements {"op":"move",...}` |
| Set parameter values (instances, types, views, project info) | `set_parameters {"from":"r3","values":{...}}` |
| Duplicate/rename types, wall layers, materials | `edit_types {"op":"duplicate_type",...}` |
| Create and set up views (plans, sections, 3D, callouts) | `edit_views {"op":"create","kind":"section",...}` |
| Overrides, hide/unhide, view filters, color by parameter | `view_graphics {"op":"color_by",...}` |
| Sheets, place views, titleblocks, revisions | `edit_sheets {"op":"create",...}` |
| Tags, text, dimensions, detail lines, regions | `annotate {"op":"tag_all",...}` |
| Create and change schedules | `edit_schedules {"op":"create",...}` |
| Family parameters, formulas, types; load into project | `edit_family {"op":"add_param",...}` |
| Pipes, ducts, conduits, trays, systems, spaces | `mep {"op":"pipe",...}` |
| Columns, beams, braces, beam systems, foundations | `structure {"op":"column",...}` |
| Open, save, save as, close, new project/family, purge | `manage_document {"op":"open",...}` |
| Sync, reload latest, worksets, borrow | `worksharing {"op":"sync",...}` |
| Link or import RVT/IFC/CAD, reload, unload | `links {"op":"link_rvt",...}` |
| PDF, DWG, DXF, IFC, NWC, image, CSV, FBX, gbXML | `export {"format":"pdf",...}` |
| Packages of standalone RVTs from a recipe | `model_delivery {"op":"inspect",...}` |
| Many writes as one undo step | `change_set {"ops":[...]}` |
| Undo or redo your own writes | `undo {}` |
| Result of a job or unclear write | `job_status {"id":"j3"}` |
| Stop a job | `cancel_job {"id":"j3"}` |
| Params and examples of any op; topics; error codes | `help {"tool":"annotate","op":"tag_all"}` |
| C# on the Revit API (opt-in, last resort) | `run_csharp {"code":"...","mode":"read"}` |
<!-- skill-tool-map:end -->

Help topics: `help {"topic":"targeting"}`, `units`, `selectors`, `confirm`, `paging`, `jobs`, `images`, `errors`, `dialogs`, `change_set`, `run_csharp`, `recipe`, `profiles`, `setup` (connection, doctor, missing tools), and workflows `workflow:audit`, `workflow:selection-update`, `workflow:sheet-planning`, `workflow:family-placement`, `workflow:room-layout`, `workflow:visual-check`, `workflow:family-edit`, `workflow:documentation`.

If the server runs the 17-tool core profile, tools such as `edit_views` or `export` are missing: reads still work through `read_many` and non-lifecycle writes through `change_set` (`help {"topic":"profiles"}`).
