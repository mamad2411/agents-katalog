---
name: signup
description: "Signup, registration and account-creation flow optimization. Use when signup conversion, friction or trial activation is underperforming."
metadata:
  version: 2.0.0
---

# Signup Flow CRO

Cut friction, raise completion, and leave users ready to activate. Read `.agents/product-marketing.md` (or `.claude/product-marketing.md`) first when it exists.

## Assess first

Ask only what is missing: flow type (free trial, freemium, paid, waitlist; B2B or B2C), steps and required fields today, completion rate and where users drop, compliance needs, and what happens right after signup.

## Principles

1. **Fewest fields.** Essential: email (or phone) and password. Often: name. Usually deferrable: company, role, team size, phone, address. For each field ask whether the product needs it now, whether progressive profiling can collect it later, whether it can be inferred (company from email domain).
2. **Value before commitment.** Let people experience the product before the account where possible.
3. **Lower perceived effort.** Progress indicator if multi-step, grouped fields, smart defaults, pre-fill.
4. **Remove uncertainty.** "Takes 30 seconds", what happens next, no surprise steps or hidden requirements.

Per-field rules and flows by product type (B2B trial, B2C app, waitlist, e-commerce): [references/fields-and-patterns.md](references/fields-and-patterns.md).

## Decisions

- **Single step** for 3 or fewer fields, simple B2C, high-intent traffic. **Multi-step** for more than 3 or 4 fields or when segmentation is needed.
- Multi-step: easy questions first (email), harder ones after commitment, each step completable in seconds, back navigation, progress saved across refresh. Progressive commitment: email only, then password and name, then optional customization.
- **Social auth** often converts better than email: prominent, visually separated from the email form. B2C: Google, Apple, Facebook. B2B: Google, Microsoft, SSO.
- Email: single field, no confirm field, typo hints (gmial.com to gmail.com). Password: show toggle, rules upfront and updating live, allow paste, strength meter over rigid rules, offer passwordless or magic link.
- Defer email verification until needed and let users explore while it is pending: explain what to do, easy resend, spam-folder reminder, option to change the email.

## Trust and errors

- Near the form: "No credit card required" (only if true), trial length, privacy line, testimonial, relevant security badge.
- Validate inline, name the problem specifically ("Email already registered" with a recovery path), keep entered values, focus the failing field.
- Labels stay visible; placeholders hold examples only. Help text only where needed, next to the field.

## Mobile

Touch targets 44px+, the right keyboard type per field (email, tel), autofill, single column, sticky CTA, social auth and pre-fill to cut typing. Test on real devices.

## Measure

Form start rate, completion rate, field-level drop-off, time to complete, error rate by field, mobile vs desktop, social vs email ratio, time between steps. Track focus, blur and error per field.

## Output

- **Findings**: issue, impact (estimated if possible), fix, priority (High/Medium/Low).
- **Changes** grouped as quick wins (same day), high-impact (week-level), and test hypotheses.
- **Redesign** if requested: field set with rationale, order, copy for labels, placeholders, buttons and errors, layout.

Test ideas (layout, fields, auth options, CTA text, trial length, card required vs not, verification timing, post-submit): [references/experiments.md](references/experiments.md).

Related: `onboarding` for what happens after signup; `cro` for the landing page leading to it and for non-signup forms.
