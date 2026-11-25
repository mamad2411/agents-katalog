---
name: frontend-quality-gates
description: Mandatory quality gates, visual-verification rules, WCAG audit steps, multi-phase build checklist, and content edge-case testing for ANY frontend/UI/website work. Use whenever building, reviewing, or shipping a website, web app, page, or UI component — and whenever running or coordinating the quality-check agent. Triggers include "build website", "build site", "landing page", "UI", "frontend", "quality check", "ready to ship", "production build", "responsive", "accessibility/WCAG", or spawning coder/ui-expert/quality-check agents on visual work.
---

# MANDATORY QUALITY GATES FOR UI/FRONTEND WORK

**THIS SECTION IS NON-NEGOTIABLE. FAILURE TO FOLLOW THESE RULES WILL RESULT IN BROKEN WEBSITES.**

## ⛔ HARD STOP: Browser Tools Requirement

**If browser automation tools (Playwright MCP or Chrome DevTools) are NOT available:**

1. **STOP THE SESSION IMMEDIATELY**
2. **DO NOT proceed with any frontend/UI work**
3. Inform the user: "Browser automation tools are required for frontend work. Please ensure Playwright MCP or Chrome DevTools MCP is configured before continuing."
4. **Wait for user to fix the tooling before proceeding**

This is non-negotiable. Frontend work without visual verification WILL produce broken websites.

**Test browser tools at session start:**
```
Before any UI work, verify you can:
1. Navigate to a URL
2. Take a screenshot
3. Read console output
If ANY of these fail, STOP and alert the user.
```

---

## The Dev Server Rule

**Before ANY frontend coding begins:**
1. Start the dev server (`npm run dev` or equivalent)
2. Keep it running for the ENTIRE session
3. Verify it's accessible at localhost

If the dev server is not running, you CANNOT verify visual output. Code that hasn't been visually verified is NOT complete.

---

## Visual Verification Gates

### Gate 1: Coder Self-Check (MANDATORY)
Every coder agent working on UI MUST:
1. After writing code, take a screenshot of the affected page/component
2. Verify the visual output matches intent
3. Check for console errors
4. If there are ANY visual issues, fix them before reporting "complete"

**Do NOT mark UI coding tasks complete without visual verification.**

### Gate 2: Phase Completion Check (MANDATORY)
After EACH phase of a multi-phase build:
1. Spawn a `quality-check` agent to verify the phase output
2. The quality check MUST take screenshots
3. The quality check MUST pass before proceeding to the next phase
4. If the quality check fails, fix issues before continuing

**Timeline for a typical website build:**
```
Phase 1 (Foundation) → quality-check → proceed
Phase 2 (Core Pages) → quality-check → proceed
Phase 3 (Additional Pages) → quality-check → proceed
Phase 4+ (Polish/SEO) → quality-check → proceed
FINAL → production build test → quality-check → ship
```

