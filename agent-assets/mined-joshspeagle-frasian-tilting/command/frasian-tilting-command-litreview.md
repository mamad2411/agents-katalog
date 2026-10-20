---
description: Run the literature-reviewer subagent to find real citations for a method.
---

Run the `literature-reviewer` subagent on `$ARGUMENTS`.

The argument should look like `<method-name> [one-sentence-description]`,
for example:

  /litreview fisher_rao Fisher-Rao geodesic between Gaussians
  /litreview bartlett

If only the method name is given, read `docs/methods/<name>.md` to
extract a one-sentence description from the Summary section before
invoking the agent.

The literature-reviewer will:

1. Search for real, citable papers (foundational / closely-related /
   contrasting).
2. Audit the brief for uncited claims.
3. Output a markdown block ready to paste into the brief's
   "Literature" section, plus a citation-audit list.

Relay the output verbatim. The user will copy it into the brief.
