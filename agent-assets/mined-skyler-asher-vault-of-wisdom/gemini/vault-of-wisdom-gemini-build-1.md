# Project Instructions: Personal Day Planner

This document provides foundational mandates and architectural guidance for the Personal Day Planner project. Adhere to these standards for all modifications and extensions.

## Core Philosophy
- **No-Framework Architecture:** Do not introduce frontend frameworks (React, Vue, etc.), package managers (npm), or build steps. Keep logic in vanilla JavaScript and styles in standard CSS.
- **Self-Hostable & Portable:** The project is designed to run locally via a Python server. Maintain this simplicity to ensure ease of deployment and data portability.

## Project Structure
- `index.html`: The primary day planner and entry point.
- `bank.html`: The "Task Bank" library for reusable tasks.
- `core.js`: Centralized shared logic, constants (COLORS, KEYS, ICON_LABELS), and utility functions.
- `storage.js`: Drop-in async persistence shim that routes data to the local server.
- `shared.css`: Global design tokens, layout variables, CSS custom properties, and bottom navigation styles.
- `planner.css`: Style overrides and layouts specific to the Day page (`index.html`).
- `bank.css`: Style overrides and layout specific to the Tasks page (`bank.html`).
- `server.py`: The local backend handling flat-file JSON data storage.
- `data.json`: The flat-file JSON database containing user settings, custom sections, and tasks.
- `start.bat`: Windows batch script launcher that starts the backend and opens the app in the browser.
- `PreviewUI.html`: Interactive mockup file demonstrating the Ethereal Note Popup system.
- `icons/`: Directory hosting local Tabler Icons assets.
- `icons_structure.txt`: Directory layout of the local icons folder.
- `AI_PROJECT_NOTES.txt`: The human-readable project history and handoff note.

## Persistence Patterns
- **Do Not Use localStorage:** All persistent state must be handled through `window.store` in `storage.js`.
- **Async Operations:** All storage calls (`get`, `set`, `remove`) are asynchronous. Always use `await` when performing operations that depend on saved state.
- **Data Keys:**
    - `monday_schedule_v2`: Boolean "checked" states.
    - `day_order_v1`: Structural order of sections and tasks.
    - `day_sections_v1`: Custom section labels.
    - `task_bank_v1`: Reusable task library.
    - `day_custom_tasks_v1`: Tasks imported from the bank.

## Coding Standards
- **Inline Logic:** JavaScript for page-specific UI interactions should remain inline within the HTML files unless the logic becomes globally reusable.
- **CSS Variables:** Use the established CSS variables in `:root` for colors, spacing, and radius to maintain visual consistency.
- **Encoding Safety:** Be extremely careful when editing text to avoid corrupting existing special characters or emojis. Always save files with UTF-8 encoding.

## Documentation Mandate
- **Update AI_PROJECT_NOTES.txt:** After every significant change or audit, add a new entry to the `Change Log` in `AI_PROJECT_NOTES.txt`. Include the date, files changed, behavior changed, and checks performed.
