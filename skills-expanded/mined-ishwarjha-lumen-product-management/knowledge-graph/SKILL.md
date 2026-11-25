---
name: knowledge-graph
description: Knowledge Graph entity types and relationships (v2.2)
triggers:
  [
    "knowledge graph",
    "KG",
    "entity",
    "experiment",
    "decision",
    "opportunity",
    "launch",
    "governance event",
    "persist",
    "remember",
    "persona",
    "metric formula",
    "pricing band",
    "regulatory constraint",
    "tech debt",
    "org chart",
  ]
---

v2.2 Entity Types (15):

- UserSegment
- Opportunity
- Persona
- Experiment
- Feature
- Decision
- Metric
- MetricFormula
- Launch
- GovernanceEvent
- PricingBand
- EventTaxonomy
- RegulatoryConstraint
- TechDebtItem
- OrgNode

Required behavior:

- Agents must check `supabase_connected` before any KG write. If false, write is skipped and the agent must include the exact language: "Knowledge Graph write skipped — connect Supabase to persist this finding."
- Outcome tracking edges: Decision → outcome_confirmed_by → Experiment (30/60/90 day).

Implementers should include fields for each entity and the relationship table; use pgvector for vector content where needed.
