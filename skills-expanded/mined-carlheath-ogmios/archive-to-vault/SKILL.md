---
name: archive-to-vault
description: |
  Smart routing from the Ogmios KNOWLEDGE area to a configured Obsidian vault.
  Reads a KNOWLEDGE node (or direct input), analyses entity type, picks the
  right vault template + target folder, creates a file with correct frontmatter,
  updates the KNOWLEDGE node's `vault_link`.

  [WHAT] Routing skill from Ogmios → vault. Seven entity types map to vault MOCs.
  No vault structure changes — uses the user's existing templates and MOCs.

  [WHEN] Use when: "save it to the vault", "archive this", "move to the vault",
  "save in the vault".

  [LANGUAGE] Configurable. Strict vault convention.
argument-hint: "[KNOWLEDGE slug or direct entity data]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Archive to Vault

**Role:** smart routing from KNOWLEDGE → vault on the user's active request.

## Triggers

- "save to the vault"
- "archive this"
- "move X to the vault"
- "into the vault"

## Flow

### 1. Identify input

Two variants:
- **KNOWLEDGE slug** (e.g. `john-doe`): read `~/.claude/memory/KNOWLEDGE/{type}/{slug}.md`
- **Direct entity data** (frontmatter + body): from user prompt or pipe

### 2. Read entity type and map to vault

Configure per project. Default mapping for a generic vault:

| Ogmios type | Vault folder (default Unsorted) | Vault template | Classification in Links |
|-------------|--------------------------------|----------------|--------------------------|
| People | `Unsorted/` | `Person.md` | (per vault convention) |
| Organizations | `Unsorted/` | `Note.md` | `[[organization]]` + theme links |
| Places | `Unsorted/` | `Note.md` | `[[place]]` + place-name link |
| Events | `Unsorted/` | `Note.md` | `[[event]]` + relevant theme |
| Concepts | `Unsorted/` | `Concept.md` | (per vault convention) |
| Sources | `Unsorted/` | `Article.md` / `Zotero.md` | (per source type) |
| Research | `Unsorted/` | `Research.md` | (per vault convention) |

**Default folder is always `Unsorted/`** (common vault convention for new files). The user moves manually to MOC folders as needed.

### 3. Generate the vault file with correct frontmatter

```yaml
---
MOC: "[[People MOC]]"          # Determined by entity type
Created: YYYY-MM-DD
Modified: YYYY-MM-DD
Links:
  - "[[organization]]"            # Classification for Organizations
  - "[[topic1]]"
  - "[[topic2]]"
tags:
  - status-new                   # Only canonical status tags
Type:
---

# {Title}

{Body from KNOWLEDGE converted to vault format}
```

**Strict vault convention:**
- `tags:` ONLY status (status-new, status-active, status-done, status-draft)
- `Links:` wikilinks for all classification, themes, hierarchy
- `MOC:` exactly one, from the canonical list
- `Type:` empty for manual notes (or e.g. `[[Article]]` for the Article template)

### 4. Body conversion

KNOWLEDGE body uses a Miessler-style structure (Thesis/Background/Key Facts/Evidence/Notes).
Vault body follows the user's structure (heading + flowing prose or thematic structure).

Conversion:
- `## Thesis` → first paragraph in body (core claim)
- `## Background` → second paragraph
- `## Key Facts` → bullet list under "## Background" or similar
- `## Evidence` → "## Sources" or footnotes
- `## Notes` → "## Notes" or integrated

### 5. Update the KNOWLEDGE node's `vault_link`

After the vault file is created:

```yaml
# Before
vault_link:

# After
vault_link: "[[Unsorted/John Doe]]"
```

This is a **one-way coupling** (KNOWLEDGE → vault). Two-way (vault updates reflected back) is deferred.

### 6. User confirmation

Before the vault file is created, present:

```markdown
## Suggested archiving

**KNOWLEDGE node:** People/john-doe
**Vault file:** Unsorted/John Doe.md
**MOC:** [[People MOC]]
**Template:** Person.md
**Links:** [[ExampleOrg]], [[ExampleProject]], [[collaboration]]

OK to archive?
```

User: "yes" / "change X to Y" / "no, put it in Spaces/" etc.

## Special cases

### People in the People MOC

Vault has a `Person.md` template with specific fields per project convention. Map KNOWLEDGE → Person.md format.

### Organizations without a vault MOC

If the vault lacks a clear organisations MOC: default to `Note.md` with `MOC: "[[People MOC]]"` + `Links: ["[[organization]]", ...]`.

### Sources with Zotero

If the source was imported from Zotero (has `zotero-key` in frontmatter), use the `Zotero.md` template instead of `Article.md`.

## Safety and validation

- **Never overwrite an existing vault file** without user confirmation
- **Never modify vault templates** (the templates folder should be treated as read-only)
- **Never invent new MOCs** — only use the canonical set
- **Never invent new tags** beyond the configured status set

## Version history

- v3.0 (2026-05-02): initial public release.
