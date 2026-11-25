---
name: playbook-technical-writing-document-pipeline
description: "DOCX reports and slide decks produced deterministically from content models."
---
# Playbook: Operate a generated-documents pipeline

> DOCX reports and slide decks produced deterministically from content models.

**Track:** 🗺️ Technical Writing · **Domain:** Journey Playbooks · **Level:** journey · **~65 min**

**Who this is for:** Technical Writers, Developer Advocates, Engineers Who Document, Content Leads

## When to Use This Skill

DOCX reports and slide decks produced deterministically from content models.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Generate professional DOCX reports programmatically: start with "Build a template with named styles; generate content INTO styles, never inline formatting"
2. Step 2 — Design slide decks as narratives, not bullet dumps: start with "Write the slide TITLES first as a story outline; if titles alone don't persuade, fix the narrative"
3. How it fits together: Styles and titles-first are what separate generation from word-processor cosplay.

### Referenced Skills

- `document-generation-docx-report-generation`
- `document-generation-slide-narrative-design`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill document-generation-docx-report-generation && npx skills add aniruddhaadak80/skills --skill document-generation-slide-narrative-design
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills