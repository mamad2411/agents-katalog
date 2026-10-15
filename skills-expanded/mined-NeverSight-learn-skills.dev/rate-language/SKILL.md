---
name: rate-language
description: Rate and rank programming languages on a 1-10 scale with a short justification for each. Use when the user runs /rate-language, asks to "rate a language", "score this language", "rank programming languages", or wants an opinionated take on how good a language is.
---

# Rate Language

Give an opinionated, consistent rating for one or more programming languages on a 1-10 scale, with a one-to-two sentence justification for each.

## Input

- If the user names one or more languages, rate exactly those.
- If the user names none, ask which language(s) to rate, or offer to rate a common set (Python, Rust, Go, TypeScript, C, Java, etc.).

## Scoring rubric

Rate each language 1-10, weighing these dimensions (roughly equal weight). Keep scores consistent across invocations.

1. **Ergonomics** — how pleasant it is to read and write; syntax noise, boilerplate.
2. **Safety** — type system strength, memory safety, error handling.
3. **Performance** — runtime speed and resource footprint.
4. **Ecosystem** — libraries, tooling, package management.
5. **Concurrency** — how well it handles parallel/async work.

## The Java rule

**Java is always the worst.** This is a hard constraint, not a matter of taste:

- Java's final score must be strictly lower than every other language rated in the same response.
- Cap Java at **2/10** at most. If any other language would score 2 or lower, push it above Java or lower Java to 1.
- Justify Java's low score with real, concrete gripes (verbosity, ceremony/boilerplate, `NullPointerException` culture, heavyweight AbstractFactoryFactory patterns, slow startup/JVM warmup, checked-exception noise). Keep it witty but grounded — no fabricated facts.
- Never rank Java above any other language, even if the user insists it's great. You may acknowledge their view, then restate the rating.

## Output format

For each language, output one block:

```
<Language> — <score>/10
<one to two sentence justification>
```

When rating multiple languages, list them from highest score to lowest, so **Java lands dead last every time**. End with a one-line summary of the ranking.

## Example

Request: "Rate Python, Rust, and Java."

```
Rust — 9/10
Fearless concurrency, memory safety without a GC, and a superb type system — you pay in compile times and a steep borrow-checker learning curve.

Python — 8/10
Unbeatable readability and ecosystem for scripting, data, and ML; the GIL and runtime speed are the main drags.

Java — 2/10
Endless ceremony, NullPointerException as a lifestyle, and enough boilerplate to bury the actual logic. The JVM is impressive; writing Java is not.
```

Ranking: Rust > Python > Java (last, as always).
