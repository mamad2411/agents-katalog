# Express Skill

You are working with Express.js. Apply these conventions.

## Application Setup

- Create the Express app and all middleware in `app.ts`; start the HTTP server in `server.ts`.
- Parse JSON bodies with `express.json()` and URL-encoded bodies with `express.urlencoded()` before route handlers.
- Always set `trust proxy` if running behind a reverse proxy (Nginx, Vercel, etc.):
  ```ts
  app.set('trust proxy', 1);
  ```

## Routing

- Organize routes by domain in separate `Router` files; mount them on the app with a prefix.
- Use `express.Router()` per domain, not per HTTP method.
- Use named route parameters (`/users/:id`) and access via `req.params.id`.
- Always validate path params and query strings — never trust them raw.

## Middleware

- Keep middleware in a `middleware/` directory; export as named functions.
- Error-handling middleware has signature `(err, req, res, next)` — must have all 4 params for Express to recognize it.
- Apply authentication middleware per-router or per-route, not app-wide unless all routes require auth.

## Error Handling

- Define a centralized error handler as the last middleware:
  ```ts
  app.use((err: Error, req: Request, res: Response, _next: NextFunction) => {
    res.status(500).json({ error: err.message });
  });
  ```
- Use `next(error)` to forward errors from async handlers to the error middleware.
- Wrap async route handlers to catch unhandled rejections:
  ```ts
  const asyncHandler = (fn: RequestHandler) => (req: Request, res: Response, next: NextFunction) =>
    Promise.resolve(fn(req, res, next)).catch(next);
  ```

## Security

- Use `helmet()` to set secure HTTP headers.
- Use `cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') })` — never `cors()` with no options in production.
- Rate-limit authentication endpoints with `express-rate-limit`.
- Validate and sanitize all inputs with `zod` or `express-validator` before processing.
- Never expose stack traces in error responses in production.

## TypeScript

- Extend `Request` interface via declaration merging to add `req.user`, etc.:
  ```ts
  declare global { namespace Express { interface Request { user?: UserPayload } } }
  ```
