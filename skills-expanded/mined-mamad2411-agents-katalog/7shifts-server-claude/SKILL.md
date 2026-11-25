# Server rules

Node API. Root rules in [../CLAUDE.md](../CLAUDE.md) apply here too.

- **Layering is strict: route → service → repository.** Handlers hold no
  business logic. Nothing outside the repository layer touches the database.
- **Validate all external input at the edge** with a schema. Past that line, the
  data is typed and trusted.
- **Domain errors are typed** and mapped to HTTP status codes only at the
  boundary. Services never reference HTTP.
- **Log structurally.** Never log secrets, tokens, or bodies containing either.
