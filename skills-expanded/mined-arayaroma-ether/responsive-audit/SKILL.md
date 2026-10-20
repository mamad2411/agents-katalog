---
name: responsive-audit
description: Audit and fix web layouts across mobile, laptop, and ultrawide viewports, with a required horizontal-overflow check.
allowed-tools: Read, Edit, Grep, Glob
---

# Responsive Audit

Use this skill for responsive UI changes or reviews. Check the rendered page at 390px, 1366px, and 2560px; add a viewport near any layout breakpoint when relevant.

Treat horizontal overflow as a release blocker. At every checked width, measure `document.documentElement.scrollWidth` and `document.documentElement.clientWidth`; they must be equal unless the task explicitly calls for a horizontal-scrolling region. Do not accept screenshots alone as evidence.

Fix the smallest owning layout. Common causes are `width: 100%` plus padding under `content-box`, intrinsic minimum widths in flex children or Shadow DOM, and controls that remain on one row at mobile widths. Preserve semantic table scrolling only when reflow would make the data less usable.

Finish by running the normal build or type check and report the tested viewport measurements.
