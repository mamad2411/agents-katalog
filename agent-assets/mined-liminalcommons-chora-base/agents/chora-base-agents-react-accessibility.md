---
sap_id: SAP-026
version: 1.0.0
status: active
last_updated: 2025-11-09
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 12
progressive_loading:
  phase_1: "lines 1-250"   # Quick Reference + Core Workflows
  phase_2: "lines 251-500" # Advanced Operations (WCAG 2.2 compliance, testing)
  phase_3: "full"          # Complete including best practices
phase_1_token_estimate: 5000
phase_2_token_estimate: 10000
phase_3_token_estimate: 14000
---

## 📖 Quick Reference

**New to SAP-026?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Install accessibility dependencies
- 📚 **Time Savings** - Significant time savings with battle-tested patterns
- 🎯 **Feature 1** - 9 new criteria (October 2023) including Focus Not Obscured, Target Size, Accessible Auth
- 🔧 **Feature 2** - eslint-plugin-jsx-a11y + axe-core catch most issues at build/test time
- 📊 **Feature 3** - jest-axe/vitest-axe validates components against WCAG rules
- 🔗 **Integration** - Works with SAP-005, SAP-020, SAP-021, SAP-022, SAP-024, SAP-025

This AGENTS.md provides: Agent-specific patterns for implementing SAP-026.
s.

---

# React Accessibility (SAP-026) - Agent Awareness

**SAP ID**: SAP-026
**Last Updated**: 2025-11-09
**Audience**: Generic AI Coding Agents

---

## Quick Reference

### When to Use

**Use React Accessibility (SAP-026) when**:
- Building React applications with public-facing interfaces (legal requirement)
- Government contracts requiring Section 508 compliance
- Enterprise SaaS products needing WCAG 2.2 Level AA compliance
- E-commerce sites (accessibility = better UX = more conversions)
- Setting up automated accessibility testing infrastructure
- Implementing accessible component patterns (modals, forms, buttons)

**Don't use when**:
- React Native mobile apps (different accessibility APIs - future SAP)
- Legacy React <18 applications (class-based patterns not covered)
- Projects requiring WCAG 2.2 Level AAA (this SAP focuses on Level AA)
- Non-React frameworks (use framework-specific accessibility patterns)

### Key Technology Versions

| Technology | Version | Why This Version |
|------------|---------|------------------|
| **WCAG** | 2.2 Level AA | W3C Recommendation (October 5, 2023), legal standard |
| **eslint-plugin-jsx-a11y** | 6.10.2+ | Catches 85% of common violations automatically |
| **jest-axe** | 9.0.0+ | Component testing for Next.js (axe-core integration) |
| **vitest-axe** | 1.0.0+ | Component testing for Vite (axe-core integration) |
| **axe-core** | 4.10.2+ | Industry standard, 85% WCAG violation detection |
| **react-focus-lock** | 2.13.2+ | Focus trap for modals/dialogs |

### WCAG 2.2 vs WCAG 2.1 (IMPORTANT: 9 New Criteria)

**WCAG 2.2 became the standard on October 5, 2023**, adding 9 new success criteria beyond WCAG 2.1:

| New Criterion | Level | Impact on React Apps |
|---------------|-------|----------------------|
| **2.4.11 Focus Not Obscured (Minimum)** | AA | Sticky headers must not hide focused elements |
| **2.5.7 Dragging Movements** | AA | Provide click alternative to drag-and-drop |
| **2.5.8 Target Size (Minimum)** | AA | Interactive elements ≥ 24×24 CSS pixels |
| **3.2.6 Consistent Help** | A | Help links in same location across pages |
| **3.3.7 Redundant Entry** | A | Don't re-ask for information (use autocomplete) |
| **3.3.8 Accessible Authentication (Minimum)** | AA | No CAPTCHAs, support password managers |
| **2.4.12, 2.4.13, 3.3.9** | AAA | Out of scope (Level AAA) |

**Migration from WCAG 2.1 to 2.2**: All WCAG 2.1 criteria still apply. WCAG 2.2 adds requirements, does not remove any.

---

