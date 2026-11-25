---
name: "party-tph-catalog"
description: "Use when adding a small polymorphic catalog dimension (Gender, BlogTag, BlogPostStatus, statuses, types, categories-as-lookup) instead of scaffolding a full entity. Covers the Party base (TPH, int key, PartyType discriminator), PartyRelation for party-to-party links, DTO inheritance from Info/Create/UpdatePartyDto, BasePartyService with SetPolicies and SearchByCriteriaByPartyTypeAsync, and discriminator registration. Domain: Persistence, Domain Modeling. Level: Intermediate. Tags: party, tph, discriminator, catalog, lookup."
allowed-tools: [Read, Grep, Glob]
---

## Activation

```yaml
ACTIVATION:
  triggers:
    - "party pattern"
    - "catalog dimension"
    - "lookup table"
    - "TPH"
    - "new tag/status/type entity"
  context: decision-point | implementation
  anti-triggers:
    - "Entities with their own rich schema — use scaffold-template-entity"
    - "Anything needing its own table or non-int key"
```

## Detail

# Party (TPH) Catalog Pattern

## Problem

Small catalog dimensions (Gender, BlogTag, BlogPostStatus, BlogPostVisibility…) each need audit fields, state, soft
delete, permissions and CRUD — but giving each its own table + migration + full scaffold is overkill for rows that are
basically `(id, description)`.

## Solution

All catalog dimensions share **one table** (`Parties`) via TPH with a `PartyType` string discriminator.

1. **Inherit `Party`** (which already implements `IEntity<int>`, `IAuditableEntity`, `IStateEntity`; `Description`
   serves as the display name). New properties must be **nullable/defaulted** so they don't interfere with sibling types:

```csharp
public class BlogTag : Party
{
    public string Slug { get; set; } = string.Empty;
    public string TagName => Description ?? string.Empty;   // computed alias for clarity
}
public class Gender : Party { }
```

2. **Register the discriminator** in `PartyConfiguration` (`.HasValue<Gender>(ResourceIdentifiers.Gender)`), add
   `DbSet<Gender> Genders` to `AppDbSetter`, and the `ResourceIdentifiers` constant. **No new table/migration** for the
   type itself (only if you added columns).
3. **DTOs inherit the Party DTOs** in one file: `InfoGenderDto : InfoPartyDto`, `CreateGenderDto : CreatePartyDto`,
   `UpdateGenderDto : UpdatePartyDto` (reuse `DeletePartyDto`).
4. **Service inherits `BasePartyService<TParty, TInfo, TCreate, TUpdate, TDelete>`** (int key, extends
   `PayloadService<>`): call `SetPolicies(_cachePolicies)` in the constructor; `CreateAsync` stamps
   `createDto.PartyType = typeof(TParty).Name` automatically; type-scoped reads via
   `SearchByCriteriaByPartyTypeAsync<TDerived>(model)` / `ExportByPartyTypeAsync<TDerived>(...)` which filter by
   discriminator through `_repository.AsQueryableOfType<TDerived>(false)`.
5. **Party-to-party links** use the `PartyRelation` table (`PartyId`, `RelatedPartyId`, `RelationshipType`,
   `StartDate/EndDate`, notes; auditable) — don't invent join tables between dimensions.
6. Endpoints/permissions follow the standard recipe (`GenderEndpoints : IEndpointDefinition`, attribute triad).

## Applicability

| Condition | Apply? |
|---|---|
| Small lookup shared-shape dimension (id + description + state) | ✅ Yes |
| Dimension with 1-3 extra nullable columns | ✅ Yes |
| Entity with rich schema, relations, own lifecycle | ❌ No — full scaffold |
| Read-only projection | ❌ No — `QueryPayloadService<>` |

## Gotchas

1. **Key is `int`** (Party owns it) — not the `Guid` default of full entities.
2. New properties on a derived type live on the shared table — keep them nullable or defaulted, or sibling inserts break.
3. Forgetting the discriminator registration makes EF treat rows as base `Party` — type-scoped queries return empty.
4. `SearchByCriteriaByPartyTypeAsync` caches under the first policy (falls back to `CacheRoutes.Parties`) — call
   `SetPolicies` or you share the generic Parties cache.
5. Root SKILL.md declares this pattern as its **anti-trigger** — one entry point per flow: full entity → root skill,
   catalog dimension → this one.

## Related Skills

- `scaffold-template-entity`, `permission-model`, `cache-policy-eviction`
