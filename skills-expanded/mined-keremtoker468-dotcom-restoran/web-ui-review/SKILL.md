---
name: web-ui-review
description: "Comprehensive web UI review for quality, accessibility, usability, performance, responsive design, cross-browser compatibility, and code quality. Use this skill when users ask you to review, audit, or critique a web page, web application UI, frontend code, or deployed website for design quality, WCAG accessibility compliance, responsive behavior, performance, UX best practices, browser compatibility, or HTML/CSS/JS code quality."
---

# Web UI Review

This skill provides a structured, expert-level review of web user interfaces. It evaluates a web UI across seven dimensions: visual/design quality, accessibility (WCAG), responsive design, performance, UX best practices, cross-browser compatibility, and frontend code quality.

## When to Use This Skill

Activate this skill when the user requests:
- A review or audit of a web page or web application UI
- An accessibility review or WCAG compliance check
- A responsive design evaluation
- A performance review of a frontend
- A UX or usability assessment of a website
- A cross-browser compatibility review
- A code quality review of HTML, CSS, or JavaScript
- A general "is this good?" evaluation of a web interface
- A pre-launch quality checklist review

## Review Process

### Step 1: Gather Context

Before beginning, establish what you are reviewing and any constraints. Ask the user if not already clear:

1. **What is being reviewed?** (URL, screenshot, code files, component, full page, entire app)
2. **Target audience** (general public, internal tool, specific demographics, accessibility needs)
3. **Browser/device requirements** (which browsers, mobile support, minimum viewport)
4. **Accessibility target level** (WCAG 2.1/2.2 Level A, AA, or AAA)
5. **Design system or brand guidelines** in use
6. **Known constraints** (legacy browser support, framework limitations, timeline)
7. **Priority areas** (which of the seven review dimensions matter most)

### Step 2: Conduct the Review

Evaluate the UI across all seven dimensions below, then produce a structured report.

---

## Dimension 1: Visual Inspection and Design Quality

Assess the visual presentation and design coherence of the interface.

### What to Evaluate

**Layout and Composition**
- Is there a clear visual hierarchy guiding the eye?
- Is the grid system consistent and well-structured?
- Is whitespace used effectively to create breathing room and group related content?
- Are elements properly aligned (no off-by-pixel misalignments)?
- Is visual weight distributed in a balanced way?

**Typography**
- Are font choices appropriate for the content and audience?
- Is there a clear typographic hierarchy (headings, subheadings, body, captions)?
- Is the type scale consistent and systematic?
- Is line length comfortable for reading (45-75 characters per line)?
- Is line height adequate (1.4-1.6 for body text)?
- Is the base font size at least 16px?
- Are no more than 2-3 font families used?

**Color**
- Is the color palette cohesive and intentional?
- Are colors used consistently (same color = same meaning)?
- Does color convey semantic meaning appropriately (red for errors, green for success)?
- Is the palette accessible for color-blind users (information is not conveyed by color alone)?
- Are accent colors used purposefully to draw attention?

**Imagery and Icons**
- Are images crisp and appropriately sized (not stretched or pixelated)?
- Do icons follow a consistent style (outline vs. filled, weight, size)?
- Are icons meaningful and recognizable?
- Are decorative elements purposeful and not distracting?

**Consistency**
- Are similar elements styled identically throughout?
- Do spacing values follow a consistent scale (e.g., 4px, 8px, 16px, 24px, 32px)?
- Are interactive elements (buttons, links, form controls) visually consistent?
- Does the design feel like a unified system rather than assembled piecemeal?

**Polish and Attention to Detail**
- Are transitions and animations smooth and purposeful?
- Are loading states, empty states, and error states designed (not just default browser chrome)?
- Do hover, focus, active, and disabled states all look intentional?
- Is the overall impression professional and polished?

### Common Issues to Flag
- Inconsistent spacing or alignment
- Too many competing visual elements (cluttered layout)
- Typography that is too small, too large, or poorly contrasted
- Misuse of color (too many colors, clashing combinations, color as sole indicator)
- Missing or inconsistent interactive states
- Generic, template-like appearance lacking design intent

---

## Dimension 2: Accessibility (WCAG) Review