### Gate 3: Code Review Visual Check (MANDATORY)
Code reviewers working on UI code MUST:
1. Run `npm run dev` (or ensure it's running)
2. Navigate to the affected pages
3. Take at least ONE screenshot
4. Check browser console for errors
5. Fail the review if ANY visual issues are present

**A code review that only reads files and never looks at the browser output is INCOMPLETE.**

### Gate 4: Integration Check After Parallel Agents (MANDATORY)
When multiple coder agents work in parallel on UI components:
1. **After ALL parallel agents complete**, spawn a quality-check agent
2. The quality check must verify components work TOGETHER, not just individually
3. Check for:
   - Overlapping elements
   - Conflicting styles
   - Z-index issues
   - Layout breaks when components are combined
4. **Do NOT proceed until integration is verified**

**Example:**
```
Parallel: Agent A (Header) + Agent B (Hero) + Agent C (Services)
         ↓
Integration Check: Verify Header + Hero + Services render correctly TOGETHER
         ↓
Only then proceed to next phase
```

### Gate 5: Production Build Test (MANDATORY before final approval)
Before declaring ANY website ready to ship:
1. Run `npm run build` (or equivalent production build command)
2. Run `npm run start` (or serve the production build)
3. Take screenshots of the PRODUCTION build, not just dev
4. Check for:
   - Build errors or warnings
   - Hydration mismatches
   - Missing assets in production
   - CSS differences between dev and prod
   - Static export issues (if applicable)

**Dev mode is NOT production. Always verify the production build.**

---

## What Counts as "Visual Verification"

- Using Playwright MCP browser automation to navigate and screenshot
- Using Chrome DevTools MCP to take screenshots
- Actually seeing the rendered page in a browser

What does NOT count:
- Reading the code and assuming it works
- Trusting that CSS/JSX will render correctly
- Skipping browser testing because "it should work"

---

## Mandatory Viewport Testing

**Every quality check MUST include screenshots at these SPECIFIC viewports:**

| Viewport | Width | Required |
|----------|-------|----------|
| Mobile | 375px | ✅ MANDATORY |
| Tablet | 768px | ✅ MANDATORY |
| Desktop | 1440px | ✅ MANDATORY |

**A quality check without mobile screenshots is INCOMPLETE and must be re-run.**

Do not assume "responsive design works" - actually test it at each breakpoint.

---

## Orchestrator Responsibilities

When coordinating a website build:

1. **Before coding starts:**
   - Verify browser automation tools are available (HARD STOP if not)
   - Start dev server and verify it's running
   - Take initial screenshot to confirm tools work

2. **After each coding agent completes UI work:**
   - Verify the coder took screenshots
   - If no screenshots, ask for visual verification
   - Spawn quality-check if coder reports issues or uncertainty

3. **After parallel agents complete:**
   - ALWAYS run integration check
   - Verify components work together, not just individually
   - Do NOT proceed if integration issues found

4. **Between major phases:**
   - ALWAYS spawn quality-check agent
   - Do NOT proceed if quality check finds Critical issues
   - Fix ALL Critical issues before moving to next phase (no exceptions)

5. **Before declaring "done":**
   - Run production build (`npm run build`)
   - Test production build (not just dev server)
   - Run final quality-check on production build
   - Quality check MUST test: homepage, key pages, ALL viewports
   - ONLY declare done if quality check returns "READY TO SHIP"

---

## Strict Pass/Fail Rules

**There is NO "proceed with warnings" for Critical issues.**

| Quality Check Result | Action |
|---------------------|--------|
| READY TO SHIP ✅ | Proceed |
| NEEDS WORK (Minor only) ⚠️ | May proceed with documented issues |
| NEEDS WORK (Major issues) ⚠️ | Fix issues before proceeding |
| NOT READY (Critical issues) ❌ | **STOP. Fix ALL critical issues. Re-run quality check.** |

**Critical issues are BLOCKING. No exceptions. No "we'll fix it later."**

---

## Anti-Sycophancy Rule for Quality Checks

**The quality-check agent is NOT trying to be helpful by approving things.**

The quality-check agent must:
- Default to FAIL, not pass
- Find problems, not confirm things work
- Be harshly critical, not supportive
- Compare to professional standards (Apple, Stripe, Linear), not "good enough"
- List EVERY issue found, not stop at a few
- Justify why something PASSES, not why it fails

**If a quality check comes back saying "everything looks good" for a site that clearly isn't professional:**
1. Do NOT trust that result
2. Ask for a more critical re-evaluation
3. Or manually inspect the screenshots yourself

**A quality check that approves mediocre work is WORSE than no quality check at all** - it creates false confidence.

The goal is a site that would make a real client proud, not a site that merely "works".

---

## Red Flags That Require Immediate Quality Check

Spawn quality-check immediately if:
- Coder mentions "animation", "opacity", "transition", or "fadeIn" (visibility issues common)
- Any CSS framework version mismatch
- Next.js version upgrade (async params, app router changes)
- Any mention of "should work" without verification
- Multiple components being created in parallel (integration issues)
- Coder reports "done" without mentioning screenshots
- Any error in console, even if "minor"
- Forms without labels or ARIA attributes (accessibility failures common)
- Custom interactive components without keyboard testing (dropdowns, modals, accordions)
- Color palette changes (may break WCAG contrast requirements)
- Focus style removal (`outline: none` without visible alternative)

---

## Context Anchoring for Long Sessions

**IMPORTANT: Re-read this section every 10 turns in long sessions.**

In sessions longer than 2 hours, earlier instructions may be compressed. These rules remain in effect regardless of context length:

1. ⛔ Browser tools required - hard stop if unavailable
2. 📱 Mobile viewport testing is MANDATORY
3. 🔨 Production build must be tested before shipping
4. 🔗 Integration check required after parallel agents
5. ❌ Critical issues are ALWAYS blocking - no exceptions
6. ♿ WCAG automated audit (axe-core) is MANDATORY before shipping

If you find yourself wanting to skip any of these steps, STOP and re-read this document.

---

# Quality Check Agent Rules

The `quality-check` agent MUST be EXTREMELY STRICT. A site that looks unprofessional, unfinished, or has ANY visible issues is NOT ready to ship. Default to FAILING the check unless the site looks genuinely professional.

### MANDATORY: Use Browser Automation
1. **MUST use Chrome DevTools or Playwright** - no exceptions
2. **Take screenshots at ALL THREE viewports** - mobile (375px), tablet (768px), desktop (1440px)
3. **Screenshot representative pages from EACH template type** - not just homepage
4. **If browser tools unavailable, FAIL the check** - never approve without visual verification

### MANDATORY: Network and Console Checks
1. **Check browser console** for errors, warnings, and failed requests
2. **Check network tab** for:
   - Failed resource loads (images, fonts, scripts)
   - 404 errors
   - Slow-loading resources
   - Mixed content warnings (HTTP on HTTPS)
3. **External resources must load** - Google Fonts, CDN images, third-party scripts

### MANDATORY: Animation Verification
For any page with animations:
1. Take screenshot IMMEDIATELY on page load (before any scroll)
2. Wait 2 seconds, take another screenshot
3. Scroll down slightly, take another screenshot
4. **All three screenshots must show content correctly**
5. If content is invisible in ANY screenshot, it's a CRITICAL failure

This catches intermittent animation bugs that might pass a single screenshot check.

### MANDATORY: Representative Page Testing
Don't just test the homepage. Test at least ONE page from each template type:

For a typical local business site:
- [ ] Homepage
- [ ] One service page (e.g., /services/plumbing)
- [ ] One location page (e.g., /locations/london)
- [ ] One matrix page if applicable (e.g., /london/plumbing)
- [ ] Contact page
- [ ] About page

**Pages not tested may be broken. Test representatives from every template.**

### MANDATORY: Automated WCAG 2.1 AA Audit (axe-core)
1. **Inject axe-core via CDN** into each representative page using browser automation JS execution
2. **Run `axe.run()` with WCAG 2.1 AA rulesets** (`wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `best-practice`)
3. **Test at ALL THREE viewports** (375px, 768px, 1440px) - responsive layouts create viewport-specific a11y issues
4. **Critical axe-core violations are BLOCKING** - same as any other Critical issue, no exceptions
5. **If CDN injection fails**, flag as Major issue and proceed with manual-only checks (but note reduced audit reliability)

Full axe-core injection snippets and severity mapping are in the `quality-check` agent definition.

### AUTOMATIC FAILURES (any of these = not ready to ship)

**Debug/Development Artifacts:**
- ANY error badges, debug indicators, or "Issue" markers visible (including Next.js dev indicators)
- Console errors or warnings visible in browser dev tools
- Placeholder text ("Lorem ipsum", "TODO", "FIXME", "[placeholder]")
- Default/unstyled components that look like library defaults
- Visible component borders or debug outlines

**Visual Polish Issues:**
- Poor text contrast (text hard to read against backgrounds)
- Badges, pills, or labels that look unfinished or poorly styled
- Inconsistent spacing or alignment between similar elements
- Icons or images that look misaligned or poorly positioned
- Sections that look rushed or unpolished compared to others
- Trust badges or credentials that are hard to read
- CTAs that don't stand out or look clickable

**Layout Problems:**
- Elements overlapping incorrectly
- Content touching edges without proper padding
- Inconsistent margins between sections
- Cards or boxes with mismatched heights in a row
- Text that wraps awkwardly or gets cut off
- Content not visible on page load (opacity/animation issues)
- Icons positioned outside their containers

**Responsive Issues:**
- Horizontal scrolling on mobile
- Text too small to read on mobile
- Buttons too small to tap on mobile
- Navigation that doesn't work on mobile
- Images that overflow their containers

**Animation/Transition Issues:**
- Content invisible on page load due to animation initial states
- Animations that never trigger (intersection observer issues)
- Flickering or janky transitions
- Content that requires scrolling to appear when it should be visible

**Network/Resource Issues:**
- Failed font loads (fallback fonts visible)
- Broken images (missing or 404)
- Failed script loads causing functionality issues
- Mixed content warnings

**Production Build Issues:**
- Works in dev but broken in production build
- Hydration mismatches
- Missing static assets after build

**Accessibility (WCAG) Violations:**
- Any critical axe-core violations (missing form labels, no keyboard access, broken ARIA)
- Forms without associated labels or ARIA labelling
- Interactive elements not reachable via keyboard
- Missing language declaration (`<html lang="...">`)
- Images conveying content with no alt text
- Insufficient color contrast on body text (below WCAG AA 4.5:1)
- Focus styles removed with no visible alternative

**Professional Standards:**
- Would a paying client be embarrassed to show this to customers?
- Does it look like a real business website or a coding exercise?
- Are there ANY elements that scream "this is unfinished"?

### Reporting Requirements
1. **Screenshot every issue found** with clear annotations
2. **Be specific** - "The trust badges in the hero have poor contrast and look unpolished" not "some styling issues"
3. **Prioritize issues** - Critical (blocks launch) vs Minor (should fix)
4. **NEVER say "ready to ship" if there are Critical issues**
5. **List ALL issues found** - don't stop at the first few
6. **Include viewport tested** for each screenshot

### Mindset
Pretend you are a harsh client who paid good money for this website. Would you accept it? If there's ANY hesitation, it's not ready.

---

# Multi-Phase Build Checklist

For any website build with multiple phases, follow this checklist:

```
[ ] Browser automation tools verified working (HARD STOP if not)
[ ] Dev server started and verified
[ ] Initial screenshot taken to confirm tools work

PHASE 1 - Foundation:
[ ] Coder agents completed foundation code
[ ] Dev server still running
[ ] Quick screenshot taken of initial page
[ ] No console errors

PHASE 2 - Core Pages:
[ ] Coder agents completed core pages
[ ] INTEGRATION CHECK if parallel agents used
[ ] quality-check agent spawned
[ ] Quality check screenshots at ALL THREE viewports (mobile/tablet/desktop)
[ ] Quality check tested representative pages (not just homepage)
[ ] Automated WCAG audit (axe-core) run on representative pages at all viewports
[ ] Zero critical axe-core violations (or fixed before proceeding)
[ ] Quality check passed OR issues fixed

PHASE 3 - Additional Pages:
[ ] Coder agents completed additional pages
[ ] INTEGRATION CHECK if parallel agents used
[ ] quality-check agent spawned
[ ] Quality check verified all page templates render correctly
[ ] Quality check passed OR issues fixed

PHASE 4+ - Polish/SEO:
[ ] Animations tested with MULTIPLE screenshots (immediately, after 2s, after scroll)
[ ] SEO elements verified
[ ] quality-check agent spawned
[ ] Quality check passed OR issues fixed

PRE-FINAL - Production Build:
[ ] npm run build completed without errors
[ ] Production build served (npm run start or equivalent)
[ ] Screenshots taken of PRODUCTION build (not dev)
[ ] No differences between dev and production

FINAL:
[ ] Final quality-check with full site crawl
[ ] ALL THREE viewports tested (mobile 375px, tablet 768px, desktop 1440px)
[ ] Network tab checked for failed resources
[ ] Console checked for errors
[ ] Automated WCAG audit (axe-core) run on ALL representative pages at ALL viewports
[ ] Zero critical axe-core violations confirmed
[ ] All serious axe-core violations documented or fixed
[ ] Manual WCAG inspection completed (keyboard nav, focus states, motion, skip links)
[ ] All critical issues resolved
[ ] Quality check returns "READY TO SHIP"
[ ] ONLY NOW declare the build complete
```

**DO NOT skip any checkbox. Each one exists because of past failures.**

---

# Content Testing Requirements

## Realistic Content Lengths

Don't test with perfect placeholder content. Test with:
- **Long titles** - What if the business name is 40 characters?
- **Long descriptions** - Real service descriptions may be 3 paragraphs
- **Short content** - What if there's only one testimonial?
- **Special characters** - Ampersands, quotes, accents in business names
- **Long location names** - "Royal Leamington Spa" vs "Bath"

If layout breaks with realistic content, it's NOT ready to ship.

## Edge Cases to Verify
- [ ] What happens with very long service/location names?
- [ ] What happens with minimal content (1 service, 1 location)?
- [ ] What happens with maximum content (20 services, 50 locations)?
- [ ] Do phone numbers wrap correctly on mobile?
- [ ] Do email addresses break layout if long?
