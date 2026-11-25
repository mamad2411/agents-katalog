---
name: research-topic
description: Researches a technical question and returns a short sourced brief with options compared and one clear recommendation.
disable-model-invocation: true
---

Research this question and give a brief: $ARGUMENTS

1. Restate the question and the constraints you can see in this repository: language, runtime, hosting, existing dependencies, license rules. Ask one clarifying question only if the answer would change the result.
2. Find two to four candidates. Use official documentation, release notes and the project's repository first; check last release date, open issue trends and license. Search the codebase for existing solutions before proposing a new dependency.
3. Compare on what matters here: fit, effort to adopt, operating cost, lock-in, maturity, security record.
4. Prefer facts you can cite. Mark anything uncertain as such. Never invent version numbers or benchmark results.

Format, under 400 words:
**Recommendation** (one sentence), **Options** (table with pros, cons, source link each), **Why this one**, **Risks**, **What would change my mind**, **Sources** (URLs with the date accessed).

Do not install packages or edit files. Offer a small proof of concept as a next step and ask whether to start it.