Evaluate compliance with WCAG 2.1/2.2. Default to Level AA unless the user specifies otherwise. Accessibility is a critical dimension -- issues here can prevent entire groups of users from using the interface.

### Perceivable (WCAG Principle 1)

**Text Alternatives (1.1)**
- [ ] All `<img>` elements have meaningful `alt` attributes (or `alt=""` for purely decorative images)
- [ ] Icon-only buttons and links have accessible labels (`aria-label`, `aria-labelledby`, or visually hidden text)
- [ ] Complex images (charts, diagrams) have extended descriptions
- [ ] SVG elements have accessible names (`<title>`, `aria-label`, or `role="img"` with label)
- [ ] Background images that convey information have text alternatives

**Time-Based Media (1.2)**
- [ ] Videos have captions
- [ ] Audio content has transcripts
- [ ] Live video has captions where feasible

**Adaptable (1.3)**
- [ ] Page structure uses semantic HTML (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`)
- [ ] Heading hierarchy is logical and sequential (no skipped levels)
- [ ] Form inputs have associated `<label>` elements (using `for`/`id` or wrapping)
- [ ] Tables use `<th>`, `scope`, and `<caption>` properly
- [ ] Reading order in the DOM matches visual order
- [ ] Content is meaningful without CSS

**Distinguishable (1.4)**
- [ ] Text contrast meets 4.5:1 for normal text and 3:1 for large text (18pt or 14pt bold)
- [ ] UI component and graphical object contrast meets 3:1 against adjacent colors
- [ ] Color is not the sole means of conveying information (links, errors, status)
- [ ] Text can be resized to 200% without loss of content or functionality
- [ ] Content reflows at 320px viewport width without horizontal scrolling (1.4.10)
- [ ] Text spacing can be overridden without breaking layout (1.4.12)
- [ ] Hover/focus-triggered content is dismissible, hoverable, and persistent (1.4.13)

### Operable (WCAG Principle 2)

**Keyboard Accessible (2.1)**
- [ ] All interactive elements are reachable and operable via keyboard
- [ ] There are no keyboard traps
- [ ] Custom widgets implement expected keyboard patterns (arrow keys for tabs, Enter/Space for buttons)
- [ ] Skip links are present to bypass repetitive navigation

**Enough Time (2.2)**
- [ ] Time limits can be extended or removed
- [ ] Auto-playing content can be paused, stopped, or hidden

**Seizures and Physical Reactions (2.3)**
- [ ] No content flashes more than 3 times per second

**Navigable (2.4)**
- [ ] Page has a descriptive `<title>`
- [ ] Focus order is logical and follows visual flow
- [ ] Focus indicators are clearly visible (not suppressed with `outline: none` without a replacement)
- [ ] Link text is descriptive (no "click here" or "read more" without context)
- [ ] Headings and labels accurately describe their content
- [ ] Multiple ways to find pages (nav, search, sitemap)

**Input Modalities (2.5)**
- [ ] Touch targets are at least 44x44 CSS pixels
- [ ] Pointer gestures have single-pointer alternatives
- [ ] Drag operations have non-drag alternatives (2.5.7, WCAG 2.2)

### Understandable (WCAG Principle 3)

**Readable (3.1)**
- [ ] Page language is declared (`<html lang="en">`)
- [ ] Language changes within the page are marked (`lang` attribute on elements)

**Predictable (3.2)**
- [ ] Focus and input do not trigger unexpected context changes
- [ ] Navigation is consistent across pages
- [ ] Components with the same function are identified consistently

**Input Assistance (3.3)**
- [ ] Form errors are clearly identified with descriptive text (not color alone)
- [ ] Labels, instructions, and formatting hints are provided
- [ ] Error suggestions are offered when possible
- [ ] Critical submissions (financial, legal, data deletion) can be reversed, reviewed, or confirmed

### Robust (WCAG Principle 4)

**Compatible (4.1)**
- [ ] HTML validates without significant errors
- [ ] `id` attributes are unique
- [ ] ARIA roles, states, and properties are used correctly
- [ ] Custom components expose name, role, and value to assistive technology
- [ ] Status messages use `role="status"` or `aria-live` so screen readers announce them

### Accessibility Testing Recommendations
- **Automated**: axe DevTools, WAVE, Lighthouse accessibility audit, Pa11y
- **Keyboard**: Tab through the entire page; verify all actions are reachable and focus is visible
- **Screen reader**: Test with NVDA (Windows), VoiceOver (macOS/iOS), or TalkBack (Android)
- **Zoom**: Test at 200% and 400% zoom
- **Color contrast**: Use WebAIM Contrast Checker or browser DevTools contrast tool

---

## Dimension 3: Responsive Design

Evaluate how the interface adapts across viewport sizes and devices.

### What to Evaluate

**Breakpoint Strategy**
- Are breakpoints well-chosen and sufficient for the content (not just device widths)?
- Is the layout coherent at every width between breakpoints (no awkward intermediate states)?
- Does content reflow gracefully rather than jumping abruptly?

**Mobile Experience**
- Is the mobile layout usable and complete (not a degraded desktop layout)?
- Are touch targets large enough (minimum 44x44 CSS pixels with adequate spacing)?
- Is navigation accessible on mobile (hamburger menu, bottom nav, or equivalent)?
- Are forms easy to complete on mobile (correct input types, appropriate keyboards)?
- Is horizontal scrolling avoided?

**Tablet and Intermediate Sizes**
- Is the layout optimized for medium viewports (not just phone and desktop)?
- Are sidebars, multi-column layouts, and data tables handled appropriately?

**Large Screens**
- Does the layout make good use of wide viewports (not just a narrow centered column)?
- Is there a sensible max-width to prevent overly long line lengths?

**Content Adaptation**
- Do images scale properly (responsive images with `srcset` or CSS `object-fit`)?
- Do tables become scrollable or reflow on small screens?
- Do complex components (charts, maps, carousels) adapt to available space?
- Is text readable at all sizes without pinch-zooming?

**Viewport and Scaling**
- Is the viewport meta tag correctly set (`<meta name="viewport" content="width=device-width, initial-scale=1">`)?
- Is user scaling not disabled (`maximum-scale=1` and `user-scalable=no` should be avoided)?

### Common Issues to Flag
- Fixed-width elements causing horizontal overflow on small screens
- Touch targets that are too small or too close together
- Navigation that becomes inaccessible on mobile
- Text that becomes unreadable without zooming
- Images or media that overflow their containers
- Layouts that break at intermediate widths
- Missing or incorrect viewport meta tag

---

## Dimension 4: Performance Considerations

Evaluate the frontend for performance issues that affect user experience. Focus on what is observable or inferable from the code and UI behavior.

### What to Evaluate

**Loading Performance**
- Are images optimized (proper format: WebP/AVIF, appropriate dimensions, lazy-loaded below the fold)?
- Are fonts loaded efficiently (`font-display: swap`, preloaded, subset if possible)?
- Is CSS and JavaScript minified and bundled appropriately?
- Are critical resources preloaded or inlined?
- Is there unnecessary render-blocking CSS or JS in the `<head>`?
- Are third-party scripts loaded asynchronously or deferred?

**Perceived Performance**
- Is there a loading indicator or skeleton screen while content loads?
- Is above-the-fold content prioritized (no layout shift as content loads)?
- Are interactions responsive (no perceptible delay on click/tap)?
- Are optimistic UI updates used where appropriate?

**Runtime Performance**
- Are animations using GPU-accelerated properties (`transform`, `opacity`) rather than layout-triggering properties (`width`, `height`, `top`, `left`)?
- Are scroll event handlers debounced or throttled?
- Are large lists virtualized?
- Are expensive computations memoized or deferred?

**Asset Optimization**
- Are unused CSS and JavaScript removed (tree-shaking, code splitting)?
- Are images using modern formats (WebP, AVIF) with fallbacks?
- Are icon systems efficient (SVG sprites or icon font, not individual image files)?
- Is there evidence of excessive dependency size (large bundles)?

**Core Web Vitals Awareness**
- **LCP (Largest Contentful Paint)**: Is the largest element above the fold loading quickly?
- **FID/INP (Interaction to Next Paint)**: Are interactions responsive without long tasks blocking the main thread?
- **CLS (Cumulative Layout Shift)**: Are dimensions set on images/embeds? Are fonts loaded without causing reflow?

### Performance Testing Recommendations
- **Lighthouse**: Run performance audit in Chrome DevTools
- **WebPageTest**: For detailed waterfall and filmstrip analysis
- **Core Web Vitals**: Check via Chrome DevTools Performance panel or PageSpeed Insights
- **Bundle analysis**: Use webpack-bundle-analyzer or similar tools

### Common Issues to Flag
- Unoptimized images (wrong format, oversized, not lazy-loaded)
- Render-blocking resources in the `<head>`
- Layout shift caused by dynamically loaded content or unsized images
- Excessive JavaScript bundle size
- Unthrottled scroll or resize handlers
- Animations that trigger layout recalculations
- Missing loading/skeleton states

---

## Dimension 5: UX Best Practices

Evaluate the interface against established usability principles and conventions.

### Nielsen's Usability Heuristics

1. **Visibility of System Status**: Does the UI keep users informed about what is happening (loading indicators, progress bars, confirmation messages, active states in navigation)?
2. **Match Between System and Real World**: Does the UI use language and concepts familiar to the user (not developer jargon)? Does it follow real-world conventions (e.g., shopping cart metaphor)?
3. **User Control and Freedom**: Can users easily undo, redo, go back, or cancel? Are there clear exit paths from any flow?
4. **Consistency and Standards**: Does the UI follow platform conventions? Are similar actions triggered the same way throughout?
5. **Error Prevention**: Does the UI prevent errors before they happen (disabling invalid options, confirmation dialogs for destructive actions, sensible defaults)?
6. **Recognition Rather Than Recall**: Are options, actions, and information visible rather than requiring users to remember them?
7. **Flexibility and Efficiency of Use**: Are there shortcuts or advanced features for power users without complicating the interface for beginners?
8. **Aesthetic and Minimalist Design**: Does every element serve a purpose? Is irrelevant or rarely needed information hidden or de-emphasized?
9. **Help Users Recognize, Diagnose, and Recover from Errors**: Are error messages written in plain language, specific about what went wrong, and suggesting how to fix it?
10. **Help and Documentation**: Is help available where users need it (tooltips, inline help, contextual guidance)?

### Additional UX Considerations

**Navigation and Wayfinding**
- Is the primary navigation clear and consistently placed?
- Can users always tell where they are (breadcrumbs, active nav states, page titles)?
- Are important features discoverable (not buried in menus)?
- Is navigation depth reasonable (3 levels or fewer)?

**Forms and Data Entry**
- Are labels clear and always visible (not placeholder-only)?
- Are required fields indicated?
- Is inline validation used where appropriate?
- Are error messages specific and placed near the relevant field?
- Do input types match the expected data (`type="email"`, `type="tel"`, etc.)?
- Is tab order logical?

**Feedback and Communication**
- Do interactive elements respond immediately to user input?
- Are success and error states clearly communicated?
- Are empty states informative and actionable?
- Are destructive actions guarded by confirmation?
- Are notifications and alerts non-intrusive and dismissible?

**Content and Information Architecture**
- Is content organized logically and predictably?
- Are headings descriptive and scannable?
- Is the most important content prioritized visually?
- Is microcopy (button labels, tooltips, empty states) clear, concise, and helpful?

**Cognitive Load**
- Is the interface simple enough for its purpose (not overwhelming)?
- Are complex tasks broken into manageable steps?
- Are sensible defaults provided?
- Is progressive disclosure used for advanced options?

### Common Issues to Flag
- Missing feedback for user actions (silent failures, no confirmation)
- Unclear or generic error messages ("Something went wrong")
- Navigation that hides important features
- Forms with poor validation UX (errors only on submit, unclear messages)
- Inconsistent interaction patterns across the interface
- Excessive cognitive load (too many choices, too much information at once)
- Missing empty states or onboarding guidance
- Destructive actions without confirmation

---

## Dimension 6: Cross-Browser Compatibility

Evaluate the UI for potential cross-browser issues.

### What to Evaluate

**CSS Compatibility**
- Are modern CSS features used with appropriate fallbacks?
- Are vendor prefixes included where still necessary?
- Are CSS Grid and Flexbox used with awareness of older browser support?
- Are CSS custom properties (variables) used with fallbacks if legacy browsers must be supported?
- Are newer features like `container queries`, `has()`, `color-mix()`, or `subgrid` used with progressive enhancement?

**JavaScript Compatibility**
- Are modern JS features (optional chaining, nullish coalescing, etc.) transpiled if older browsers are targeted?
- Are polyfills included for APIs not supported in target browsers (IntersectionObserver, ResizeObserver, etc.)?
- Is the JavaScript framework/library version compatible with target browsers?

**HTML Compatibility**
- Are semantic HTML5 elements used with awareness that very old browsers may not style them by default?
- Are `<dialog>`, `<details>/<summary>`, and other newer elements used with fallbacks where needed?
- Are form input types (`date`, `color`, `range`) tested across browsers?

**Font and Typography**
- Are web fonts loaded with appropriate format fallbacks (`woff2`, `woff`)?
- Does the `font-display` strategy prevent invisible text during load?
- Are system font stacks used as fallbacks?

**Layout and Rendering**
- Are there known browser-specific layout bugs being triggered (e.g., Safari flexbox issues, Firefox sub-pixel rendering)?
- Are `scrollbar-gutter`, `overscroll-behavior`, and similar newer properties used with awareness of support?
- Do fixed/sticky positioned elements work correctly across browsers?

**Media and Assets**
- Are modern image formats (WebP, AVIF) served with `<picture>` fallbacks?
- Are video/audio elements using formats supported across target browsers?

### Browser Testing Checklist
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest, macOS and iOS)
- [ ] Edge (latest)
- [ ] Mobile Chrome (Android)
- [ ] Mobile Safari (iOS)
- [ ] Any additional browsers specified in project requirements

### Cross-Browser Testing Recommendations
- **BrowserStack** or **LambdaTest** for cross-browser testing
- **Can I Use** (caniuse.com) for checking feature support
- **Autoprefixer** for CSS vendor prefixes
- **Babel** for JavaScript transpilation
- **Browser DevTools** in each target browser

### Common Issues to Flag
- CSS features used without fallbacks for target browsers
- Missing vendor prefixes for properties that still require them
- JavaScript APIs used without polyfills for target browsers
- Image formats without `<picture>` fallbacks
- Browser-specific layout bugs (especially in Safari)
- Form input types that render differently across browsers
- Scrolling and overflow behavior inconsistencies

---

## Dimension 7: Code Quality of HTML/CSS/JS

Evaluate the quality, maintainability, and correctness of the frontend source code.

### HTML Quality

**Semantics and Structure**
- Is semantic HTML used throughout (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`)?
- Are headings used for structure (not just styling) with a proper hierarchy?
- Are lists, tables, and other structural elements used for their intended purpose?
- Is `<div>` and `<span>` usage limited to cases where no semantic element applies?
- Is the document outline logical and meaningful?