## User Signal Patterns

### Accessibility Setup Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "setup accessibility testing" | configure_axe_testing() | jest-axe or vitest-axe | Core infrastructure |
| "add accessibility linting" | configure_jsx_a11y() | ESLint plugin (in SAP-022) | Already included |
| "check WCAG compliance" | run_accessibility_audit() | Lighthouse + axe-core | Manual + automated |
| "test with screen reader" | manual_screen_reader_test() | NVDA (Windows, free) | 15% manual coverage |
| "validate color contrast" | check_color_contrast() | Chrome DevTools / axe | WCAG 1.4.3 (4.5:1 ratio) |

### Component Accessibility Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "make modal accessible" | implement_accessible_modal() | Focus trap + ARIA | Pattern in protocol-spec.md |
| "accessible form validation" | implement_accessible_form() | aria-invalid + role="alert" | Error announcements |
| "fix button accessibility" | implement_accessible_button() | Semantic <button> + aria-label | Icon buttons need labels |
| "keyboard navigation" | implement_keyboard_navigation() | Tab order + Arrow keys | Roving tabindex for toolbars |
| "skip to main content" | add_skip_link() | <SkipLink /> component | WCAG 2.4.1 bypass blocks |

### Common Variations

**Testing Setup**:
- "setup accessibility testing" / "add axe tests" / "configure a11y testing" → configure_axe_testing()
- "check WCAG compliance" / "audit accessibility" / "validate WCAG 2.2" → run_accessibility_audit()

**Component Fixes**:
- "make modal accessible" / "fix dialog accessibility" / "accessible popup" → implement_accessible_modal()
- "accessible form" / "fix form labels" / "validation errors accessible" → implement_accessible_form()

---

## Common Workflows

### Workflow 1: Setup Automated Accessibility Testing (10-15 minutes)

**User signal**: "Setup accessibility testing", "Add axe tests", "Configure WCAG compliance"

**Purpose**: Configure jest-axe or vitest-axe for automated WCAG 2.2 Level AA testing

**Steps**:
1. Install dependencies:
   ```bash
   # For Next.js with Jest:
   npm install --save-dev jest-axe @axe-core/react

   # For Vite with Vitest:
   npm install --save-dev vitest-axe @axe-core/react
   ```

2. Configure testing setup file:
   **Next.js (jest.setup.ts)**:
   ```typescript
   import { toHaveNoViolations } from 'jest-axe';
   import { configureAxe } from 'jest-axe';

   // Extend Jest matchers
   expect.extend(toHaveNoViolations);

   // Configure axe-core (WCAG 2.2 Level AA)
   export const axe = configureAxe({
     rules: {
       'region': { enabled: false }, // React portals cause false positives
     },
   });
   ```

   **Vite (vitest.setup.ts)**:
   ```typescript
   import { expect } from 'vitest';
   import { axe, toHaveNoViolations } from 'vitest-axe';

   // Extend Vitest matchers
   expect.extend(toHaveNoViolations);

   // Export configured axe instance
   export { axe };
   ```

3. Add test to component:
   ```typescript
   import { render } from '@testing-library/react';
   import { axe } from '../jest.setup';  // or '../vitest.setup'
   import { MyComponent } from './MyComponent';

   describe('MyComponent Accessibility', () => {
     it('should have no accessibility violations', async () => {
       const { container } = render(<MyComponent />);
       const results = await axe(container);
       expect(results).toHaveNoViolations();
     });
   });
   ```

4. Run tests:
   ```bash
   npm run test
   # Or: npm run test:a11y (if configured)
   ```

**Expected outcome**: Automated accessibility testing catching 85% of WCAG violations

**Time saved**: 2-3 hours (manual WCAG checks) → 10-15 minutes (automated axe-core)

**Detection rate**: axe-core catches ~85% of WCAG violations, 15% requires manual testing

---

### Workflow 2: Implement Accessible Modal/Dialog (15-20 minutes)

**User signal**: "Make modal accessible", "Fix dialog accessibility", "Accessible popup"

**Purpose**: Create WCAG 2.2 compliant modal with focus trap, keyboard handling, and ARIA

