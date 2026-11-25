# api-conventions

Apply the team's REST conventions when writing or reviewing an HTTP handler.

- **Resource naming**: plural nouns, no verbs in paths — `POST /orders`, not
  `POST /createOrder`.
- **Pagination**: cursor-based (`?cursor=…&limit=…`). Never offset pagination for
  a set that can grow large.
- **Errors**: one envelope everywhere —
  `{ "error": { "code": "...", "message": "...", "details": {} } }` — with the
  correct HTTP status alongside it.
- **Versioning**: the version lives in the path (`/v1/…`). Never change a response
  shape within a version; add a field, don't repurpose one.

When reviewing, cite the specific rule each finding violates and show the
corrected request/response.