**Correctness**
- Does the HTML validate (no unclosed tags, invalid nesting, duplicate IDs)?
- Are `lang`, `charset`, and `viewport` meta tags present and correct?
- Are `alt` attributes on all images?
- Are form elements properly associated with labels?
- Are `id` values unique?

**Best Practices**
- Is the HTML clean and readable (proper indentation, logical ordering)?
- Are data attributes used for JavaScript hooks instead of classes?
- Are inline styles avoided in favor of CSS classes?
- Are deprecated elements and attributes avoided?

### CSS Quality

**Architecture and Organization**
- Is CSS organized methodically (component-based, BEM, utility classes, CSS modules, or CSS-in-JS)?
- Are CSS custom properties (variables) used for theming and repeated values?
- Is specificity kept low and manageable (avoiding `!important`, deep selectors, IDs as selectors)?
- Is there a clear naming convention?

**Maintainability**
- Are magic numbers avoided (values explained via variables or comments)?
- Are responsive styles organized logically (mobile-first or desktop-first, consistently)?
- Is duplicate CSS minimized?
- Are shorthand properties used appropriately?

**Modern Practices**
- Is Flexbox or Grid used for layout (not floats)?
- Are modern units used where appropriate (`rem`, `em`, `ch`, `vw`, `vh`, `dvh`)?
- Are `calc()`, `clamp()`, `min()`, `max()` used for fluid sizing?
- Are logical properties used for internationalization (`margin-inline`, `padding-block`)?

