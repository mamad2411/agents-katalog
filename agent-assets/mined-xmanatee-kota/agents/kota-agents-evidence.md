# Evidence Policy

This directory owns the shared policy for durable evidence records and client
projections.

- Use this boundary for retention, redaction, provenance, and pruned-reference
  behavior across event journals, workflow runs, decisions, approvals, setup
  state, traces, and exported reports.
- Storage and API code should call the typed policy helpers instead of adding
  local sensitive-key regexes or target-specific redaction rules.
- Keep module setup manifests and scope policy as inputs. Do not duplicate
  module-owned requirement declarations here.
