---
name: accessibility-testing
description: Test web applications for WCAG 2.1 AA accessibility compliance using automated scanning, screen reader testing, and keyboard navigation validation. Outputs axe-core integration, Playwright accessibility tests, and remediation guides.
argument-hint: [compliance target (WCAG AA/AAA), application type, user base, existing test framework]
allowed-tools: Read, Write, Bash
---

# Accessibility Testing

Accessibility testing ensures your application is usable by people with disabilities — including those using screen readers, keyboard navigation, voice input, or high-contrast modes. WCAG 2.1 AA is the legal minimum in most jurisdictions and the ethical baseline for any public-facing product.

## Process

1. **Automated scan first** — axe-core catches 30-40% of accessibility issues automatically.
2. **Keyboard navigation testing** — Tab through every interactive element, verify focus visibility and order.
3. **Screen reader testing** — use NVDA+Firefox (Windows), VoiceOver+Safari (Mac/iOS), TalkBack (Android).
4. **Color contrast check** — minimum 4.5:1 for normal text, 3:1 for large text.
5. **Manual WCAG checklist** — cover areas automated tools miss (semantic HTML, alt text quality).
6. **Integrate into CI** — fail builds on critical automated violations.
7. **Remediation and retest** — fix issues by WCAG criterion, retest with tools + manual.

## Output Format

### Automated Testing with axe-core + Playwright

```typescript
// tests/accessibility/axe.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility - Core Pages', () => {
  test('homepage passes WCAG 2.1 AA', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();
    
    // Attach results to report for visibility
    await test.info().attach('axe-results', {
      body: JSON.stringify(results, null, 2),
      contentType: 'application/json',
    });
    
    expect(results.violations).toEqual([]);
  });
  
  test('product listing page', async ({ page }) => {
    await page.goto('/products');
    
    // Exclude third-party widgets with known issues
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .exclude('#third-party-chat-widget')
      .analyze();
    
    // Fail only on critical/serious violations
    const blocking = results.violations.filter(v =>
      ['critical', 'serious'].includes(v.impact!)
    );
    
    if (blocking.length > 0) {
      console.log('Accessibility violations:');
      blocking.forEach(v => {
        console.log(`  [${v.impact}] ${v.id}: ${v.description}`);
        v.nodes.forEach(n => console.log(`    ${n.html}`));
      });
    }
    
    expect(blocking, `${blocking.length} critical/serious violations found`).toHaveLength(0);
  });
  
  test('checkout flow - all steps', async ({ page }) => {
    const checkoutSteps = [
      { url: '/cart', name: 'cart' },
      { url: '/checkout/shipping', name: 'shipping' },
      { url: '/checkout/payment', name: 'payment' },
    ];
    
    const allViolations = [];
    
    for (const step of checkoutSteps) {
      await page.goto(step.url);
      await page.waitForLoadState('networkidle');
      
      const results = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
        .analyze();
      
      if (results.violations.length > 0) {
        allViolations.push({
          page: step.name,
          violations: results.violations,
        });
      }
    }
    
    expect(allViolations, JSON.stringify(allViolations, null, 2)).toHaveLength(0);
  });
});


// Component-level accessibility tests
test.describe('Accessibility - Components', () => {
  test('modal dialog is accessible', async ({ page }) => {
    await page.goto('/');
    
    // Open modal
    await page.click('[data-testid="open-modal"]');
    await page.waitForSelector('[role="dialog"]');
    
    // Check: focus should move to modal
    const focusedElement = await page.evaluate(() => document.activeElement?.tagName);
    expect(focusedElement).not.toBe('BODY');
    
    // Check: background is inert
    const bodyAriaHidden = await page.getAttribute('body > *:not([role="dialog"])', 'aria-hidden');
    // Not all implementations use aria-hidden, but focus should be trapped
    
    // Check: axe on modal state
    const results = await new AxeBuilder({ page })
      .include('[role="dialog"]')
      .analyze();
    expect(results.violations).toHaveLength(0);
    
    // Check: Escape closes modal
    await page.keyboard.press('Escape');
    await expect(page.locator('[role="dialog"]')).not.toBeVisible();
    
    // Check: focus returns to trigger
    const focusAfterClose = await page.evaluate(() =>
      document.activeElement?.getAttribute('data-testid')
    );
    expect(focusAfterClose).toBe('open-modal');
  });
  
  test('form validation is accessible', async ({ page }) => {
    await page.goto('/signup');
    
    // Submit empty form
    await page.click('[type=submit]');
    
    // Check: error messages are associated with inputs
    const emailError = page.locator('[data-testid="email-error"]');
    await expect(emailError).toBeVisible();
    
    // The input should have aria-describedby or aria-errormessage pointing to the error
    const emailInput = page.locator('[name=email]');
    const ariaDescribedBy = await emailInput.getAttribute('aria-describedby');
    const ariaErrorMessage = await emailInput.getAttribute('aria-errormessage');
    const ariaInvalid = await emailInput.getAttribute('aria-invalid');
    
    expect(ariaInvalid).toBe('true');
    expect(ariaDescribedBy || ariaErrorMessage).toBeTruthy();
    
    // Check axe
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations).toHaveLength(0);
  });
});
```

