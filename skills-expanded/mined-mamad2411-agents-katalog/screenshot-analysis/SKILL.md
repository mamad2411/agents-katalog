---
name: screenshot-analysis
description: How to interpret accessibility tree elements and correlate them with screenshot regions for accurate GUI interaction.
---

# Screenshot & Accessibility Tree Analysis

## Reading the Accessibility Tree
The a11y_tree is your primary guide for finding interactive elements:
```
[role=window] "Document - LibreOffice Calc"
  [role=menubar]
    [role=menuitem] "File"
    [role=menuitem] "Edit"
  [role=toolbar]
    [role=button] "Save" (x=120, y=45)
  [role=table] "Sheet"
    [role=cell] "A1" (x=80, y=200)
```

## Coordinate mapping
- a11y_tree provides (x, y) center coordinates for each element
- Use these for pyautogui.click(x, y)
- If coordinates seem wrong, the element may be scrolled off-screen

## Element roles cheat sheet
- `button`: clickable action (Save, OK, Cancel)
- `menuitem`: menu entry (click to open submenu or execute)
- `textbox`/`text`: editable text field (click then type)
- `combobox`: dropdown (click to open, then select)
- `checkbox`: toggle (click to check/uncheck)
- `cell`: spreadsheet cell (click to select, then type)
- `tab`: tab selector (click to switch)
- `dialog`: modal window (must handle before other actions)

## When a11y_tree is insufficient
- Some custom widgets don't expose a11y info — use screenshot + coordinates
- For canvas-based apps (GIMP): rely on menu navigation, not direct canvas clicks
- For web content in Chrome: a11y_tree reflects DOM, usually reliable

## Tips
- Always check a11y_tree AFTER an action to verify the state changed
- If an element disappears from a11y_tree, the UI updated (menu closed, dialog dismissed)
- Count elements to verify you're clicking the right one (e.g., 3rd button in toolbar)
