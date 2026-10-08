<!-- llm-process-gen: managed source=gemini_visual_test_skill source_sha256=6ae7b44e401ad75c3d54c566c944f87fa78797dd693dfd8f7b7a6d4457c62c13 content_sha256=f7ca124dce204caaec5677b0702de4a022dd1f046abf4197d142bd4bbea53541 -->
# visual_test

Source: `.gemini/commands/visual_test.toml`

Visual regression testing — screenshot comparison, layout validation, responsive checks, accessibility."

un visual regression testing for the given UI feature or component. Requires Chrome MCP.

Phase 1: Baseline Capture
- Launch the UI (TUI via terminal capture, GUI via Chrome MCP)
- Capture screenshots at key breakpoints: 320px, 768px, 1024px, 1440px (GUI)
- Capture terminal output at 80x24, 120x40 column sizes (TUI)
- Store baselines in test/visual/<feature>/baseline/

Phase 2: Current State Capture
- Capture current state with same parameters as baseline
- Store in test/visual/<feature>/current/

Phase 3: Comparison
- Diff baseline vs current screenshots
- Report pixel differences, layout shifts, color changes
- Flag regressions with severity: [CRITICAL] layout break, [WARN] minor shift, [INFO] cosmetic

Phase 4: Layout Validation
- Verify element alignment, spacing consistency
- Check overflow/clipping at each breakpoint
- Validate text truncation behavior
- Confirm scrollbar presence where expected

Phase 5: Responsive Breakpoint Testing (GUI only)
- Verify layout transitions between breakpoints
- Check element reflow, stacking order changes
- Validate touch target sizes (min 44x44px) on mobile breakpoints

Phase 6: Accessibility Checks
- Color contrast ratio (WCAG AA: 4.5:1 text, 3:1 large text)
- Focus indicator visibility
- Screen reader landmark structure
- Keyboard-only navigation completeness

Report: test/visual/<feature>/report.md
- Summary table: [PASS], [FAIL], [WARN] per check
- Inline diff images where applicable
- Recommended fixes for failures