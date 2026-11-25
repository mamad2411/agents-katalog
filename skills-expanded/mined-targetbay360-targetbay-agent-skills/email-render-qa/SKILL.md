---
name: email-render-qa
description: Use when a built email needs checking for whether every recipient can actually read it — how it behaves on a narrow phone screen, in dark mode, with images blocked, and for someone using a screen reader; whether alt text, contrast, link text and the plain-text part hold up; and whether the footer and opt-out survive. Answers "is this email ready to send?", "will this break in dark mode?" and "does it work with images off?". Use content-optimization when the wording itself is the problem, and email-quality-auditor for the whole pre-send gate of which rendering is one part.
license: MIT
metadata:
  targetbay.display_name: Email Render QA
  targetbay.version: "1.0.0"
  targetbay.category: content
  targetbay.requires: email_sms.template_management, email_sms.campaign_analytics, email_sms.store_profile
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Email Render QA

## Purpose

Decide whether a built message is readable by the whole list rather than by the person who designed
it — across narrow screens, dark mode, blocked images and assistive technology — and decide which of
the defects found must be fixed before sending and which may ship.

The failure this skill exists to prevent: a message that arrives and cannot be read. It costs
exactly as much as one that never arrived, but nothing in the sending report shows it, because a
recipient who cannot read the message simply does not act. The single-large-image email and the
white-logo-on-white-background dark mode failure are the two most common versions.

Design guidance is not restated here. The visual decisions live in
[targetbay-email-template-design](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-template-design)
and the accessibility rules in
[targetbay-email-sms-best-practices](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-sms-best-practices);
this skill decides what to do about a specific message against them.

## When to Use

- A campaign or template is built and needs checking before it goes anywhere near a send
- Deciding whether a rendering defect is a blocker or an acceptable imperfection
- A message reportedly "looks broken" for some recipients and the cause is unknown
- Auditing an existing template library for defects that repeat across every send
- Checking that a template still holds after a change to its modules or brand colours

## When Not to Use

- The wording, offer or subject line is the problem. Use
  [content-optimization](../content-optimization/SKILL.md).
- The whole pre-send gate is needed — audience, consent, frequency, conflicts and deliverability as
  well as rendering. Use [email-quality-auditor](../email-quality-auditor/SKILL.md), which composes
  this skill.
- The merge fields and their fallbacks are the concern. Use
  [dynamic-content-personalizer](../dynamic-content-personalizer/SKILL.md), which owns what each
  personalised element resolves to; this skill checks only that the empty case renders.
