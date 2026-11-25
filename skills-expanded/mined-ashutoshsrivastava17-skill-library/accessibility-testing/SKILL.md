---
name: accessibility-testing
description: >
  Plan accessibility testing — WCAG 2.1 criteria, screen reader testing,
  keyboard navigation, color contrast, and assistive technology coverage.
  TRIGGER when: user says /accessibility-testing, needs to test for accessibility,
  or asks about WCAG compliance testing.
argument-hint: "[application or page to test]"
user-invocable: true
---
# Accessibility Testing Plan
## Process
### Step 1: Define WCAG Compliance Target
| Level | Criteria | Typical Requirement |
|-------|---------|-------------------|
| A | Basic accessibility | Minimum legal compliance |
| AA | Standard accessibility | Most common requirement |
| AAA | Enhanced accessibility | Best practice, not usually required |
### Step 2: Automated Testing
| Tool | What It Catches |
|------|----------------|
| axe / Lighthouse | Color contrast, missing alt text, ARIA issues |
| WAVE | Structural issues, reading order |
| Pa11y | CI/CD integration, regression checking |
### Step 3: Manual Testing
| Test | Method | WCAG Criteria |
|------|--------|-------------|
| Keyboard navigation | Tab through all interactive elements | 2.1.1 |
| Focus visibility | Verify focus indicators visible | 2.4.7 |
| Screen reader | Test with NVDA/JAWS/VoiceOver | 1.3.1, 4.1.2 |
| Color contrast | 4.5:1 for text, 3:1 for large text | 1.4.3 |
| Zoom | Content usable at 200% zoom | 1.4.4 |
| Motion | Animations respect prefers-reduced-motion | 2.3.3 |
| Form labels | All inputs have associated labels | 1.3.1 |
| Error identification | Errors are clearly described | 3.3.1 |
### Step 4: Assistive Technology Matrix
| AT | OS | Browser | Priority |
|----|-----|---------|----------|
| VoiceOver | macOS | Safari | High |
| NVDA | Windows | Chrome/Firefox | High |
| JAWS | Windows | Chrome | Medium |
| TalkBack | Android | Chrome | Medium |
### Step 5: Report Findings
| Issue | WCAG | Severity | Element | Recommendation |
|-------|------|----------|---------|---------------|
| [issue] | [criteria] | H/M/L | [selector] | [fix] |
## Output Format
```markdown
## Accessibility Report: [Application]
### Compliance Target: WCAG [level]
### Automated: [X issues found]
### Manual: [Findings by category]
### AT Testing: [Screen reader results]
### Recommendations: [Prioritized fixes]
```
## Quality Checklist
- [ ] Both automated and manual testing performed
- [ ] Screen reader testing with at least 2 AT combinations
- [ ] Keyboard navigation fully tested
- [ ] Color contrast verified
- [ ] Findings mapped to WCAG criteria
## Edge Cases
- For SPAs, test dynamic content and route changes with screen readers
- For data visualizations, ensure alternative text descriptions
- For video content, verify captions and audio descriptions
