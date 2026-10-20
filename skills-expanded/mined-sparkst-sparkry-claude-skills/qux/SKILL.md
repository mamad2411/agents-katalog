---
name: QUX - UX Test Scenarios
description: Generate comprehensive UX test scenarios for UI components including happy paths, edge cases, error states, and accessibility checks
version: 1.0.0
agents: [ux-tester]
tools: []
references: [wcag-checklist.md, aria-patterns.md]
claude_tools: Read, Grep, Glob, Write
trigger: QUX
---

# QUX Skill

## Purpose

Generate comprehensive UX test scenarios for UI components to ensure:
- All user flows are tested (happy path, edge cases, error states)
- Accessibility compliance (WCAG 2.1 Level AA)
- Cross-browser and cross-device compatibility
- Keyboard and screen reader support

**When to use**: After implementing or modifying UI components, before writing automated tests

---

## Workflow

### Phase 1: Discovery

**Agent**: ux-tester

**Actions**:
1. Analyze UI component files to understand structure
2. Identify user interactions (clicks, inputs, navigation)
3. Map visual states (loading, error, success, empty)
4. Review existing tests for gaps

**Tools**: Read, Grep, Glob

**Output**: Component analysis

---

### Phase 2: Scenario Generation

**Agent**: ux-tester

**Actions**:
1. Generate happy path scenarios (expected user flows)
2. Generate edge case scenarios (boundary conditions)
3. Generate error state scenarios (validation, network, permissions)
4. Generate accessibility scenarios (keyboard, screen reader, contrast)

**Output**: Test scenario matrix

---

### Phase 3: Accessibility Check

**Agent**: ux-tester

**Actions**:
1. Check WCAG 2.1 compliance (Level A and AA)
2. Verify keyboard navigation patterns
3. Validate ARIA usage
4. Check color contrast ratios

**Tools**: Read (load references/wcag-checklist.md, references/aria-patterns.md)

**Output**: Accessibility findings

---

### Phase 4: Documentation

**Agent**: ux-tester

**Actions**:
1. Document all scenarios in structured markdown
2. Create test matrix (priority, browser, device, assistive tech)
3. Add implementation notes (tools, test data, environment)

**Output Location**: `docs/tasks/<task-id>/ux-test-scenarios.md` or `docs/ux-scenarios/<component-name>.md`

---

## Input

**From User**:
- Component path (optional): `QUX src/components/LoginForm.tsx`
- Task ID (optional): `QUX --task=TASK-123`

**From Environment**:
- Git diff (to find recently modified UI components)
- Existing test files (to identify gaps)
- CLAUDE.md (for project-specific testing standards)

---

## Output

### Test Scenario Document

```markdown
# UX Test Scenarios: [Component Name]

## Component Overview
- **File**: [path]
- **Purpose**: [description]
- **Key Interactions**: [list]

## Happy Path Scenarios
[scenarios with Given/When/Then/Verification]

## Edge Case Scenarios
[boundary conditions, timing issues, browser variations]

## Error State Scenarios
[validation errors, network failures, permission errors]

## Accessibility Scenarios
[keyboard nav, screen reader, color contrast]

## Test Matrix
[priority, browser, device, assistive tech table]

## Implementation Notes
[tools, test data, environment setup]
```

**File**: `docs/tasks/<task-id>/ux-test-scenarios.md`

---

## Configuration

### Default Settings

- **WCAG Level**: AA (can be overridden with `--wcag-level=AAA`)
- **Browser Coverage**: Chrome, Safari, Firefox (can customize with `--browsers`)
- **Device Coverage**: Desktop, Mobile (iOS, Android)
- **Assistive Tech**: Keyboard, NVDA/JAWS, VoiceOver

### Custom Configuration

Create `.qux.json` in project root:

```json
{
  "wcag_level": "AAA",
  "browsers": ["chrome", "safari", "firefox", "edge"],
  "devices": ["desktop", "tablet", "mobile"],
  "assistive_tech": ["keyboard", "nvda", "jaws", "voiceover"],
  "output_dir": "docs/ux-scenarios",
  "include_patterns": ["src/components/**/*.tsx", "src/pages/**/*.tsx"],
  "exclude_patterns": ["**/*.spec.tsx", "**/*.test.tsx"]
}
```

---

## Examples

### Example 1: Single Component

**Command**:
```
QUX src/components/auth/LoginForm.tsx
```

**Output**: `docs/ux-scenarios/LoginForm.md` with:
- 10-15 test scenarios
- Accessibility checks
- Test matrix
- Implementation notes

**Estimated Effort**: 0.2 SP

---

### Example 2: All Modified Components

**Command**:
```
QUX
```

**Output**: Analyzes `git diff` to find modified UI components, generates scenarios for each

**Estimated Effort**: 0.3-0.5 SP (depends on number of components)

---

### Example 3: Full Accessibility Audit

**Command**:
```
QUX --wcag-level=AAA --focus=accessibility
```

**Output**: Deep accessibility audit with:
- WCAG AAA compliance checks
- Detailed ARIA validation
- Color contrast analysis
- Focus management review

