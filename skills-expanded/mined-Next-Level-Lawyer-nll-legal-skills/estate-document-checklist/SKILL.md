---
name: estate-document-checklist
description: Generate a client-specific checklist of estate planning documents (will, trust, powers of attorney, healthcare directive) needed based on asset profile and family structure. Use whenever the user asks what estate planning documents a client needs, wants a checklist for a new estate plan engagement, or wants to compare a client's existing documents against what's recommended.
---

# Estate Plan Document Checklist Generator

Produces the recommended document set for a specific client's asset profile and family structure, not a generic "everyone needs a will" list.

## Workflow

1. **Gather the profile**: marital status, children (including from prior relationships), asset types (real property, business interests, retirement accounts, life insurance), rough estate size, and any special circumstances (minor beneficiaries, special-needs beneficiary, blended family, out-of-state property, non-citizen spouse).
2. **Recommend the core document set**: last will and testament, revolving trust if warranted (multi-state property, probate avoidance goals, privacy), durable power of attorney (financial), healthcare power of attorney/proxy, HIPAA authorization, living will/advance directive.
3. **Flag situation-specific additions**: special-needs trust (special-needs beneficiary), QDOT (non-citizen spouse, estate tax exposure), pour-over will (if using a trust), guardian nominations (minor children), business succession documents (business interests).
4. **If existing documents are provided**, mark each as Current / Outdated (flag if older than ~5 years or predates a major life event) / Missing.
5. **Note beneficiary designation review** separately — retirement accounts and life insurance pass outside the will/trust via beneficiary designation, and this is one of the most commonly missed items.

## Output format

```
## Recommended Estate Plan — [Client name]

### Core Documents
- [ ] Will/Trust — status
- [ ] Durable POA (financial) — status
- [ ] Healthcare POA / Proxy — status
- [ ] HIPAA Authorization — status
- [ ] Living Will / Advance Directive — status

### Situation-Specific
- [ ] [item] — why it applies

### Beneficiary designations to review
- [account type] — [currently unknown / needs confirmation]
```

## Document Output Format

For a deliverable version, use the `docx` skill:

- **Header:** firm name/logo placeholder, client name, "Recommended Estate Plan" title, date.
- **Body:** real checkbox lists or a two-column table (document / status), Word heading styles for Core Documents vs. Situation-Specific sections.
- **Beneficiary designation review:** set apart visually (shaded callout) so it doesn't get lost among the document checkboxes — it's easy to miss and consequential when missed.
- **Typography:** Calibri or Arial 11pt, 1" margins.

## Notes

- Beneficiary designation review should be flagged every time real property/retirement/insurance assets are involved — it's the most common gap.
- Don't assert specific tax thresholds (estate tax exemption amounts) without verifying current figures — flag that these should be checked against current law.
