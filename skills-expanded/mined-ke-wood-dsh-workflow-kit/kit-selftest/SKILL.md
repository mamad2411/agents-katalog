---
name: kit-selftest
description: Self-containment probe for dsh-workflow-kit. Only exists inside the package, not in ~/.dsh/skills. If this skill is loadable, the bundled skill provider works.
---

# Kit Self-Test

This skill exists **only** inside the `dsh-workflow-kit` package directory.
It is not present in `~/.dsh/skills/`.

If you can load this skill, the package's own `index.js` skill provider
is registered and working — meaning the kit is self-contained.
