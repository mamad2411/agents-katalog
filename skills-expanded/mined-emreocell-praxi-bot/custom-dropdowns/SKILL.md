---
name: custom-dropdowns
description: Operate non-native dropdowns, comboboxes and autocomplete lists built from divs.
version: 0.1.0
when:
  keywords: [dropdown, select, combobox, autocomplete, listbox, choose option]
---
# Custom dropdowns

Native select element: use `browser_select` with the option text or value.

Custom (div/ul based) dropdowns:
1. Click the control with `browser_click` to open it.
2. Run `browser_snapshot` again; options usually appear as `option` or `listitem` entries, often at the end of the page (rendered in a portal).
3. If the list is long, type to filter first (`browser_fill` on the combobox input) and then re-snapshot.
4. Click the option by its ref. If it is off-screen, `browser_scroll` inside the list.
5. Verify: the control now shows the chosen text. Some widgets only commit on blur, so press Tab with `browser_press` if the value reverts.

Keyboard fallback: focus the control, press ArrowDown to open or move, Enter to choose, Escape to cancel.

Autocomplete inputs need a short wait (`browser_wait`) for suggestions after typing.
