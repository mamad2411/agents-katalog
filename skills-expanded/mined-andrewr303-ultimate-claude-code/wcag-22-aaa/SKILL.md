---
name: wcag-22-aaa
description: "Web development standard guide and engineering patterns for WCAG 2.2 Level AAA compliance. Use when building high-inclusion applications, meeting Level AAA enhanced criteria, implementing 7:1 contrast, 2.4.13 focus appearance, 44x44px target sizes, zero focus obscurity (2.4.12), cognitive load reduction, or passwordless authentication without cognitive function tests (3.3.9)."
risk: safe
source: local
date_added: "2026-09-16"
---

# WCAG 2.2 Level AAA Web Development Standard Guide

> Definitive engineering and design standard for building web applications compliant with WCAG 2.2 Level AAA (the highest tier of digital accessibility, designed for specialized applications, healthcare, government, cognitive support, and maximum inclusion).

## When to Use This Skill

- Developing applications required to meet WCAG 2.2 Level AAA or public-sector high-accessibility mandates.
- Designing specialized software for users with severe low vision, severe motor control challenges, or cognitive and memory impairments.
- Implementing enhanced visual contrast (7:1 normal text, 4.5:1 large text).
- Engineering focus indicators that satisfy **2.4.13 Focus Appearance** (minimum area, 3:1 contrast against both unfocused state and adjacent background).
- Implementing **2.4.12 Focus Not Obscured (Enhanced)** where no part of a focused element may be hidden under sticky content.
- Designing large touch targets (**2.5.5 Target Size Enhanced - 44×44px**).
- Building cognitive-friendly interfaces (jargon tooltips, abbreviations, reading level summaries, context-sensitive help, error prevention for all submissions, zero cognitive tests for auth).

---

## 1. What's New in WCAG 2.2 for Level AAA

WCAG 2.2 introduces 3 new Level AAA criteria:

| Criterion | Summary & Developer Mandate |
| :--- | :--- |
| **2.4.12 Focus Not Obscured (Enhanced)** | When a user interface component receives keyboard focus, **no part** of the component is hidden by author-created content (sticky headers, sticky footers, floating widgets, cookie banners). Unlike Level AA (which allows partial obscurity), Level AAA requires 100% full visibility. |
| **2.4.13 Focus Appearance** | When the focus indicator is visible, it must: <br>1. Have an area at least as large as a **2 CSS pixel thick perimeter** of the component. <br>2. Have a contrast ratio of at least **3:1** between the focused and unfocused states of the pixels in the indicator. <br>3. Have a contrast ratio of at least **3:1** against adjacent non-focus indicator colors. |
| **3.3.9 Accessible Authentication (Enhanced)** | A cognitive function test (e.g. memorizing usernames/passwords, solving puzzles, transcribing CAPTCHAs, or recognizing objects/images) is **not required** for any step in an authentication process. Unlike Level AA, Level AAA strictly forbids object and image recognition tests. |

---

## 2. Core AAA Principles & Requirements

### Principle 1: Perceivable (Enhanced)

#### 1.4.6 Contrast (Enhanced)
- **Normal text** (< 18pt / 24px or < 14pt / 18.66px bold): Minimum **7:1** contrast ratio against background.
- **Large text** (≥ 18pt / 24px or ≥ 14pt / 18.66px bold): Minimum **4.5:1** contrast ratio against background.
```css
:root {
  /* Level AAA compliant color tokens (7:1+ contrast on white/dark) */
  --color-text-aaa: #1e293b; /* 12.6:1 on #ffffff */
  --color-text-muted-aaa: #334155; /* 9.5:1 on #ffffff */
  --color-bg-aaa: #ffffff;
  --color-primary-aaa: #1d4ed8; /* 7.2:1 on #ffffff */
}
```

#### 1.4.8 Visual Presentation
For blocks of text, web applications must satisfy all 5 conditions:
1. **User Theme Controls**: Foreground and background colors can be selected by the user.
2. **Line Length Limit**: Width is no more than **80 characters** (or 40 glyphs for CJK).
3. **No Justified Text**: Text is NOT fully justified (`text-align: justify` is strictly forbidden). Use `text-align: left` (or `right` for RTL).
4. **Line & Paragraph Spacing**: Line spacing is at least **1.5** within paragraphs, and paragraph spacing is at least **2.25** times font size (1.5 times the line spacing).
5. **Horizontal Scroll Prevention**: Text can be resized up to **200%** without requiring horizontal scrolling on a desktop viewport.

```css
/* Level AAA Typography Class */
.prose-aaa {
  max-width: 75ch; /* Under 80 character limit */
  line-height: 1.6; /* >= 1.5 line height */
  text-align: left; /* Never justified */
}

.prose-aaa p + p {
  margin-top: 2.25em; /* >= 1.5x line spacing */
}
```

#### 1.4.9 Images of Text (No Exception)
- Raster images of text (PNG/JPEG) are prohibited completely, even when customizable (only exception is brand logos). Use pure CSS, Web fonts, or SVG with accessible text elements.

---

### Principle 2: Operable (Enhanced)