### Keyboard Navigation Tests

```typescript
// tests/accessibility/keyboard.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Keyboard Navigation', () => {
  test('can navigate entire header with keyboard', async ({ page }) => {
    await page.goto('/');
    
    // Tab through all interactive elements in header
    await page.keyboard.press('Tab');  // Skip to nav
    
    const header = page.locator('header');
    const interactiveElements = header.locator(
      'a, button, input, select, [tabindex]:not([tabindex="-1"])'
    );
    const count = await interactiveElements.count();
    
    for (let i = 0; i < count; i++) {
      await page.keyboard.press('Tab');
      const focused = await page.evaluate(() => ({
        tag: document.activeElement?.tagName,
        text: document.activeElement?.textContent?.trim().slice(0, 50),
        inHeader: document.activeElement?.closest('header') !== null,
      }));
      
      // Every focused element in Tab order should be visible and in header
      if (focused.inHeader) {
        const focusedLocator = page.locator(':focus');
        await expect(focusedLocator).toBeVisible();
      }
    }
  });
  
  test('dropdown menu is keyboard operable', async ({ page }) => {
    await page.goto('/');
    
    // Navigate to dropdown trigger
    await page.locator('[data-testid="nav-products"]').focus();
    
    // Open with Enter or Space
    await page.keyboard.press('Enter');
    await expect(page.locator('[data-testid="products-dropdown"]')).toBeVisible();
    
    // Navigate items with arrow keys
    await page.keyboard.press('ArrowDown');
    const firstItem = page.locator('[data-testid="products-dropdown"] a').first();
    await expect(firstItem).toBeFocused();
    
    await page.keyboard.press('ArrowDown');
    const secondItem = page.locator('[data-testid="products-dropdown"] a').nth(1);
    await expect(secondItem).toBeFocused();
    
    // Escape closes and returns focus
    await page.keyboard.press('Escape');
    await expect(page.locator('[data-testid="products-dropdown"]')).not.toBeVisible();
    await expect(page.locator('[data-testid="nav-products"]')).toBeFocused();
  });
  
  test('data table is keyboard navigable', async ({ page }) => {
    await page.goto('/admin/orders');
    
    const table = page.locator('[role="grid"], table');
    await table.locator('a, button').first().focus();
    
    // Tab should move between focusable cells
    await page.keyboard.press('Tab');
    const focusedInTable = await page.evaluate(
      () => document.activeElement?.closest('table') !== null
    );
    expect(focusedInTable).toBe(true);
  });
  
  test('skip to main content link works', async ({ page }) => {
    await page.goto('/');
    
    // First Tab should reveal skip link
    await page.keyboard.press('Tab');
    const skipLink = page.locator('[href="#main-content"], [href="#main"]');
    await expect(skipLink).toBeFocused();
    
    // Activate skip link
    await page.keyboard.press('Enter');
    
    // Focus should be on or within main content
    const mainContent = page.locator('#main-content, main');
    const focusedElement = page.locator(':focus');
    
    // Either main is focused, or focus moved past the header
    const focused = await page.evaluate(() => ({
      id: document.activeElement?.id,
      tagName: document.activeElement?.tagName,
    }));
    
    expect(['main-content', 'main'].includes(focused.id) || focused.tagName === 'MAIN').toBe(true);
  });
});
```

### Color Contrast Checker