**Steps**:
1. Install focus management library:
   ```bash
   npm install react-focus-lock
   ```

2. Create accessible modal component:
   ```typescript
   import { useEffect, useRef } from 'react';
   import FocusLock from 'react-focus-lock';

   interface ModalProps {
     isOpen: boolean;
     onClose: () => void;
     title: string;
     children: React.ReactNode;
   }

   export function AccessibleModal({ isOpen, onClose, title, children }: ModalProps) {
     const titleId = useRef(`modal-title-${Math.random()}`);
     const previousFocusRef = useRef<HTMLElement | null>(null);

     // Focus restoration
     useEffect(() => {
       if (isOpen) {
         previousFocusRef.current = document.activeElement as HTMLElement;
       } else if (previousFocusRef.current) {
         previousFocusRef.current.focus();
       }
     }, [isOpen]);

     // Escape key handler
     useEffect(() => {
       const handleEscape = (e: KeyboardEvent) => {
         if (e.key === 'Escape' && isOpen) {
           onClose();
         }
       };
       document.addEventListener('keydown', handleEscape);
       return () => document.removeEventListener('keydown', handleEscape);
     }, [isOpen, onClose]);

     if (!isOpen) return null;

     return (
       <div
         role="dialog"
         aria-modal="true"
         aria-labelledby={titleId.current}
         className="modal-overlay"
       >
         <FocusLock>
           <div className="modal-content">
             <h2 id={titleId.current}>{title}</h2>
             {children}
             <button onClick={onClose}>Close</button>
           </div>
         </FocusLock>
       </div>
     );
   }
   ```

3. Add accessibility test:
   ```typescript
   import { render } from '@testing-library/react';
   import { axe } from '../jest.setup';
   import { AccessibleModal } from './AccessibleModal';

   describe('AccessibleModal Accessibility', () => {
     it('should have no accessibility violations when open', async () => {
       const { container } = render(
         <AccessibleModal isOpen={true} onClose={() => {}}>
           <p>Modal content</p>
         </AccessibleModal>
       );
       const results = await axe(container);
       expect(results).toHaveNoViolations();
     });
   });
   ```

4. Verify keyboard navigation:
   - Press Tab repeatedly: Focus should cycle within modal only
   - Press Escape: Modal should close
   - After close: Focus should return to trigger element

**Expected outcome**: Fully accessible modal meeting WCAG 2.2 Level AA

**WCAG Criteria Met**:
- 2.1.1 Keyboard (all functionality via keyboard)
- 2.1.2 No Keyboard Trap (Escape closes modal)
- 2.4.3 Focus Order (logical tab order within modal)
- 4.1.2 Name, Role, Value (aria-modal, aria-labelledby)

---

### Workflow 3: Implement Accessible Form with Validation (20-25 minutes)

**User signal**: "Accessible form validation", "Fix form errors accessible", "Screen reader form"

**Purpose**: Create form with proper labels, error announcements, and WCAG 2.2 compliance

**Steps**:
1. Create accessible form component:
   ```typescript
   import { useState } from 'react';

   export function AccessibleForm() {
     const [email, setEmail] = useState('');
     const [error, setError] = useState('');

     const emailId = 'email-input';
     const hintId = 'email-hint';
     const errorId = 'email-error';

     const validate = () => {
       if (!email.includes('@')) {
         setError('Please enter a valid email address');
         return false;
       }
       setError('');
       return true;
     };

     return (
       <form onSubmit={(e) => { e.preventDefault(); validate(); }}>
         <div>
           <label htmlFor={emailId}>
             Email Address <span aria-label="required">*</span>
           </label>

           <input
             id={emailId}
             type="email"
             value={email}
             onChange={(e) => setEmail(e.target.value)}
             aria-describedby={`${hintId} ${error ? errorId : ''}`}
             aria-invalid={!!error}
             aria-required="true"
             required
           />

           <p id={hintId} className="hint">
             We'll never share your email
           </p>

           {error && (
             <p id={errorId} role="alert" aria-live="assertive" className="error">
               {error}
             </p>
           )}
         </div>

         <button type="submit">Submit</button>
       </form>
     );
   }
   ```

