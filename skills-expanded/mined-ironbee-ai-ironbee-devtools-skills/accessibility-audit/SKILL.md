---
name: accessibility-audit
description: Audit web accessibility using ARIA snapshots, AX tree analysis, and WCAG validation. Use when the user asks about accessibility, a11y, WCAG compliance, screen reader compatibility, ARIA roles, or keyboard navigation.
allowed-tools: Bash(ironbee-browser-devtools-cli:*)
---

# Accessibility Audit Skill

Audit web accessibility using ARIA snapshots, AX tree analysis, and WCAG validation.

## When to Use

This skill activates when:
- User asks about accessibility or a11y
- User mentions WCAG compliance
- User wants to check screen reader compatibility
- User needs to audit ARIA roles and labels
- User asks about keyboard navigation

## Capabilities

### ARIA Snapshots
```bash
ironbee-browser-devtools-cli a11y take-aria-snapshot
ironbee-browser-devtools-cli a11y take-aria-snapshot --selector ".main-content"
```

### AX Tree Analysis
```bash
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot --roles button,link,textbox
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot --check-occlusion
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot --only-visible
```

### Keyboard Navigation Testing
```bash
ironbee-browser-devtools-cli interaction press-key --key "Tab"
ironbee-browser-devtools-cli interaction press-key --key "Tab" --selector "body"
ironbee-browser-devtools-cli interaction press-key --key "Enter"
ironbee-browser-devtools-cli interaction press-key --key "Escape"
```

## WCAG Checklist

### Perceivable
- [ ] Images have alt text
- [ ] Videos have captions
- [ ] Color is not the only indicator
- [ ] Text has sufficient contrast

### Operable
- [ ] All functionality via keyboard
- [ ] No keyboard traps
- [ ] Skip links present
- [ ] Focus visible

### Understandable
- [ ] Language specified
- [ ] Labels on form inputs
- [ ] Error messages clear
- [ ] Consistent navigation

### Robust
- [ ] Valid HTML
- [ ] ARIA used correctly
- [ ] Works with assistive tech

## Audit Workflow

```bash
SESSION="--session-id a11y-audit"

# 1. Navigate to page
ironbee-browser-devtools-cli $SESSION navigation go-to --url "https://example.com"
ironbee-browser-devtools-cli $SESSION sync wait-for-network-idle

# 2. Get ARIA snapshot (quick overview, returns refs e1,e2,...)
ironbee-browser-devtools-cli $SESSION a11y take-aria-snapshot

# Optional: include custom clickable elements (div/span with cursor:pointer)
ironbee-browser-devtools-cli $SESSION a11y take-aria-snapshot --cursor-interactive

# 3. Get detailed AX tree
ironbee-browser-devtools-cli $SESSION --json a11y take-ax-tree-snapshot \
  --roles button,link,textbox,checkbox,radio,combobox

# 4. Check for interactive elements with occlusion
ironbee-browser-devtools-cli $SESSION --json a11y take-ax-tree-snapshot \
  --roles button,link \
  --check-occlusion

# 5. Test keyboard navigation
ironbee-browser-devtools-cli $SESSION interaction press-key --key "Tab"
ironbee-browser-devtools-cli $SESSION content take-screenshot --name "first-focus"

# 6. Cleanup
ironbee-browser-devtools-cli session delete a11y-audit
```

## Common Issues

### Missing Alt Text
```bash
# Check images in AX tree
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot --roles image
```

### Missing Form Labels
```bash
# Check form elements
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot --roles textbox,checkbox,radio,combobox
```

### Empty Buttons/Links
```bash
# Check for buttons and links with no accessible name
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot --roles button,link
```

### Hidden but Focusable Elements
```bash
# Check for visibility issues
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot --check-occlusion
```

## Specific Audits

### Heading Hierarchy
```bash
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot --roles heading
```

### Form Accessibility
```bash
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot \
  --roles textbox,checkbox,radio,combobox,button
```

### Navigation Elements
```bash
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot \
  --roles navigation,link,menu,menuitem
```

### Interactive Elements
```bash
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot \
  --roles button,link,tab,switch,slider
```

## Best Practices

1. **Always use ARIA snapshot first** for quick overview
2. **Use AX tree with occlusion check** for layout issues
3. **Filter by roles** to focus on interactive elements
4. **Check both visible and hidden elements**
5. **Test with keyboard only** before reporting
6. **Take screenshots** to document focus states
7. **Test at different viewport sizes** for responsive a11y
