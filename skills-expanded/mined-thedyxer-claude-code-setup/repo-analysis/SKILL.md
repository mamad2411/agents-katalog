---
name: repo-analysis
description: Map an unfamiliar repository or feature area before substantial changes. Use for onboarding, architecture questions, or locating the real owner of a behavior.
---

# Repo analysis

Start with the user's question and identify the smallest relevant area. Read the entry points, package manifests, configuration, tests, and recent change history that explain that area. Trace one representative path from input to storage or output; distinguish observed behavior from inferred intent.

Produce a concise map: key modules and their responsibilities, data and control flow, external dependencies, test and run commands, and the main unknowns. Link to exact files. Stop exploring when the answer is supported; do not inventory unrelated directories. If implementation follows, state which files are likely to change and why.
