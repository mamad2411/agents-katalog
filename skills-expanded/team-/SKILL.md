# Base MERN template — Cursor IDE rules

Repository root contains `client/` and `server/` side by side. For diagrams and request flow, read `docs/architecture/ARCHITECTURE.md`.

You are working on a MERN stack application with the following architecture:

## Tech Stack
- **Frontend**: Vite + React 18 + TypeScript
- **Styling**: Tailwind CSS (utility-first)
- **Backend**: Express.js + TypeScript
- **Database**: Neon Postgres with Prisma ORM
- **Authentication**: Auth0 (JWT-based)

## Project Structure
```
client/          # React frontend
  src/
    components/  # Reusable UI components
    pages/       # Route-level components
    hooks/       # Custom React hooks
    services/    # API calls (axios)
    context/     # React context providers
    types/       # TypeScript interfaces
server/          # Express backend
  src/
    controllers/ # Business logic (currently inline in routes)
    middleware/  # Express middleware (auth, errors)
    prisma/      # Prisma schema + migrations
    lib/         # Prisma client singleton
    routes/      # API route definitions
    services/    # External service integrations
    config/      # Configuration (database, etc.)
    types/       # TypeScript interfaces
```

## Code Conventions

### TypeScript
- Use strict mode
- Define interfaces for all data structures
- Prefer `interface` over `type` for object shapes
- Use explicit return types for functions when not obvious

### React (Frontend)
- Use functional components with hooks
- Use `useAuth0` hook for authentication
- API calls go through `services/api.ts` with token injection
- Use Tailwind utility classes, avoid custom CSS unless necessary
- Component files use PascalCase: `MyComponent.tsx`

### Express (Backend)
- Use async/await with asyncHandler wrapper for error handling
- Routes are protected with `checkJwt` middleware from Auth0
- Extract user ID with `extractUserId(req)` from auth payload
- Use Prisma client (`server/src/lib/prisma.ts`) for database operations
- Return consistent JSON responses

### Patterns to Follow

**Creating a new API route:**
```typescript
// server/src/routes/newRoute.ts
import { Router, Response } from 'express';
import { checkJwt, AuthRequest, extractUserId } from '../middleware/auth';
import { asyncHandler, createError } from '../middleware/errorHandler';
import { Model } from '../models';

const router = Router();
router.use(checkJwt);

router.get('/', asyncHandler(async (req: AuthRequest, res: Response) => {
  const userId = extractUserId(req);
  if (!userId) throw createError('Unauthorized', 401);
  
  const items = await Model.find({ user: userId });
  res.json(items);
}));

export default router;
```

**Creating a new React page:**
```typescript
// client/src/pages/NewPage.tsx
import { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import api from '../services/api';

function NewPage() {
  const { user } = useAuth0();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/endpoint');
        setData(response.data);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Content */}
    </div>
  );
}

export default NewPage;
```

**Creating a new Prisma model:**
```typescript
// server/prisma/schema.prisma — add model, then: npm run prisma:migrate --prefix server

model NewModel {
  id        String   @id @default(cuid())
  name      String
  userId    String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

## Common Tasks

### Add a protected route
1. Create route file in `server/src/routes/`
2. Import and use `checkJwt` middleware
3. Register route in `server/src/index.ts`

### Add a new page
1. Create component in `client/src/pages/`
2. Add route in `client/src/App.tsx`
3. Wrap with `<ProtectedRoute>` if auth required

### Add a database model
1. Add model to `server/prisma/schema.prisma` and run `npm run prisma:migrate --prefix server`
2. Use `prisma` from `server/src/lib/prisma.ts` in routes
3. Create corresponding routes/controllers

## Environment Variables

### Client (.env)
- `VITE_API_URL` - Backend API URL
- `VITE_AUTH0_DOMAIN` - Auth0 tenant domain
- `VITE_AUTH0_CLIENT_ID` - Auth0 application client ID
- `VITE_AUTH0_AUDIENCE` - Auth0 API identifier

### Server (.env)
- `PORT` - Server port (default: 3001)
- `DATABASE_URL` - Neon Postgres connection string (Prisma)
- `AUTH0_DOMAIN` - Auth0 tenant domain
- `AUTH0_AUDIENCE` - Auth0 API identifier

## Shopify Integration Notes

For Shopify embedded apps, you'll need to:
1. Install `@shopify/app-bridge-react`
2. Replace Auth0Provider with Shopify's AppBridgeProvider
3. Use Shopify session tokens instead of Auth0 JWT
4. Configure Shopify OAuth flow in server

The current auth setup is modular - the `checkJwt` middleware can be swapped for Shopify verification.
