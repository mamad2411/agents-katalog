---
name: php-check
description: Inspect the local PHP CLI for PHP 8.1 or newer, curl, json, and process execution. Use when the user asks to check PHP compatibility or troubleshoot missing runtime capabilities.
---
# PHP check

1. Read `references/checks.md` to learn the requirements and limits of this
   check.
2. Run `php scripts/check.php`.
3. Compare the observed values with the requirements. Report which checks pass
   and give the relevant next step for each unmet requirement.

If the script cannot run, explain the limitation. Do not claim that the runtime
passed checks you could not perform.
