---
name: cds-modeling
description: >
  Use when defining or reviewing CDS data models: entities, aspects, associations,
  compositions, projections, views, annotations, cuid and managed aspects, or any
  schema.cds / db/*.cds work in a SAP CAP project. Covers CDL syntax, reuse types
  from @sap/cds/common, naming conventions, and model-design best practices.
metadata:
  category: cap
  version: "1.0.0"
  keywords: [CDS, CDL, entity, schema, cuid, managed, temporal, localized, aspect, association, composition, projection, db/schema.cds, data model]
  related:
    service-handlers: implement service logic on top of CDS entities
    security-auth: add @requires and @restrict to services and entities
    fiori-annotations: add UI annotations to CDS entities for Fiori Elements
    localization: add localized elements and i18n to CDS entities
    performance: optimize CDS queries and projections
---

# CDS Modeling — CAP Best Practices

> **Primary reference**: https://cap.cloud.sap/docs/cds/cdl
> **Domain modeling**: https://cap.cloud.sap/docs/guides/domain-modeling
> **Reuse types**: https://cap.cloud.sap/docs/cds/common

## Always start from @sap/cds/common reuse types

```cds
using { cuid, managed, temporal, Currency, Country, Language } from '@sap/cds/common';

entity Products : cuid, managed {
  title       : localized String(111);
  description : localized String(1024);
  price       : Decimal(9,2);
  currency    : Currency;              // association to sap.common.Currencies
  category    : Association to Categories;
  items       : Composition of many OrderItems on items.product = $self;
}
```

- `cuid` → UUID key aspect — write `entity Foo : cuid` NOT `key ID : UUID` or `key ID : UUID = cuid()`
- `cuid` is an **aspect** (mixin), not a function — `cuid()` is WRONG syntax and will fail
- `managed` → createdAt/By, modifiedAt/By for free — NEVER define these manually
- `temporal` → validFrom/validTo (use for time-variant data)
- `localized` → generates _texts table + i18n support automatically

### ❌ Wrong vs ✅ Correct — the most common mistakes

```cds
// ❌ WRONG — manual UUID key
entity Products {
  key ID : UUID @default: #uuidv4;
  name   : String;
}

// ❌ WRONG — cuid() is not a function
entity Products {
  key ID : UUID = cuid();
  name   : String;
}

// ❌ WRONG — manual audit fields
entity Products {
  createdAt  : Timestamp;
  createdBy  : String;
  modifiedAt : Timestamp;
}

// ✅ CORRECT — use aspects
entity Products : cuid, managed {
  name     : String(111);
  price    : Decimal(9,2);
  currency : Currency;
}
```

## Associations vs Compositions

```cds
// Association: reference to an independent entity (no cascade delete)
product   : Association to Products;

// Composition: child is part of the parent (cascade delete, deep-insert supported)
items     : Composition of many Items on items.order = $self;
```

**Rule**: use `Composition` when the child cannot exist without the parent (order items, addresses on a person). Use `Association` for cross-entity references.

## Aspects for reusable patterns

```cds
// Define once, reuse everywhere
aspect Auditable {
  approvedBy  : String;
  approvedAt  : Timestamp;
  status      : String enum { Draft; Approved; Rejected; } default 'Draft';
}

entity PurchaseOrders : cuid, managed, Auditable { ... }
entity SalesOrders    : cuid, managed, Auditable { ... }
```

## Projections and Views

```cds
// Projection — thin wrapper, updatable
entity MyProductView as projection on Products {
  key ID, title, price, currency
};

// View with expressions — read-only
entity ProductSummary as select from Products {
  key ID,
  title,
  price * 1.19 as grossPrice : Decimal(9,2)
};
```

Use projections in service definitions, not the base entity, to control exposure.

## Enumeration types

```cds
type OrderStatus : String enum {
  Draft   = 'D';
  Open    = 'O';
  Shipped = 'S';
  Closed  = 'C';
}

entity Orders : cuid {
  status : OrderStatus default 'D';
}
```

Prefer enums over plain strings for status fields — they generate value help automatically in Fiori.

## Annotations: UI and ODM alignment

```cds
annotate Products with @(
  title : '{i18n>Products}',
  UI.LineItem : [
    { Value: title,  Label: '{i18n>Title}' },
    { Value: price,  Label: '{i18n>Price}' },
  ],
  UI.FieldGroup #General : {
    Data: [
      { Value: title },
      { Value: description },
    ]
  }
);
```

Keep annotations in a separate `annotations.cds` file, not inline in the entity — improves readability.

## Naming conventions

| Item | Convention | Example |
|------|-----------|---------|
| Entities | PascalCase, plural | `Products`, `SalesOrders` |
| Elements | camelCase | `orderDate`, `netAmount` |
| Services | PascalCase + `Service` | `CatalogService`, `AdminService` |
| Actions/Functions | camelCase verb | `submitOrder`, `calculateTax` |
| Namespaces | reverse-DNS | `com.acme.procurement` |

## Common mistakes to avoid

- ❌ `key ID : UUID @default: #uuidv4` — use `cuid` aspect instead
- ❌ `key ID : UUID = cuid()` — `cuid` is an aspect, not a function
- ✅ Always: `entity Foo : cuid, managed { ... }`

- ❌ Defining `createdAt`, `modifiedAt` manually — use `managed` aspect
- ❌ Exposing `db` entities directly in a service without a projection:
  ```cds
  // ❌ WRONG
  service CatalogService {
    entity Products;   // exposes db entity directly
  }
  // ✅ CORRECT
  service CatalogService {
    entity Products as projection on db.Products;
  }
  ```
- ❌ Using `String` without length in HANA deployments (defaults may differ)
- ❌ Forgetting `on` condition for managed associations in compositions exposed via service
