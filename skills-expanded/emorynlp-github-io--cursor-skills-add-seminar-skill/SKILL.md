---
name: add-seminar
description: >-
  Adds or updates an Emory NLP seminar (frontmatter + optional body). Asks for
  missing facts before drafting. After the talk, renames slides to
  YYYYMMDD-Firstname_Lastname.pdf and uploads to the lab weekly-meetings Google
  Drive folder, then sets slidesUrl. Use when creating src/content/seminars/,
  uploading seminar slides, or when the user says "add a seminar".
---

# Add a seminar (Emory NLP site)

Golden references:

- `src/content/seminars/2025s-grace-byun.md` — slides on Drive + `slidesUrl`
- `src/content/seminars/2025f-nayoung-choi.md` — PhD defense, no slides yet
- `src/content/seminars/2026s-nayoung-choi.md` — TBA abstract
- `src/content/seminars/2022f-meera-hahn-part-1.md` — guest talk + markdown body

Schema: `src/content.config.ts` → `seminars`.

Listing UI: `/seminars/` uses theses-style rows (`src/pages/seminars/index.astro`); detail page shows separate **Date** and **Time** rows.

## Two phases (same skill)

| Phase | When | Actions |
|-------|------|---------|
| **Schedule** | Before the talk | Create `src/content/seminars/{slug}.md` (no `slidesUrl` unless slides already exist) |
| **Slides** | After the talk | Rename PDF → upload to Drive → add `slidesUrl` to the same markdown file |

If the user attaches a PDF in the same message as seminar details, run both phases.

## Gather necessary information first

Ask for anything missing before editing files.

**Required for a new entry:**

- **Title**
- **Date** — `YYYY-MM-DD` (seminar day)
- **Speaker(s)** — full names, matching people profiles when possible
- **Term** — e.g. `Spring 2026`, `Fall 2025` (infer from date if obvious; confirm if June–July)

**Usually include (defaults if lab standard):**

- **time** — default `3:00 - 4:00 PM` when not specified
- **location** — default `White Hall 100` for in-person; Zoom URL when remote

**Optional:**

- **abstract** — omit or `TBA` until known
- **videoUrl** — recording after the fact
- **coverImage** — `/seminars/{slug}.webp` under `public/` (optional; single-speaker talks also use people photo on the list)
- **Markdown body** — guest bio, etc. (uncommon for internal talks)

Do **not** fabricate titles, abstracts, or links.

## Slug and filename

File: `src/content/seminars/{slug}.md` → URL `/seminars/{slug}/`

Pick a slug consistent with siblings in the same term:

| Kind | Pattern | Examples |
|------|---------|----------|
| Regular (Spring) | `{yy}s-{kebab-name}` | `2025s-grace-byun`, `2025s-jinho-choi` |
| Regular (Fall) | `{yy}f-{kebab-name}` | `2024f-benjamin-ascoli`, `2023f-ellie-paek` |
| Split session | `{yy}{s\|f}-{name}-part-2` | `2021f-emily-mower-provost-part-1` |
| Multi-speaker / panel | `{yy}{s\|f}-{descriptive-kebab}` | `2024f-literature-review-1`, `2022f-summer-interns-phd` |

Do **not** use type prefixes (`guest-`, `phd-`, `honors-`, `undergrad-`, `faculty-`, etc.) in slugs.

`{yy}` = last two digits of the calendar year in the term (e.g. Fall **20**25 → `25f`).

**Do not** put degree suffixes (`-phd`, `-ms`, `-bs`, `-ba`) or `-copy` in slugs — use `{yy}s-{name}` or `{yy}f-{name}` only.

**Term inference** (confirm edge cases): Jan–May → Spring; Aug–Dec → Fall.

If the slug exists, append `-1`, `-2`, or a short topic disambiguator (not `-copy`).

## Frontmatter template

```yaml
---
title: Talk Title
date: 2026-04-11
term: Spring 2026
time: '3:00 - 4:00 PM'
speakers:
  - Grace Byun
location: White Hall 100
abstract: >-
  Abstract text or TBA.
slidesUrl: 'https://drive.google.com/file/d/…/view?usp=sharing'
---
```

- Quote `time` and URLs.
- Use `abstract: >-` for long text; `abstract: TBA` is fine for placeholders.
- **slidesUrl** — Google Drive **file** view link (`https://drive.google.com/file/d/{id}/view?…`), not the folder link.

## Upload slides (after the seminar)

**Drive folder (weekly-meetings):**  
[https://drive.google.com/drive/folders/1cs1k978XpBH8PCAmR0tHyYYUMLfc2anG](https://drive.google.com/drive/folders/1cs1k978XpBH8PCAmR0tHyYYUMLfc2anG)

**PDF name on Drive:**

```text
YYYYMMDD-Firstname_Lastname.pdf
```

Examples:

- Grace Byun, 2025-04-11 → `20250411-Grace_Byun.pdf`
- Mack Hutsell + Daniil Huryn → `20210408-Mack_Hutsell-Daniil_Huryn.pdf`

Use the **seminar date** (not upload date). For multiple speakers, one `First_Last` segment per person, joined with `-`.

### Script (preferred)

```bash
node scripts/upload-seminar-slides.mjs /path/to/deck.pdf --date 2025-04-11 --speaker "Grace Byun"
```

Multiple speakers:

```bash
node scripts/upload-seminar-slides.mjs deck.pdf --date 2021-04-08 --speakers "Mack Hutsell,Daniil Huryn"
```

Options:

- `--dry-run` — print target filename only
- `--no-upload` — rename/copy locally; user uploads manually

The script copies the file to `{same-dir}/{YYYYMMDD-First_Last}.pdf`, then uploads via **rclone** when installed.

### rclone setup (one-time, for automatic upload)

1. `brew install rclone` (or your package manager)
2. `rclone config` → new remote named **`gdrive`** → **Google Drive** → complete the **browser sign-in** (required)
3. Use the Google account that can **edit** the [weekly-meetings folder](https://drive.google.com/drive/folders/1cs1k978XpBH8PCAmR0tHyYYUMLfc2anG)
4. Optional: `export RCLONE_REMOTE=gdrive` (default)

**If upload says `empty token`** or `reconnect` fails, the remote was created without finishing sign-in. Delete and recreate (this opens the browser):

```bash
rclone config delete gdrive
rclone config create gdrive drive scope drive
```

(`rclone config reconnect gdrive:` only works after a successful first login.)

Verify:

```bash
rclone about gdrive: --drive-root-folder-id=1cs1k978XpBH8PCAmR0tHyYYUMLfc2anG
```

Credentials live in `~/.config/rclone/rclone.conf` — never commit that file.

If rclone is missing, the script prints manual steps; upload the renamed PDF to the folder above, share **Anyone with the link**, and paste the file URL into `slidesUrl`.

### Update the seminar markdown

After upload, set on the existing entry:

```yaml
slidesUrl: 'https://drive.google.com/file/d/FILE_ID/view?usp=sharing'
```

Use the link from `rclone link` output or from Drive’s Share dialog.

## Speakers and people profiles

- `speakers` strings link to `/people/` when they match a profile (`src/lib/publicationAuthorLinks.ts`).
- Use the same spelling as on people pages (e.g. `Nayoung Choi`, `Sarah E. Finch`).
- New member? Run **add-member** first, then this skill.

## Validate

```bash
npm run check
```

Optional: `npm run build`

## Related skills

- **add-member** — new speaker needs a people profile
- **convert-photo** — optional `public/seminars/{slug}.webp` cover for the list
