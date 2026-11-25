---
name: already-translated-skill
description: Skill that already carries the translation sentinel; translator must no-op.
argument-hint: "<input>"
---

<!-- omc-port-translated: v1 -->
<!-- source: packages/copilot-cli-plugin/scripts/translate-test-fixtures/fixture-02-already-translated/input/SKILL.md | wave: 4.5 -->
This file already declares the translated sentinel as the first body line.

The translator should not modify it. It should not insert a second sentinel.
It should not rewrite identifiers. It should exit 0 with "no-op (already translated)".
