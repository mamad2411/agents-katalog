---
sap_id: SAP-026
version: 1.0.0
status: active
last_updated: 2025-11-09
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 10
progressive_loading:
  phase_1: "lines 1-200"   # Quick Start + Core Workflows
  phase_2: "lines 201-400" # Advanced Patterns (WCAG 2.2, Server Components)
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 4500
phase_2_token_estimate: 9000
phase_3_token_estimate: 12000
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

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-026.
s.

---

# React Accessibility (SAP-026) - Claude-Specific Awareness

**SAP ID**: SAP-026
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-09

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for implementing WCAG 2.2 Level AA accessibility.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic accessibility workflows
2. Use this file for Claude Code tool integration (Read for audits, Edit for fixes, Bash for testing)
3. Check component templates in `templates/react/accessibility/shared/components/` before building from scratch

### Tool Usage Priority

```markdown
# Accessibility audits → Read + Bash
Read component files → Bash: npx lighthouse http://localhost:3000

# Fix violations → Edit (targeted fixes)
Edit ComponentName.tsx
# old_string: <div onClick={...}>
# new_string: <button onClick={...}>

# Add new accessible components → Write (from templates)
Write src/components/AccessibleModal.tsx
# Copy from templates/react/accessibility/shared/components/accessible-modal.tsx
```

---

## Claude Code Accessibility Workflows

### Workflow 1: Setup Automated Testing with Read and Bash

```markdown
User: "Setup accessibility testing"

Claude (Phase 1: Check Current Setup - 0-5k tokens):
1. Read package.json to check if jest-axe or vitest-axe installed:
   Read package.json
   # Look for: "jest-axe" or "vitest-axe" in devDependencies

2. Check test framework (Next.js uses Jest, Vite uses Vitest):
   Read jest.config.js or Read vitest.config.ts

Claude (Phase 2: Install Dependencies - 5-15k tokens):
3. Install axe testing library:
   Bash: npm install --save-dev jest-axe @axe-core/react
   # Or for Vite: npm install --save-dev vitest-axe @axe-core/react

4. Check if setup file exists:
   Bash: ls jest.setup.ts || ls vitest.setup.ts

Claude (Phase 3: Configure Setup File - 15-25k tokens):
5. If jest.setup.ts doesn't exist, create it:
   Write jest.setup.ts
   ```typescript
   import { toHaveNoViolations } from 'jest-axe';
   import { configureAxe } from 'jest-axe';

   expect.extend(toHaveNoViolations);

   export const axe = configureAxe({
     rules: {
       'region': { enabled: false }, // React portals cause false positives
     },
   });
   ```

   Or for Vite:
   Write vitest.setup.ts
   ```typescript
   import { expect } from 'vitest';
   import { axe, toHaveNoViolations } from 'vitest-axe';

   expect.extend(toHaveNoViolations);

   export { axe };
   ```

6. Update test config to use setup file:
   Edit jest.config.js
   # old_string: // setupFilesAfterEnv: []
   # new_string: setupFilesAfterEnv: ['<rootDir>/jest.setup.ts']

   Or Edit vitest.config.ts
   # old_string: // setupFiles: []
   # new_string: setupFiles: ['./vitest.setup.ts']

Claude (Phase 4: Verify Setup - 25-30k tokens):
7. Run tests to verify:
   Bash: npm run test
   # Should see: "expect.extend(toHaveNoViolations)" in output

Claude (response to user):
"✅ Automated accessibility testing configured!

**Testing library**: jest-axe (Next.js) or vitest-axe (Vite)
**Coverage**: ~85% of WCAG 2.2 Level AA violations
**Setup file**: jest.setup.ts or vitest.setup.ts

**Add to any component test**:
```typescript
import { axe } from '../jest.setup';

