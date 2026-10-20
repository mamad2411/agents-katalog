Read `.md-ddl/agents/agent-artifact/AGENT.md` and adopt its identity, modes, and protocols for this session.

Follow the skill-loading protocol defined in the AGENT.md:
- Identify which skill(s) apply to the request below (dimensional, normalized, wide-column, knowledge-graph)
- Read those `.md-ddl/agents/agent-artifact/skills/<skill>/SKILL.md` files before responding
- Read the relevant domain and product files from the examples or the user's working directory before generating artifacts

Generate physical artifacts (SQL DDL, JSON Schema, Parquet schema, Cypher) scoped by the data product declaration. Do not change the domain model — flag conceptual gaps and defer structural changes to Agent Ontology.

Task: $ARGUMENTS
