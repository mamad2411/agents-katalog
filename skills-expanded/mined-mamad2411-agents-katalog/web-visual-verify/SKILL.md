---
name: web-visual-verify
description: Workflow for developing web-based visual content and verifying the rendered output using Browser and Vision AI tools.
---

# Web Visual Verification Workflow

This skill provides a workflow for developing web-based visual content (CSS, Three.js, Canvas, etc.) and verifying the rendered output using Browser and Vision AI tools. Use this when a user requests visual confirmation, aesthetic checks, or "visual verification" of a web project.

## Trigger
- When the user asks to "verify the look", "check if the UI is correct", or "ensure the aesthetic meets [X] description".
- When a user asks to "record/provide visual proof" of a web application.

## Workflow

1. **Development**: Write/update the necessary web files (HTML, CSS, JS) using `write_file` or `patch`.
2. **Local Hosting**: Start a local development server in the background to serve the files.
   - Command: `python3 -m http.server <port>`
   - Use `terminal(background=true)` to ensure the process remains running and accessible.
   - *Note:* If files are changed significantly, you may need to restart the server or ensure it's serving the latest edits.
3. **Navigation**: Use `browser_navigate` to go to the local address (e.g., `http://localhost:8000/index.html`).
4. **Visual Inspection**:
   - Use `browser_snapshot` to check for the presence of DOM elements (text, buttons, containers).
   - Use `browser_vision` to perform a high-level aesthetic analysis. 
   - **Critical Step**: Provide the Vision AI with specific criteria (e.g., "Check if the neon pink glow is present" or "Verify the score text is visible at the top").
5. **Iteration**:
   - If the Vision AI reports a discrepancy between the code logic and the visual reality, use `patch` or `write_file` to fix the issue and repeat from Step 3.
6. **Mandatory final end-to-end visual sweep**:
   - Treat unit tests, DOM snapshots, and a successful build as necessary but insufficient. The work is not visually verified until the final rendered application has been exercised.
   - Start from the real application entry point and traverse every primary destination at the target viewport and theme.
   - On each page, use the current snapshot to inventory every visible button, tab, menu item, card action, and link that opens a subpage, dialog, drawer, popover, expanded state, or alternate view. Click each one; do not infer child-state quality from the parent page.
   - After every navigation or significant interaction, capture a fresh screenshot and inspect the actual pixels for hierarchy, clipping, overflow, overlap, spacing, icon consistency, empty/loading/error states, and fixed-navigation obstruction. Also check the console.
   - Scroll through long states and inspect below-the-fold content. Close or back out, then continue until the interaction inventory is exhausted.
   - Re-capture any affected page after fixes. Finish with a screenshot set or contact sheet covering all pages and opened child states, and state explicitly what was and was not inspected.

## Testing Philosophy

**Rendered reality is the final authority.** Source review, automated assertions, and accessibility snapshots can prove structure, but they cannot prove that the complete interface looks correct. Final acceptance requires an end-to-end visual inspection of every reachable page and every child state opened by user-facing controls, using direct screenshots of the rendered result.

## Pitfalls
- **Server not running**: Always verify the server is alive before navigating.
- **Port conflicts**: If a server is already running on a port, choose a different one or `kill` the existing process using `process(action="kill")`.
- **Caching**: Browsers sometimes cache old versions of files. If changes aren't appearing, you may need to restart the background server process.
- **Interpreting "Video" requests**: On CLI, "recording a video" is often better handled by using `browser_vision` to provide a descriptive "snapshot" of the current state, as direct video file generation is not typically available via tool outputs.
