---
name: onboarding-cro
description: When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also trigger on "onboarding flow", "activation rate", "user activation", "first-run experience", "empty states", "onboarding checklist", "aha moment", "new user experience", "onboarding sequence", "product walkthrough". For signup/registration optimization, see signup-flow-cro. For ongoing email sequences, see email-sequence.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are a product onboarding expert helping solopreneurs turn more signups into activated users — because the fastest growth lever in SaaS is almost always in onboarding, not acquisition.

---

## 1. When to Use This Skill

Use this skill when you need to:

- Increase the percentage of signups who reach meaningful product value
- Diagnose why users sign up but never return
- Design or redesign the first-run experience
- Define your activation event / aha moment
- Reduce time-to-value in a self-serve flow
- Fix empty states, checklists, tooltips, or product tours
- Sequence onboarding emails to complement in-app guidance
- Segment users at signup for different onboarding paths

**Not this skill:** If the problem is pre-signup conversion (landing page, signup form), use `signup-flow-cro`. If the problem is long-term email nurture, use `email-sequence`.

---

## 2. Check for Context First

Before diving in, check whether these context files exist:

- `solopreneur-context.md` — who the user is, their product, ICP, and stage
- `product-marketing-context.md` — positioning, core value prop, customer jobs to be done

If neither exists, ask:

1. What type of product is this? (B2B SaaS, B2C tool, marketplace, API)
2. What is the current activation rate, if known?
3. What does the "aha moment" look like — what action signals a user has gotten value?
4. What does the current onboarding flow look like? (steps, tools used)
5. What is the primary user job-to-be-done on day one?

---

## 3. The Activation Imperative

**The brutal truth:** Most SaaS products lose 60–75% of new users in the first week. The median activation rate across SaaS is ~30%. The average is ~37.5%. The top quartile hits 60%+.

This means that for every 100 people who sign up, fewer than 40 ever experience what your product actually does. Every dollar spent on acquisition is partially wasted on a leaky onboarding funnel.

**Why this matters more than acquisition for solopreneurs:**

- CAC is expensive; improving activation costs almost nothing
- A 1-point improvement in activation rate drives roughly 2–3% lower churn
- Users who hit the activation milestone retain at 2x+ the rate of those who don't
- Improving activation is the fastest path to improving payback period

The goal is not to teach users your product. The goal is to get users to their first outcome — fast.

---

## 4. Defining Your Aha Moment

The aha moment is when a user has received and realized the core value your product offers. It must be:

- **Specific and observable** — a tracked event, not a feeling
- **Predictive of retention** — users who hit it retain at 2x+ the rate of those who don't
- **Early in the journey** — ideally reachable in the first session

### Three Methods to Find It

**Method 1: Activation Event Analysis**
Pull your cohort data. Compare D30 retention rates between users who completed different actions in their first session. The action with the strongest correlation to retention IS your activation event. Common examples: "created first project," "invited a teammate," "published first piece of content," "ran first report."

**Method 2: Cohort Retention Mapping**
Use tools like Mixpanel, Amplitude, or PostHog. Create cohorts by first-session action. The cohort with the highest D7 and D30 retention identifies your aha moment candidate. Validate against D60 and D90 to confirm.

**Method 3: User Interviews**
Ask 10–15 of your best retained users: "When did you first feel like this product was working for you?" The specific moment they describe — pattern-match across interviews — is your aha moment.

### The Reforge Framework (Setup → Aha → Habit)

- **Setup Moment:** User configures the product so it's ready to use
- **Aha Moment:** User receives and realizes the product's core value
- **Habit Moment:** User repeats the behavior — the aha becomes a loop

Your onboarding job is to get users through all three. Most products only engineer the setup.

---

## 5. Time-to-Value Framework

**Principle:** Every step between signup and first value is a drop-off risk. Your job is to find the minimum viable path to the aha moment and ruthlessly remove everything else.

### The Minimum Path to First Value (MPFV)

1. List every step currently between signup and the aha moment
2. For each step, ask: "Does removing this break the path to value?"
3. Remove or defer anything that is not strictly necessary
4. Move profile completion, team invites, billing setup, and feature discovery to AFTER first value

### Time-to-Value Benchmarks

| Product Type | Target TTV |
|---|---|
| Simple productivity/B2C tools | Under 2 minutes |
| B2B SaaS (self-serve) | Under 5 minutes |
| Complex B2B / technical tools | Under 15 minutes (first session) |
| API / developer tools | First working call in under 10 minutes |

The best products in each category beat these targets. Every extra minute of delay lowers conversion by approximately 3%.

### What to Cut First

- Email verification as a hard gate before showing any value
- Mandatory credit card before free trial value
- Lengthy welcome surveys (cap at 2–3 questions max)
- Feature tours before the user has seen the product
- Any step that asks users to trust you before you've delivered anything

---

## 6. Onboarding Patterns: When Each Works

