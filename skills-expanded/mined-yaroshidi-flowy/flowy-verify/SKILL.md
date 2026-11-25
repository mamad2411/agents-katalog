---
name: flowy-verify
description: Use after a batch of Webflow MCP writes (data_whtml_builder, data_element_builder, data_element_tool, data_element_settings_tool, data_style_tool, data_cms_tool, data_component_tool, data_component_props_tool, data_component_variants_tool, data_variable_tool, data_scripts_tool, asset_tool, data_sites_tool publish) to verify the writes actually landed — catching silently-dropped classes, Webflow-injected style defaults, bindings that only look broken, and stale live-page state. A PostToolUse hook shipped with the flowy plugin reminds the agent to invoke this skill.
---

# flowy-verify

The post-write check. Part of the set: **[flowy](../flowy/SKILL.md)** (which hand) →
**[flowy-manual](../flowy-manual/SKILL.md)** (what's true) → **flowy-verify** (did it land).

> 🚫 **Verifying is NOT publishing.** If verification reveals the live page is stale, report it as a
> finding and **STOP**: never publish to "fix" it, and never offer to.
> [house-rules.md](../flowy/house-rules.md).

## When to invoke

At a **logical batch boundary**: after a section and its children, after a batch of style writes,
before saying "done". Not after every call. If the hook fires
mid-batch, acknowledge and continue; verify at the boundary.

**Not** after pure reads (`query_*`, `get_*`, `list_*`, `*_snapshot`, `webflow_guide_tool`). The hook
matches tools, not actions, so reads will sometimes trigger it: that's noise, not a signal.

## Routine

Run in order; skip a step only if no calls of that type happened.

### Step 1 — Class attachment (if `data_whtml_builder` or `data_element_builder` ran)

**This trap is still live in 2.0.1** (verified 2026-07-25): `data_whtml_builder` inserted
`<div class="ghost-class">` with no `css`, and the class was silently dropped. No style created, no
error.

`data_element_tool > query_elements` with an `element_id` filter on each inserted element.

- **Pass:** the element carries `styleNames` containing every class from your markup.
- **Fail:** `styleNames` is **absent entirely**; that is the drop signal.
- **Confirm** with `data_style_tool > query_styles name_path:["<class>"]` → `matches: []` means it
  was never created.
- **Fix:** `data_style_tool > create_style {name, properties: []}`, then
  `data_element_tool > set_style {id, style_names:[…]}`.

Passing a `css` rule alongside the html avoids the drop: `styleNames` then appears normally.

### Step 2 — Injected style defaults (if new Designer styles were auto-created)

`data_style_tool > query_styles include_properties:true` on each new style. Flag `max-width`,
`min-width`, `max-height`, `min-height`, `aspect-ratio`, and any `position` that fights your CSS.

**Fix:** `update_style {style_name, remove_properties:[…]}`.

*2026-07-25: a whtml div with a `color` rule got **no** injections. Not a clearance: the historical
injections were on **Image** elements, untested in 2.0.1. Keep the step.*

### Step 3 — Bindings (if `data_element_settings_tool` wrote a binding)

**Read with `type:"all_raw_settings"`, never `all_resolved_settings`.** Verified 2026-07-25: a
correctly bound CMS field reads back as `null` under the resolved view because CMS bindings cannot
resolve at design time: **the resolved view makes a working bind look broken.** The raw view shows
full binding metadata (`sourceType`, `collectionName`, `fieldName`, `fieldType`), and the canvas
renders the real value.

For elements inside a component definition, pass the same `scope_component_id` you wrote with.

### Step 4 — Element tree (after any tree change)

`data_element_tool > query_elements`: parent/child intact, no orphans, types are what you expected
(requested `CMSCollection` legitimately returns `DynamoWrapper`; `TextBlock` returns `Block`), no
accidental duplicates.

### Step 5 — Embed code (if an embed was written)

- MCP-written: `get_settings all_raw_settings` → compare the returned `code` to what you sent.
- Clipboard/CM6-written: in-editor SHA **before** save and again **after** reopening. Compare
  in-page and return only a **boolean**; returning the hex digest trips the extension's
  `[BLOCKED: Base64 encoded data]` filter. Procedure: [embeds.md](../flowy/embeds.md).

### Step 6 — Live-page diagnostic (only after an authorized publish)

Never trigger the publish yourself. After propagation (~15–30s):

1. `navigate` to `https://<site>.webflow.io/<slug>?bust=<ts>`
2. `read_console_messages` with `pattern: "error|TypeError|null|exception"`
3. `javascript_tool`: the block from [diagnostics.md](../flowy-manual/diagnostics.md)
4. `computer screenshot` at the relevant scroll position

### Step 7 — Report

```
flowy-verify report:
✅ Verified: [each item + the tool call and data point that proved it]
⚠️  Flagged: [anomaly + element id / style name / measured value / proposed fix]
❌ Failed:   [definite failure + element id + fix applied or proposed]
🔍 Unchecked:[anything not verifiable here — incl. runtime behaviour, deferred by house rule]
```

Omit empty categories.

## Hard rules

- **Never claim "verified" without naming the call and the data point.** "Looks fine" is not verification.
- **A write response is not verification.** `set_settings` and `update_style` both report success
  regardless; always re-read.
- **If a step is unrunnable via MCP, it is NOT yet unrunnable.** [house-rules.md](../flowy/house-rules.md)
  #13: switch to the `claude-in-chrome` hand and check by eye before writing anything down. `🔍 Unchecked`
  is only permitted after **both** hands have been tried, and must name what was tried in each.
  The single exception is embed **runtime**, which genuinely needs a publish (rule #12).
  Test: *could the user see this by opening the Designer themselves?* If yes, go look.
- **Never silently skip** a step.
- **Canvas ≠ live.** Only Step 6 is live verification, and it only runs after the user's own publish.
- Cite [flowy-manual](../flowy-manual/SKILL.md) when applying a fix.
