---
name: menu-lookup
description: Locate a specific FileMaker custom menu or menu set in `agent/xml_parsed/custom_menus/` or `agent/xml_parsed/custom_menu_sets/`. Extracts the real UUIDs required before creating or modifying any menu XML. Use when the user asks to create, modify, review, or look up a custom menu or menu set by name or ID.
---

# Menu Lookup

Locate a FileMaker custom menu or menu set in the parsed XML export and extract the critical UUIDs required before any menu XML can be created or modified. Without the correct UUIDs, FileMaker silently ignores paste operations.

Resolves using either:
- A **menu name** (exact/contains/fuzzy match), or
- A **menu ID** (numeric, from the filename pattern `- ID {N}.xml` or menu set's `<CustomMenuReference id="N">`)

**Performance target**: 3 tool calls for unambiguous lookups (discover + read + confirm), 4 for ambiguous.

## Lookup workflow

### Step 1 — Discover files (PARALLEL)

Run these in **parallel** (single message, multiple tool calls):

**Tool call A — List all menu files:**

```bash
ls "agent/xml_parsed/custom_menus/"*/  "agent/xml_parsed/custom_menu_sets/"*/ 2>/dev/null
```

This returns every menu and menu set file across all solutions in one call. The output groups by directory — solution names appear as path prefixes. If no directories exist or the output is empty, report that menus haven't been exported and stop.

**Tool call B — List sandbox:**

```bash
ls agent/sandbox/
```

Check for any in-progress menu XML.

### Step 2 — Match and read

From the Step 1A file listing:

**Multi-solution handling**: If files appear under multiple solution subfolders, check whether the user mentioned a solution name or whether `CONTEXT.json` identifies one. If still ambiguous, use `AskUserQuestion` to disambiguate before proceeding.

**Determine menu type**: Infer from the user's request whether the target is a **CustomMenu** (individual menu, in `custom_menus/`) or **CustomMenuSet** (container assigned to a layout, in `custom_menu_sets/`). If unclear, search both — filenames are distinct between the two directories.

**Match against the file listing** using this priority (stop at first high-confidence match):

1. **ID match** (highest confidence) — filename contains `- ID {N}.xml`
2. **Exact name match** (case-insensitive) — filename prefix matches the menu name
3. **Contains match** (all tokens from the hint present in a candidate filename)
4. **Fuzzy match** (most tokens match) — pick the best, include up to 3-5 alternates

If the match is ambiguous (multiple plausible candidates, no clear best), use `AskUserQuestion` to present candidates and ask which menu to work with.

Once matched, **derive the full path** from the directory listing. Menu filenames follow the pattern `{MenuName} - ID {N}.xml`.

**Read the matched file** to extract UUIDs. If a sandbox match also exists (from Step 1B, matched by name), note it in the report.

### Step 3 — Menu match report + confirmation

Present the report and confirm in one response:

**Selected menu**
- Name: `{menu name}`
- ID: `{id}`
- Type: CustomMenu / CustomMenuSet
- Confidence: High / Medium / Low (reason)

**Paths found**
- Source XML: `{path in xml_parsed/custom_menus/ or custom_menu_sets/, or "not found"}`
- In-progress sandbox: `{path in agent/sandbox/, or "not found"}`

**Extracted UUIDs**
- Catalog UUID: `{UUID}`
- Menu/Set UUID: `{UUID}`
- Menu item count: `{N from MenuItemList membercount}`

**Alternates (if any)**
- Up to 3-5 other candidates (name + ID + path)

Then use `AskUserQuestion`: "Is this the correct menu? -- {Menu Name} (ID: {id}) in {solution}"
- Options: `yes` -- "Yes, proceed" / `no` -- "No, let me clarify"

## Critical UUIDs -- why they matter

FileMaker uses UUIDs to match pasted XML against existing objects in the solution. If either UUID is wrong or made up, the paste silently does nothing.

| UUID | Location in XML | Purpose |
|---|---|---|
| **CustomMenuCatalog UUID** | `<CustomMenuCatalog> > <UUID>` | Identifies the solution's menu catalog |
| **CustomMenu UUID** | `<CustomMenu> > <UUID>` | Identifies the specific menu to update |
| **CustomMenuSetCatalog UUID** | `<CustomMenuSetCatalog> > <UUID>` | Identifies the solution's menu set catalog |
| **CustomMenuSet UUID** | `<CustomMenuSet> > <UUID>` | Identifies the specific menu set to update |

Always read these directly from `xml_parsed/` -- never invent them.

## Handoff: creating or modifying menu XML

Once confirmed:

### Modifying an existing menu

1. Use the source XML from `xml_parsed/custom_menus/` as the base -- copy to `agent/sandbox/` if not already there.
2. Apply the requested changes following the structure in `agent/docs/CUSTOM_MENUS.md`.
3. Keep both the `CustomMenuCatalog UUID` and `CustomMenu UUID` from the original -- do not regenerate them.
4. Write to clipboard: `python3 agent/scripts/clipboard.py write agent/sandbox/<menu>.xml`
5. In FileMaker: open Manage > Custom Menus, select the target menu, paste.

### Creating a new menu item block for an existing menu

1. Confirm the menu's real UUIDs from the match report above.
2. Build new `<CustomMenuItem>` elements using the patterns in `agent/docs/CUSTOM_MENUS.md`.
3. `CustomMenuItem UUID` and `hash` values can be placeholder -- FileMaker reassigns on paste.
4. Increment `MenuItemList membercount` to match the new total.
5. Write and paste as above.

### Creating a brand-new menu (no existing XML)

The `xml_parsed/` export for this menu won't exist yet. The correct workflow is:

1. In FileMaker, create the empty menu in Manage > Custom Menus.
2. Copy it from FileMaker and save: `python3 agent/scripts/clipboard.py read agent/sandbox/<menu>-original.xml`
3. Use this file as the base -- it contains the real UUIDs.
4. Build the menu XML from there following `agent/docs/CUSTOM_MENUS.md`.

## Key reference

Full XML patterns, shortcut modifier values, `<Override>` rules, `<Base>` element behavior, and the `ut16` clipboard format are documented in:

`agent/docs/CUSTOM_MENUS.md`

## Examples

### Example 1 — Single solution, unambiguous match (3 tool calls)

User: "Add a Sort Lines item to the Format menu"

**Step 1 (parallel):**
- List: `ls "agent/xml_parsed/custom_menus/"*/ "agent/xml_parsed/custom_menu_sets/"*/ 2>/dev/null` -- shows files under `Invoice Solution/` only
- Sandbox: `ls agent/sandbox/` -- no existing menu XML

**Step 2:**
- Match: "agentic-fm -- Format - ID 40.xml" matches "Format" (contains match, high confidence)
- Read: `agent/xml_parsed/custom_menus/Invoice Solution/agentic-fm — Format - ID 40.xml` -- extract UUIDs

**Step 3:** Report + confirm -- "Is this the correct menu? -- agentic-fm -- Format (ID: 40) in Invoice Solution"

On confirmation: add the new `<CustomMenuItem>` block, write to clipboard.

**Tool calls: 3** (2 parallel discover + 1 read + confirm in same response)

### Example 2 — Multiple solutions present (4 tool calls)

User: "Look up the Format menu"

**Step 1 (parallel):**
- List: shows files under both `Invoice Solution/` and `agentic-fm/`
- Sandbox: no match

**Step 1.5:** `AskUserQuestion`: "Multiple solution files found: Invoice Solution, agentic-fm -- which are you working with?"

**Step 2:** User selects -- read the matched file, extract UUIDs.

**Step 3:** Report + confirm.

**Tool calls: 4** (2 parallel + 1 ask + 1 read)

### Example 3 — Ambiguous menu name (4 tool calls)

User: "Open the Format menu"

**Step 1 (parallel):**
- List: shows "agentic-fm -- Format - ID 40.xml", "Format 2 - ID 34.xml", "Format 3 - ID 37.xml", etc. in one solution
- Sandbox: no match

**Step 1.5:** `AskUserQuestion`: "Multiple Format menus found -- which one? agentic-fm -- Format (ID 40) / Format 2 (ID 34) / Format 3 (ID 37)"

**Step 2:** User selects -- read file, extract UUIDs.

**Step 3:** Report + confirm.

**Tool calls: 4** (2 parallel + 1 ask + 1 read)

### Example 4 — New menu with no existing XML (2 tool calls)

User: "Create a View menu"

**Step 1 (parallel):**
- List: no View menu found in any solution subfolder
- Sandbox: no match

**Step 2:** Report that the menu hasn't been exported yet. Instruct: create the empty menu in FileMaker, copy it, then run `clipboard.py read` to capture the real UUIDs before generation begins.

**Tool calls: 2** (2 parallel discover -- done)