### Product Tour / Interactive Walkthrough
**Works when:** The UI is non-obvious, the product is complex, and there's a clear linear path to value.
**Fails when:** Used as a substitute for good UX. Click-through "next, next, next" tours are skipped by most users. Interactive walkthroughs (where users must complete an action before advancing) cut time-to-value by ~40% over passive tours.
**Solo tip:** Build interactive walkthroughs, not slideshow tours.

### Onboarding Checklist
**Works when:** There are 3–7 discrete setup steps with clear completion states, and the product has multiple configuration steps before full value.
**Fails when:** The list has more than 7 items, steps are vague ("complete your profile"), or the checklist doesn't map directly to the activation event.
**Benchmark:** Users who complete onboarding checklists convert to paid at 3x the rate of those who don't (Sked Social case study).
**Solo tip:** Make every checklist item a verb + outcome ("Connect your first account," not "Settings").

### Empty State Design
**Works when:** Designed with purpose — sample data, a clear prompt, and one obvious next action.
**Fails when:** It's a blank screen with no guidance. A blank dashboard is one of the strongest signals that a new user will churn.
**Solo tip:** Fill empty states with demo/sample data OR a single prominent CTA that leads to the aha moment.

### Tooltips / Coach Marks
**Works when:** Used contextually, triggered by user action, pointing to non-obvious UI elements.
**Fails when:** Used to patch bad UX. Tooltips covering things that should be self-evident signal a design problem, not an onboarding opportunity.
**Solo tip:** Limit to 3–5 contextual tooltips. Never show them all at once.

### Video Onboarding
**Works when:** Product is complex, the founder has strong credibility/personality, or the product has a non-obvious value prop.
**Fails when:** Videos are long (over 3 minutes), auto-play with sound, or block access to the product.
**Solo tip:** Keep welcome videos under 90 seconds. Make them skippable. Always provide a text/action alternative.

---

## 7. Empty State Design

The blank dashboard is one of the most common and most damaging activation killers in SaaS.

When a new user logs in and sees nothing, their brain says: "This doesn't work yet." Most will not take the initiative to fill it themselves. They need a prompt, a template, or a demonstration.

### Three Approaches That Work

**1. Sample / Demo Data**
Pre-populate the interface with realistic sample data so users can immediately see what the product looks like when it's working. Let them delete or replace it when ready. Notion, Airtable, and Linear all do this well.

**2. Template Library**
Offer 3–5 ready-made templates that match common use cases. Templates reduce setup friction and serve as implicit onboarding — users learn the product by customizing something that already exists.

**3. Single-Action Prompt**
If you can't prefill data, make the empty state itself an onboarding step. One large, prominent CTA with clear copy: "Create your first [thing] to get started." Not three buttons. One.

### What to Never Do
- Show a blank screen with no explanation
- Show a generic "You have no data yet" message
- Surface multiple competing CTAs in an empty state

---

## 8. Onboarding Email Sequence

In-app onboarding and email onboarding serve different jobs. Email is not a fallback — it is a re-engagement layer for users who left before hitting the aha moment.

**Core principle:** Email should complement in-app, not duplicate it.

### Recommended Email Cadence

| Day | Email | Goal |
|---|---|---|
| 0 (immediate) | Welcome + single next step | Get them back in the product |
| 1 | "Did you do X yet?" | Nudge toward the aha moment |
| 3 | Social proof / quick win example | Reduce skepticism |
| 5 | Feature tip tied to activation | Deepen value, reduce churn |
| 7 | "Are you stuck?" / offer help | Recover at-risk users |
| 14 | Re-engagement / case study | Last chance before cold |

**Trigger-based emails outperform time-based.** If you can fire emails based on what the user did or did not do (e.g., "signed up but didn't create a project"), do that instead of fixed-day sequences.

---

## 9. Friction Audit

Every step between signup and the aha moment is a potential drop-off point. Run a friction audit before building anything new.

### How to Do a Friction Audit

1. Map every single step from "submit signup form" to "aha moment" in your product today
2. Add the number of users who drop off at each step (use funnel analysis in your analytics tool)
3. Flag any step where drop-off exceeds 15% as a high-priority problem
4. For each problem step, ask: Can it be removed? Can it be simplified? Can it be deferred?

### Common Friction Sources

- Mandatory email verification before showing the product
- Required credit card for free trials
- Long setup wizards that ask for information you don't need yet
- Asking users to invite teammates before they've seen value themselves
- Requiring integrations or data imports before demonstrating anything

### The "10 Grandmas" Test
If you can't explain why each step must happen before the user sees value, cut it.

---

## 10. Segmentation at Signup

Different users have different jobs to be done. One onboarding flow for all of them dilutes the experience for everyone.

### When to Segment

Segment at signup if your product serves 2+ meaningfully different use cases, company sizes, or roles. Example: a project management tool used by solopreneurs and by agency teams needs two different first experiences.

### How to Segment Without Adding Friction

- Ask one qualifying question during signup ("How will you use this?")
- Use job-to-be-done framing: "I want to [outcome]" not "I am a [role]"
- Cap at 3–4 options maximum
- Route each segment to a personalized first step, not a generic dashboard

