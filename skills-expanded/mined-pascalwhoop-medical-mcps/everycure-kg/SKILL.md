---
name: everycure-kg
description: "Expert guide for querying the Everycure Knowledge Graph (9.2M nodes, 77M relationships) for drug repurposing, mechanistic pathway discovery, and biomedical research. Use this skill when working with Everycure KG MCP tools to: (1) Find drug-disease connections and repurposing opportunities, (2) Explore mechanistic pathways (drug→protein→gene→disease), (3) Discover gene-disease associations, (4) Avoid path explosion in dense graph queries, (5) Navigate schema quirks and validate queries, (6) Design custom metapaths for novel hypotheses. Critical for biomedical researchers, drug discovery teams, and anyone performing knowledge graph-based drug repurposing analysis."
---

# Everycure Knowledge Graph Skill

## Overview

The Everycure KG is a massive biomedical knowledge graph (9.2M nodes, 77M relationships) built on the Biolink Model. It integrates data on drugs, diseases, genes, proteins, pathways, and their relationships.

**Key Challenge**: The graph is extremely densely connected. Naive queries cause **path explosion** (~440x growth per hop).

**Safety Built-In**: The MCP server includes automatic safety checks:
- Warns on high-degree nodes (>1K edges)
- Blocks queries on super-hubs (>10K edges)
- Prevents path explosion before executing queries
- Handles schema quirks automatically in predefined metapaths

This skill teaches you to query effectively and work within the safety guardrails.

---

## Quick Start

### Finding Drug Repurposing Opportunities

**Question**: "Does Metformin treat Idiopathic Pulmonary Fibrosis?"

**Step 1**: Find node IDs
```python
# Use execute_cypher to find nodes
result = execute_cypher("""
    MATCH (d) WHERE d.name CONTAINS 'Metformin' AND 'biolink:Drug' IN labels(d)
    RETURN d.id, d.name LIMIT 5
""")
# Result: CHEBI:6801

result = execute_cypher("""
    MATCH (dis) WHERE dis.name CONTAINS 'pulmonary fibrosis' AND 'biolink:Disease' IN labels(dis)
    RETURN dis.id, dis.name LIMIT 5
""")
# Result: MONDO:0800029
```

**Step 2**: Check direct treatment relationship (1-hop)
```python
result = find_paths_by_metapath(
    source_id="CHEBI:6801",
    target_id="MONDO:0800029",
    metapath_name="drug_to_disease_direct"
)
# Result: FOUND - Direct treatment relationship exists!
```

**Step 3**: Find mechanistic targets (2-hop)
```python
result = find_paths_by_metapath(
    source_id="CHEBI:6801",
    target_id="MONDO:0800029",
    metapath_name="drug_to_disease_via_target"
)
# Result: 50+ proteins including HDAC6 (AMPK pathway)
```

---

## Core Principles

### 1. Always COUNT Before RETURN

Path explosion happens when you RETURN data before counting.

```cypher
// WRONG (will hang on large results):
MATCH (d)-[r1]-(mid)-[r2]-(target)
WHERE d.id = $drug_id
RETURN d, mid, target LIMIT 100

// CORRECT (count first):
MATCH (d)-[r1]-(mid)-[r2]-(target)
WHERE d.id = $drug_id
RETURN COUNT(*) as path_count
// If path_count < 1000, then run:
// MATCH... RETURN d, mid, target LIMIT 100
```

### 2. Start from Drug or Disease Nodes

**Safe Starting Points** (low degree):
- Drug: 73K nodes, avg degree ~125
- Disease: 112K nodes, avg degree ~1.4K

**Risky Starting Points** (high degree):
- Protein: 458K nodes, avg degree ~3.5K
- Gene: 264K nodes

**NEVER Start From** (path explosion guaranteed):
- OrganismTaxon: 3.2M nodes
- SmallMolecule: 3M nodes

### 3. Use Specific Relationship Types

**Good**: `-[:directly_physically_interacts_with]->` (specific)
**Bad**: `-[*]->` (wildcard - path explosion!)

### 4. Limit Hops to 2-3 Maximum

- **1-hop**: Fast (<1s), safe, 0-100 results
- **2-hop**: Acceptable (1-5s), 0-1000 results
- **3-hop**: Risky (5-30s), may explode without filtering
- **4+ hops**: Path explosion inevitable (millions-billions of paths)

