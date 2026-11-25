---
name: use-multi-lang
description: >
  LANGUAGES of this project — which set is authoritative, when you translate and when you deliberately
  do not, and where the debt for that is recorded. Load it before writing any user-visible string, any
  language cell, any dictionary, and whenever you wonder "how many languages does this need". Two
  things here you cannot infer from the code: the set belongs to the OWNER of this project and never
  to the number your neighbours happen to have, and during development you write in ONE language on
  purpose — the missing translations are a recorded debt, closed by a separate run at the end.
---

# use-multi-lang

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

## 1. The set is the owner's, and it lives in one place

`NEXT_PUBLIC_SUPPORTED_LANGUAGES` in this project's `.env.local`. The owner changes it in the panel;
it applies on a rebuild. That is the only answer to "how many languages" for anything this project's
visitors see.

🔒 **Never count languages by looking at existing files.** Posts shipped with the starter carry ten
cells because they were written when ten were enabled — that is history, not a norm, and copying it
means writing eight translations nobody asked for. Two agents in a row stumbled on exactly this.

The set also decides the SHAPE of addresses: one language — routes from the root; several — `/{lang}/`.
`proxy.ts` switches that, and it is not edited without the owner's direct request.

## 2. During development, one language — and that is a decision, not laziness

**You write in the default language while the thing is being built.** During construction strings get
rewritten several times, and every translation is paid for again in time and tokens, giving nothing.
Translate when the feature is finished and confirmed.

🔒 **The other half of that decision is what makes it honest: the debt is RECORDED.** A postponed
translation disappears from view together with the step, and a month later nobody can say which
routes and components are still single-language.

**`development-docs/TRANSLATION-DEBT.md`** — the register. Creating a route or a component with
user-visible strings in one language, add its address there in the same change. The entry lives until
the step that owns it is finished and translated, then it is struck out.

Keep in it only what cannot be derived: the promise ("this one is reusable, so it owes 82") and the
owner's decision to defer. Coverage itself is derived — `npm run check:i18n` already knows every
dictionary and the enabled set, and the difference between them IS the debt. A hand-kept register
goes stale first.

At the end of the work the debt is closed by its own run: `expand-site-language` is the only correct
way to add a language to a site that already exists.

## 3. Two shapes of translated strings, and they are not interchangeable

| Shape | Where | How many languages |
|---|---|---|
| **language cell** — the content of one page | `_data/<lang>.ts` beside the page | the ENABLED set. A partial cell is legal: `resolve.ts` falls back to English key by key |
| **dictionary** — `<name>.i18n.ts` beside a reusable component | `components/`, a widget's folder | a reusable part of the product owes every language the owner can switch on; a widget's own words are ten by decision |

The dividing line is reuse, not size: something that appears in any language the owner enables the
minute he enables it must already speak it. Something that belongs to one route does not.

🔒 **A client file never imports a dictionary.** Eighty-two languages times a dictionary is hundreds
of kilobytes shipped to the browser on every page. Strings resolve in the server component and travel
into the island as props. A file where many languages sit together has no right to carry `"use client"`.

**A shared message lives once.** "No OpenAI key" is the same refusal for voice input, translation and
everything thinking that comes later — `lib/i18n/platform-errors.ts`, not a copy per feature. Copies
drift, and they drift in the rare languages where nobody will notice.

## 4. What is never translated

Machine strings: identifiers, slugs, enum values, codes, file names, and the keys themselves.
Translating those breaks lookups. A slug is chosen once, from the default-language title, and one post
spans all its languages under that one slug.

## 5. Before you call it done

- `npm run check:i18n` — it does not run by itself, and it is what stands between your change and a
  missing string in a language you never opened.
- Open the page in every enabled language and read it, rather than trusting that a cell exists.
- If you left something single-language, say so out loud and point at its line in the debt register.
  Silence there reads as "everything is translated", and that is the expensive lie.
