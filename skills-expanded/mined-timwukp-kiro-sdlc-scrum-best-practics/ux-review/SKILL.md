---
name: ux-review
description: Run UX review checklist for banking user flows, validate WCAG accessibility compliance, assess security UX patterns, and review customer interface design
---

# UX Review Skill

## When to Use
Invoke when reviewing wireframes, user flows, or UX designs for banking customer-facing applications, with emphasis on security-conscious user experience.

## Banking UX Principles
1. **Trust**: Clear, professional design that inspires confidence
2. **Clarity**: Financial information must be unambiguous
3. **Accessibility**: WCAG 2.1 AA minimum for all customer interfaces
4. **Security perception**: Visible security indicators (lock icons, session timers)
5. **Error prevention**: Confirmation dialogs for irreversible financial actions

## Review Checklist
- [ ] User flow covers happy path and all error states
- [ ] Financial amounts always show currency code
- [ ] Confirmation step before any money movement
- [ ] Session timeout warning at 2 minutes before expiry
- [ ] Keyboard navigation works for all interactive elements
- [ ] Color contrast ratio >= 4.5:1 for all text
- [ ] Screen reader compatible (ARIA labels, semantic HTML)
- [ ] Mobile responsive (320px minimum viewport)
- [ ] Loading states for all async operations
- [ ] Empty states designed (no accounts, no transactions)

## Banking-Specific UX Patterns
- Account selector: show account name + last 4 digits + balance
- Transaction list: date, description, amount (color-coded debit/credit), running balance
- Transfer flow: source -> amount -> destination -> review -> confirm -> receipt
- Error messages: never expose internal system details to customers

## Security UX Patterns

### Anti-Phishing UX
- Consistent branding across all screens (logo, colors, typography)
- Display personalized security image/phrase on login to prove authenticity
- Never include clickable links to external domains in notifications
- Clearly distinguish bank communications from third-party content
- Show the official domain prominently in all communications

### Secure Error Messages
- Never expose system internals (no stack traces, SQL errors, or server paths)
- Use generic messages: "Something went wrong. Please try again."
- Provide actionable guidance without revealing system architecture
- Log detailed errors server-side with correlation IDs for support
- Never confirm or deny existence of accounts/users in error messages

### Session Timeout UX
- Display countdown warning 2 minutes before session expiry
- Allow one-click session extension without losing current work
- Graceful re-authentication: preserve form state and redirect after login
- Clear visual indicator of active session status
- Automatic secure logout with confirmation message

### Security Indicator Visibility
- Lock icon visible during all authenticated sessions
- Secure connection badge on sensitive pages (transfers, settings)
- Transaction signing UX: clear display of what is being signed
- Visual confirmation of encryption status for sensitive operations
- Device trust indicators (recognized device vs new device warning)

### MFA User Flow Design
- Clear explanation of why MFA is required at each step
- Multiple MFA options with easy switching (SMS, authenticator app, biometric)
- Graceful fallback when primary MFA method is unavailable
- Progress indicator during MFA verification
- Minimize friction: remember trusted devices for low-risk operations
- Recovery flow that does not compromise security (identity verification required)
