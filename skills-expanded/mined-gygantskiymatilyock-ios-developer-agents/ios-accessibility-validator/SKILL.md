# iOS Accessibility Validator

Use this skill to audit iOS apps for accessibility compliance with Apple Human Interface Guidelines, WCAG 2.2 standards, and iOS accessibility best practices.

## When to Use

- When building new UI components
- Before app releases
- When improving accessibility
- When targeting accessibility certifications
- After receiving accessibility feedback
- When building apps for enterprise/government (Section 508)

## How to Apply

Read the full agent prompt from `agents/accessibility-validator/accessibility-validator.md` in the ios-developer-agents repository.

Follow the audit process:

1. **VoiceOver Compatibility** - Labels, hints, traits, element grouping, reading order
2. **Dynamic Type Support** - Text scaling, layout adaptation
3. **Color & Visual** - Contrast ratios (4.5:1/3:1), color independence, Dark Mode
4. **Motion & Animation** - Reduce Motion support, flashing content
5. **Touch Targets** - 44x44pt minimum, gesture alternatives
6. **Switch Control & Voice Control** - Keyboard access, scanning
7. **Audio & Haptics** - Captions, audio descriptions, alternatives
8. **Cognitive Accessibility** - Clear language, predictable behavior
9. **Accessibility APIs** - UIKit/SwiftUI implementation review

## Output Format

Provide structured findings with:
- Compliance summary (Apple HIG, WCAG 2.2 Level A/AA)
- Critical issues (blocks users)
- VoiceOver audit table
- Dynamic Type audit
- Color contrast audit
- Touch target audit
- Accessibility settings support table
