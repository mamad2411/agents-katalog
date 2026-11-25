---
name: bansos-add-entry
description: Add, review, or update a bansos.dev listing using the current folder-based catalog and contributor profile flow. Use when an AI agent needs to verify a program source, run `npm run add:bansos`, create or update a listing folder, attribute a first-time or existing contributor, validate data, or prepare and review a wauputr4/bansos pull request.
---

# Bansos Add Entry

## Workflow

1. Read the repository README, `.github/CONTRIBUTING.md`, and the official program source.
2. Verify volatile claims such as availability, expiry, quotas, eligibility, pricing, and claim URLs. Do not publish an entry whose primary source cannot be verified.
3. Search existing folders for duplicate IDs, titles, providers, and URLs.
4. Use `npm run add:bansos` to create `src/lib/data/bansos/<slug>/index.json` and its README.
5. Set `contributorSlug` on every listing. Reuse an existing contributor profile; for a first submission, also provide `--contributor-name` and optionally `--contributor-url`.
6. Review the generated listing, contributor manifest, README files, and catalog index. Keep generated changes only when they match the intended data.
7. Run `npm run validate:data`, `npm run check`, and `npm run lint`. Run `npm run build` when the change affects rendering, SEO, generated output, or shared behavior.
8. Open a focused PR with source evidence, contributor attribution, uncertainty, and validation results. Address actionable review threads and wait for required CI when asked to finish the flow.

Public submissions currently use email or a Git clone and pull request. Do not recommend the disabled public `npx bansosdev` flow, form, or bots.

## Local Command

```bash
npm run add:bansos -- \
  --id contoh-bansos \
  --title "Contoh Bansos Developer" \
  --provider "Provider" \
  --description "Deskripsi singkat bansos." \
  --benefits "Benefit satu|Benefit dua" \
  --validity-type fixed \
  --validity-date 2026-08-31 \
  --validity-desc "Selama kuota masih ada" \
  --published-at 2026-07-22 \
  --requirements "Buat akun|Klaim program" \
  --cta-link "https://example.com/program" \
  --source "https://example.com/announcement" \
  --contributor-slug "nama-kontributor" \
  --contributor-name "Nama Kontributor" \
  --contributor-url "https://github.com/example" \
  --tags "Cloud,Gratisan"
```

Omit `--contributor-name` and `--contributor-url` when the contributor manifest already exists.

## Rules

- Use lowercase kebab-case IDs and valid `YYYY-MM-DD` dates.
- Use `fixed`, `uncertain`, or `forever` validity and `active`, `expired`, or `upcoming` status.
- Keep `ctaLink` for the claim or landing page and `source` for supporting evidence.
- Mark ended programs as expired instead of deleting their history.
- Keep listing `contributorSlug` and profile `contributedBansos` synchronized.
- Prefer a GitHub profile URL for avatar discovery. A contributor without external links is valid.
- Treat `src/lib/data/bansos/index.json`, commit contributor metadata, and `static/llms*.txt` as generated outputs; regenerate them through repository scripts rather than hand-editing them.

## Reference

Read `references/bansos-entry-rules.md` for folder schemas, contributor profiles, and PR review details.
