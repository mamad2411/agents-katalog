# Events

Owns synchronous event delivery, scope attribution, module-event declarations,
and the durable event journal. Module payload catalogs stay with their declaring
modules; the event journal records occurrence and provenance, while workflow
state and outbox delivery remain workflow-owned.

Verification uses observable delivery, rejection, replay, persisted redaction,
and retention. Scope isolation must assert the complete received set, including
the absence of another scope's traffic. Journal examples use representative
payloads rather than copied product declarations or projection snapshots.
Registry and declaration checks exercise collision rejection or downstream
validation; strict types and the declaration itself own static field shape.
Journal and dead-letter projections share schema-aware event redaction, including
events rejected before persistence. Redaction examples use neutral field names
and values so generic secret-key heuristics cannot mask a missing schema check.
