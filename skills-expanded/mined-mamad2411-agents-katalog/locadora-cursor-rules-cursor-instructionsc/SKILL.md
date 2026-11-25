# Locadora Project Guidelines

## Stack and architecture

- Backend with .NET/ASP.NET Core.
- PostgreSQL with Entity Framework Core and Npgsql.
- Layers: `Locadora.API`, `Locadora.Application`, `Locadora.Domain`, and
  `Locadora.Infrastructure`.
- The domain must not depend on ASP.NET Core, Entity Framework Core, or
  PostgreSQL.
- Controllers must only translate HTTP, invoke handlers, and build responses.
- Repository contracts belong to the domain interfaces and their implementations
  live in Infrastructure.
- HTTP responses use DTOs; entities are never exposed directly.

## Model source of truth

The database is Pagila, documented in
`.cursor/rules/estrutura-banco-pagila.mdc`. The code must not create entities or
tables parallel to the schema. Domain entities must correspond to database
tables:

| Entity | Table |
| --- | --- |
| `Actor` | `actor` |
| `Address` | `address` |
| `Category` | `category` |
| `City` | `city` |
| `Country` | `country` |
| `Customer` | `customer` |
| `Film` | `film` |
| `FilmActor` | `film_actor` |
| `FilmCategory` | `film_category` |
| `FilmEmbedding` | `film_embedding` |
| `FilmPriceHistory` | `film_price_history` |
| `Inventory` | `inventory` |
| `Language` | `language` |
| `Payment` | `payment` |
| `Rental` | `rental` |
| `Staff` | `staff` |
| `Store` | `store` |
| `StoreFilmPriceOverride` | `store_film_price_override` |

`Rental` represents one `rental` row: a copy (`Inventory`) rented by a
`Customer` and recorded by a `Staff` member. Returning a rental changes
`Rental.ReturnDate`. Do not create an aggregate of multiple films, an
intermediate item table, or Guid identifiers to replace Pagila keys.

`Film` is a catalog title. Availability must be calculated from free
`Inventory` copies: a copy whose `Rental.ReturnDate` is null is occupied. A
title with multiple copies remains available when at least one copy can be
rented.

## Recommended organization

```text
src/
├── Locadora.API/
│   └── Controllers/
├── Locadora.Application/
│   ├── DTOs/
│   └── UseCases/
├── Locadora.Domain/
│   ├── Entities/
│   ├── Enums/
│   ├── Interfaces/
│   ├── Results/
│   └── ValueObjects/
└── Locadora.Infrastructure/
    └── Persistence/
        ├── Configurations/
        ├── Context/
        └── Repositories/
```

Each table must have an `IEntityTypeConfiguration<T>` configuration. Use
explicit column names when they differ from property names, and preserve schema
types, keys, nullability, indexes, and default values.

## Domain rules

- Entity properties use `private set`.
- Creation that can fail returns `Result<T>`.
- State changes use methods expressing business intent.
- `Customer` must prevent rentals when `IsActive` is false.
- `Rental` must prevent a second return.
- Selecting an available copy belongs to the rental flow and must respect the
  `Staff` member's store.
- Business rules must not be duplicated in controllers, configurations, or
  repositories.

## Current use cases

```text
UseCases/
├── Customers/
│   ├── CreateCustomer/
│   └── UpdateCustomer/
├── Films/
│   ├── CreateFilm/
│   ├── GetFilm/
│   ├── ListFilms/
│   ├── RentFilm/
│   └── ReturnFilm/
└── Rentals/
    ├── GetRental/
    └── ReturnRental/
```

The rental flow must:

1. Validate `Film`, `Customer`, and `Staff`.
2. Check the `Customer` activity rule.
3. Find a free `Inventory` copy in the `Staff` member's store.
4. Create a `Rental` with `rental_date`, `inventory_id`, `customer_id`, and
   `staff_id`.
5. Persist the entity through `IRentalRepository`.

The return flow must load `Rental`, call `Rental.Return()`, and persist
`return_date`.

## Tests

- Test `Customer` and `Rental` rules in the domain project.
- Test handlers with fakes of domain interfaces.
- Integration tests must validate API and Infrastructure composition.
- When changing the schema or model, update the tests and this rule.

Before completing a change, run:

```text
dotnet build Locadora.sln
dotnet test Locadora.sln
```