**Average growth**: ~440x per hop
- 1-hop: 125 neighbors
- 2-hop: 67,000 neighbors (535x)
- 3-hop: 29M+ neighbors (unusable)

### 5. Always Include LIMIT Clauses

```cypher
// NEVER do this:
MATCH (d:Drug)-[r]->(dis:Disease)
RETURN d, dis  // Will return 35K rows!

// ALWAYS do this:
MATCH (d:Drug)-[r]->(dis:Disease)
RETURN d, dis LIMIT 100
```

---

## Workflow for Drug Repurposing Queries

### Standard Workflow

1. **Find Node IDs** (use name search + label filtering)
2. **Check Direct Relationship** (1-hop, use `drug_to_disease_direct` metapath)
3. **Find Mechanistic Connections** (2-hop, use `drug_to_disease_via_target`)
4. **Explore Pathways** (if needed, 3-hop with caution)
5. **Assess Side Effects** (check contraindications)

### Example: Complete Drug Repurposing Analysis

```python
# Step 1: Find drug
drug_query = """
MATCH (d) WHERE d.name CONTAINS 'Lenalidomide'
  AND ('biolink:Drug' IN labels(d) OR 'biolink:SmallMolecule' IN labels(d))
RETURN d.id, d.name, labels(d)
LIMIT 5
"""
drug_result = execute_cypher(drug_query)
drug_id = drug_result["data"][0]["d.id"]  # CHEMBL:CHEMBL1336

# Step 2: Find disease
disease_query = """
MATCH (dis) WHERE dis.name CONTAINS 'multiple sclerosis'
  AND 'biolink:Disease' IN labels(dis)
RETURN dis.id, dis.name
LIMIT 5
"""
disease_result = execute_cypher(disease_query)
disease_id = disease_result["data"][0]["dis.id"]  # MONDO:0005301

# Step 3: Direct treatment?
direct = find_paths_by_metapath(
    source_id=drug_id,
    target_id=disease_id,
    metapath_name="drug_to_disease_direct"
)

# Step 4: Mechanistic via proteins?
via_targets = find_paths_by_metapath(
    source_id=drug_id,
    target_id=disease_id,
    metapath_name="drug_to_disease_via_target"
)

# Step 5: Genetic connections?
via_genes = find_paths_by_metapath(
    source_id=drug_id,
    target_id=disease_id,
    metapath_name="drug_to_disease_via_gene"
)

# Step 6: Safety check
contraindications = execute_cypher("""
    MATCH (d:Drug {id: $drug_id})-[:contraindicated_in]->(dis:Disease {id: $disease_id})
    RETURN COUNT(*) as contraindicated
    """,
    {"drug_id": drug_id, "disease_id": disease_id}
)

# Step 7: Synthesize evidence
evidence_score = (
    10 if direct["data"]["paths"] else 0 +
    5 if via_targets["data"]["paths"] else 0 +
    3 if via_genes["data"]["paths"] else 0 -
    20 if contraindications["data"][0]["contraindicated"] > 0 else 0
)
```

---

## Predefined Metapaths

Use these via `find_paths_by_metapath()` tool:

### All 6 Predefined Metapaths (Reliable)

The MCP server provides 6 predefined metapaths that automatically handle schema quirks and prevent path explosion:

1. **drug_to_disease_direct** (1-hop) - Direct clinical evidence
2. **drug_to_disease_via_target** (2-hop) - Mechanistic protein targets
3. **drug_to_disease_via_gene** (3-hop) - Via gene associations
4. **drug_to_disease_via_pathway** (3-hop) - Via pathway mechanisms
5. **disease_to_disease_shared_gene** (2-hop) - Shared genetic basis
6. **drug_side_effect_path** (1-hop) - Side effects (direct causation)

**Key Features**:
- Schema quirks (reversed relationships, specific predicates) handled automatically
- Safety checks prevent path explosion on high-degree nodes
- Tested with known working drug-disease pairs

**See [metapaths.md](references/metapaths.md) for detailed descriptions and when to use each**

---

## Common Query Patterns

### Pattern 1: Find Disease Genes

```cypher
MATCH (g:Gene)-[r:gene_associated_with_condition]->(dis:Disease)
WHERE dis.id = $disease_id
RETURN g.id, g.name, type(r)
ORDER BY r.score DESC
LIMIT 50
```

