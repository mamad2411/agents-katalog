---
name: rgaa-scripts
description: "Audit a web page for RGAA v4.1.2 Theme 7 – Scripts accessibility compliance. Checks that JavaScript components are compatible with assistive technologies (proper ARIA roles/states/properties), alternatives exist when needed, all interactions are keyboard- and pointer-accessible, context changes inform the user, and status messages use ARIA live regions. Use this skill when someone asks to check JavaScript/script accessibility, verify RGAA Theme 7, audit interactive components, or check ARIA usage on a website."
---

# RGAA Scripts Accessibility Audit (Theme 7)

Audits a web page against the 5 criteria of RGAA v4.1.2 Theme 7: Scripts.

## Audit procedure

### Step 1: Gather interactive component data

```javascript
(() => {
  const components = [];

  // ARIA widgets
  const ariaRoles = ['button','tab','tabpanel','tablist','dialog','alertdialog','menu',
    'menuitem','menubar','listbox','option','combobox','slider','spinbutton',
    'progressbar','tooltip','tree','treeitem','grid','gridcell','switch',
    'checkbox','radio','radiogroup','accordion','alert','status','log','marquee','timer'];

  ariaRoles.forEach(role => {
    document.querySelectorAll(`[role="${role}"]`).forEach(el => {
      components.push({
        tag: el.tagName.toLowerCase(),
        role: role,
        ariaLabel: el.getAttribute('aria-label'),
        ariaLabelledby: el.getAttribute('aria-labelledby'),
        ariaDescribedby: el.getAttribute('aria-describedby'),
        ariaExpanded: el.getAttribute('aria-expanded'),
        ariaSelected: el.getAttribute('aria-selected'),
        ariaChecked: el.getAttribute('aria-checked'),
        ariaHidden: el.getAttribute('aria-hidden'),
        ariaLive: el.getAttribute('aria-live'),
        ariaDisabled: el.getAttribute('aria-disabled'),
        tabindex: el.getAttribute('tabindex'),
        hasOnclick: !!el.getAttribute('onclick') || el.tagName === 'DIV' || el.tagName === 'SPAN',
        text: el.textContent.trim().substring(0, 60)
      });
    });
  });

  // Clickable non-interactive elements (potential issues)
  const clickables = [];
  document.querySelectorAll('div[onclick], span[onclick], div[tabindex], span[tabindex]').forEach(el => {
    if (!el.getAttribute('role')) {
      clickables.push({
        tag: el.tagName.toLowerCase(),
        tabindex: el.getAttribute('tabindex'),
        role: el.getAttribute('role'),
        text: el.textContent.trim().substring(0, 60),
        hasKeyHandler: !!(el.getAttribute('onkeydown') || el.getAttribute('onkeypress') || el.getAttribute('onkeyup'))
      });
    }
  });

  // Live regions
  const liveRegions = [];
  document.querySelectorAll('[aria-live], [role="alert"], [role="status"], [role="log"], [role="marquee"], [role="timer"]').forEach(el => {
    liveRegions.push({
      tag: el.tagName.toLowerCase(),
      role: el.getAttribute('role'),
      ariaLive: el.getAttribute('aria-live'),
      ariaAtomic: el.getAttribute('aria-atomic'),
      ariaRelevant: el.getAttribute('aria-relevant'),
      text: el.textContent.trim().substring(0, 80)
    });
  });

  return JSON.stringify({
    ariaComponents: components.slice(0, 40),
    clickableNonInteractive: clickables.slice(0, 20),
    liveRegions: liveRegions
  }, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 7.1** – Scripts are compatible with assistive technologies.

For each script-driven component, check:
- It has a proper ARIA role (or uses a native HTML element)
- It has an accessible name (aria-label, aria-labelledby, or visible text)
- Its states are communicated (aria-expanded, aria-selected, aria-checked, etc.)
- State changes are reflected in the DOM (not just visual changes)
- Non-interactive elements (`div`, `span`) used as buttons/links have appropriate `role` and keyboard support

**Criterion 7.2** – Script alternatives are relevant.
If a script component has a fallback (noscript content), verify it provides equivalent functionality.

**Criterion 7.3** – Scripts are keyboard- and pointer-controllable.
- Every interaction possible with a mouse must also work with keyboard
- No keyboard trap (user can always tab away)
- Click handlers on non-interactive elements need corresponding keydown/keypress handlers
- Touch-only gestures need an alternative

Test by tabbing through the page and verifying all interactive elements receive focus and can be activated.

**Criterion 7.4** – Context changes initiated by scripts inform the user.
- If a script changes page content (e.g., auto-updating region, dynamic content load), the user must be informed
- Form auto-submission on selection change needs prior warning
- New windows opened by scripts need indication

**Criterion 7.5** – Status messages use ARIA live regions.
Status messages (form validation, loading indicators, search results count, cart updates) must be announced without moving focus. Check for:
- `role="status"` or `aria-live="polite"` for non-urgent updates
- `role="alert"` or `aria-live="assertive"` for important/urgent messages
- Messages dynamically injected into the DOM must be inside a live region that existed before the content was added

### Step 3: Keyboard testing

Use the browser to tab through the page:
1. Verify all interactive components receive visible focus
2. Verify they can be activated (Enter/Space for buttons, arrows for tabs/menus)
3. Verify there are no keyboard traps
4. Verify custom widgets follow WAI-ARIA Authoring Practices keyboard patterns

### Step 4: Generate report

For each interactive component, list its role, accessible name, state management, and keyboard accessibility. Flag missing ARIA attributes, keyboard traps, and absent live regions.

WCAG references: 9.2.1.1 (A), 9.2.1.2 (A), 9.3.2.1 (A), 9.4.1.2 (A), 9.4.1.3 (AA)