**Estimated Effort**: 0.5-0.8 SP

---

## Integration with Other QShortcuts

### With QCODET (Test-Driven Development)

```bash
# 1. Implement UI component
QCODE src/components/Dashboard.tsx

# 2. Generate UX test scenarios
QUX src/components/Dashboard.tsx

# 3. Implement automated tests based on scenarios
QCODET --from-ux-scenarios

# 4. Verify tests fail (TDD)
npm test

# 5. Fix implementation to pass tests
QCODE

# 6. Commit
QGIT
```

---

### With QCHECK (Code Review)

```bash
# 1. Implement feature
QCODE

# 2. Generate UX scenarios
QUX

# 3. Code review
QCHECK

# 4. Verify UX scenarios are testable
@pe-reviewer Review UX test scenarios for completeness
```

---

## Quality Checklist

Before marking QUX complete, verify:

- [ ] All user interactions have test scenarios
- [ ] Edge cases are covered (boundary values, timing, browser variations)
- [ ] Error states have recovery paths documented
- [ ] Keyboard navigation scenarios are complete
- [ ] Screen reader scenarios are included
- [ ] Color contrast is checked
- [ ] Test matrix includes priority levels
- [ ] Implementation notes specify tools and test data

---

## Common Patterns

### Pattern: Form Testing

**Components**: Login forms, registration, search, contact forms

**Scenarios**:
- Valid input submission
- Field validation (required, format, length)
- Error display and recovery
- Submit button debounce
- Keyboard submission (Enter key)
- Screen reader announcements for errors
- Autofill compatibility

---

### Pattern: Modal/Dialog Testing

**Components**: Modals, dialogs, popovers

**Scenarios**:
- Open/close interactions
- Focus management (trap focus, return focus on close)
- Escape key to close
- Click outside to close (optional)
- Scroll locking (prevent body scroll)
- Screen reader announcements (role="dialog", aria-modal)
- Keyboard navigation within modal

---

### Pattern: List/Table Testing

**Components**: Data tables, lists, grids

**Scenarios**:
- Empty state
- Loading state
- Error state (failed to load)
- Pagination/infinite scroll
- Sort/filter interactions
- Row selection (single, multiple)
- Keyboard navigation (arrow keys, Home/End)
- Screen reader table semantics

---

### Pattern: Navigation Testing

**Components**: Headers, sidebars, breadcrumbs, tabs

**Scenarios**:
- Active state indication
- Keyboard navigation (Tab, arrow keys)
- Skip links (bypass navigation)
- Breadcrumb hierarchy
- Mobile menu (hamburger, drawer)
- Focus management on route change
- ARIA landmarks (navigation, main, complementary)

---

## Anti-Patterns to Avoid

❌ **Too Generic**: "Test that the button works"
✅ **Specific**: "Given user is on login page, when user clicks 'Log In' with valid credentials, then user is redirected to dashboard within 2 seconds"

❌ **No Accessibility**: Only happy path scenarios
✅ **Inclusive**: Include keyboard, screen reader, and contrast scenarios

❌ **No Error Handling**: Only test success cases
✅ **Resilient**: Test validation errors, network failures, permission errors

❌ **No Browser/Device Variation**: Assume all browsers behave the same
✅ **Compatible**: Test across Chrome, Safari, Firefox, mobile browsers

❌ **No Priority Levels**: All scenarios are equally important
✅ **Prioritized**: P0 for critical flows, P1 for common, P2 for edge cases, P3 for nice-to-haves

---

## Troubleshooting

### Issue: No UI Components Found

**Problem**: QUX reports "No UI components found in git diff"

**Solution**: Specify component path explicitly
```bash
QUX src/components/MyComponent.tsx
```

---

### Issue: Too Many Scenarios Generated

**Problem**: QUX generates 50+ scenarios, overwhelming

**Solution**: Focus on critical paths
```bash
QUX --priority=P0,P1  # Only generate high-priority scenarios
```

---

### Issue: Accessibility Checks Too Strict

**Problem**: WCAG AAA requirements are too stringent for current project

**Solution**: Lower WCAG level to AA
```bash
QUX --wcag-level=AA
```

Or configure in `.qux.json`:
```json
{
  "wcag_level": "AA"
}
```

---

## Story Point Estimation

| Complexity | Component Type | Scenarios | Effort (SP) |
|------------|----------------|-----------|-------------|
| Simple | Button, Link, Icon | 3-5 | 0.05-0.1 |
| Moderate | Form, Card, Modal | 10-15 | 0.2-0.3 |
| Complex | Table, Multi-step Wizard, Dashboard | 20-30 | 0.5-0.8 |

**Baseline**: 1 SP = Full app accessibility audit with 50+ scenarios

---

## References

See `references/` directory:
- `wcag-checklist.md` - WCAG 2.1 quick reference
- `aria-patterns.md` - Common ARIA patterns and examples

---

## Contributing

For issues or enhancements to QUX skill:
- **Email**: skills@sparkry.ai
- **License**: MIT