### Pattern 2: Find Drugs Targeting Gene

```cypher
MATCH (d:Drug)-[:directly_physically_interacts_with]->(p:Protein)
      -[:gene_product_of]->(g:Gene)
WHERE g.id = $gene_id
RETURN d.id, d.name, p.id, p.name
LIMIT 50
```

### Pattern 3: Find Disease Pathways

```cypher
// Option 1: Direct (sparse, only 607 edges)
MATCH (dis:Disease)-[:disease_has_basis_in]->(path:Pathway)
WHERE dis.id = $disease_id
RETURN path.id, path.name
LIMIT 20

// Option 2: Via proteins (more results)
MATCH (dis:Disease)<-[:associated_with]-(p:Protein)
      <-[:has_participant]-(path:Pathway)
WHERE dis.id = $disease_id
RETURN path.id, path.name, COUNT(p) as protein_count
ORDER BY protein_count DESC
LIMIT 20
```

### Pattern 4: Check Drug Safety (Contraindications)

```cypher
MATCH (d:Drug)-[:contraindicated_in]->(dis:Disease)
WHERE d.id = $drug_id
RETURN dis.id, dis.name
LIMIT 50
```

### Pattern 5: Find Drug Side Effects

```cypher
// Side effects as Disease (primary, 35K edges)
MATCH (d:Drug)-[:causes]->(se:Disease)
WHERE d.id = $drug_id
RETURN se.id, se.name
LIMIT 50

// Side effects as PhenotypicFeature (alternative, 25K edges)
MATCH (d:Drug)-[:causes]->(se:PhenotypicFeature)
WHERE d.id = $drug_id
RETURN se.id, se.name
LIMIT 50
```

**See [query-patterns.md](references/query-patterns.md) for complete pattern library with performance metrics**

---

## Schema Quirks (Handled in Predefined Metapaths)

The Everycure KG has deviations from Biolink Model. **Predefined metapaths handle these automatically**, but custom queries must account for them.

### Key Schema Differences

1. **Protein → Pathway REVERSED**
   - Biolink expectation: `Protein -[:actively_involved_in]-> Pathway` (23.9K edges)
   - Actual schema: `Pathway -[:has_participant]-> Protein` (312K edges - 13x more!)
   - Predefined metapaths use correct direction

2. **Disease → Pathway REVERSED**
   - Biolink expectation: `Pathway -[:associated_with]-> Disease`
   - Actual schema: `Disease -[:disease_has_basis_in]-> Pathway` (607 edges)
   - Predefined metapaths use correct direction

3. **Gene → Disease: Specific Predicate Required**
   - Generic: `Gene -[:associated_with]-> Disease` (38.6K edges)
   - Specific: `Gene -[:gene_associated_with_condition]-> Disease` (52.8K edges)
   - Predefined metapaths use specific predicate

4. **Side Effects: Dual Modeling**
   - Both Disease (35K edges) AND PhenotypicFeature (25K edges)
   - Predefined `drug_side_effect_path` uses 1-hop direct to Disease

**When Schema Quirks Matter**:
- Writing custom Cypher queries (not using predefined metapaths)
- Using `find_paths_by_custom_metapath()` (must specify correct relationships)
- Debugging why custom queries return 0 results

**See [schema-quirks.md](references/schema-quirks.md) for complete details when writing custom queries**

---

## Tools Reference

### Core Query Tools

**execute_cypher(query, parameters, database)**
- Run custom Cypher queries
- Use for node lookups, custom patterns, validation
- **Always include LIMIT clauses**

**get_neighborhood(node_id, relationship_types, node_labels, max_hops, limit)**
- Get neighbors of a node
- Safety checks prevent explosion on high-degree nodes
- Use `get_neighborhood_stats` first to check degree

**find_paths_by_metapath(source_id, target_id, metapath_name, max_paths)**
- Use predefined biochemically sound metapaths
- Prevents path explosion
- Limited to 6 predefined patterns

**find_paths_by_custom_metapath(source_id, target_id, metapath_pattern, max_paths, max_hops)**
- Design custom metapath patterns
- **Max 5 hops** for safety
- Validates node/relationship types before querying

### Discovery Tools

**get_schema(database)**
- Get all node labels and relationship types
- Use to validate schema assumptions

