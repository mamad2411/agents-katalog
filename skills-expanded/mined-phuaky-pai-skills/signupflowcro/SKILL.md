---
name: SignupFlowCro
description: When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the user mentions "signup conversions," "registration friction," "signup form optimization," "free trial signup," "reduce signup dropoff," or "account creation flow." USE WHEN signup flow, registration, sign up.
---

# Signup Flow CRO

You are an expert in optimizing signup and registration flows. Your goal is to reduce friction, increase completion rates, and set users up for successful activation.

## Core Principles

### 1. Minimize Required Fields
Every field reduces conversion. Ask:
- Do we need this before they can use the product?
- Can we collect this later?
- Can we infer this from other data?

**Priority:** Email → Password → Name → Everything else (defer)

### 2. Show Value Before Commitment
- What can you show before requiring signup?
- Can they experience the product first?

### 3. Reduce Perceived Effort
- Show progress if multi-step
- Use smart defaults
- Pre-fill when possible

### 4. Remove Uncertainty
- Clear expectations ("Takes 30 seconds")
- Show what happens after signup

---

## Field Optimization

### Email
- Single field (no confirmation)
- Inline validation, check for typos (gmial → gmail)

### Password
- Show/hide toggle
- Show requirements upfront, not after failure
- Allow paste, consider passwordless

### Name
- Single "Full name" vs. First/Last (test this)
- Consider making optional

### Social Auth
- Place prominently (often higher conversion)
- B2C: Google, Apple, Facebook
- B2B: Google, Microsoft, SSO

---

## Single-Step vs. Multi-Step

### Single-Step Works When:
- 3 or fewer fields
- Simple B2C products
- High-intent visitors

### Multi-Step Works When:
- More than 3-4 fields needed
- Complex B2B products
- Need different types of info

### Multi-Step Best Practices
- Show progress indicator
- Lead with easy questions
- Each step completable in seconds
- Save progress (don't lose data)

---

## Trust & Friction Reduction

- "No credit card required" (if true)
- Privacy note: "We'll never share your email"
- Testimonial near signup form
- Security badges if relevant

### Error Handling
- Inline validation (not just on submit)
- Specific messages ("Email already registered" + recovery path)
- Don't clear form on error

---

## Mobile Optimization

- Larger touch targets (44px+)
- Appropriate keyboard types
- Autofill support
- Single column layout
- Sticky CTA button

---

## Key Metrics

- Form start rate (landed → started)
- Form completion rate (started → submitted)
- Field-level drop-off
- Social auth vs. email ratio
- Mobile vs. desktop completion

---

## Common Patterns

### B2B SaaS Trial
1. Email + Password (or Google auth)
2. Name + Company (optional: role)
3. → Onboarding flow

### B2C App
1. Google/Apple auth OR Email
2. → Product experience
3. Profile completion later

### Waitlist
1. Email only
2. Optional: Role/use case
3. → Confirmation

---

## Experiment Ideas

**Form Design:**
- Single-step vs. multi-step
- Reduce to minimum fields
- SSO prominent vs. email prominent

**Copy:**
- CTA: "Create Account" vs. "Start Free Trial"
- Add "No credit card required"

**Trial:**
- Credit card required vs. not
- Trial length (7 vs. 14 vs. 30 days)

---

## Questions to Ask

1. What's your current completion rate?
2. Do you have field-level analytics?
3. What data is required before product use?
4. What happens immediately after signup?

---

## Related Skills

- **OnboardingCro**: For post-signup optimization
- **FormCro**: For non-signup forms
- **PageCro**: For landing page leading to signup
- **AbTestSetup**: For testing signup changes
