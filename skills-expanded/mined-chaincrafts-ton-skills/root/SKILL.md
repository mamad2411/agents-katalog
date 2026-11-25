# TONSkills Content Contract

TONSkills treats `content/` as a machine-readable source of truth for six scoped collections only:

- `content/root`
- `content/skills`
- `content/recipes`
- `content/checklists`
- `content/compare`
- `content/glossary`

## Slugs

- Folder names and glossary filenames are the canonical slugs.
- Slugs must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`.
- Do not add a separate `slug` field to metadata.
- Compare entries must contain exactly one `-vs-` segment in the slug.

## Required Files

- `content/root`: `SKILL.md`, `STYLE_GUIDE.md`
- `content/skills/<slug>`: `metadata.json`, `index.mdx`, `SKILL.md`
- `content/recipes/<slug>`: `metadata.json`, `index.mdx`
- `content/checklists/<slug>`: `metadata.json`, `index.mdx`
- `content/compare/<slug>`: `metadata.json`, `index.mdx`
- `content/glossary/<slug>.mdx`: one file with frontmatter and body

Optional files:

- `content/root`: `ABOUT.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `TAXONOMY.md`
- `content/skills/<slug>`: `checklist.mdx`, `assets/`
- `content/recipes/<slug>`, `content/checklists/<slug>`, `content/compare/<slug>`: `assets/`

## Metadata Rules

Directory-based content stores typed metadata in `metadata.json` only.

Required directory metadata fields:

- `kind`
- `title`
- `summary`
- `audiences`
- `difficulty`
- `tags`
- `prerequisites`
- `related`

Additional fields:

- `skill`: `templateRefs`
- `recipe`, `checklist`, `compare`: `skills`
- `compare`: `subjects`

Glossary frontmatter requires:

- `kind`
- `term`
- `summary`

Glossary optional frontmatter:

- `aliases`
- `tags`
- `skills`
- `related`

Unknown metadata keys are invalid.

## Relationship Rules

- `prerequisites` accepts skill slugs only.
- `related` accepts `"<kind>:<slug>"` references for `skill`, `recipe`, `checklist`, `compare`, and `glossary`.
- `related` must not point to `root`.
- Content must not relate to itself.

## Canonical Routes

- `skill` -> `/skill/<slug>`
- `recipe` -> `/recipes/<slug>`
- `checklist` -> `/checklists/<slug>`
- `compare` -> `/compare/<slug>`
- `glossary` -> `/glossary/<slug>`

## Raw Agent Endpoints

- skill source prompt -> `/skill/<slug>/SKILL.md`
- root routing document -> `/SKILL.md`

`root` is a singleton documentation surface with a dedicated raw route at `/SKILL.md`.

## Validation Expectations

- Required files must exist and contain content.
- `index.mdx` and `SKILL.md` must not carry frontmatter.
- `summary` must be a single-line plain text string.
- `audiences`, `difficulty`, and `tags` must come from `@tonskills/taxonomy`.
- A skill folder must be valid from schema checks alone, without app code.
