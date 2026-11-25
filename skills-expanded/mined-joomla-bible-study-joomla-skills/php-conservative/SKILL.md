---
name: php-conservative
description: Check a Joomla extension or any PHP project for compatibility with every stable PHP version it claims to support, using PHP_CodeSniffer with the PHPCompatibility standard over a testVersion range derived from composer.json. Knows that Joomla's bundled Symfony polyfills make some findings false positives in extensions but real in standalone projects. Use when auditing PHP version compatibility, chasing deprecation notices, or deciding whether a supported PHP range is actually safe — and when explicitly invoked for a PHP compatibility pass.
---

# Address stable PHP compatibility

You are an experienced PHP developer making this repository run cleanly across every stable PHP
version it claims to support.

## The goal

The software must run without warnings or notices from deprecated or obsolete PHP features, across
the **entire supported PHP version range** — not just the newest one.

That framing is what makes this different from a modernisation pass. You are auditing a *range*.

## Do not use Rector for this

Rector rewrites code **to** a target version. Its suggestions raise the floor — they break the bottom
of a supported range rather than reporting on it — so it is the wrong shape for auditing a range.

Several repositories still carry a years-old `rector.yaml`. Ignore it. Do not propose running Rector,
and do not spend the user's time re-deriving this conclusion.

The right tool is PHPCompatibility. It is token-based, so it needs no autoloading, no bootstrap, and
no CMS installation, and it takes seconds rather than minutes.

## Workflow

### Step 1 — Determine a realistic PHP version range

Read `require.php` (or `config.platform.php`) from the root `composer.json`.

**Derive the `testVersion` range from what the project declares — never guess or hard-code it**, so
the range checked always matches the range the project claims. Check the declared maximum against the
currently supported PHP versions at <https://www.php.net/supported-versions.php>.

If dependencies force a narrower window, document it and explain the options.

### Step 2 — Run PHP_CodeSniffer with the PHPCompatibility standard

Requires `squizlabs/php_codesniffer` plus `phpcompatibility/php-compatibility` at
**10.0.0-alpha2 or later**.

> The 9.3.5 release is from 2019 and knows nothing past PHP 7.4. Run it against a modern range and it
> reports almost nothing — which reads exactly like a pass. Check the installed version before you
> trust a clean result.

```
phpcs --standard=PHPCompatibility --runtime-set testVersion <min>-<max> .
```

Everything this does is read-only. Run `phpcs`, never `phpcbf`, and pass no `--fix`.

### Step 3 — Read the ceiling warning before trusting a clean report

**PHPCompatibility does not validate `testVersion`.** Ask it about a PHP version it has no sniff data
for and it reports *nothing at all*, indistinguishable from a clean bill of health.

Determine the highest PHP version the installed release actually has data for — check its changelog
or releases if unsure. If the declared `<max>` is above that ceiling, clamp the range to the ceiling
**and say so plainly in your findings**. Those versions are **unchecked, not clean**.

Never report "compatible with PHP X" on the strength of a static sweep that was clamped below X.
Covering the versions above the ceiling means executing the code on them, which is a different job.

### Step 4 — Triage the findings

Not every finding is a bug. Sort them into three piles and say which pile each went in:

- **Genuine problems.** Fix them.
- **Deliberate behaviour the sniff cannot know about.** A check whose entire purpose is to detect a
  removed feature gets flagged for mentioning it. Do not delete such a check to silence the sniff —
  that changes behaviour. Add a `phpcs:ignore <sniff code>` with a comment explaining why the code is
  correct as written, aimed at the next person tempted to "fix" it.
- **Provided by a polyfill.** Joomla ships Symfony polyfills, so PHP 8.0/8.1 symbols are available on
  every supported Joomla version. When PHPCompatibility flags a polyfilled symbol **in a Joomla
  extension**, suppress that specific finding with a `phpcs:ignore` naming the polyfill.
  **Do not apply that suppression to a standalone or CLI project** — nothing polyfills those symbols
  there, and hiding the finding would hide real breakage.

Where a genuine fix would break an already-supported version, gate it on `PHP_VERSION_ID`; if that is
not possible, flag it for manual review.

### Step 5 — Record a baseline only if the user asks

`phpcs --report=json` output can be saved as a baseline so later runs report only what is new. That
is for adopting this sweep in a repository with a large known backlog.

It is not a way to make a report go away, and a baseline is meant to shrink over time, never grow.
**Do not create one on your own initiative.**

### Step 6 — Feedback round

The user is a subject matter expert and will evaluate the findings and give further guidance.

### Step 7 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

Re-run the sweep after the fixes land, and report the before/after counts.

---

*Adapted for this suite from the `php-conservative` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
