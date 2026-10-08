---
name: android-finance-spec
description: Use when generating, reviewing, or refactoring Android Kotlin code for financial apps that require BigDecimal/String precision, RTL/i18n safety, Kotlin style discipline, and "do not reinvent existing project patterns" constraints.
---

# Android Finance Spec

This skill turns the Android finance coding specs into an actionable workflow for AI coding agents.

## Use When

- Building or reviewing Android / Kotlin financial, trading, wallet, crypto, billing, or investment code.
- Checking precision-sensitive values such as amount, price, balance, fee, rate, PnL, margin, or quantity.
- Reviewing RTL / multilingual UI, especially Arabic, Persian, Hebrew, mixed numbers, symbols, dates, and currency pairs.
- Enforcing project-first Kotlin style: reuse existing architecture, helpers, naming, Result wrappers, MVI/MVVM patterns, coroutine and Flow conventions.

## Workflow

1. Inspect the target repository before generating code.
   - Search for existing architecture, helpers, formatters, extension functions, base classes, and dependency patterns.
   - Do not invent missing project APIs. Add the smallest necessary abstraction only when no existing one fits.
2. Load only the relevant reference files:
   - Financial precision: `references/finance-number-skill.md`
   - RTL / i18n: `references/rtl-adaption.md`
   - Kotlin / Android style: `references/kotlin-style.md`
3. Apply every `MUST` and `MUST NOT` rule as a hard review gate.
4. For code review, run the bundled scanner when a local repository is available:

```bash
python3 <skill-dir>/scripts/android_finance_scan.py <project-root>
```

5. Treat scanner output as a first pass, not a substitute for engineering review. Inspect each finding in context.

## Hard Gates

- Financial decimal values must use `String` or `BigDecimal`, never `Double` / `Float`.
- Invalid or empty financial values must not silently become `0`; logic returns `null`, UI displays `--`.
- UI-visible strings must not be hardcoded.
- RTL-sensitive numeric text must keep signs, units, symbols, ranges, dates, and currency pairs in LTR isolation.
- Layout must prefer `start` / `end`; `layoutDirection` is allowed only for fixed-direction regions with a clear reason.
- New code must follow the target project's existing architecture and utilities before adding anything new.

## Output Expectations

- For generation: explain which existing project patterns were reused.
- For review: list findings by severity with file paths and line numbers.
- For refactoring: keep changes narrowly scoped and avoid unrelated style churn.