#### 2.1.3 Keyboard (No Exception)
- Every single interaction, feature, and visual control must be operable using keyboard only. There are **zero exceptions** (unlike Level A 2.1.1 which exempts freehand drawings). If a canvas or drawing feature exists, an equivalent structured numerical or keyboard coordinate input must be provided.

#### 2.2 Timing Limits (2.2.3, 2.2.4, 2.2.5, 2.2.6)
- **2.2.3 No Timing**: Timing is not an essential part of the event or activity, or time limits can be turned off entirely before starting.
- **2.2.4 Interruptions**: Push notifications, live score popups, and alert banners can be postponed or suppressed by the user.
- **2.2.5 Re-authenticating**: If an active session expires, the user can re-authenticate and continue their work without losing any entered form or state data.
- **2.2.6 Timeouts**: When an authenticated session contains a timeout that could result in data loss, the user is warned of the duration of inactivity that will cause data loss at the beginning of the interaction.

#### 2.3 Flashes & Animations (2.3.2 & 2.3.3)
- **2.3.2 Three Flashes**: Content contains zero instances of anything flashing more than 3 times in any 1-second period (zero exceptions).
- **2.3.3 Animation from Interactions**: Motion animation triggered by user interaction (parallax scrolling, button morphing, micro-interactions) can be disabled completely unless the animation is essential to the functionality.
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

#### 2.4 Navigation & Focus (2.4.8, 2.4.9, 2.4.10, 2.4.12, 2.4.13)
- **2.4.8 Location**: Breadcrumbs, site map, or step progression indicators must show the user's current location within the hierarchy of web pages.
- **2.4.9 Link Purpose (Link Only)**: The purpose of each link can be identified from the link text alone (e.g. "Download Annual Report 2026 PDF", never "Download", "More", or "Read").
- **2.4.10 Section Headings**: Section headings are used to organize all content chunks.
- **2.4.12 Focus Not Obscured (Enhanced - WCAG 2.2 AAA)**: When an element receives keyboard focus, **no part** of the element may be obscured by sticky headers, footers, or overlays.
- **2.4.13 Focus Appearance (WCAG 2.2 AAA)**: Focus indicators must have an area ≥ 2px perimeter, 3:1 contrast against unfocused state, and 3:1 contrast against adjacent background.

#### 2.5 Input Modalities (2.5.5 Target Size Enhanced & 2.5.6)
- **2.5.5 Target Size (Enhanced)**: The size of the target for pointer inputs is at least **44×44 CSS pixels**, except when:
  - Equivalent: Target is available through another control on the same page that meets 44×44px.
  - Inline: Target is in a sentence or block of text.
  - User Agent: Target is determined by user agent (browser native default checkboxes).
  - Essential: Specific presentation is essential (e.g., geographic map pins).
- **2.5.6 Concurrent Input Mechanisms**: Users can switch seamlessly between mouse, keyboard, touch screen, stylus, and voice control at any point without restricting input methods.

---

### Principle 3: Understandable (Enhanced)

#### 3.1 Readability (3.1.3, 3.1.4, 3.1.5, 3.1.6)
- **3.1.3 Unusual Words**: A mechanism is available for identifying specific definitions of words or phrases used in an unusual or restricted way, including idioms and jargon. Use `<dfn>` or glossary links.
- **3.1.4 Abbreviations**: A mechanism for identifying the expanded form of all abbreviations is available (using `<abbr title="expanded">` or expanding on first mention in text).
- **3.1.5 Reading Level**: When text requires reading ability more advanced than lower secondary education level (approx. 9th grade / age 14), supplementary content or a simplified summary must be provided.
- **3.1.6 Pronunciation**: Pronunciation guides are provided where the meaning of words is ambiguous without pronunciation (e.g. Japanese kanji readings using `<ruby>`).

#### 3.2 Predictability (3.2.5 Change on Request)
- Changes of context (navigating pages, opening popups, refreshing page) are initiated **only by user request** (e.g. clicking a button), never on input change, radio select, or focus.

#### 3.3 Input Assistance (3.3.5, 3.3.6, 3.3.9)
- **3.3.5 Error Prevention (All)**: For **all** web pages that require user submissions (not just legal/financial transactions):
  1. Submissions are reversible, OR
  2. Data entered is checked for errors and the user is provided an opportunity to correct them, OR
  3. A mechanism is available for reviewing, confirming, and correcting information before finalizing submission.
- **3.3.6 Context-Sensitive Help**: Context-sensitive help is provided for every form input field (via persistent help text or an accessible tooltip/button).
- **3.3.9 Accessible Authentication (Enhanced - WCAG 2.2 AAA)**: No cognitive function test (no passwords to recall, no CAPTCHAs, no math puzzles, and **no image/object recognition puzzles**). Authentication must use passwordless methods (WebAuthn/Passkeys, email magic links, or copy-paste friendly tokens).

---

## 3. Production Code Patterns for Level AAA

### Pattern 1: Focus Appearance Formula (2.4.13) & Zero Focus Obscurity (2.4.12)
To satisfy 2.4.13, the focus ring must have at least 3:1 contrast against both the unfocused element and adjacent background. A double outline (inner dark, outer light) is the gold standard:

```css
/* WCAG 2.2 AAA Focus Ring: Visible on ANY background (Dark or Light) */
:focus-visible {
  outline: 3px solid #005fcc; /* Outer high-contrast blue (3:1 against white) */
  outline-offset: 2px;
  box-shadow: 0 0 0 2px #ffffff; /* Inner separator (ensures contrast on dark backgrounds) */
}

/* Ensure 2.4.12: 100% of focused element is unobstructed by sticky headers */
:target,
[tabindex]:focus-visible,
input:focus-visible,
button:focus-visible,
a:focus-visible {
  /* Height of fixed navbar (e.g., 80px) + extra safety margin (24px) */
  scroll-margin-top: 104px;
  scroll-margin-bottom: 64px;
}
```

### Pattern 2: 44×44px Minimum Target Size (2.5.5)
```css
/* Enforce 44x44 CSS px for every interactive element */
.target-aaa {
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.625rem 1rem;
}

/* Expand hit area of compact icon buttons to 44x44px */
.icon-btn-aaa {
  position: relative;
  width: 28px;
  height: 28px;
  border-radius: 4px;
}
.icon-btn-aaa::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 44px;
  height: 44px;
  transform: translate(-50%, -50%);
}
```

### Pattern 3: Jargon Definition & Abbreviations (3.1.3 & 3.1.4)
```html
<p>
  The service uses 
  <abbr title="European Accessibility Act">EAA</abbr>
  regulations to enforce 
  <dfn id="def-vpat">
    <a href="#glossary-vpat" aria-describedby="tooltip-vpat">VPAT</a>
  </dfn>
  compliance across all digital channels.
</p>

<!-- Inline definition tooltip for screen reader and keyboard users -->
<div id="tooltip-vpat" role="tooltip" class="tooltip-aaa">
  <strong>VPAT:</strong> Voluntary Product Accessibility Template, a document evaluating product conformance with accessibility standards.
</div>
```

### Pattern 4: Context-Sensitive Help & Reversible Submission (3.3.5 & 3.3.6)
```html
<form action="/update-profile" method="POST" class="form-aaa" id="profile-form">
  <div class="field-group">
    <label for="tin-input" class="label-aaa">
      Tax Identification Number (TIN)
    </label>
    
    <!-- 3.3.6 Context-Sensitive Help -->
    <div class="field-help" id="tin-help">
      <span>Where do I find this? Your 9-digit TIN is printed on the upper right corner of your tax assessment notice.</span>
    </div>

    <input 
      type="text" 
      id="tin-input" 
      name="tin" 
      aria-describedby="tin-help"
      class="input-aaa" 
      required 
    />
  </div>

  <!-- 3.3.5 Review and Confirmation Step -->
  <button type="button" class="btn-aaa" onclick="openReviewModal()">
    Review and Confirm Changes
  </button>
</form>
```

### Pattern 5: Passkey Authentication (3.3.9 Accessible Auth Enhanced)
```typescript
/**
 * WCAG 2.2 AAA Compliant: Passwordless, Zero-Cognitive Test Authentication
 */
export async function authenticatePasskey(): Promise<boolean> {
  if (!window.PublicKeyCredential) {
    throw new Error('WebAuthn not supported');
  }

  // 1. Fetch challenge from backend
  const options = await fetch('/api/auth/webauthn-options').then(res => res.json());

  // 2. Browser triggers biometric/device PIN without memorizing complex secrets or solving puzzles
  const assertion = await navigator.credentials.get({
    publicKey: {
      ...options,
      challenge: Uint8Array.from(atob(options.challenge), c => c.charCodeAt(0)),
    },
  });

  // 3. Complete authentication
  const verifyRes = await fetch('/api/auth/webauthn-verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(assertion),
  });

  return verifyRes.ok;
}
```

---

## 4. Conformance Audit Protocol for Level AAA

1. **Automated Audit**: Run axe-core with tag `wcag2aaa`:
   ```bash
   npx @axe-core/cli https://example.com --tags wcag2aaa
   ```
2. **Contrast Inspection**: Measure all text against a 7:1 threshold and all non-text UI items against 3:1.
3. **Focus Verification**:
   - Check that every single interactive item has an indicator with ≥ 2px perimeter thickness.
   - Verify that focus is never even 1% obscured by sticky navigation or floating widgets.
4. **Target Size Inspection**: Inspect touch target bounding rectangles (`>= 44px` on both width and height).
5. **No Timing Check**: Confirm there are no un-extendable countdown timers, forced auto-refreshes, or sudden session drops.
6. **Authentication Check**: Verify users can authenticate entirely with WebAuthn/Passkeys or magic links without solving any cognitive tests.

---

## 5. Reference Files

- [checklist-aaa.md](file:///Users/kvivek/.gemini/config/skills/wcag-22-aaa/references/checklist-aaa.md): Complete WCAG 2.2 Level AAA success criteria checklist.
- [code-patterns-aaa.md](file:///Users/kvivek/.gemini/config/skills/wcag-22-aaa/references/code-patterns-aaa.md): Design tokens, theme color switchers, focus indicator calculators, and confirmation dialogs for AAA.
