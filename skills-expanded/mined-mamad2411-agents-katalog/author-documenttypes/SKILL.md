---
name: author-documentTypes
description: Determines the business domain for a given business plan and derives business objects correlated to documentTypes, documentTypes plus search criteria, or search criteria. Use when creating a new site from a business plan.
intent: >-
  Determine the business domain for a business plan, extract the underlying business objects, and classify each concept as a documentType, a documentType plus search criteria projection, or search criteria only. Use this when creating a new site from a business plan. This workflow uses the author-search-criteria skill to help decide search-related implementation details.
type: workflow
best_for:
  - "Creating a new site from a business plan"
  - "Deriving business objects from product or business-plan requirements"
  - "Deciding documentType vs documentType plus search criteria vs search criteria"
  - "Mapping domain objects to search projections and microservice ownership"
  - "Drafting repo-aligned documentType definitions from business requirements"
scenarios:
  - "We have a business plan and need the site domain model before coding"
  - "Which business objects should become documentTypes versus search criteria?"
  - "Create customer, picker, bundle, and order documentTypes from this plan"
  - "Determine which concepts should be naturally searchable in the new site"
---

# Author DocumentTypes

Translate a business plan into this repo's domain architecture before implementation starts.

## What This Skill Does

1. Determines the business domain implied by a business plan.
2. Extracts the business objects required to implement the site.
3. Correlates each concept to one of three implementation categories:
- `documentType`
- `documentType + searchCriteria`
- `searchCriteria`
4. Maps stateful documentTypes to the appropriate microservice pair.
5. Drafts planning artifacts and, when requested, concrete documentType definitions.

## Required Companion Skill

Use `author-search-criteria` when deciding whether a concept should stay in object modeling, be projected into search, or exist only as natural-language search criteria.

This skill owns the broader domain-modeling workflow. `author-search-criteria` is the specialized decision aid for search criteria design.

## Repo-Specific Rules

### Actor Rule

Any system actor or user type must have a corresponding `user` document with the same `id`.

Examples:
- `customer` requires `user`
- `picker` requires `user`

The `user` document is owned by auth and supports verification, validation, and ACL behavior.

Avoid duplicating auth-owned identity properties in actor documentTypes unless the business domain explicitly requires them.

### Runtime Metadata Rule

The following fields are added by creation flows and usually should not be declared in a documentType definition:

- `owner`
- `lastModifiedDate`
- `simulationId`
- `idHash`

Keep lifecycle metadata out of the documentType unless the platform explicitly models it as a business field.

### Relationship Rule

Prefer foreign-key style properties for transactional relationships.

Examples:
- `customerId`
- `pickerId`
- `bundleId`
- `correctionBundleId`

Avoid embedding whole referenced business objects directly into transactional records unless that pattern is already required by the platform.

### Search Projection Rule

Do not make every business object directly searchable.

Prefer a small number of explicit search projections such as:
- `searchBundle`
- `searchOrder`

The source entity remains the system of record. Search documents are generated projections enriched by inferred search properties.

### Shared Lookup Rule

Values defined once and reused across documentTypes should be modeled as shared lookup documentTypes.

Examples:
- `contentCountry`
- `contentRegion`
- `shippingOption`

Follow existing repo conventions for `controlType`, `customTypeOptions`, and `sharedLookup` usage.

## Workflow

### Step 1: Determine the Business Domain

Read the business plan and identify:
- actors
- catalog objects
- transactional objects
- finance objects
- policy objects
- remediation and review objects
- search-facing concepts

Do not confuse screens, filters, or workflow steps with domain objects unless they own state.

### Step 2: Extract Business Objects

List all business objects needed to implement the plan.

Use the business plan's rules, not just its nouns. If a flow implies state, ownership, fulfillment, pricing, or review behavior, capture the underlying object.

### Step 3: Correlate Objects to Implementation Types

Classify each object as one of:

#### `documentType`

Use when the concept has:
- independent lifecycle
- state transitions
- ownership or permission rules
- audit or financial effects
- operational consequences if modeled incorrectly

#### `documentType + searchCriteria`

Use when the lifecycle entity exists and some of its fields should be projected into natural-language search.

#### `searchCriteria`

Use when the concept is mainly:
- a classifier
- a facet for query interpretation
- a ranking signal
- an inferred search descriptor on a flattened search document

### Step 4: Use `author-search-criteria`

Invoke `author-search-criteria` to help decide:
- whether a concept is object modeling, search criteria, or hybrid
- whether a property should be primary or secondary in the search workflow
- which properties belong on `searchBundle`, `searchOrder`, or similar search projections

### Step 5: Assign Microservice Ownership

Assign each documentType to the microservice pair that owns its lifecycle.

Use lifecycle ownership, not convenience.

Common service boundaries:
- `Auth Service`
- `Customer Portal UI + Subscription Service`
- `Picker Portal UI + Fulfillment Service`
- `Catalog UI + Catalog Service`
- `Payments UI + Payments Service`
- `Compute Admin UI + Compute Service`

### Step 6: Draft Artifacts

Produce the planning artifacts needed to move into implementation:
- business-domain note
- documentType list
- service ownership table
- search projection list
- search criteria list
- draft documentType JSON files when requested

## Output Template

### A) Domain summary
- business domain:
- core flows:
- key constraints:

### B) Business objects
- actors:
- catalog:
- transactions:
- finance:
- policy:
- remediation:

### C) Correlation results
- documentTypes:
- documentTypes plus searchCriteria:
- searchCriteria only:

### D) Search projection plan
- searchable documentTypes:
- primary searchProperties:
- secondary searchProperties:

### E) Service ownership
- microservice pair:
- supported documentTypes:

### F) Draft assets
- business-domain note
- documentType drafts
- search planning notes

## Anti-Patterns

- Modeling every business concept as directly searchable.
- Creating a standalone search boundary when search is only a projection of source-owned records.
- Duplicating auth-owned fields such as `email` on actor documentTypes without business need.
- Declaring runtime metadata fields inside documentType definitions.
- Embedding referenced entities instead of using IDs for transactional relationships.
- Conflating operational state and accuracy state in one property.
- Modeling correction items directly on orders when the domain behavior is actually a hidden correction bundle.
- Putting bundle-derived pricing directly on orders when the bundle or bundle item owns pricing.

## Example Triggers

- "Review this business plan and derive the business objects"
- "Which concepts should be documentTypes versus search criteria?"
- "Create a domain model for this new site from the business plan"
- "Map these business objects to microservice pairs"
- "Draft the initial documentTypes from this business plan"

## References

- `/.github/skills/author-search-criteria/SKILL.md`
- `shared-lib/schema/documentType-schema.json`
- `sites/companions/assets/documentTypes/serviceProvider.json`
- `sites/companions/assets/documentTypes/search.json`
- `sites/companions/assets/search-engine/search/source-data-map.json`
- `sites/companions/assets/search-engine/search/search-ranking-rules.json`
- `sites/companions/assets/computeFlows/getAdComputeFlow.mjs`