2. Add accessibility test:
   ```typescript
   import { render } from '@testing-library/react';
   import { axe } from '../jest.setup';
   import { AccessibleForm } from './AccessibleForm';

   describe('AccessibleForm Accessibility', () => {
     it('should have no accessibility violations', async () => {
       const { container } = render(<AccessibleForm />);
       const results = await axe(container);
       expect(results).toHaveNoViolations();
     });
   });
   ```

3. Verify screen reader announcements (manual test):
   - Install NVDA (free): https://www.nvaccess.org/
   - Navigate form with Tab key
   - Verify label announced: "Email Address, edit, required"
   - Trigger validation error
   - Verify error announced: "Alert, Please enter a valid email address"

**Expected outcome**: Accessible form with proper labels, hints, and error announcements

**WCAG Criteria Met**:
- 1.3.1 Info and Relationships (label associated with input)
- 3.3.1 Error Identification (errors clearly identified)
- 3.3.2 Labels or Instructions (all inputs have labels)
- 3.3.3 Error Suggestion (error message suggests fix)
- 4.1.2 Name, Role, Value (aria-invalid, aria-describedby, aria-required)

---

### Workflow 4: Check WCAG 2.2 Compliance (20-30 minutes)

**User signal**: "Check WCAG compliance", "Audit accessibility", "Validate WCAG 2.2"

**Purpose**: Run comprehensive accessibility audit using automated + manual testing

**Steps**:
1. Run automated tests (85% coverage):
   ```bash
   # Component-level tests
   npm run test

   # Lighthouse CI (full page audit)
   npx lighthouse http://localhost:3000 --only-categories=accessibility --view
   ```

2. Review automated test results:
   - jest-axe/vitest-axe: Check for 0 violations
   - Lighthouse: Target ≥90 accessibility score
   - ESLint jsx-a11y: Fix all errors in IDE