**Performance**
- Are selectors efficient (no deeply nested selectors, no universal selectors in expensive positions)?
- Is unused CSS eliminated?
- Are animations using compositor-friendly properties?

### JavaScript Quality

**Code Organization**
- Is JavaScript modular and well-structured (components, modules, clear separation of concerns)?
- Are functions small and single-purpose?
- Are variable and function names descriptive and consistent?
- Is the code DRY (Don't Repeat Yourself) without being overly abstract?

**Correctness and Safety**
- Are edge cases handled (null checks, empty arrays, missing data)?
- Is error handling present and meaningful (try/catch, error boundaries)?
- Are event listeners cleaned up when components unmount?
- Are memory leaks avoided (no orphaned references, intervals, or subscriptions)?

**Modern Practices**
- Is modern JavaScript used (`const`/`let` over `var`, arrow functions, template literals, destructuring)?
- Are async operations handled properly (`async`/`await`, proper error handling)?
- Are TypeScript types used if the project uses TypeScript (no excessive `any`)?

**DOM Interaction**
- Is direct DOM manipulation minimized when using a framework?
- Are event handlers delegated where appropriate?
- Are DOM queries cached rather than repeated?
- Is `innerHTML` avoided in favor of safer alternatives?

**Security**
- Is user input sanitized before rendering (no XSS vulnerabilities)?
- Is `innerHTML` or `dangerouslySetInnerHTML` used safely?
- Are sensitive data not exposed in client-side code?
- Are Content Security Policy headers considered?

### Common Issues to Flag
- Non-semantic HTML (div/span soup)
- Invalid or malformed HTML
- Overly specific CSS selectors or excessive `!important` usage
- Inline styles used extensively
- Unused CSS or JavaScript
- JavaScript that directly manipulates DOM in a framework context
- Missing error handling
- Potential XSS vulnerabilities
- Inconsistent coding style
- Large monolithic files that should be split

---

## Review Output Format

Structure your review report as follows:

### Executive Summary
- Overall quality assessment (2-3 sentences)
- Top 3 strengths
- Top 3 areas requiring attention
- Overall risk level for launch (if applicable)

### Findings by Dimension

For each of the seven dimensions, provide:

**[Dimension Name]**
- **Score**: Strong / Adequate / Needs Improvement / Critical Issues
- **Strengths**: What is done well
- **Issues Found**: Each issue should include:
  - **Severity**: CRITICAL / HIGH / MEDIUM / LOW
  - **Description**: What the issue is
  - **Impact**: Who is affected and how
  - **Location**: Where in the UI or code
  - **Recommendation**: Specific, actionable fix
  - **Reference**: Relevant standard or guideline (WCAG criterion, MDN link, etc.)

### Severity Definitions

- **CRITICAL**: Blocks users from completing core tasks, prevents access for entire user groups, security vulnerability, or data loss risk. Must fix before launch.
- **HIGH**: Significantly degrades experience for many users, major WCAG AA violation, or major code quality problem. Should fix before launch.
- **MEDIUM**: Creates friction but has workarounds, minor inconsistency, or improvement that would meaningfully enhance quality. Plan to fix soon.
- **LOW**: Polish item, minor enhancement, or best-practice recommendation. Address when convenient.

### Prioritized Action Items
- Numbered list of all issues, ordered by severity (CRITICAL first, then HIGH, MEDIUM, LOW)
- Each item should be a concise, actionable task

### Recommended Tools and Next Steps
- Suggest relevant automated tools for further testing
- Recommend manual testing procedures
- Suggest areas for deeper investigation if needed

---

## Communication Guidelines

When delivering the review:
- Begin with what is done well before discussing problems
- Be specific and actionable (not "improve the design" but "increase the contrast ratio of body text from 3.2:1 to at least 4.5:1")
- Explain the user impact of each issue (not just the technical violation)
- Provide code examples for fixes when reviewing code
- Reference specific standards and guidelines (WCAG criteria, MDN docs)
- Prioritize clearly so the team knows what to fix first
- Be constructive, not dismissive
- Acknowledge project constraints when making recommendations
- Distinguish between objective issues (WCAG violations, HTML errors) and subjective suggestions (design preferences)