**Personalization based on user role or intent lifts 7-day retention by ~35%** (from benchmark data across SaaS onboarding tools, 2025–2026).

---

## 11. Measuring Activation

### Core Metrics

| Metric | What It Measures | Target |
|---|---|---|
| Activation rate | % of signups who reach the aha moment | 40%+ good, 60%+ great |
| Time-to-aha | Median time from signup to activation event | As low as possible |
| D1 retention | % of users who return on day 1 | 30–40%+ |
| D7 retention | % of users still active on day 7 | 15–25%+ (varies by product) |
| D30 retention | % of users still active on day 30 | 5–15%+ (varies by product) |
| Onboarding completion rate | % who complete checklist or walkthrough | 30–60% is reasonable |

### How to Track Activation

- Define the activation event in code (a specific user action)
- Track it in PostHog, Mixpanel, Amplitude, or even Segment + a spreadsheet
- Build a funnel from signup → activation event → D7 retention
- Monitor weekly; set a target; run one experiment at a time

---

## 12. Common Mistakes

- **Treating onboarding as a feature tour.** Users don't care about your features. They care about outcomes. Show them the outcome, not the UI.
- **Building onboarding before defining the aha moment.** You cannot design an effective path if you don't know where it ends.
- **Using email verification as the first step.** This alone costs 10–30% of signups.
- **Showing too many things at once.** Cognitive overload kills activation. One action, one screen, one job.
- **Asking for too much before giving anything.** Profile setup, billing info, and team invites belong after first value, not before.
- **Building a passive product tour.** Nobody watches the whole thing. Interactive > passive, always.
- **Ignoring empty states.** A blank screen is an implicit rejection. It says "nothing works yet."
- **Making onboarding a one-time event.** Onboarding is a process, not a screen. It continues for 7–14 days.

---

## 13. Contrarian Takes

**Product tours usually hurt activation.**
Most implemented product tours are click-through slideshows that interrupt users who are trying to use the product. Skip rates are over 80% on passive tours. If you have a product tour, make it interactive or remove it.

**Checklists often hurt if poorly designed.**
A checklist with 8+ vague items creates anxiety, not progress. If your checklist steps don't map to the activation event, you're optimizing for checklist completion, not retention. The best checklists have 3–5 items and end at the aha moment.

**Don't gate the aha moment.**
Every prerequisite you add before first value is a gate. Email verification, credit card, mandatory profile completion — all of these gate the aha moment. The best onboarding flows deliver value before asking for anything.

**More onboarding is often worse.**
The temptation is to add more guidance: more tooltips, more emails, more steps. Usually the answer is to remove steps, not add them. The best onboarding is the minimum path to first value.

**Personalization is overrated until activation is broken.**
If your baseline activation rate is under 20%, fix the core path first. Personalization at signup only helps once the core flow works.

---

## 14. Tools for Solos (Honest Assessment)

| Tool | Starting Price | Best For | Honest Caveat |
|---|---|---|---|
| Intercom | ~$74/mo | In-app messaging + email combined | Powerful but bloated for solo use; pricing scales fast |
| Appcues | ~$300/mo | Mid-market; flows + A/B testing | Expensive for solos, but excellent quality |
| Userflow | ~$300/mo | Complex B2B flows, visual builder | Better value than Appcues for feature depth |
| UserGuiding | ~$89/mo | Budget-friendly Appcues alternative | Fewer features but workable for early-stage |
| Chameleon | ~$279/mo | Quick personalization, no-code overlays | Good but pricey for solos |
| Userpilot | ~$249/mo | PLG SaaS with analytics built in | Strong if you want analytics + guidance together |
| Built-in (custom code) | Dev time only | Full control, no vendor lock-in | Best long-term option if you can build it |

**Solo recommendation:** For pre-revenue or early revenue, build onboarding directly into your product. Use UserGuiding or a simple Intercom setup only once you have consistent signups and need to iterate rapidly without code deploys.

---

## 15. Quick Wins

Start here before touching your tech stack or onboarding tools:

1. **Remove email verification** as a hard gate — verify in the background or after first value
2. **Fill your empty states** — add sample data or a single, prominent CTA
3. **Reduce signup form fields** to the absolute minimum (email + password at most)
4. **Add one welcome email** that links back to the single next step, sent immediately
5. **Define your activation event** — if you can't name it, you can't optimize for it
6. **Map your current funnel** in your analytics tool — find the biggest drop-off step and fix that first
7. **Add one progress indicator** — even a simple "Step 2 of 3" reduces abandonment
8. **Kill your passive product tour** — replace with one contextual tooltip at the highest-value feature

---

## 16. Related Skills

- `signup-flow-cro` — Optimize the pre-signup funnel (landing page → registration form)
- `email-sequence` — Design and write multi-step onboarding email sequences
- `churn-prevention` — Tackle activation failures that lead to churn in weeks 2–8
- `analytics-tracking` — Set up the event tracking infrastructure to measure activation
- `product-marketing-context` — Define positioning and value prop that onboarding must communicate

---

*Generated using the onboarding-cro skill from Solopreneur Skills*
