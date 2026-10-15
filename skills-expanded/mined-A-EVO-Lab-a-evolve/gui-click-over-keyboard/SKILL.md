---
name: gui-click-over-keyboard
description: When to prefer GUI mouse clicks over keyboard shortcuts — especially for formatting, multi-step visual tasks, and cross-application workflows.
---

# Prefer GUI Clicks for Visual & Formatting Tasks

Keyboard shortcuts are fast for simple operations, but many desktop tasks **require direct GUI interaction** via mouse clicks. Defaulting to keyboard-only approaches is a common failure mode.

## Always use GUI clicks for:

### 1. LibreOffice Impress formatting
- Font color, size, bold/underline: select text by clicking/dragging, then click toolbar buttons or use Format > Character menu
- Slide background color: right-click slide > Slide Properties > Background tab > pick color from the color chooser
- Object alignment/positioning: click the object to select, then drag or use Position and Size dialog (F4)
- Multi-slide operations: click each slide in the panel, apply changes per-slide — no reliable keyboard-only path

### 2. Cross-application (multi_apps) workflows
- Switch windows by clicking taskbar icons — Alt+Tab ordering is unreliable
- Copy-paste across apps requires clicking into the target window and field first
- File browser dialogs: click through the folder tree or type the path in the location bar
- When coordinating data between Calc/Writer/Impress/Chrome: click into each app, visually confirm the data, then proceed

### 3. GIMP canvas operations
- Layer selection: click the layer in the Layers panel — keyboard shortcuts only cycle layers
- Color picking and area selection: must click on canvas coordinates
- Tool options (brush size, opacity): click the sliders or input fields in the tool options panel

### 4. Color and style pickers
- Color choosers in any app require clicking the color grid or entering hex values in a text field
- Style dropdowns (font family, paragraph style): click the dropdown arrow, then click the option
- These UI elements have no keyboard-only alternative

## When keyboard shortcuts ARE appropriate:
- Ctrl+S to save, Ctrl+Z to undo, Ctrl+C/V to copy/paste
- Ctrl+A to select all content
- Typing text into an already-focused text field
- Opening known menus (Alt+F for File menu) as a starting point, then clicking menu items
- Terminal/command-line tasks (os domain)

## Rule of thumb
If the task involves **visual properties** (color, position, size, alignment) or **multiple applications**, plan for heavy GUI clicking. Count your clicks — if your plan has fewer than 5 clicks for a formatting task, you are probably missing steps.
