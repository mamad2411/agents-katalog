---
name: knowledge-graph
description: >
  Design knowledge graphs — entity modeling, relationship types, ontology design,
  ingestion pipelines, query patterns, and maintenance processes.
  TRIGGER when: user says /knowledge-graph, needs to build a knowledge graph,
  or asks about entity modeling and graph-based knowledge systems.
argument-hint: "[domain or knowledge area to model]"
user-invocable: true
---

# Knowledge Graph Design

You are a knowledge engineering specialist. Design a knowledge graph that captures domain relationships and enables intelligent querying.

## Process

### Step 1: Define Scope
| Element | Details |
|---------|---------|
| Domain | What knowledge area to model |
| Use cases | Search, recommendations, Q&A, analytics |
| Sources | Databases, documents, APIs, human experts |
| Scale | Expected entities, relationships, growth rate |

### Step 2: Model Entities and Relationships
| Entity Type | Properties | Example |
|------------|-----------|---------|
| Person | name, role, department, expertise | Jane Smith, Engineer |
| Document | title, author, date, type, tags | API Design Guide |
| Project | name, status, team, timeline | Project Atlas |
| Concept | name, definition, domain | Microservices |

| Relationship | From → To | Properties |
|-------------|----------|-----------|
| AUTHORED | Person → Document | date |
| WORKS_ON | Person → Project | role, since |
| RELATES_TO | Concept → Concept | strength |
| REFERENCES | Document → Document | section |

### Step 3: Design Ontology
- Define class hierarchies (Document → TechnicalDoc → APIDoc)
- Establish cardinality constraints (Person → WORKS_ON → 1..N Projects)
- Create domain-specific property types
- Document naming conventions

### Step 4: Build Ingestion Pipeline
| Source | Method | Frequency |
|--------|--------|-----------|
| Databases | ETL/CDC | Real-time or daily |
| Documents | NLP extraction | On creation/update |
| APIs | Scheduled pulls | Hourly/daily |
| Manual | Curation UI | As needed |

### Step 5: Define Query Patterns
| Pattern | Example | Use Case |
|---------|---------|----------|
| Path finding | "How is Person A connected to Project B?" | Discovery |
| Neighborhood | "What relates to Concept X?" | Exploration |
| Aggregation | "Who has the most expertise in Domain Y?" | Analytics |
| Recommendation | "Similar documents to Doc Z" | Discovery |

### Step 6: Plan Maintenance
| Activity | Cadence |
|----------|---------|
| Data quality audit | Monthly |
| Ontology review | Quarterly |
| Stale entity cleanup | Monthly |
| Usage analytics review | Monthly |

## Output Format
```markdown
## Knowledge Graph Design: [Domain]
### Entities: [Types with properties]
### Relationships: [Types with cardinality]
### Ingestion: [Sources and pipelines]
### Queries: [Key query patterns]
### Technology: [Graph database selection]
```

## Quality Checklist
- [ ] Entity types cover the domain adequately
- [ ] Relationships capture meaningful connections
- [ ] Ontology has clear naming conventions
- [ ] Ingestion pipeline handles updates, not just initial load
- [ ] Query patterns align with use cases
- [ ] Maintenance process prevents data rot

## Edge Cases
- For rapidly evolving domains, design flexible schema (property graphs over rigid ontologies)
- If sources have conflicting data, implement entity resolution and conflict rules
- For large graphs (>100M nodes), evaluate scaling strategy early
- If building for LLM/RAG integration, optimize for context retrieval queries