- The message is not arriving at all. Use [deliverability-qa](../deliverability-qa/SKILL.md).
- The question is which channel should carry the message. Use
  [channel-optimization](../channel-optimization/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The built message, including its HTML and plain-text part | The object being checked | Blocked |
| Image assets and their alt text | Images-off and screen-reader behaviour | Blocked |
| Link targets and their visible text | Broken and undescriptive links are the most common defect | Blocked |
| Brand colour values used in the template | Contrast, and what happens when dark mode inverts them | Partial; contrast cannot be judged |
| Which clients and devices this store's opens come from | Ranks the defects by how many recipients they reach | Partial; every defect is weighted equally |
| The footer, opt-out and sender identity block | A missing or broken opt-out is a hard stop, not a defect | Blocked |
| Locale and writing direction | Alignment and directionality for non-Latin or right-to-left audiences | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.template_management` | The message itself — markup, modules, plain-text part, footer block |
| `email_sms.campaign_analytics` | Which clients and devices this store's recipients actually use, to weight defects |
| `email_sms.store_profile` | Brand colours, locale and writing direction |

## Decision Process

```
1. Confirm the message can be read at all      <- opt-out present, plain-text part present
2. Check the images-off view first             <- the harshest view, and the cheapest to fail
3. Check the narrow-screen view                <- most opens are on a phone
4. Check the dark-mode view                    <- inverted brand colours, transparent logos, shadows
5. Check assistive-technology behaviour        <- alt text, link text, heading order, language
6. Check links and their targets resolve
7. Weight each defect by the share of this store's recipients it reaches
8. Split into must-fix and may-ship, and say why each landed where it did
```

## Decision Rules

Binding: [../../rules/content-rules.md](../../rules/content-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/personalization-rules.md](../../rules/personalization-rules.md).

- A missing, broken or hidden opt-out is not a rendering defect. It stops the send (N9, S7).
- Accessibility is a requirement, not a polish step (N8). Missing alternative text on a meaningful
  image and undescriptive link text are defects, not preferences.
- The message must carry its meaning with images off. A message that is one large image fails for
  the recipients who block images and for everyone using a screen reader.
- Defect severity is weighted by the share of *this store's* recipients affected, read from its own
  client and device mix, never from a published distribution (G2).
- Check the empty case for every personalised element (P12). A greeting that renders as a blank or a
  literal placeholder is a render failure even when the personalisation logic is correct.
- One primary call to action, and it must be reachable and tappable at narrow width (N2).
- Dark mode is a recipient setting, not an edge case. Colours are checked in both appearances, and a
  transparent or single-colour logo is checked against the inverted background.
- Subject line, preheader and first screen are checked together as the opening unit — a preheader
  that renders as the message's first body text is a defect
  ([../../knowledge/email-principles.md](../../knowledge/email-principles.md)).
- Never report a check that was not run. Where a view could not be inspected, say the view is
  unchecked rather than implying it passed (G15, S12).
- Recommend fixes, never apply them. Editing the template belongs to the skill that owns it.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read the built message, assets, links, brand values, client and device mix | `read_only` |
| ANALYZE | Run each view; locate defects; weight them by recipients affected | `analysis` |
| PLAN | Must-fix and may-ship lists, each defect with its cause and remedy | `recommendation` |
| PREVIEW | Present the lists with the share of recipients each defect reaches | `recommendation` |
| VALIDATE | Run the checks below | — |
| MEASURE | Whether the defect class recurs in the next build, indicating a template rather than a campaign problem | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: a verdict per view — images off,
narrow screen, dark mode, assistive technology, links, footer; the must-fix list with the rule each
defect breaches and its remedy; the may-ship list with what is being accepted; the share of this
store's recipients each defect reaches; and the views that could not be checked, named explicitly.

## Validation

- [ ] Opt-out present, visible and functional — otherwise the result is blocking, not advisory (N9, S7)
- [ ] Plain-text part present and carrying the same offer
- [ ] Images-off view checked and the message still carries its meaning
- [ ] Narrow-screen view checked, primary call to action reachable (N2)
- [ ] Dark-mode view checked, including logo and brand colours against an inverted background
- [ ] Alternative text present on meaningful images, empty on decorative ones (N8)
- [ ] Link text describes its destination; every target resolves
- [ ] Empty case checked for every personalised element (P12)
- [ ] Defects weighted by this store's own client and device mix, not a published one (G2)
- [ ] Unchecked views named rather than omitted (G15)
- [ ] No fix applied — recommendations only

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read the message, assets and client mix | `read_only` / `analysis` | None |
| Report defects and remedies | `recommendation` | None |
| Apply a fix to the template | `mutation` | Out of scope; owned by the skill that holds the template |
| **Send despite a must-fix defect** | `high_impact` | **Explicit**, and never for a missing opt-out (S7) |

## Examples

**"Is this Black Friday email ready to send?"**
Finds the hero is a single image carrying the entire offer, which means the discount is invisible to
recipients with images blocked and to screen readers. Finds the brand's dark navy footer text
disappears against the inverted background in dark mode, and one product tile links to a page that
no longer resolves. Weights them: the hero affects a meaningful share of this store's opens, the
footer affects the share on clients that force dark mode, and the dead link affects everyone who
clicks it. Must-fix: live text for the offer and the broken link. May-ship: the footer, with the
remedy recorded for the template rather than this campaign. Rejected: a full template rebuild, which
the campaign's timeline does not allow and which two fixes make unnecessary.

**"Some customers say our emails look broken but we can't reproduce it."**
Establishes that the reports cluster on a client family that represents a modest but real share of
this store's opens, and reproduces the defect as a layout table that reflows at narrow width.
Recommends the structural fix at template level rather than per campaign, because the same defect
will recur in every send built from it. States plainly that one reported symptom could not be
reproduced and remains unexplained, rather than closing it.

## Failure Handling

| Situation | Response |
|---|---|
| The built message is unavailable | **Blocked.** There is nothing to check; do not review a description of the message instead |
| Plain-text part missing | Report as a must-fix defect rather than generating one — generating it hides the omission from the template |
| Opt-out missing or broken | **Blocked**, and stated as a stop rather than a defect (N9, S7) |
| Alt text unavailable for inspection | **Partial.** Report the images-off view as unchecked; do not assume alt text exists |
| Brand colour values unavailable | **Partial.** Report contrast and dark mode as unchecked rather than eyeballing them (G15) |
| Client and device mix unavailable | **Partial.** Present defects unweighted and say the ranking is by defect class, not by reach |
| A view cannot be rendered or inspected | Name the view as unchecked. Never infer that it passes from another view passing (S12) |
| Defect found but the send is imminent | Present the must-fix list and the blast radius, and let a human decide. Never quietly downgrade a must-fix to may-ship |

Degraded outcomes set `status` and populate `unmet_requirements`.
