---
name: profile-me
description: Write professional-branding content — LinkedIn (headline, About, Experience), résumé, portfolio, Lattes — from validated facts, using the X-Y-Z method and honest metrics, adapted per channel and de-duplicated across sections. Use when the user wants to write or improve a LinkedIn profile, résumé/CV bullets, a portfolio bio, personal positioning, a headline, or an About section.
---

# Profile Me

Turns validated career facts into positioning content that reads right for each channel. It writes; it does not invent. Pairs with [brag-me](../brag-me/SKILL.md): brag-me **harvests** the facts from git/PRs, this skill **writes** the positioning from them.

## Quick start

1. **Get the facts** — from the user's own source-of-truth (a `brag.md`, a validated-facts doc, or an interview). Never pull achievements from thin air. See [REFERENCE.md](REFERENCE.md) for the input format.
2. **Pick the channel** — LinkedIn headline / About / Experience, résumé, portfolio hero / About / project, Lattes. Each has its own format and detail level ([REFERENCE.md](REFERENCE.md) §3).
3. **Write X-Y-Z** — "Accomplished **X**, measured by **Y**, by doing **Z**." Result + proof always travel together ([REFERENCE.md](REFERENCE.md) §1).
4. **Check honesty and redundancy** — no invented number; no two sections saying the same thing ([REFERENCE.md](REFERENCE.md) §2, §4).

## The honesty rule

**Never invent a metric.** No number in the source → ask the user, or fall back to honest proof-of-scope (a real version bump, a real count, a specific true outcome) — never a vague "improved quality". If while drafting you realize you inferred a number the source doesn't contain, **stop, flag it, and correct** before finalizing. This is the same discipline as [brag-me](../brag-me/SKILL.md); if the facts come from git, harvest them there first.

## Your data stays yours

This skill is the **method**, not your data. Keep your real projects, metrics, salary research, and client names in your own private source-of-truth file — never paste them into the published skill, and don't commit them to a public repo. The examples in [REFERENCE.md](REFERENCE.md) are anonymized on purpose.
