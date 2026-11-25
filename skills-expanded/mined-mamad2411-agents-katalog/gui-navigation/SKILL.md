---
name: gui-navigation
description: General GUI navigation patterns for desktop environments — finding elements, interacting with menus, and handling dialogs.
---

# GUI Navigation Patterns

## Finding UI elements
- Read the accessibility tree (a11y_tree) first — it lists all interactive elements with roles and labels
- Match elements by role (button, menuitem, textbox) + name/label text
- If a11y_tree is ambiguous, use screenshot coordinates as fallback

## Menu navigation
- Most apps: click menu bar item → submenu appears → click target
- LibreOffice: Menu bar is always at top (File, Edit, View, Insert, Format, ...)
- GIMP: Right-click canvas for context menu; Filters/Colors/Tools in menu bar
- Chrome: Three-dot menu (top-right) for settings, extensions, history

## Dialog handling
- File dialogs: type path directly in the filename field instead of navigating folders
- Confirmation dialogs: look for OK/Save/Yes buttons — don't dismiss with Escape unless intentional
- If dialog blocks interaction, it must be handled before continuing

## Window management
- Alt+Tab: switch between windows
- Alt+F4: close current window
- If app is behind another window, click its taskbar icon

## Scrolling
- pyautogui.scroll(-3) to scroll down, scroll(3) to scroll up
- Some elements need to be scrolled into view before clicking
- For long lists: scroll incrementally and re-check a11y_tree each time

## Common pitfalls
- Clicking coordinates from a11y_tree that are offscreen — scroll first
- Double-clicking when single-click is needed (or vice versa)
- Not waiting for UI to update after an action — use time.sleep(1-2)
