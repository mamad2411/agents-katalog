---
name: document-generation-docx-report-generation
description: "Template-first structure, style hierarchy over direct formatting, and programmatic population patterns."
---
# Generate professional DOCX reports programmatically

> Template-first structure, style hierarchy over direct formatting, and programmatic population patterns.

**Track:** ✍️ Technical Writing · **Domain:** Document Generation · **Level:** foundation · **~30 min**

**Who this is for:** Technical Writers, Developer Advocates, Engineers Who Document, Content Leads

## When to Use This Skill

Template-first structure, style hierarchy over direct formatting, and programmatic population patterns.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Build a template with named styles; generate content INTO styles, never inline formatting
2. Separate content model from rendering: data → sections → document order
3. Handle tables via real table objects, not tab-separated text
4. Embed charts as images with alt text; native chart XML only when editable output required
5. Validate output opens correctly in Word AND LibreOffice before delivering
6. Keep generation code deterministic: same inputs, byte-comparable outputs

## Common Pitfalls

- Direct formatting soup making template updates impossible
- Generated docs failing validation in non-Word viewers

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill document-generation-docx-report-generation
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill document-generation-docx-report-generation -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills