---
alwaysApply: false
description: "Shop product context: type-driven product logic, indexing, and API integration points"
keywords: ["shop product", "shop products", "shop catalog", "nomenclature", "ProductRepository", "product types", "ingredient", "constructor", "product indexers", "catalog cache", "Webkul Product"]
---

# Shop Product Context Rules

## Scope

This rule describes Shop-facing product behavior and implementation context for `packages/Webkul/Product`.

- Use this rule when tasks involve Shop catalog/nomenclature behavior, product availability, constructor/ingredient flows, or product read APIs.
- This rule complements `.cursor/rules/products.mdc` and should be preferred for Shop domain tasks.

## Source of Truth

- Core domain module: `packages/Webkul/Product`
- Product types registry: `packages/Webkul/Product/src/Config/product_types.php`
- Product lifecycle provider: `packages/Webkul/Product/src/Providers/ProductServiceProvider.php`
- Main orchestration repository: `packages/Webkul/Product/src/Repositories/ProductRepository.php`
- Type base class and custom types:
  - `packages/Webkul/Product/src/Type/AbstractType.php`
  - `packages/Webkul/Product/src/Type/Ingredient.php`
  - `packages/Webkul/Product/src/Type/Constructor.php`

## Architecture Guardrails

1. Product behavior is type-driven.
   - Any change to product create/update/cart/saleability logic must be checked against:
     - `product_types.php`
     - related `Type/*` classes
     - `Product::getTypeInstance()`

2. `Webkul/Product` is domain layer, not API endpoint layer.
   - Shop/Admin routes and controllers are defined in neighbor packages (`Webkul/RestApi`, `Webkul/Admin`).
   - For endpoint changes, inspect both domain and API packages.

3. Product updates affect multiple denormalized/indexed layers.
   - Always assess side effects for:
     - flat index
     - inventory index
     - price index
     - elastic index

## Shop Integration Points (Read Before Editing)

Even for Shop product tasks, API entries are outside `Webkul/Product`:

- Shop routes: `packages/Webkul/RestApi/src/Routes/V1/Shop/catalog-routes.php`
- Shop product controller: `packages/Webkul/RestApi/src/Http/Controllers/V1/Shop/Catalog/ProductController.php`
- Shop catalog category controller: `packages/Webkul/RestApi/src/Http/Controllers/V1/Shop/Catalog/CatalogCategoryController.php`
- Shop nomenclature controller: `packages/Webkul/RestApi/src/Http/Controllers/V1/Shop/Catalog/NomenclatureController.php`

Admin touchpoints often impacted by product domain changes:

- Admin routes: `packages/Webkul/Admin/src/Routes/catalog-routes.php`
- Admin product controller: `packages/Webkul/Admin/src/Http/Controllers/Catalog/ProductController.php`
- Admin REST product controller: `packages/Webkul/RestApi/src/Http/Controllers/V1/Admin/Catalog/ProductController.php`

## Critical Product Flows

### Create / Update Product

Controller -> `ProductRepository` -> type-specific logic -> product events -> listeners/jobs -> index refresh.

Always verify:

- type-specific `create()` / `update()` behavior
- EAV attribute persistence (`ProductAttributeValueRepository`)
- constructor-specific persistence (`ProductConstructorRepository`) when type is `constructor`

### Indexing and Async Side Effects

Main files:

- `packages/Webkul/Product/src/Listeners/Product.php`
- `packages/Webkul/Product/src/Helpers/Indexers/*`
- `packages/Webkul/Product/src/Jobs/UpdateCreateInventoryIndex.php`
- `packages/Webkul/Product/src/Jobs/UpdateCreatePriceIndex.php`
- `packages/Webkul/Product/src/Jobs/ElasticSearch/UpdateCreateIndex.php`
- `packages/Webkul/Product/src/Jobs/ElasticSearch/DeleteIndex.php`

Required check:

- if product mutation changes searchable/filterable fields, ensure downstream indices remain consistent.

### Cache Invalidation

Product observer clears Shop catalog caches:

- `packages/Webkul/Product/src/Observers/ProductObserver.php`
- triggers cache clearing in `CatalogCategoryController` and `NomenclatureController`

If product save/delete flow changes, verify cache invalidation is still guaranteed.

## Data Model Focus for Shop Tasks

Primary tables/entities:

- `products`
- `product_flat`
- `product_attribute_values`
- `product_price_indices`
- `product_inventory_indices`
- `product_constructor`
- `product_constructor_group`
- `product_constructor_group_products`
- `product_ingredients_incompatibility`

Custom project-specific concerns to keep in mind:

- ingredient and constructor types
- drinks relations
- ingredient incompatibility templates
- half/double portion and portion-size fields
- nutrition and category image extensions

## Change Checklist for AI Agent

For any non-trivial product change, validate all points:

1. Domain behavior
   - updated repository/type logic is aligned with `product_types.php`
2. API layer
   - Shop/Admin REST endpoints still match domain contracts
3. Read models/indexes
   - `product_flat`, price/inventory/elastic are refreshed correctly
4. Cache
   - catalog/nomenclature cache invalidation still runs
5. Database integrity
   - mapping uniqueness and FK consistency are preserved

## Implementation Notes

- Prefer extending existing type classes over adding conditional logic in controllers.
- Avoid duplicating product business logic in API controllers; keep orchestration in repositories/types.
- When adding new product behaviors, define expected effect on indexing and cache in the same task.
