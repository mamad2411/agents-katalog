# Contracts Instructions

## Applies to

`3-Domain/MotorcycleRAG.Contracts/` only. Read the repository [AGENTS.md](../../AGENTS.md) first.

## Read before changing

- [Architecture placement rules](../../6-Docs/rules/architecture-general.md)
- [System architecture](../../6-Docs/system/architecture.md)

## Scoped constraints

- Contracts contains interfaces only: repositories, service abstractions, and factories.
- Do not add DTOs/models or implementations. Shared DTOs belong in Contracts.Models; implementations belong in an owning outer layer.

## Verify

Run the affected `dotnet test` projects.
