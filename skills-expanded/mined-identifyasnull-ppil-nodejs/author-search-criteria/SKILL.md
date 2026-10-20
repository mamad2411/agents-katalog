---
name: author-search-criteria
description: Used to extend the search ontology with rules to determine which class options to use when running text through the search-engine classifier. Use when ontology is missing to infer a noun-adjective class option.
intent: >-
  Author and update search criteria safely. This workflow helps decide whether a concept should stay in documentTypes (object modeling) or be implemented as search criteria, then drafts compliant criteria and ontology term keys.
type: workflow
best_for:
  - "Adding new noun/adjective/classOption ontology for natural-language search"
  - "Deciding object modeling vs search criteria for a concept"
  - "Drafting criteria files and global search term keys together"
scenarios:
  - "The classifier misses a concept users search in plain English"
  - "We need to add a new primary or secondary searchProperty"
  - "Should this concept be a documentType relation or search ontology?"
---

# Author Search Criteria

Extend search ontology when classifier coverage is missing, while avoiding incorrect modeling decisions.

## What This Skill Does

1. Classifies a candidate concept as either:
- object modeling in documentTypes
- search ontology via criteria files

2. Applies operational criticality rules for searchProperties:
- primary searchProperty: missing value creates workflow uncertainty or object ambiguity
- secondary searchProperty: useful for matching/ranking, but missing value does not materially change core flow

3. Produces implementation-ready assets:
- criteria-<concept>.json draft
- required searchTerms and attributiveSearchTerms keys for global-search-terms.json
- validation checklist before integration

## Decision Framework

### Step 1: Object Modeling vs Search Criteria

Use documentTypes/object modeling when the concept has:
- independent lifecycle and CRUD ownership
- transactional constraints, auditability, permissions, or financial effects
- cross-workflow state transitions that are not just descriptors

Use search criteria when the concept is:
- a reusable classifier or facet for query interpretation
- stable as a categorical descriptor on a flattened search object
- primarily needed for discoverability, classification, or ranking

Hybrid pattern is preferred for many domains:
- keep lifecycle entity in documentTypes
- project searchable classification fields into the search object
- classify via criteria rules and ontology keys

### Step 2: Primary vs Secondary SearchProperty Assignment

Primary if either is true:
- missing classification prevents choosing the correct workflow step
- missing classification makes object instance materially ambiguous

Secondary if:
- classification improves search/ranking UX
- workflow remains materially unchanged when absent

### Step 3: Criteria Structure Rules

Every new criteria file should include:
- name
- searchProperties
- searchTokenWindowSize
- baseProperties
- nlpProperties
- noun block with searchTerms
- adjectives block with searchTerms, searchProperty, classOptions
- nlpRules.matchRules default entry

Optionally include:
- inferenceRules for structured-to-classification mapping
- transformations to project or normalize computed fields

## Authoring Process

1. Capture concept and user query examples.
2. Run Step 1 decision (object model vs criteria).
3. Assign primary and secondary properties using Step 2.
4. Draft criteria-<concept>.json with noun plus adjective classOptions.
5. Add all referenced term keys into global-search-terms.json.
6. Validate JSON and schema compatibility.
7. Smoke-test with representative plain-English queries.
8. Promote to shared asset paths only after test pass.

## Output Template

### A) Modeling decision
- Concept:
- Decision: documentTypes | search criteria | hybrid
- Why:

### B) Search properties
- primary:
- secondary:

### C) Criteria draft plan
- file name:
- noun term key:
- adjective groups:
- classOptions by group:

### D) Ontology keys to add
- key list for global-search-terms.json

### E) Validation
- schema valid
- keys resolve
- classifier returns expected classOptions for sample queries

## Anti-Patterns

- Forcing entity lifecycle concerns into search criteria.
- Marking properties primary only because they are frequently queried.
- Adding criteria files without adding the required ontology term keys.
- Encoding private or internal-only information as user-facing search criteria.
- Duplicating concept semantics across multiple criteria files without ownership.

## Example Triggers

- "Users type a product phrase and classifier cannot map class options"
- "Need criteria-product-ireland with noun and adjective ontology"
- "Should sourceCountry be primary or secondary in this workflow?"

## References

- shared-lib/schema/search-criteria-schema.json
- shared-lib/search-engine.js
- sites/companions/assets/search-engine/search/global-search-terms.json
- sites/companions/assets/search-engine/search/criteria-location-ireland.json
