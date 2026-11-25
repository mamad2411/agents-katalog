---
name: grid-filter-to-criteria-converter
description: Convert a UI grid filter DTO (gridFilters + tagFilters + pageable) to MongoDB Criteria using CriteriaMakeHelper, supporting equals/contains/greaterThan/inRange operators
triggers:
  - grid filter to criteria
  - FiltersPageableDto
  - CriteriaMakeHelper
  - mongodb dynamic filter
  - UI filter to query
scope: user
source_project: lucida-domain-sms
version: 0.1.0-draft
tags: [spring, mongodb, filter, criteria, pagination, grid]
category: backend
---

# Grid Filter to Criteria Converter

## Problem
A UI data grid sends structured filter conditions (field name, operator, value) and tag-based filters as part of a pageable request. The backend must translate these into MongoDB `Criteria` objects without writing per-endpoint query builders or leaking query logic into controllers.

## Pattern
- The request body is `FiltersPageableDto` containing:
  - `gridFilters` — list of `GridFilterDto` (field, operator, value)
  - `tagFilters` — list of tag key/value conditions
  - `pageable` — sort + page info via `toPageable()`
- Two singleton helpers handle translation:
  - `CriteriaMakeHelper.INSTANCE.gridFiltersToCriteria(gridFilters)` → `Criteria`
  - `CriteriaMakeHelper.INSTANCE.tagFiltersToCriteria(tagKey, tagValue, tagFilters)` → `Criteria`
- The controller combines the two Criteria and passes them to the service layer.
- Supported operators (declared in `@ExtensionProperty` for OpenAPI): `equals`, `notEqual`, `contains`, `notContains`, `startsWith`, `endsWith`, `greaterThan`, `greaterThanOrEqual`, `lessThan`, `lessThanOrEqual`, `inRange`.

## Example (sanitized)

```java
// DTO received from UI
// FiltersPageableDto {
//   gridFilters: [ { field: "hostname", operator: "contains", value: "web" } ],
//   tagFilters:  [ { key: "osType", value: "LINUX" } ],
//   sortFieldSets: [ { index: 0, sortDirection: "ASC", fieldName: "hostname" } ]
// }

@PostMapping("/resources/list-filter")
@FunctionId({FunctionIds.RESOURCE_VIEW})
public ApiResponseData<Object> listResources(
    @RequestHeader(HttpHeaders.AUTHORIZATION) String auth,
    @RequestBody FiltersPageableDto filtersPageableDto) {

    // 1. Convert tag filters (stored as embedded doc array in MongoDB)
    Criteria tagCriteria = CriteriaMakeHelper.INSTANCE.tagFiltersToCriteria(
        "tag.key", "tag.value", filtersPageableDto.getTagFilters());

    // 2. Convert grid filters (direct field operators)
    Criteria gridCriteria = CriteriaMakeHelper.INSTANCE
        .gridFiltersToCriteria(filtersPageableDto.getGridFilters());

    // 3. Delegate to service
    Page<ResourceDto> page = resourceService.findByCriteria(
        tagCriteria, gridCriteria, filtersPageableDto.toPageable());

    return ApiResponseData.createSuccess(page);
}

// Service layer merges criteria
public Page<ResourceDto> findByCriteria(
    Criteria tagCriteria, Criteria gridCriteria, Pageable pageable) {

    // combine however the repository expects:
    return resourceRepository.findByCriteria(tagCriteria, gridCriteria, pageable);
}
```

## When to Use
- REST endpoints backed by MongoDB that need server-side filtering driven by a UI grid component.
- Filtering logic must be consistent across many endpoints without duplicating `Criteria` construction.
- The field set allowed per endpoint is declared in OpenAPI `x-filterable-fields` extensions.

## Pitfalls
- **Undeclared fields**: `gridFiltersToCriteria` uses the field name as-is in the MongoDB query. A UI bug or injection attempt can query arbitrary fields. Validate the allowed field list or use a field allowlist in the service layer.
- **Tag document structure**: `tagFiltersToCriteria` requires knowing the exact embedded document field paths (`tag.key`, `tag.value`). These vary per collection — always verify the schema before reusing the call.
- **Sort default**: if `sortFieldSets` is omitted by the client, the query uses MongoDB's natural order. Set a sensible default sort in the controller before calling `toPageable()`.
- **Page size on export**: for Excel export endpoints reuse `FiltersPageableDto` but set `pageSize = Integer.MAX_VALUE` and `pageNumber = 1` before querying.

## Related
- `excel-export-enum-replacer` — uses the same `FiltersPageableDto` for export endpoints.
