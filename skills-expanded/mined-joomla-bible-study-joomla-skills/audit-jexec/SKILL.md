---
name: audit-jexec
description: Audit Joomla extension PHP files for the missing `_JEXEC` direct-access guard, then add it. Use when checking distributed Joomla extension files for direct web access protection, or when explicitly invoked for a `_JEXEC` check.
---

# Audit Joomla `_JEXEC` guards

You are an experienced Joomla extension developer auditing this repository's extensions for the
`_JEXEC` runtime guard.

## Context

Every PHP file belonging to a Joomla extension needs this line at the top, after the file docblock
and after the `namespace` declaration if one is present:

```php
defined('_JEXEC') || die;
```

Without it, the file can be requested directly over HTTP and executed outside the CMS bootstrap —
with no configuration loaded, no session, and no access checks. What that leaks depends on the file:
a warning with a full path at best, a fatal error exposing the server layout, or executable behaviour
with none of Joomla's gating at worst.

Both `defined('_JEXEC') or die;` and the older `defined('_JEXEC') or die('Restricted access');` are
functionally equivalent. Joomla core uses `|| die;` — prefer it for new lines, but do not churn
existing files that already carry a working variant.

### Files that legitimately have no guard

Do not report these:

- Anything under a Composer `vendor/` directory.
- Unit and integration test files — they run under the test bootstrap, not the CMS, and are not
  shipped to clients.
- PHP files that are not part of a distributed extension: build scripts, tooling, CI helpers.
- Entry points that Joomla itself invokes before `_JEXEC` is defined, if the repository has any.
- Files that only declare a `namespace` and immediately `return` a closure consumed by the DI
  container are **not** an exception — `services/provider.php` needs the guard like anything else.

## Workflow

### Step 1 — Discovery

Find every distributed extension PHP file missing the guard. Report them as an alphabetically sorted
list of paths, grouped by extension where the repository holds more than one, and present it to the
user.

Note any file where the guard is present but misplaced — after code has already run, or before the
`namespace` declaration (which is a fatal error) — as a separate group. Those need a move, not an
insertion.

### Step 2 — Feedback round

The user is a subject matter expert and may remove entries from the list, or explain why a given file
is intentionally unguarded. Wait for that feedback before changing anything.

### Step 3 — Rectify

Add the missing line to the remaining files, placing it after the docblock and after the `namespace`
declaration where present. Preserve each file's existing formatting and blank-line style. Report what
changed.

---

*Adapted for this suite from the `audit-jexec` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
