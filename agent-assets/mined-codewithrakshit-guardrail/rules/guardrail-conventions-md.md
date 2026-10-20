# GuardRail AI — Code Conventions

## File Naming
- Backend services: `kebab-case.js` (e.g. `patch-generator.js`)
- Frontend components: `PascalCase.tsx`
- Frontend pages: `page.tsx` inside named route folders
- Config files: `kebab-case.json`

## Backend Patterns

### Route handler shape
```js
router.post('/', async (req, res, next) => {
  try {
    const result = await someService.doThing(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
});
```

### Service shape
```js
class SomeService {
  constructor() { /* init AWS clients here */ }
  async doThing(input) { /* logic */ }
}
module.exports = new SomeService();
```

### Error responses
```json
{ "error": "message", "timestamp": "ISO string" }
```

### Success responses
```json
{ "scanId": "uuid", "status": "...", "data": {} }
```

## Frontend Patterns
- Use `axios` for all API calls to `http://localhost:3001`
- Tailwind only — no inline styles, no CSS modules
- Use `lucide-react` for all icons
- Pages are async server components by default; add `'use client'` only when needed

## Environment Variables
- Backend: `api/.env` (see `api/.env.example`)
- Frontend: `web/.env.local`
- Never commit `.env` files — they are in `.gitignore`

## AWS
- Always use AWS SDK v3 (`@aws-sdk/client-*`)
- Initialize clients once per service file, not per request
- Use `process.env.AWS_REGION` for region
- Tag all provisioned resources with `{ Project: 'guardrail-ai', Session: sessionId }`
