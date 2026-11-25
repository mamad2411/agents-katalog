---
name: personal-page-polish
description: Polish an existing single-file personal page after the user asks for a clearer, more readable design while preserving its content and no-build setup.
license: MIT
---

# Personal Page Polish

Use this first-party Skill only when an existing `index.html` already works and the user asks to improve its presentation.

## Workflow

1. Read `index.html` and restate the requested mood plus any content that must not change.
2. Make the smallest HTML/CSS edit that improves hierarchy, spacing, contrast, and mobile readability.
3. Keep the page single-file and dependency-free. Do not add personal data, analytics, remote assets, or new features.
4. Show the changed sections and ask the user to inspect them before making another pass.

## Acceptance check

- Open the page at desktop size and at `390 × 844`.
- Confirm there is no horizontal overflow and all text remains readable.
- Use Tab and Enter to reach every interactive element in a logical order.
- Enable reduced motion and confirm the page remains usable.
- Confirm the console has no errors and the page makes no unexpected network requests.

Stop when these checks pass and the user accepts the visual change.
