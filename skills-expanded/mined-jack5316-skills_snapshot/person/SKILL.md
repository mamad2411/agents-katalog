---
name: person
description: Build profiles on people you follow or study. Use when user asks for person profile, people they follow, study someone, or /person.
---

# Person Profile Skill

Creates structured profiles on people (authors, researchers, entrepreneurs, thinkers) you follow or study. Saves to the vault for your people database.

## Usage

```bash
python3 _scripts/person_profile.py "Person Name" [--role "author|researcher|entrepreneur|..."] [--notes "Your observations"]
```

- **Name**: Person's full name (required)
- `--role`: Context hint (author, researcher, entrepreneur, founder, artist, etc.) to focus the profile
- `--notes`: Your observations, why you follow them, or excerpts to incorporate

## Output

`Sources/Person - {Name}.md` with:

- **Metadata**: Role(s), domain, affiliations
- **Background**: Brief bio, career, education
- **Key Ideas / Contributions**: What they're known for, their thinking
- **Notable Quotes**: Memorable statements
- **Works / Projects**: Books, articles, companies, products
- **Personal Notes**: Your observations (if provided via `--notes`)
- **Connections**: [[wikilinks]] to related people, concepts, ideas

Uses `[[wikilinks]]` for Obsidian interconnection. No YAML frontmatter in output.
