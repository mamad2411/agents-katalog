---
name: gherkin
description: Reference on Gherkin, the plain-language format for Behaviour-Driven Development (BDD) used by Cucumber and similar tools, drawing on the Cucumber reference and Seb Rose and Gáspár Nagy's BDD Books — syntax, writing good scenarios, discovering examples, and organizing feature files. Use when writing, reviewing, or refactoring .feature files or acceptance criteria, turning requirements into executable specifications, or running example mapping.
---

# Gherkin

Gherkin is a plain-text language for describing a system's behaviour as concrete examples. Tools such as Cucumber, SpecFlow/Reqnroll, Behave, and pytest-bdd turn each example into an automated test. This makes the spec "living documentation" that fails when it stops matching the system. The guidance here comes from the Cucumber Gherkin reference and Seb Rose and Gáspár Nagy's *The BDD Books*.

BDD has three practices: **discovery** (finding the rules and examples together), **formulation** (writing them as Gherkin), and **automation** (binding steps to code). Gherkin is the formulation step. Its main reader is a person, so write it for the business first and the test runner second.

## Table of contents

| Concept | Read when |
|---|---|
| [Syntax](references/syntax.md) | Looking up a keyword, outline, table, doc string, tag, or localization rule. |
| [Writing scenarios](references/writing-scenarios.md) | Writing or rewriting scenarios, or choosing between declarative and imperative steps. |
| [Discovery](references/discovery.md) | Turning a story or requirement into rules and examples before writing Gherkin. |
| [Organizing features](references/organizing.md) | Structuring feature files, rules, backgrounds, tags, and step definitions. |
| [Bad scenarios](references/bad-scenarios.md) | Reviewing feature files for common traps. |

## Validating

After writing or editing `.feature` files, run the validator and fix what it reports:

```sh
uv run scripts/validate.py <file-or-dir> [--json] [--strict] [--ignore RULE,...] [--max-steps N]
```

It parses each file with the official Cucumber Gherkin parser and reports syntax errors. It also lints the files against this guidance, such as one `When` per scenario, Given → When → Then order, step count, outline placeholders and columns, `Background` content, UI-driven steps, and placeholder data. Run `--list-rules` to see every rule ID. Errors mean the file is broken. Warnings are heuristics, so judge each one against the references above before changing the scenario.
