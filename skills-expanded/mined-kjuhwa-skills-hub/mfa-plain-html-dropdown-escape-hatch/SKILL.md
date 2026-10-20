---
name: mfa-plain-html-dropdown-escape-hatch
description: When a library Dropdown component infinite-loops or cross-origin-fails inside a Module Federation remote, replace it with a plain HTML `<button>` + absolutely-positioned menu `<ul>`. Cheaper than debugging the library's portal/context assumptions.
category: frontend
tags: [module-federation, dropdown, antd, infinite-loop, cross-origin, react]
triggers: ["Dropdown infinite loop", "options useMemo", "MFA dropdown", "portal cross-origin", "library dropdown broken in remote"]
source_project: lucida-ui
version: 0.1.0-draft
---

# Plain-HTML Dropdown Escape Hatch in MFA

Skip the library Dropdown in MFA-exposed components. Use a button + absolutely-positioned `<ul>` and close on outside click.

See `content.md`.
