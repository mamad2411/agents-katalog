# SOURCE — Schema Loading Strategy

**Part of migra-go** — PostgreSQL schema diff tool.

## OVERVIEW

Loader interface + strategy pattern for loading schema from SQL files, directories, or live databases. Normalizes after load.

## FILES

| File | Purpose |
|------|---------|
| `loader.go` | `Loader` interface definition |
| `registry.go` | Loader factory/registry |
| `sql_file_loader.go` | Loads single `.sql` file |
| `dir_loader.go` | Recursively loads all `.sql` in a directory |
| `db_loader.go` | Loads via database introspection (delegates to `introspect`) |

## CONVENTIONS

- Strategy: `Loader` interface with `LoadSchema() → *model.Schema`
- Registry maps source type string → loader constructor
- `dir_loader`: files sorted by path, concatenated, parsed as single unit
- `db_loader`: wraps `introspect` with connection management
- All loaders produce normalized SchemaModel (normalize applied post-load)

## ANTI-PATTERNS

- New source type without registering in `registry.go` won't be found
- Never skip normalization after loading raw schema
