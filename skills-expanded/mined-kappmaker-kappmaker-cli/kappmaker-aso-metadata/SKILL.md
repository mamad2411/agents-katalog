---
name: kappmaker-aso-metadata
description: Write the per-locale App Store metadata for a KAppMaker app — name, subtitle, keywords and description across locales, plus the rules that decide what goes where: no word repeated within a locale, uniqueness across locales, and quality over uniqueness. Use when the user asks what to call the app in the stores, or to write or fix the title, subtitle, keyword field or localized listing.
---

# KAppMaker — ASO Metadata (per locale)

## Before starting

**Read `AiGuidelines/` first** — the PRD and positioning already answer most questions. This is a
skill-driven procedure: you (Claude) execute it with your own tools. No `kappmaker` binary is
involved and none needs to be installed.

### Localize ASO Metadata — Per-locale Name / Subtitle / Keywords / Description

This is a **skill-driven procedure**, not an external CLI command. Claude (you) executes the prompts in this section directly using the Read/Write tools — there is no shell binary to invoke and no AI API key required. All text generation and ASO-rule enforcement happens in-conversation.

**Trigger phrases** (any of these in the user's message routes here):
- `Using kappmaker, localize metadata mode=keyword-expansion ...`
- `Using kappmaker, localize metadata mode=market-localization ...`
- "localize aso", "localize metadata", "aso keyword expansion", "aso keywords"

**Argument parsing** (extract from the user message):
- `mode` — required, one of `keyword-expansion` | `market-localization`
- `keywords` — required for `keyword-expansion`; comma-separated list (strip surrounding quotes, trim each entry, drop empties)
- `base` — optional for `market-localization`; defaults to `en-US`
- `locales` — required for `market-localization`; comma- or space-separated codes (no autodetect)
- `distribution_dir` — optional override. Default resolution: search upward from cwd for a directory containing `MobileApp/distribution/`; if not found, use `./MobileApp/distribution`. If neither exists, create `./MobileApp/distribution/` and use that.

If `mode` is missing or invalid, stop and ask the user to pick one of the two modes and provide its required args.

#### Output layout (strict — same for both modes)

- **iOS**: `<distribution_dir>/ios/appstore_metadata/texts/<iosLocale>/{name,subtitle,keywords,description}.txt`
  - The `texts/` subfolder IS literal and intentional. Not standard Fastlane `deliver` layout.
- **Android**: `<distribution_dir>/android/playstore_metadata/<playLocale>/{title,short_description,full_description}.txt`

`en-US` (or the user-chosen base) is **never** modified once it exists. No images, screenshots, or other files are touched.

#### Preflight checklist (run BEFORE either mode procedure)

1. Resolve `<distribution_dir>` (see argument parsing above).
2. **Base-locale bootstrap (NEVER fail when missing)**: read the base-locale folders:
   - iOS: `<distribution_dir>/ios/appstore_metadata/texts/<base>/{name,subtitle,keywords,description}.txt`
   - Android: `<distribution_dir>/android/playstore_metadata/<base>/{title,short_description,full_description}.txt`
   
   If either folder is missing entirely, OR any of the expected files is missing OR empty (zero bytes), enter **bootstrap mode**:
   - Ask the user (single prompt): `"Base locale '<base>' is missing some metadata. Briefly describe the app and its core value (1–2 sentences):"` Wait for the reply.
   - For Mode 1 (`keyword-expansion`), use the user's app description + the `keywords=` list to compose the base-locale files. For Mode 2 (`market-localization`), use just the app description.
   - Apply the **ASO Guidelines** (`references/aso-guidelines.md`) to the bootstrapped output: front-load the strongest keyword in `name`/`title`, no spaces after commas in keywords, no word repetition across `name`/`subtitle`/`keywords` in the iOS folder, respect every char limit.
   - Write the missing base files first (only those that were missing or empty — preserve any non-empty siblings as the source for the rest).
3. After bootstrap (or directly if everything was present), read all 7 base-locale files into local variables you can reference as `<BASE_NAME>`, `<BASE_SUBTITLE>`, `<BASE_KEYWORDS>`, `<BASE_DESCRIPTION>`, `<BASE_TITLE>`, `<BASE_SHORT_DESC>`, `<BASE_FULL_DESC>`.
4. For Mode 2: validate every code in `locales=` resolves in the locale table in `references/mode2-locales.md`. If any code is unknown, abort with the full supported-codes list printed and do NOT create any folders.

#### Mode 1 — keyword-expansion procedure

**Locale set (FIXED)** — the 9 US-indexed locales:

| iOS folder | Play folder |
|---|---|
| `ar-SA`   | `ar` |
| `fr-FR`   | `fr-FR` |
| `ko`      | `ko-KR` |
| `pt-BR`   | `pt-BR` |
| `ru`      | `ru-RU` |
| `vi`      | `vi` |
| `zh-Hans` | `zh-CN` |
| `zh-Hant` | `zh-TW` |
| `es-MX`   | `es-MX` |

**Overwrite behavior**: always overwrite these 9 locales without prompting. The base locale (`en-US`) is the only protected folder and is never touched (except by the bootstrap step above, which writes it once if missing).

**How to execute**: read `references/mode1-reasoning.md` and follow it exactly — it contains the
full reasoning script (distribution rules, uniqueness rules A/B, quality-over-uniqueness), the
self-verification checklist, the writing step (63 files: 9 iOS folders x 4 + 9 Android folders x 3),
and the summary-table format. The character limits it enforces live in
`references/aso-guidelines.md` — read that first if you have not already.

#### Mode 2 — market-localization procedure

**Locale resolution**: parse `locales=` (comma- or space-separated), look each up in the locale
table in `references/mode2-locales.md`, build `(iosLocale, playLocale)` pairs. If one platform's
code is `(none)` for that language, skip that platform and note it in the summary. If a
user-supplied code matches NO table entry, abort with the full supported-codes list printed and do
NOT create any folders. Natural-language presets ("top 10", "European markets", "tier 1 but skip
ru") are also accepted — the same reference file defines every preset and combiner. Always confirm
the expanded set with the user before generating.

**Existing-files check**: for each target locale, check whether ANY of its files already exist.
If some do, prompt ONCE — `"Found existing metadata in N locale(s): a, b, c. Overwrite ALL
existing metadata? [y/N]"`. `N` excludes those locales and continues with the rest; an emptied
list exits with "No locales to generate".

**How to execute**: read `references/mode2-locales.md` and follow its per-locale reasoning script —
adapt for local search behaviour (never translate literally), then write each locale's iOS folder
(4 files) and Android folder (3 files), skipping any `(none)` platform. End with the summary:
wrote / skipped-declined / skipped-one-platform / char-limit warnings at >=95% of a cap.

#### The rules that make or break the output

Both modes live and die on the same constraints, spelled out in `references/aso-guidelines.md`:
per-field character limits, zero word repetition across name/subtitle/keywords within a locale, no
brand name and no filler words in the iOS keywords field, front-loading by search volume, and the
native-feel bar for Mode 2. Read it before writing any file — a single over-limit field or a
duplicated word is exactly the kind of mistake that survives to the store listing.

---

## Where this sits in the flow

- **Before this:** **kappmaker-aso** — you need the keyword research before writing the fields.
- **After this:** **kappmaker-asc** / **kappmaker-gpc** to upload the metadata to the stores.