it('should have no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

**Run tests**: npm run test

**Manual testing** (15% coverage):
- Keyboard navigation (Tab key)
- Screen reader (NVDA: https://www.nvaccess.org/)
- Color contrast (Chrome DevTools)

= 100% WCAG 2.2 Level AA coverage"

Result: Automated accessibility testing catching 85% of violations
```

---

### Workflow 2: Fix Common Violations with Read and Edit

```markdown
User: "Fix accessibility issues in LoginForm component"

Claude (Phase 1: Read Component and Audit - 0-10k tokens):
1. Read component to understand current state:
   Read src/components/LoginForm.tsx

2. Run accessibility audit:
   Bash: npm run test -- LoginForm.test.tsx
   # Look for axe violations in output

3. Or run Lighthouse audit:
   Bash: npx lighthouse http://localhost:3000/login --only-categories=accessibility --view

Claude (Phase 2: Identify Violations - 10-20k tokens):
4. Common violations to check:
   - Missing alt text on images
   - Missing labels on form inputs
   - Non-semantic HTML (<div onClick> instead of <button>)
   - Low color contrast
   - Missing ARIA attributes

Claude (Phase 3: Fix Violations with Edit - 20-40k tokens):
5. Fix missing form labels:
   Edit src/components/LoginForm.tsx
   # old_string:
   <input type="email" placeholder="Email" />

   # new_string:
   <label htmlFor="email">Email</label>
   <input id="email" type="email" />

6. Fix non-semantic button:
   Edit src/components/LoginForm.tsx
   # old_string:
   <div onClick={handleSubmit} className="button">
     Login
   </div>

   # new_string:
   <button onClick={handleSubmit} className="button">
     Login
   </button>

7. Fix missing error announcements:
   Edit src/components/LoginForm.tsx
   # old_string:
   {error && <p className="error">{error}</p>}

   # new_string:
   {error && (
     <p id="login-error" role="alert" className="error">
       {error}
     </p>
   )}

   # AND update input:
   # old_string:
   <input id="email" type="email" />

   # new_string:
   <input
     id="email"
     type="email"
     aria-invalid={!!error}
     aria-describedby={error ? "login-error" : undefined}
   />

Claude (Phase 4: Verify Fixes - 40-50k tokens):
8. Re-run tests:
   Bash: npm run test -- LoginForm.test.tsx
   # Should show: 0 axe violations

9. Re-run Lighthouse:
   Bash: npx lighthouse http://localhost:3000/login --only-categories=accessibility
   # Target: ≥90 score

Claude (response to user):
"✅ LoginForm accessibility violations fixed!

**Violations resolved**:
- ✅ Added explicit labels for email and password inputs
- ✅ Replaced <div onClick> with semantic <button>
- ✅ Added error announcements with role="alert" and aria-describedby
- ✅ Added aria-invalid for validation state

**WCAG 2.2 criteria met**:
- 1.3.1 Info and Relationships (semantic HTML)
- 3.3.1 Error Identification (errors linked to inputs)
- 3.3.2 Labels or Instructions (all inputs have labels)
- 4.1.2 Name, Role, Value (ARIA attributes)

**Test results**:
- axe violations: 0
- Lighthouse accessibility score: 95/100

**Manual testing recommended**:
- Tab through form (verify focus order)
- Test with NVDA screen reader (verify error announcements)"

Result: All automated violations fixed, component WCAG 2.2 compliant
```

---

### Workflow 3: Implement Accessible Modal with Write and Templates

```markdown
User: "Create accessible modal component"

Claude (Phase 1: Check Templates - 0-5k tokens):
1. Check if template exists:
   Bash: ls templates/react/accessibility/shared/components/accessible-modal.tsx

Claude (Phase 2: Create Component from Template - 5-15k tokens):
2. If template exists, copy and customize:
   Read templates/react/accessibility/shared/components/accessible-modal.tsx

3. Create component in project:
   Write src/components/AccessibleModal.tsx
   # Paste template content, customize props as needed

4. Or if template doesn't exist, create from scratch with all WCAG requirements:
   Write src/components/AccessibleModal.tsx
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

Claude (Phase 3: Add Test - 15-25k tokens):
5. Create accessibility test:
   Write src/components/AccessibleModal.test.tsx
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

Claude (Phase 4: Verify Component - 25-30k tokens):
6. Run test:
   Bash: npm run test -- AccessibleModal.test.tsx
   # Should show: 0 violations

7. Manual keyboard test (provide instructions):
   "Test keyboard navigation:
   1. Open modal
   2. Press Tab repeatedly: Focus should cycle within modal only
   3. Press Escape: Modal should close
   4. After close: Focus should return to trigger button"

Claude (response to user):
"✅ Accessible modal component created!

**File**: src/components/AccessibleModal.tsx

**WCAG 2.2 features**:
- ✅ Focus trap (Tab cycles within modal only)
- ✅ Focus restoration (returns to trigger on close)
- ✅ Escape key closes modal
- ✅ ARIA attributes (role="dialog", aria-modal, aria-labelledby)
- ✅ Screen reader announcements (modal title announced)

**WCAG criteria met**:
- 2.1.1 Keyboard (all functionality via keyboard)
- 2.1.2 No Keyboard Trap (Escape closes modal)
- 2.4.3 Focus Order (logical tab order within modal)
- 4.1.2 Name, Role, Value (proper ARIA)

**Test results**: 0 axe violations

**Usage**:
```tsx
<AccessibleModal
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  title="Edit Profile"
>
  <p>Modal content here</p>
</AccessibleModal>
```

**Dependencies**: react-focus-lock (install with: npm install react-focus-lock)"

Result: Production-ready accessible modal component
```

---

### Workflow 4: Run WCAG 2.2 Compliance Audit with Bash

```markdown
User: "Check WCAG 2.2 compliance"

Claude (Phase 1: Automated Tests - 0-10k tokens):
1. Run component accessibility tests:
   Bash: npm run test
   # Check for 0 axe violations

2. Run Lighthouse audit:
   Bash: npx lighthouse http://localhost:3000 --only-categories=accessibility --view
   # Target: ≥90 score

3. Check ESLint jsx-a11y warnings:
   Bash: npx eslint src/**/*.{ts,tsx} --ext .ts,.tsx
   # Fix all jsx-a11y/* warnings

Claude (Phase 2: WCAG 2.2 Specific Checks - 10-20k tokens):
4. Check WCAG 2.2 new criteria (manual verification needed):
   "Manual WCAG 2.2 checks:

   **2.5.8 Target Size (Minimum)** [NEW in WCAG 2.2]:
   - Measure button/link sizes with DevTools
   - Requirement: ≥24×24 CSS pixels
   - Test: Right-click element → Inspect → Check width/height

   **2.4.11 Focus Not Obscured (Minimum)** [NEW in WCAG 2.2]:
   - Tab through page with sticky header/footer
   - Verify: Focused element not fully hidden
   - Test: Press Tab repeatedly, check if focus visible

   **3.3.8 Accessible Authentication (Minimum)** [NEW in WCAG 2.2]:
   - Verify: No CAPTCHAs (use hCaptcha accessible mode if needed)
   - Verify: Password managers work (autocomplete='current-password')
   - Test: Try to log in with password manager

   **3.3.7 Redundant Entry** [NEW in WCAG 2.2]:
   - Verify: Information entered earlier is auto-filled
   - Example: Billing address = shipping address (checkbox to copy)
   - Test: Multi-step forms don't re-ask for same info

   **2.5.7 Dragging Movements** [NEW in WCAG 2.2]:
   - Verify: Drag-and-drop has click alternative
   - Example: File upload supports both drag-drop and 'Browse files' button
   - Test: Complete all actions without dragging

   **3.2.6 Consistent Help** [NEW in WCAG 2.2]:
   - Verify: Help links in consistent location across pages
   - Example: 'Help' link always in footer, right side
   - Test: Check 3+ pages for consistent help placement"

Claude (Phase 3: Manual Keyboard Test - 20-30k tokens):
5. Provide keyboard testing instructions:
   "Keyboard navigation test (10 minutes):
   1. Put away mouse (don't touch during test)
   2. Press Tab from URL bar: Verify skip link appears
   3. Press Tab repeatedly: All interactive elements reachable
   4. Verify focus indicators visible (3:1 contrast minimum)
   5. Test modals: Open with Enter/Space, close with Escape
   6. Test dropdowns: Navigate with Arrow keys
   7. Test forms: Tab through fields, Space for checkboxes"

Claude (Phase 4: Manual Screen Reader Test - 30-40k tokens):
6. Provide screen reader testing instructions:
   "Screen reader test with NVDA (10 minutes):
   1. Download NVDA (free): https://www.nvaccess.org/
   2. Start NVDA (Ctrl+Alt+N)
   3. Navigate with Down Arrow: Reads each element
   4. Jump to headings with H key
   5. Jump to buttons with B key
   6. Jump to form fields with F key
   7. Verify all images have alt text (or decorative with alt='')
   8. Verify error messages announced (aria-live)
   9. Verify modal title announced when opened"

Claude (Phase 5: Color Contrast Check - 40-50k tokens):
7. Provide color contrast testing instructions:
   "Color contrast test (5 minutes):
   1. Open Chrome DevTools
   2. Inspect text elements
   3. Check contrast ratio in Accessibility tab
   4. Requirements:
      - Normal text: ≥4.5:1
      - Large text (18pt+ or 14pt bold): ≥3:1
      - UI components (buttons, icons): ≥3:1
      - Focus indicators: ≥3:1
   5. Fix low contrast with Tailwind: text-gray-300 → text-gray-700"

Claude (response to user):
"✅ WCAG 2.2 Level AA compliance audit complete!

**Automated tests** (85% coverage):
- Component tests (axe-core): PASS (0 violations)
- Lighthouse accessibility score: 92/100 (GOOD)
- ESLint jsx-a11y: PASS (0 errors)

**Manual tests required** (15% coverage):
- ⚠️ Keyboard navigation test (see instructions above)
- ⚠️ Screen reader test with NVDA (see instructions above)
- ⚠️ Color contrast check (see instructions above)
- ⚠️ WCAG 2.2 specific checks (see checklist above)

**WCAG 2.2 NEW criteria to verify**:
1. 2.5.8 Target Size (≥24×24px)
2. 2.4.11 Focus Not Obscured (sticky headers don't hide focus)
3. 3.3.8 Accessible Authentication (no CAPTCHAs, password managers work)
4. 3.3.7 Redundant Entry (auto-fill previous inputs)
5. 2.5.7 Dragging Movements (click alternatives)
6. 3.2.6 Consistent Help (help links in same location)

**Next steps**:
1. Complete manual keyboard test (10 min)
2. Complete screen reader test with NVDA (10 min)
3. Complete color contrast check (5 min)
4. Verify WCAG 2.2 specific criteria (10 min)

= 100% WCAG 2.2 Level AA coverage"

Result: Comprehensive WCAG 2.2 compliance report with actionable next steps
```

---

## Claude-Specific Tips

### Tip 1: Use Read Before Edit for Accessibility Fixes

**Pattern**:
```markdown
# Always read component first to understand structure:
Read src/components/LoginForm.tsx
# Check current implementation, identify violations

# Then make targeted edits:
Edit src/components/LoginForm.tsx
# Fix specific violations without breaking other code
```

**Why**: Understanding current implementation prevents breaking existing functionality

---

### Tip 2: Use Bash for Quick Lighthouse Audits

**Pattern**:
```markdown
# Run Lighthouse accessibility audit:
Bash: npx lighthouse http://localhost:3000 --only-categories=accessibility --view

# Or specific page:
Bash: npx lighthouse http://localhost:3000/login --only-categories=accessibility --view

# Target: ≥90 score (good accessibility)
```

**Why**: Lighthouse provides comprehensive WCAG audit in seconds, identifies specific violations

---

### Tip 3: Copy Accessible Components from Templates

**Pattern**:
```markdown
# Check if template exists first:
Bash: ls templates/react/accessibility/shared/components/

# Read template to understand implementation:
Read templates/react/accessibility/shared/components/accessible-modal.tsx

# Create component in project:
Write src/components/AccessibleModal.tsx
# Paste template content, customize as needed
```

**Why**: Templates include all WCAG requirements, battle-tested patterns, saves 20-30 minutes per component

---

### Tip 4: Use Edit for Targeted Violation Fixes

**Pattern**:
```markdown
# Fix single violation without touching other code:
Edit src/components/Button.tsx
# old_string: <div onClick={handleClick}>Click me</div>
# new_string: <button onClick={handleClick}>Click me</button>

# Preserves surrounding code, comments, formatting
```

**Why**: Targeted edits minimize risk of breaking working code

---

### Tip 5: Run Tests Immediately After Fixes

**Pattern**:
```markdown
# After fixing violations:
Bash: npm run test -- ComponentName.test.tsx
# Verify: 0 axe violations

# Or full test suite:
Bash: npm run test
# Ensure no regressions in other components
```

**Why**: Immediate feedback prevents accumulating violations, catches regressions early

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Reading Component Before Editing

**Problem**: Edit component without understanding current structure, break existing functionality

**Fix**: Always Read first, then Edit

```markdown
# ❌ BAD: Edit blindly
Edit src/components/Form.tsx
# Risk breaking existing validation logic

# ✅ GOOD: Read first, understand structure
Read src/components/Form.tsx
# Understand current implementation

Edit src/components/Form.tsx
# Make targeted fix without breaking other code
```

**Why**: Reading first prevents breaking working code, enables precise edits

---

### Pitfall 2: Not Running Tests After Fixes

**Problem**: Fix violations, assume tests pass, commit broken code

**Fix**: Always run tests after fixes

```markdown
# After editing component:
Edit src/components/LoginForm.tsx
# Fix missing labels

# Immediately run tests:
Bash: npm run test -- LoginForm.test.tsx
# Verify: 0 violations, no new errors
```

**Why**: Catch regressions immediately, verify fixes actually work

---

### Pitfall 3: Using Write Instead of Edit for Fixes

**Problem**: Use Write to fix component, lose existing logic, comments, formatting

**Fix**: Use Edit for targeted changes

```markdown
# ❌ BAD: Overwrite entire component
Write src/components/Button.tsx
# Loses existing props, logic, tests

# ✅ GOOD: Targeted edit
Edit src/components/Button.tsx
# old_string: <div onClick={...}>
# new_string: <button onClick={...}>
```

**Why**: Edit preserves existing code, Write overwrites everything

---

### Pitfall 4: Not Checking Templates Before Building Components

**Problem**: Build accessible modal from scratch, miss WCAG requirements, waste 30+ minutes

**Fix**: Check templates first

```markdown
# Before building from scratch:
Bash: ls templates/react/accessibility/shared/components/

# If template exists:
Read templates/react/accessibility/shared/components/accessible-modal.tsx
Write src/components/AccessibleModal.tsx
# Customize template (5 min) instead of building from scratch (30+ min)
```

**Why**: Templates include all WCAG requirements, save time, prevent missing criteria

---

### Pitfall 5: Targeting WCAG 2.1 Instead of WCAG 2.2

**Problem**: Fix violations for WCAG 2.1 standard, miss 9 new WCAG 2.2 criteria

**Fix**: Always target WCAG 2.2 Level AA

```markdown
# ❌ BAD: Outdated standard
# Target: WCAG 2.1 Level AA (June 2018)
# Missing: 9 new criteria (2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, etc.)

# ✅ GOOD: Current standard
# Target: WCAG 2.2 Level AA (October 2023)
# Includes: All WCAG 2.1 criteria + 9 new WCAG 2.2 criteria
```

**Why**: WCAG 2.2 is current legal standard (since October 2023), WCAG 2.1 is outdated

---

## Support & Resources

**SAP-026 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic accessibility workflows
- [Capability Charter](capability-charter.md) - Business value, scope, WCAG 2.2 overview
- [Protocol Spec](protocol-spec.md) - Complete WCAG 2.2 compliance matrix, component patterns
- [Awareness Guide](awareness-guide.md) - Common pitfalls, decision trees
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - WCAG 2.2 Level AA compliance checklist

**Templates**:
- `templates/react/accessibility/shared/components/` - Accessible component templates

**External Resources**:
- [WCAG 2.2 Specification](https://www.w3.org/TR/WCAG22/) - W3C Recommendation (October 2023)
- [Understanding WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/) - Detailed guidance
- [axe DevTools](https://www.deque.com/axe/devtools/) - Browser extension for testing
- [NVDA Screen Reader](https://www.nvaccess.org/) - Free screen reader (Windows)

**Related SAPs**:
- [SAP-041 (form-validation)](../react-form-validation/) - Accessible forms with RHF + Zod
- [SAP-020 (react-foundation)](../react-foundation/) - React setup with Server Components
- [SAP-021 (react-testing)](../react-testing/) - Testing infrastructure with axe-core
- [SAP-022 (react-linting)](../react-linting/) - ESLint jsx-a11y configuration

---

## Version History

- **1.0.0** (2025-11-09): Initial CLAUDE.md for SAP-026
  - 4 workflows: Setup Automated Testing, Fix Common Violations, Implement Accessible Modal, Run WCAG 2.2 Compliance Audit
  - Tool patterns: Read for audits, Edit for fixes, Write for components, Bash for testing
  - WCAG 2.2 emphasis: 9 new criteria, migration from 2.1 to 2.2
  - axe-core as industry standard: 85% automated detection
  - Server Component accessibility benefits from RT-019 research
  - 5 Claude-specific tips, 5 common pitfalls

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic accessibility workflows
2. Review [protocol-spec.md](protocol-spec.md) for WCAG 2.2 compliance matrix
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Run accessibility audit: `npx lighthouse http://localhost:3000 --only-categories=accessibility --view`