**get_supported_types(database)**
- Get 25 common node types and 30 common relationship types
- Filtered for drug repurposing relevance

**get_supported_metapaths()**
- List all 6 predefined metapaths
- Includes descriptions and patterns

**get_stats(database)**
- Get KG size: 9.2M nodes, 77M relationships

**get_neighborhood_stats(node_id, max_hops)**
- Count neighbors WITHOUT materializing paths
- **Use this BEFORE get_neighborhood to avoid explosion**

### High-Level Tools

**find_drugs_for_disease(disease_id, include_indirect, exclude_contraindicated, max_paths_per_metapath)**
- Comprehensive drug search for a disease
- Uses multiple metapaths automatically
- Filters contraindications

**find_diseases_for_drug(drug_id, include_indications, include_contraindications, include_adverse_events)**
- Find all disease associations for a drug
- Categorizes by relationship type

---

## When to Read Reference Files

### [biolink-model.md](references/biolink-model.md) - Read when:
- You're unfamiliar with Biolink Model node types and relationships
- Designing custom metapaths and need to understand valid patterns
- Troubleshooting why a query isn't working (node type mismatch?)

### [cypher-guide.md](references/cypher-guide.md) - Read when:
- You need to write custom Cypher queries
- You're unfamiliar with Neo4j query syntax
- You need advanced Cypher patterns (aggregation, filtering, ordering)

### [query-patterns.md](references/query-patterns.md) - Read when:
- Starting a new drug repurposing query (check proven patterns first)
- Debugging failed queries (compare to anti-patterns)
- Optimizing query performance (learn from benchmarks)
- **This is the MOST IMPORTANT reference** - read it for any non-trivial query

### [metapaths.md](references/metapaths.md) - Read when:
- Using predefined metapaths and need to understand what they do
- Designing custom 3-hop metapaths (learn from examples)

### [schema-quirks.md](references/schema-quirks.md) - Read when:
- Writing custom Cypher queries (not using predefined metapaths)
- Designing custom metapaths with `find_paths_by_custom_metapath()`
- A custom query returns 0 results unexpectedly

---

## Common Mistakes and How to Avoid Them

### Mistake 1: Assuming Biolink Model = KG Reality

**Problem**: Querying `Protein -[:actively_involved_in]-> Pathway` finds only 23.9K edges

**Solution**:
- **Use predefined metapaths** - they handle schema quirks automatically
- **For custom queries**: Validate schema first, use reversed `Pathway -[:has_participant]-> Protein` (312K edges)

### Mistake 2: Not Using LIMIT

**Problem**: Query returns 35K rows, overflows context window

**Solution**: Always add `LIMIT 100` (or smaller) to queries

### Mistake 3: Starting from High-Degree Nodes

**Problem**: Querying from Protein node causes 2-hop explosion (1.4M neighbors)

**Solution**: Start from Drug or Disease nodes, use Protein as intermediate only

### Mistake 4: Using Generic Node Labels

**Problem**: Querying `biolink:SmallMolecule` returns 3M nodes

**Solution**: Filter to `biolink:Drug` specifically (73K nodes)

### Mistake 5: 3+ Hop Queries Without Validation

**Problem**: 3-hop query hangs, times out

**Solution**: Validate EACH hop independently before chaining, always COUNT first

---

## Performance Expectations

### Query Performance Tiers

| Tier | Time | Query Type | Max Results | Examples |
|------|------|------------|-------------|----------|
| 1 | <1s | Node lookups, 1-hop direct | 100 | drug_to_disease_direct |
| 2 | 1-5s | 2-hop filtered metapaths | 100 | drug_to_disease_via_target |
| 3 | 5-30s | 2-hop unfiltered, 3-hop counts | 1000 | Neighborhood stats |
| 4 | >30s | 3+ hop queries | AVOID | Path explosion |

### Success Rates from Real Queries

- **1-hop direct treatment**: 100% when relationship exists
- **2-hop via protein targets**: 90% for well-studied drugs
- **3-hop via genes**: 70% for well-studied drug-disease pairs
- **3-hop via pathways**: 50% (sparse pathway annotations in KG)

---

## Debugging Workflow

### Symptom: 0 Results Returned

