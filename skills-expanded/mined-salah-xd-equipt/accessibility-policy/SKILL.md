---
name: accessibility-policy
description: "Writes website accessibility policies with WCAG compliance commitments and accommodation procedures. Use when creating an accessibility statement for your website."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Accessibility Policy

## When to Use This Skill

Use this skill when you need to:
- Write a website accessibility statement or policy
- Document your WCAG compliance commitments
- Create accommodation request procedures
- Outline your approach to digital accessibility

**DO NOT** use this skill for technical accessibility audits, WCAG remediation, or ADA compliance consulting. This is for the policy document itself.

---

## Core Principle

AN ACCESSIBILITY POLICY DEMONSTRATES YOUR COMMITMENT TO INCLUSIVITY — IT TELLS USERS WITH DISABILITIES WHAT TO EXPECT AND HOW TO GET HELP WHEN SOMETHING DOES NOT WORK.

---

## Phase 1: Inputs

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Website URL** | "What website is this policy for?" | No default — must be provided |
| **Business name** | "What is your business name?" | No default — must be provided |
| **WCAG target** | "What WCAG level are you targeting? (A, AA, AAA)" | WCAG 2.1 Level AA |
| **Known limitations** | "Are there any known accessibility issues?" | None identified |
| **Contact for accessibility** | "Who handles accessibility requests? (name, email, phone)" | No default — must be provided |

**GATE: Do not proceed without business name, website, and contact information.**

---

## Phase 2: Policy Document

```
## Accessibility Statement

**[Business Name]** is committed to ensuring digital accessibility
for people with disabilities. We continually work to improve the
user experience for everyone and apply relevant accessibility
standards.

### Conformance Status

We aim to conform to the Web Content Accessibility Guidelines (WCAG)
2.1 at Level [AA]. These guidelines explain how to make web content
more accessible to people with disabilities, including those with
visual, auditory, physical, speech, cognitive, language, learning,
and neurological disabilities.

### Measures We Take

[Business Name] takes the following measures to ensure accessibility:

- Include accessibility as part of our design and development process
- Provide ongoing accessibility awareness training for our team
- Use automated and manual testing tools to evaluate accessibility
- Seek user feedback on accessibility of our digital properties
- Review and update our accessibility practices regularly

### Technical Specifications

This website relies on the following technologies for conformance
with WCAG 2.1:
- HTML
- CSS
- JavaScript
- WAI-ARIA

These technologies are relied upon for accessibility with the
assistive technologies and user agents that our users employ.

### Known Limitations

While we strive for full accessibility, some areas of our website
may not yet be fully accessible:

[List any known limitations, e.g.:]
- [Third-party content (embedded videos, social media feeds) may
  not meet all accessibility standards]
- [Older PDF documents may not be fully accessible — we are working
  to remediate these]
- [Some interactive elements are being updated for improved screen
  reader compatibility]

We are actively working to resolve these issues. If you encounter
a barrier, please contact us.

### Feedback and Accommodation Requests

We welcome your feedback on the accessibility of [website/business].
If you encounter any accessibility barriers or need accommodations,
please contact us:

- **Email:** [accessibility email]
- **Phone:** [phone number]
- **Mailing address:** [address]

We aim to respond to accessibility feedback within [2-5] business days.

### Compatibility

Our website is designed to be compatible with the following assistive
technologies:
- Screen readers (JAWS, NVDA, VoiceOver)
- Screen magnification software
- Speech recognition software
- Keyboard-only navigation

### Assessment and Compliance Review

This website's accessibility was last assessed on [date] using:
- [Automated testing tools used, e.g., axe, WAVE, Lighthouse]
- [Manual testing, e.g., keyboard navigation, screen reader testing]
- [Third-party audit, if applicable]

We review our accessibility practices [annually / semi-annually].

### Enforcement

If you are unsatisfied with our response to your accessibility
concern, you may escalate by contacting [appropriate authority
or alternative dispute resolution].

---

This statement was last updated on [date].
```

---

## Phase 3: Implementation Checklist

```
## Accessibility Implementation Checklist

### Content
- [ ] All images have descriptive alt text
- [ ] Videos have captions and/or transcripts
- [ ] Color is not the sole means of conveying information
- [ ] Text has sufficient color contrast (4.5:1 minimum for normal text)
- [ ] Content is readable and functional at 200% zoom
- [ ] Links are descriptive (not "click here")

### Navigation
- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible
- [ ] Skip navigation link is provided
- [ ] Page structure uses proper heading hierarchy (H1, H2, H3)
- [ ] ARIA landmarks are used appropriately

### Forms
- [ ] All form fields have associated labels
- [ ] Error messages are clear and associated with the relevant field
- [ ] Required fields are clearly indicated
- [ ] Form instructions are provided before the form

### General
- [ ] Accessibility statement published and linked from footer
- [ ] Contact information for accessibility feedback is clear
- [ ] Team trained on creating accessible content
- [ ] Regular accessibility audits scheduled
```

---

## Phase 4: Delivery

Publish the accessibility statement on a dedicated page (e.g., /accessibility) and link from the website footer.

---

## Example: E-commerce Store

**Statement excerpt:** "ShopBright is committed to WCAG 2.1 Level AA compliance. Our checkout process supports keyboard navigation and screen readers. Product images include descriptive alt text. Known limitation: some vendor-provided product videos lack captions — we are working with vendors to add them. Contact accessibility@shopbright.com for accommodation requests."

---

## Anti-Patterns

- **Empty promises** — stating you are WCAG AA compliant when your site has not been tested is misleading and legally risky
- **No contact information** — the most important part of an accessibility statement is how users can report issues and get help
- **Set and forget** — accessibility requires ongoing attention as content and features change
- **Policy without action** — publishing a statement without actually testing and fixing accessibility issues provides false comfort
- **Ignoring third-party content** — embedded videos, social feeds, and widgets must also be accessible or disclosed as limitations

---

## Recovery

- **No accessibility testing done:** Run a free automated scan (WAVE, axe, Lighthouse) to identify major issues. Fix critical items first (keyboard navigation, alt text, color contrast).
- **Received an ADA demand letter:** Consult an attorney immediately. Begin remediation and document your efforts.
- **Third-party tools are not accessible:** Contact vendors about accessibility. If they cannot comply, consider alternatives or disclose as a known limitation.
- **Limited budget for accessibility:** Focus on the highest-impact items: keyboard navigation, alt text, heading structure, and color contrast. These address the most common barriers.
