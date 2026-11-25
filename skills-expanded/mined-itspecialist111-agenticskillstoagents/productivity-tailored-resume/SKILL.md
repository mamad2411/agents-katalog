# productivity/tailored-resume — skill payload

> Machine-readable contract: [`../tailored-resume.manifest.json`](../tailored-resume.manifest.json).

## What this skill does

Tailors a base resume (DOCX) to a specific job description:

1. Parses the job description for required skills, keywords, and the
   seniority signal.
2. Re-orders bullets in each role by relevance to those signals.
3. Suggests rewordings that surface matching keywords without inventing
   experience.
4. Writes a new DOCX (via `office/docx-toolkit`) and a tracked-changes
   markdown diff so a human can audit every change before sending.

## When to use it

- A candidate is applying to multiple specific roles and wants
  per-application tailoring without losing their voice.
- An internal recruiter wants to surface relevant experience from a
  long CV.

## When **not** to use it

- The candidate is more than a small tweak away from the role — this
  skill *never* invents experience.
- The output is a public profile (LinkedIn) — write directly there, not
  via a DOCX intermediary.

## Determinism and risk

Determinism: **low** — LLM-mediated rewording. Risk: **low** — output is
reviewed via the tracked-changes diff before use.

## How it composes

Hard dependency on `office/docx-toolkit` for the output write step.
