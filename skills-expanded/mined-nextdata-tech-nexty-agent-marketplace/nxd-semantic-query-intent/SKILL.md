---
name: nxd-semantic-query-intent
description: Use when a query adapter has a verbatim semantic question, a complete agreed catalog, and a concept-name selection that must be checked for correct intent before governed execution. This narrow foundation skill validates intent; it is not an entry point for discovery, runtime lifecycle, routing, or query syntax.
allowed-tools:
  - Read
  - AskUserQuestion
metadata:
  author: nextdata
  version: 0.76.0
---

# Semantic query intent validation

Apply this foundation after the calling query adapter has collected the
verbatim question, the complete catalog for its agreed scope, and a candidate
selection. Consult
[reference/semantic-intent-validation.md](reference/semantic-intent-validation.md)
for the canonical gate.

The gate validates intent-to-selection mapping before governed execution:

1. Check that catalog coverage is complete for the agreed scope before relying
   on relevance or grain decisions.
2. Have the catalog-aware critic compare the question, selection, and model
   descriptions, including compatibility and reachability metadata. Match the
   question's terms against each concept's name and any `synonyms` its catalog
   row lists, and select the canonical `name`, never the synonym. Every SCOPE
   constraint (a named value, entity, segment, or time window that narrows the
   population) must be honored. Use a filter when a catalog dimension's
   description expresses it; when a metric definition already encodes it (for
   example, a partner-sourced metric), selecting that metric satisfies the
   constraint without a filter. A value found in exactly one candidate
   dimension resolves which dimension holds it; descriptions still decide
   whether that dimension means what the question asks. Use stored values
   verbatim: if the question phrase matches one stored value as a whole, treat
   it as one value; never split on
   `&`, `and`, or `/` unless the stored domain shows separate values that the
   question means. A requested BREAKDOWN (such as "by product" or "per month")
   maps to a grouped dimension. A comparison of named values (such as
   "Psychiatry vs Neurology") needs a filter restricting to those values and
   grouping by that dimension; grouping never substitutes for filtering on a
   named value. Add a missing filter only when the question asks for it and a
   dimension description expresses the constraint, then re-run the critic.
   Never add an unrequested filter or exclusion. Return `likely-wrong` and
   abstain or clarify only when no
   metric or dimension can express the constraint.
   Treat author `agent_instructions` (data-product and model level) like
   descriptions: evidence for scope and intent, never permission. A matching
   verified query is evidence for the selection, not a substitute for this
   check. Governance and the user's explicit request outrank both. A filter
   only an instruction or a verified query implies counts as unrequested:
   apply it only when it defines a term the question uses, and name it in the
   echo; otherwise leave it out and offer it.
3. Show a plain-language round-trip echo assembled from the selected concepts'
   descriptions, including applicable PII or governance notes.
4. Clarify or abstain when the mapping is ambiguous, likely wrong, unavailable,
   or unreachable. On an ambiguous-name refusal (SQ-108), choose among its
   listed candidates only when the question decides it, else ask; never guess.
   When the response lists `resolved` substitutions, check them against the
   approved concepts and mention one that matters to the answer.

Execute only after the critic returns `ok` or the user explicitly confirms a
surfaced ambiguity. Do not treat confirmation as making an unavailable concept
or impossible relationship valid; remap or ask for a supported concept first.

Keep discovery, catalog scoping, query grammar, routing, authentication,
storage, runtime lifecycle, and result presentation in the calling adapter.
Do not add surface-specific operator lists or transport instructions to this
foundation. Do not use it as a standalone entry point when the caller has not
supplied the question and catalog.

## Additional resources

For the detailed gate, consult
`reference/semantic-intent-validation.md` after the adapter has established
the agreed catalog and before it executes the selection.