3. Manual keyboard navigation test (10 minutes):
   - Put away mouse (don't touch during test)
   - Press Tab from URL bar: Verify skip link appears
   - Tab through entire page: All interactive elements reachable
   - Verify focus indicators visible (3:1 contrast minimum)
   - Test modals: Open with Enter/Space, close with Escape
   - Test dropdowns: Navigate with Arrow keys

4. Manual screen reader test (10 minutes):
   - Install NVDA (Windows): https://www.nvaccess.org/
   - Start NVDA (Ctrl+Alt+N)
   - Navigate with Down Arrow: Reads each element
   - Jump to headings with H key
   - Jump to buttons with B key
   - Jump to form fields with F key
   - Verify all images have alt text (or are marked decorative)
   - Verify error messages announced (aria-live)

5. Manual color contrast test (5 minutes):
   - Open Chrome DevTools
   - Inspect text elements
   - Check contrast ratio in Accessibility tab
   - Verify: Normal text ≥4.5:1, Large text ≥3:1, UI components ≥3:1

6. WCAG 2.2 specific checks (5 minutes):
   - **2.5.8 Target Size**: Measure button/link sizes (≥24×24px)
   - **2.4.11 Focus Not Obscured**: Tab through page with sticky header, verify focus visible
   - **3.3.8 Accessible Authentication**: Verify no CAPTCHAs, password manager works

**Expected outcome**: Comprehensive WCAG 2.2 Level AA compliance report

**Coverage**:
- Automated (85%): axe-core, Lighthouse, ESLint jsx-a11y
- Manual (15%): Keyboard navigation, screen reader, contrast, WCAG 2.2 new criteria

**Compliance Target**: 100% of applicable WCAG 2.2 Level AA criteria met

---

### Workflow 5: Fix Common Accessibility Violations (15-30 minutes)

**User signal**: "Fix accessibility issues", "Resolve WCAG violations", "Fix axe errors"

**Purpose**: Address most common accessibility violations from axe-core reports

**Steps**:
1. **Fix missing alt text** (WCAG 1.1.1):
   ```tsx
   // ❌ BAD: No alt text
   <img src="/logo.png" />

   // ✅ GOOD: Descriptive alt text
   <img src="/logo.png" alt="Company logo" />

   // ✅ GOOD: Decorative image (empty alt)
   <img src="/decorative.png" alt="" />
   ```

2. **Fix missing form labels** (WCAG 3.3.2):
   ```tsx
   // ❌ BAD: No label association
   <label>Email</label>
   <input type="email" />

   // ✅ GOOD: Explicit label association
   <label htmlFor="email">Email</label>
   <input id="email" type="email" />
   ```

3. **Fix button accessibility** (WCAG 1.3.1):
   ```tsx
   // ❌ BAD: Non-semantic div with onClick
   <div onClick={handleClick}>Click me</div>

   // ✅ GOOD: Semantic button
   <button onClick={handleClick}>Click me</button>
   ```

4. **Fix low color contrast** (WCAG 1.4.3):
   ```tsx
   // ❌ BAD: Light gray on white (2.5:1)
   <p className="text-gray-300">This text is too light</p>

   // ✅ GOOD: Dark gray on white (7:1)
   <p className="text-gray-700">This text meets contrast requirements</p>
   ```

5. **Fix icon-only buttons** (WCAG 4.1.2):
   ```tsx
   // ❌ BAD: Icon with no accessible name
   <button onClick={handleDelete}>
     <TrashIcon />
   </button>

   // ✅ GOOD: Icon with aria-label
   <button onClick={handleDelete} aria-label="Delete item">
     <TrashIcon aria-hidden="true" />
   </button>
   ```

6. **Fix missing error announcements** (WCAG 3.3.1):
   ```tsx
   // ❌ BAD: Error not linked to input
   <input type="email" className="error" />
   <p className="error-text">Invalid email</p>

   // ✅ GOOD: Error linked with aria-describedby + role="alert"
   <input
     type="email"
     aria-invalid="true"
     aria-describedby="email-error"
   />
   <p id="email-error" role="alert">
     Invalid email address
   </p>
   ```

7. Re-run tests:
   ```bash
   npm run test
   npx lighthouse http://localhost:3000 --only-categories=accessibility
   ```

**Expected outcome**: All common accessibility violations resolved, 0 axe violations

**Top 5 Most Common Violations** (from axe-core data):
1. Missing alt text (35% of violations)
2. Missing form labels (25% of violations)
3. Low color contrast (15% of violations)
4. Non-semantic HTML (10% of violations)
5. Missing ARIA attributes (10% of violations)

---

## Best Practices

### Practice 1: Use axe-core for 85% Automated Coverage

**Pattern**:
```typescript
// Add to every component test
import { axe } from '../jest.setup';

it('should have no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

**Why**: Catches 85% of WCAG violations automatically, prevents regressions

**Evidence**: axe-core is industry standard, used by Deque, Microsoft, Google

---

### Practice 2: Always Use Semantic HTML First, ARIA Second

**Pattern**:
```tsx
// ✅ GOOD: Semantic HTML (no ARIA needed)
<button onClick={handleClick}>Click me</button>

// ❌ BAD: Non-semantic div with ARIA (unnecessary complexity)
<div role="button" tabIndex={0} onClick={handleClick} onKeyDown={handleKeyDown}>
  Click me
</div>
```

**Why**: Semantic HTML provides keyboard support, focus management, and screen reader context automatically

**First Rule of ARIA**: If you can use a native HTML element, use it. ARIA is for filling gaps.

---

### Practice 3: Target WCAG 2.2 Level AA (Not 2.1)

**Pattern**:
```markdown
# ✅ GOOD: Target WCAG 2.2 Level AA
WCAG 2.2 Level AA compliance (October 2023 standard)
- Includes all 9 new criteria (2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, etc.)
- Legal requirement for ADA, EAA, Section 508

# ❌ BAD: Still targeting WCAG 2.1
WCAG 2.1 Level AA compliance (June 2018 standard)
- Missing 9 new criteria from WCAG 2.2
- Outdated as of October 2023
```

**Why**: WCAG 2.2 is the current W3C Recommendation (since October 5, 2023), legal compliance standard

**Migration**: All WCAG 2.1 criteria still apply, WCAG 2.2 adds 9 new criteria (no removals)

---

### Practice 4: Combine Automated (85%) + Manual (15%) Testing

**Pattern**:
```markdown
Automated Testing (85% coverage):
- axe-core (jest-axe / vitest-axe)
- Lighthouse CI
- ESLint jsx-a11y plugin

Manual Testing (15% coverage):
- Keyboard navigation (Tab order, focus indicators)
- Screen reader (NVDA / VoiceOver)
- Color contrast (visual inspection)
- WCAG 2.2 specific checks (target size, focus not obscured)

= 100% WCAG 2.2 Level AA compliance
```

**Why**: Automated tools catch most issues, but ~15% requires human judgment (keyboard flow, screen reader experience)

**Evidence**: Deque research shows automated tools detect ~85% of accessibility issues

---

### Practice 5: Use Pre-Commit Hooks to Prevent Violations

**Pattern**:
```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix --max-warnings=0",  // Blocks commit if jsx-a11y errors
      "prettier --write"
    ]
  }
}
```

**Why**: Prevents accessibility violations from being committed, catches issues at development time

**Integration**: SAP-022 (react-linting) includes jsx-a11y plugin with pre-commit hooks

---

## Common Pitfalls

### Pitfall 1: Using WCAG 2.1 Instead of WCAG 2.2

**Problem**: Target outdated WCAG 2.1 standard (June 2018), miss 9 new criteria

**Fix**: Target WCAG 2.2 Level AA (October 2023 standard)

```markdown
# ❌ BAD: Outdated standard
WCAG 2.1 Level AA compliance