1. Verify node IDs exist: `MATCH (n {id: $node_id}) RETURN n`
2. Check node labels: `MATCH (n {id: $node_id}) RETURN labels(n)`
3. List actual relationships: `MATCH (n {id: $node_id})-[r]-() RETURN DISTINCT type(r) LIMIT 20`
4. Try bidirectional: Change `-[r]->` to `-[r]-`
5. Check schema quirks in [schema-quirks.md](references/schema-quirks.md)

### Symptom: Query Hangs/Times Out

1. Add `COUNT(*)` before `RETURN *`
2. Reduce hops (3 → 2 → 1)
3. Add specific relationship types (remove wildcards)
4. Check if starting from high-degree node (Protein, Gene, OrganismTaxon)
5. Add more restrictive filters (node labels, LIMIT)

### Symptom: Too Many Results (>1000)

1. Add `LIMIT 100` (or smaller)
2. Add specific node label filters
3. Use `ORDER BY relevance_score DESC` before LIMIT
4. Use aggregation: `COUNT(*)`, `collect(...)[0..10]`

---

## Example: Complete MS Drug Discovery

Using lessons from 24 MS GWAS genes analysis:

```python
# Step 1: Get MS GWAS genes
ms_genes = execute_cypher("""
    MATCH (g:Gene)-[r:gene_associated_with_condition]->(dis:Disease)
    WHERE dis.name CONTAINS 'multiple sclerosis'
    RETURN g.id, g.name, r.score
    ORDER BY r.score DESC
    LIMIT 25
""")

# Step 2: For each gene, find drugs
for gene in ms_genes["data"]:
    gene_id = gene["g.id"]

    # Find proteins encoded by gene
    proteins = execute_cypher("""
        MATCH (g:Gene {id: $gene_id})<-[:gene_product_of]-(p:Protein)
        RETURN p.id, p.name
        LIMIT 10
        """,
        {"gene_id": gene_id}
    )

    # Find drugs targeting those proteins
    for protein in proteins["data"]:
        drugs = execute_cypher("""
            MATCH (d:Drug)-[r:directly_physically_interacts_with|affects]->(p:Protein {id: $protein_id})
            RETURN d.id, d.name, type(r)
            LIMIT 50
            """,
            {"protein_id": protein["p.id"]}
        )

        # Store drug-pathway-gene triplets
        for drug in drugs["data"]:
            triplet = {
                "drug": drug["d.name"],
                "protein": protein["p.name"],
                "gene": gene["g.name"],
                "mechanism": drug["type(r)"],
                "gwas_signal": gene["r.score"]
            }
            # Add to repurposing candidates list

# Step 3: Rank candidates by multiple criteria
# (mechanism strength, MS relevance, safety profile, etc.)
```

---

## Success Patterns from 15+ Real Drug Repurposing Queries

**Highest Success** (80-100% query success):
- Metformin → IPF (75%)
- Rituximab → CHS (90%)
- Lenalidomide → RDD (100% - 704 targets found!)
- Losartan → EB (83%)
- L-Glutamine → SCD (100%)
- JAK inhibitors → SSc (100%)

**Key Success Factors**:
1. Direct treatment relationships in KG
2. Well-studied drug-protein-disease triangles
3. Multiple parallel mechanisms
4. Complete pathway chains

**What Causes Failures**:
1. Missing schema relationships (reversed directions)
2. Sparse annotations (< 1000 edges)
3. Rare diseases (limited research)
4. Recent discoveries (not yet in KG)

---

## Next Steps

1. **Start with `find_drugs_for_disease()` or `find_diseases_for_drug()`** - High-level tools that handle complexity
2. **If those don't work, use predefined metapaths** - Tested and reliable
3. **For novel hypotheses, design custom metapaths** - But validate schema first!
4. **When in doubt, read [query-patterns.md](references/query-patterns.md)** - Proven patterns for 90% of use cases

---

## Key Takeaways

1. **Path explosion is real** - 440x growth per hop, 2-3 hop max
2. **COUNT before RETURN** - Always check path count first
3. **Start from Drug/Disease** - Never from Protein/Gene/OrganismTaxon
4. **Schema ≠ Biolink Model** - Validate directions and predicates
5. **Use specific types** - `gene_associated_with_condition` > `associated_with`
6. **LIMIT everything** - Never query without limits
7. **Proven patterns exist** - Check [query-patterns.md](references/query-patterns.md) first
8. **Tools are your friend** - Use high-level tools before custom Cypher
