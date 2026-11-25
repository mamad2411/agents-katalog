# Express notes arm

This arm implements the notes behavior with ordinary TypeScript, Zod, and
Express wiring. There is no generated architecture index.

For create/get maintenance, inspect `src/note.ts`, `src/notes-service.ts`, and
the relevant route in `src/app.ts`, then read `src/notes.test.ts` for the public
behavior. Widen to the full `src/` tree when a dependency cannot be resolved
from those files.

Verify with:

```sh
npm run typecheck --workspace @agentixdev/sandbox-express-notes
npm test --workspace @agentixdev/sandbox-express-notes
```