# ✅ GOOD: Current standard
WCAG 2.2 Level AA compliance
- Includes all 9 new criteria (2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, etc.)
```

**Why**: WCAG 2.2 is current legal standard, WCAG 2.1 is outdated

---

### Pitfall 2: Relying Only on Automated Testing

**Problem**: Run axe-core tests, assume 100% WCAG compliance

**Fix**: Combine automated (85%) + manual (15%) testing

```markdown
# ❌ BAD: Only automated testing
- Run axe-core tests
- Lighthouse CI
- ESLint jsx-a11y
= ~85% coverage (missing keyboard flow, screen reader experience)

# ✅ GOOD: Automated + manual testing
- Automated: axe-core, Lighthouse, ESLint (85%)
- Manual: Keyboard, screen reader, contrast (15%)
= 100% coverage
```

**Why**: Automated tools miss ~15% of WCAG violations (keyboard flow, screen reader UX)

---

### Pitfall 3: Using <div onClick> Instead of <button>

**Problem**: Use non-semantic div with onClick for interactive elements

**Fix**: Always use semantic <button> element

```tsx
// ❌ BAD: Non-semantic div (not keyboard accessible)
<div onClick={handleClick} className="button">
  Click me
</div>

// ✅ GOOD: Semantic button (keyboard support built-in)
<button onClick={handleClick} className="button">
  Click me
</button>
```

**Why**: <button> provides keyboard support (Enter/Space), focus management, and screen reader role automatically

---

### Pitfall 4: Missing Alt Text on Images

**Problem**: Forget alt attribute on images, screen readers say "image" with no context

**Fix**: Always provide alt text (or empty alt="" for decorative)

```tsx
// ❌ BAD: No alt text
<img src="/logo.png" />

// ✅ GOOD: Descriptive alt text
<img src="/logo.png" alt="Company logo" />

// ✅ GOOD: Decorative image (empty alt)
<img src="/decorative-border.png" alt="" />
```

**Why**: Images without alt text are invisible to screen readers

---

### Pitfall 5: Form Inputs Without Labels

**Problem**: Use placeholder text instead of label, screen readers can't identify field

**Fix**: Always use <label> element associated with input

```tsx
// ❌ BAD: No label (placeholder not sufficient)
<input type="email" placeholder="Enter email" />

// ✅ GOOD: Label with htmlFor association
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

