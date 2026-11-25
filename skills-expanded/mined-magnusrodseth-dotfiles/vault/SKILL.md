---
name: vault
description: Extract insights from conversations and store them in your Obsidian vault. Use when you want to capture learnings, how-to guides, brags, decisions, or any knowledge from the current chat into your second brain. Triggers on "save to vault", "store this in obsidian", "capture this learning", "add to vault", "remember this in obsidian", or any request to persist knowledge to the Obsidian vault.
---

# Vault Knowledge Capture

Store useful knowledge in Magnus's Obsidian vault. This skill works locally and in a cloud checkout.

## Resolve the vault

Use the local vault when it exists. Otherwise, use the current Git repository.

```bash
if [ -d "$HOME/dev/personal/vault/.git" ]; then
  VAULT="$HOME/dev/personal/vault"
else
  VAULT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
fi
```

Read `$VAULT/AGENTS.md` before making changes. It is the source of truth for structure and writing rules. Read `$VAULT/.agents/skills/vault-management/SKILL.md` for organization work and `$VAULT/.agents/skills/obsidian-markdown/SKILL.md` for Obsidian syntax.

## Workflow

1. Identify the subject and what should be retained from the conversation.
2. Search filenames and note contents before writing. Search both Norwegian and English terms, plus aliases.
3. Rank matches by filename, folder, status, and Git recency. Check the latest commit for candidate notes.
4. Update the canonical existing note when one covers the subject. Create a note only when no suitable home exists.
5. Classify the content and choose its folder. Project membership takes precedence over type.
6. Read one or two recent notes of the same type. Use a template only as a starting point.
7. Write complete frontmatter, valid wikilinks, and the captured knowledge.
8. Add at least one link to a new note from an existing note. Check its backlinks.
9. Review the diff for unsupported claims, duplicate facts, broken links, language, and frontmatter.

Use `rg` for search. Example:

```bash
rg -il -w 'topic|tema|synonym|synonym' "$VAULT" -g '*.md'
git -C "$VAULT" log -1 --format='%ad %h' --date=short -- 'path/to/Note.md'
rg -l '\[\[Note Name(?:[|#]|\]\])' "$VAULT" -g '*.md'
```

## Placement

| Content | Default location |
|---|---|
| External source summary with `#source/*` | `Learning/` |
| Reusable reference or how-to guide | `Reference/` |
| Magnus's own concept or compact idea | `Notes/` |
| Project | `Projects/` |
| Person | `Personal/People/` |
| Meeting | `Meetings/` |
| Decision or brag | Beside the subject, otherwise `Notes/` |

Keep notes about a live project inside that project's folder, even when their type would normally use another folder.

## Writing rules

- Write one subject per note. A complete synthesis of 1,000 to 3,000 words is normal.
- Split only when a note contains separate subjects or a section needs independent links.
- Use `[[wikilinks]]` for internal references. Link only to an existing target or one created in the same change.
- Give every new note two or three useful outgoing links and at least one incoming link.
- Never copy a canonical number into several notes. Link to its source of truth.
- Write English by default. Write Personlig Økonomi and other Norwegian spaces in correct Norwegian with æ, ø, and å.
- Never use an em dash.

## Frontmatter

Every note needs YAML frontmatter:

```yaml
---
type: note
created: DD.MM.YYYY
tags: []
related: []
---
```

Projects and decisions always have a status. `active` is valid only for those types. Other notes omit status unless they are `draft`, `completed`, `archived`, or `published`.

Every `learning` note must include one closed-vocabulary source tag: `#source/book`, `#source/article`, `#source/video`, `#source/podcast`, `#source/course`, `#source/research`, `#source/repo`, `#source/docs`, or `#source/experience`.

## Completion check

- No better existing note was missed.
- The note has valid frontmatter and follows current status rules.
- Every new wikilink resolves.
- New notes have useful outgoing and incoming links.
- Facts that can change were checked against Git recency or a current source.
- The final diff contains only the intended vault changes.
