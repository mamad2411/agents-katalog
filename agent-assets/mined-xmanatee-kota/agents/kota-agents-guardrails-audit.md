# Guardrails-Audit Module

Owns the guardrail audit trail: subscribes to `guardrail.assessed` events and writes entries to `.kota/audit.jsonl`.

- Provides an append-only audit store, CLI subcommands, and an HTTP route for querying guardrail decisions.