```python
# tools/contrast_checker.py
from PIL import Image
import numpy as np

def luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance (WCAG formula)."""
    def linearize(c: float) -> float:
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

def contrast_ratio(color1: tuple, color2: tuple) -> float:
    """Calculate WCAG contrast ratio between two RGB colors."""
    l1 = luminance(*color1)
    l2 = luminance(*color2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def check_wcag_aa(foreground: tuple, background: tuple, large_text: bool = False) -> dict:
    """
    Check WCAG 2.1 AA compliance.
    Normal text: 4.5:1 minimum
    Large text (18pt+ or 14pt bold): 3:1 minimum
    """
    ratio = contrast_ratio(foreground, background)
    threshold = 3.0 if large_text else 4.5
    
    return {
        "ratio": round(ratio, 2),
        "threshold": threshold,
        "passes_aa": ratio >= threshold,
        "passes_aaa": ratio >= (4.5 if large_text else 7.0),
        "large_text": large_text,
    }

# Common problem checks
def audit_design_tokens(tokens: dict) -> list:
    """Audit a design token file for contrast issues."""
    issues = []
    
    # Check all text color + background combinations
    text_colors = {k: v for k, v in tokens.items() if "text" in k or "foreground" in k}
    bg_colors = {k: v for k, v in tokens.items() if "background" in k or "bg" in k or "surface" in k}
    
    for text_name, text_color in text_colors.items():
        for bg_name, bg_color in bg_colors.items():
            result = check_wcag_aa(
                hex_to_rgb(text_color),
                hex_to_rgb(bg_color)
            )
            if not result["passes_aa"]:
                issues.append({
                    "text_token": text_name,
                    "bg_token": bg_name,
                    "ratio": result["ratio"],
                    "required": result["threshold"],
                    "deficit": result["threshold"] - result["ratio"],
                })
    
    return sorted(issues, key=lambda x: x["deficit"], reverse=True)

def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
```

### CI Integration

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Testing

on:
  pull_request:
    paths: ['src/**', 'public/**']

jobs:
  axe-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npm run build
      - run: npm start &
      - run: npx wait-on http://localhost:3000
      
      - name: Run accessibility tests
        run: npx playwright test tests/accessibility/
        
      - name: Upload accessibility report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: a11y-report-${{ github.run_id }}
          path: playwright-report/
```

### WCAG Manual Checklist (Automated Tools Miss These)

```markdown
## Perceivable
- [ ] All non-decorative images have meaningful alt text
- [ ] Decorative images have alt="" (empty alt)
- [ ] Videos have captions (auto-generated doesn't count)
- [ ] Audio content has transcripts
- [ ] Page doesn't rely on color alone to convey information
- [ ] Text can be resized to 200% without horizontal scroll

## Operable
- [ ] All functionality accessible by keyboard
- [ ] No keyboard traps (can always Tab out)
- [ ] Focus indicator is clearly visible
- [ ] Focus order is logical (matches visual reading order)
- [ ] Moving/auto-updating content can be paused
- [ ] No flashing content (risk of seizures: <3 flashes/second)

## Understandable
- [ ] `lang` attribute set correctly on `<html>`
- [ ] Form inputs have associated labels (not just placeholder text)
- [ ] Error messages describe what went wrong and how to fix it
- [ ] Errors are announced to screen readers (aria-live)
- [ ] Instructions don't rely solely on sensory characteristics ("click the red button")

## Robust
- [ ] HTML is valid (run W3C Validator)
- [ ] All interactive elements have accessible names
- [ ] Status messages announced via aria-live
- [ ] ARIA roles and attributes used correctly (don't add aria unless needed)
```

## Rules

- **Automated tests catch only 30-40%** — they are necessary but not sufficient.
- **Test with real assistive technology** — not just automated tools; screen reader behavior differs.
- **WCAG 2.1 AA is the legal baseline** — WCAG 2.2 is current, but 2.1 AA is the minimum.
- **Don't use `aria-*` to fix broken HTML** — fix the semantic HTML; ARIA is last resort.
- **Placeholder text is not a label** — it disappears on input; always use visible `<label>`.
- **Color contrast applies to icons, too** — not just text; icons that convey information must meet 3:1.
- **Focus indicators must be visible** — browsers have defaults; many designs override them — don't.
- **Block critical violations in CI** — `critical` and `serious` axe violations must not reach production.
- **Test with keyboard only** — unplug your mouse and complete each user journey; it exposes real problems.
- **Include accessibility in design review** — fixing accessibility during design is 10x cheaper than after build.
