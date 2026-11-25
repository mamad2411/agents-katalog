---
name: i18n-setup
description: "Sets up or repairs localization for a game: player-facing string extraction, locale catalogs, draft target-locale translations, fallback and locale selection, runtime switching, plural and parameter formatting, glyph coverage, and translation-safe layouts. Use when the user requests another locale or localization-ready architecture; existing translations, fallback, pluralization, locale detection, or switching are broken; or translated text overflows or renders missing glyphs. Follows the project's engine and existing localization system and marks generated translations for human review."
---

# i18n Setup

Follow the project's localization system, keep messages whole, and verify catalogs and
layouts as one change.

## 1. Inspect the project and define scope

Identify the engine or runtime, build and test commands, current localization library
or resource format, source locale, target locales, font pipeline, and supported
platforms. Determine whether the request is an audit or includes implementation.

Use the project's current, complete source locale as the fallback unless the project or
user specifies another. Confirm whether any target locale uses right-to-left layout or
grammar that changes around parameters. When it does, read
[rtl-and-grammar.md](references/rtl-and-grammar.md) and include that work in scope.

## 2. Inventory player-facing content

Sweep the whole project, including:

- HUD, menus, tutorial, hints, victory, failure, and pause screens;
- validation, recoverable errors, and player-facing system messages;
- scene, canvas, sprite, or world-space text outside the main UI layer;
- concatenated messages that need parameters;
- titles, share text, store or page metadata used by the target build;
- text baked into images or sprite sheets, reported as replacement assets.

Leave debug logs and internal identifiers unchanged unless they are visible to players.
Record each source location so a second sweep can prove extraction is complete.

## 3. Use or establish the message system

Follow the existing library's catalog format, namespace, fallback mechanism, and file
organization. If none exists, implement the smallest project-appropriate catalog and
lookup layer without committing the project to a heavyweight framework.

Regardless of storage format:

- use stable semantic keys in the project's naming convention;
- keep locale key sets, placeholders, and plural categories compatible;
- fall back to the complete source locale rather than showing a blank or raw key to a
  player;
- translate whole parameterized messages instead of concatenating fragments;
- use the platform or localization library's plural rules;
- keep grammar-dependent variants in the message system or localized data rather than
  inferring gender, case, or agreement from source-language text.

## 4. Replace and translate

Replace each inventoried literal with a message lookup and parameters. Move the source
copy into the source-locale catalog, then perform a fresh sweep for remaining
player-facing literals.

Fill every target catalog with a draft for every required message. Mark generated
translations as unreviewed in the project's supported metadata or, when none exists,
in the delivery report. Establish a glossary before changing proper nouns, character or
item names, and brand terms; ask when the intended localized form is unknown.

## 5. Detect and switch locale

Use the platform or localization library's locale matcher. Canonicalize language tags
and match available locales by its BCP 47 fallback behavior rather than raw string
prefixes. If the platform offers no matcher, implement a deterministic fallback chain
over parsed language, script, and region subtags, then use the configured fallback
locale.

Detect on first run, persist an explicit player choice, prefer that choice afterwards,
and expose a reachable switcher. Apply a change immediately to every active screen and
newly created content.

## 6. Format locale-sensitive values

Use locale-aware formatters for numbers, dates, times, relative time, and real-world
currency. For fictional game currency, localize the number and its unit or symbol as
game text rather than forcing a real-world currency formatter.

## 7. Verify catalogs and layout

Run or implement checks for:

- missing and unexpected keys in every locale;
- placeholder names and types;
- plural-category coverage supported by the message system;
- fallback, first-run detection, persistence, and immediate switching;
- font glyph coverage and line-breaking for every target locale.

Generate a pseudo-locale that expands and marks visible text while preserving
placeholders, markup, escape sequences, and control codes. Exercise every screen at the
smallest supported viewport. Fix flexible containers and wrapping rather than shortening
translations to hide layout defects.

When several viewports are required, use the `cross-device-check` skill for the broader
matrix. If the project cannot run, label layout findings inferred and provide the full
runtime verification checklist.

## Constraints

- Treat generated translations as drafts requiring review by a speaker before release.
- Preserve proper nouns according to an approved glossary or explicit user decision.
- Match the project's dependency weight and existing localization conventions.