**Why**: Placeholders disappear on focus, screen readers need persistent labels

---

## Integration with Other SAPs

### SAP-041 (form-validation)
- Form accessibility patterns (labels, validation, error messages)
- Integration: SAP-026 provides accessible form components, SAP-041 adds React Hook Form + Zod validation
- **RT-019 Finding**: Combine for WCAG 2.2 compliant forms with dual client/server validation

### SAP-020 (react-foundation)
- React project foundation (Next.js 15, TypeScript)
- Integration: SAP-020 provides base structure, SAP-026 adds accessibility layer
- **RT-019 Finding**: Server Components enable progressive enhancement (works without JS), better accessibility baseline

### SAP-021 (react-testing)
- Testing infrastructure (Vitest, Jest)
- Integration: SAP-021 provides test setup, SAP-026 adds axe-core integration (vitest-axe / jest-axe)
- **RT-019 Finding**: Automated accessibility testing in CI/CD (blocks builds with violations)

### SAP-022 (react-linting)
- ESLint configuration
- Integration: SAP-022 includes eslint-plugin-jsx-a11y, SAP-026 provides configuration and patterns
- **RT-019 Finding**: ESLint jsx-a11y catches 85% of violations during development

### SAP-039 (E2E Testing) - FUTURE
- End-to-end testing with Playwright
- Integration: SAP-039 will include accessibility testing in E2E flows (axe-core + Playwright)
- **RT-019 Finding**: Automated accessibility testing at E2E level (full user flows)

---

## Support & Resources

**SAP-026 Documentation**:
- [Capability Charter](capability-charter.md) - Business value, scope, dependencies
- [Protocol Spec](protocol-spec.md) - Complete technical specification, WCAG 2.2 compliance matrix
- [Awareness Guide](awareness-guide.md) - Common pitfalls, decision trees, component patterns
- [Adoption Blueprint](adoption-blueprint.md) - Step-by-step installation guide
- [Ledger](ledger.md) - WCAG 2.2 Level AA compliance checklist
- [CLAUDE.md](CLAUDE.md) - Claude Code-specific patterns

**External Resources**:
- [WCAG 2.2 Specification](https://www.w3.org/TR/WCAG22/) - W3C Recommendation (October 2023)
- [Understanding WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/) - Detailed guidance for each criterion
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) - Accessible widget patterns
- [axe DevTools](https://www.deque.com/axe/devtools/) - Browser extension for accessibility testing
- [NVDA Screen Reader](https://www.nvaccess.org/) - Free screen reader for Windows

**Related SAPs**:
- [SAP-041 (form-validation)](../react-form-validation/) - Accessible form patterns with React Hook Form + Zod
- [SAP-020 (react-foundation)](../react-foundation/) - React project setup with accessibility baseline
- [SAP-021 (react-testing)](../react-testing/) - Testing infrastructure with axe-core integration
- [SAP-022 (react-linting)](../react-linting/) - ESLint configuration with jsx-a11y plugin
- [SAP-039 (E2E Testing)](../e2e-testing/) - FUTURE: Playwright + accessibility testing

---

## Version History

- **1.0.0** (2025-11-09): Initial AGENTS.md for SAP-026
  - 5 workflows: Setup Automated Testing, Implement Accessible Modal, Implement Accessible Form, Check WCAG 2.2 Compliance, Fix Common Violations
  - WCAG 2.2 emphasis: 9 new criteria documented, migration from WCAG 2.1 to 2.2
  - axe-core as industry standard: 85% automated detection rate
  - Progressive enhancement patterns from RT-019 research
  - Server Component accessibility benefits
  - Integration with SAP-018, SAP-020, SAP-021, SAP-022, SAP-039 (future)
  - 2 user signal pattern tables (Accessibility Setup Operations, Component Accessibility Operations)
  - 5 best practices, 5 common pitfalls

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
2. Review [protocol-spec.md](protocol-spec.md) for WCAG 2.2 compliance matrix and component patterns
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation steps
4. Run accessibility audit: `npx lighthouse http://localhost:3000 --only-categories=accessibility --view`
