---
name: aval-release-notes
description: "Use when writing the changelog or release notes of an aval version, before cutting it, or when setting the GitHub release body after publish. Detailed, bilingual (English and Spanish), visual notes."
---

## Activation contract

Load before writing `docs/releases/vX.Y.Z.md`, its Spanish twin or the `CHANGELOG.md` section of a version, and again after publish to set the GitHub release body. `aval-release` owns the cut; `aval-docs` owns images and links. This skill owns what the notes say and how they look. The owner's standard: **detailed, explanatory, in English and Spanish, visually beautiful, very visual.**

## Hard rules

- **Two files, one structure.** Write `docs/releases/vX.Y.Z.md` (English) and `docs/releases/vX.Y.Z.es.md` (Spanish) for the base version, so an rc and its stable share them. Each file opens with a language switch to the other. The `CHANGELOG.md` section `## vX.Y.Z[-rc.N] (YYYY-MM-DD)` keeps a short summary and links both; `tests/release_notes_test.go` fails without them.
- **Scope is everything since the last stable tag**, not the PR you just merged. Read every subject in `aval release rc --dry-run` (or `minor`, `patch`) and cover each feature, fix and breaking change. Commits already on `main` count too.
- **Breaking changes come first**, in a `> [!WARNING]` right under the header: what stopped working, what to run instead, and how a script should change.
- **Explain, don't list.** Each section says what the user can do now and why it matters, then how it works. A commit subject is not a sentence for a user.
- **Every number is measured** from the repo or a run: catalog keys, views, themes, goldens. Write down how you measured each one for the report, and never invent a capability. If a claim is unverified, the notes say so, under Known limits.
- **House style in both languages:** sentence case, no emoji, no em dashes, no exclamation marks. The Spanish is neutral and professional, uses usted or impersonal forms, and follows the catalog's terms: copia de seguridad (short form copia), fijar, sincronizar. Hook, overlay and sandbox stay in English.
- **Visuals are real.** Use the GIFs, PNGs and SVGs the generators make (`aval-docs` table). A new GIF comes from a `.tape` file through vhs. A Spanish feature shows a Spanish recording, for example `docs/hub-demo-es.tape`. Never hand-edit an image.
- **Links:** relative in the repo files. In the release body they are absolute and pinned to the tag (see the release body steps).

## Structure (both files, this order; drop what a release lacks)

Copy [assets/template.md](assets/template.md).

1. **Header.** A centred wordmark `<picture>` (dark and light), the version, the date, the prerelease flag and the language switch.
2. `> [!NOTE]` for a prerelease: what it is, and that feedback is wanted.
3. `> [!WARNING]` for breaking changes.
4. **What this release means for you:** one paragraph, plain words.
5. **Highlights:** a grid of 3-column tables, each cell a bold title over one line, with 6 to 9 cells.
6. **One section per theme.** It holds a GIF or image, a table (what it does and its safety net, or key, values, env and flag), fenced commands that really work, and a Mermaid diagram where a flow or order matters.
7. **Fixes:** one line each, prefixed with the bold scope.
8. **Upgrade notes** in a `> [!IMPORTANT]`: behaviour changes and what stays the same.
9. **Known limits:** honest; untested-by-hand goes here.
10. **Verify this release:** the exact commands from `aval-release`.
11. `<details>` for contributors: the engineering changes.

## Release body (after publish)

1. Save GoReleaser's list with `gh release view <tag> --json body -q .body`.
2. Build the body: the English notes, `---`, the Spanish notes, `---`, then `<details><summary>All commits · Todos los commits</summary>` wrapping the generated list.
3. Rewrite relative paths, resolving them from `docs/releases/`:
   - images to `https://raw.githubusercontent.com/alvaroofernaandez/aval/<tag>/<path>`;
   - links to `https://github.com/alvaroofernaandez/aval/blob/<tag>/<path>`.
   - after a `promote`, the notes written after the rc are not in the tag: the body comes from `main`, so pin those links and images to `main` instead.
4. **Mermaid does not render in a release body.** Replace each diagram with a table that says the same, for example numbered columns for a flow or an Order, Source, Example table for a precedence.
5. Run `gh release edit <tag> --notes-file <file>`. This is a remote action: only with the owner's authorization.
6. Check the rendered HTML with `gh api repos/alvaroofernaandez/aval/releases/tags/<tag> -H "Accept: application/vnd.github.html+json" --jq .body_html`. It must contain no `highlight-source-mermaid`, every `src=` must be absolute, and the alerts must be there.

## Before finishing

`go test ./tests/ -run 'Release|Changelog|Readme|Docs'`, then report:
- the files written;
- the numbers measured, and how each was measured;
- what is unverified, such as rendering or a native read of the Spanish;
- whether the release body was set.
