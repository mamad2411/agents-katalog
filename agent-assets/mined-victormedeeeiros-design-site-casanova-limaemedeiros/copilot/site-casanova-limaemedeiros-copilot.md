# Copilot Instructions - Site Casanova Lima e Medeiros

## Architecture Overview

Wedding gift registry website with React/TypeScript frontend and Express.js backend, featuring dual authentication system, Stripe integration and Supabase database.

### Key Components
- **Frontend**: React 18 + Vite + TypeScript + Tailwind CSS + shadcn/ui
- **Backend**: Express.js + TypeScript + Supabase + Stripe
- **Authentication**: Dual system - Simple admin token + Google OAuth for users
- **Payments**: Stripe checkout with admin-configurable API keys
- **Database**: Supabase with products, settings, and admin tables

## Project Structure

```
├── src/                          # React frontend
│   ├── components/
│   │   ├── UserAuth.tsx         # Google OAuth login component
│   │   ├── GiftList.tsx         # Main gift display (hides admin features from users)
│   │   ├── StripeProductManager.tsx # Admin-only Stripe integration
│   │   └── admin/               # Admin-only components
│   │       ├── AdminLogin.tsx   # Token-based admin login
│   │       ├── AdminDashboard.tsx
│   │       └── AdminPanelComplete.tsx # Full admin panel with Stripe config
│   ├── hooks/
│   │   ├── useAuth.ts          # User Google OAuth management
│   │   ├── useAdminAuth.ts     # Admin token authentication
│   │   └── useGifts.ts         # Gift management & Stripe operations
│   ├── lib/
│   │   ├── supabase.ts         # Frontend Supabase client
│   │   └── stripe.ts           # Stripe utilities
│   └── pages/
│       ├── Index.tsx           # Public homepage
│       └── UserLogin.tsx       # Dedicated user login page
├── backend/src/                 # Express API
│   ├── controllers/
│   │   ├── auth.ts             # Admin JWT authentication
│   │   └── product.ts          # Stripe product sync
│   ├── config/supabase.ts      # Backend database connection
│   └── index.ts                # API routes with Stripe config endpoints
└── database/
    └── setup.sql               # Supabase table structure
```

## Authentication Patterns

### Admin System
- Uses environment variable `ADMIN_TOKEN` for simple authentication
- Protects `/admin/*` routes with `adminAuth` middleware
- Admin panel shows Stripe API key configuration and product management
- localStorage-based session management for frontend

### User System
- Google OAuth integration via Supabase Auth
- Hook `useAuth()` manages authentication state
- Users can browse gifts and make purchases
- NO ACCESS to admin features like `StripeProductManager`

## Stripe Integration Workflow

### Admin Configuration Flow
1. Admin logs in with token → `/admin/login`
2. Accesses admin panel → `/admin`
3. Enters Stripe secret key in settings
4. Backend saves key to `settings` table in Supabase
5. **Automatic bulk product sync triggered**
6. All gifts get `stripe_product_id` and `stripe_price_id`

### Key API Endpoints
```typescript
POST /admin/stripe-config    # Save Stripe API key
POST /admin/sync-products    # Sync all products to Stripe
GET  /admin/stripe-products  # List products from Stripe
```

### Data Flow Example
```typescript
// Admin saves Stripe key → automatic sync
const handleSaveApiKey = async () => {
  await fetch('/admin/stripe-config', { 
    body: { stripe_secret_key: key }
  });
  await handleSyncProducts(); // Auto-triggered
};
```

## Development Patterns

### Component Visibility Control
```typescript
// In GiftList.tsx - Hide admin features from regular users
const isAdmin = localStorage.getItem('adminToken') !== null;

{isAdmin && (
  <Button>Gerenciar Produtos Stripe</Button>
)}
```

### Environment Configuration
- Frontend: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_STRIPE_PUBLISHABLE_KEY`
- Backend: `STRIPE_SECRET_KEY`, `ADMIN_TOKEN`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`

## Database Schema

### Key Tables
```sql
settings(id, stripe_secret_key, updated_at)     # Stripe configuration
products(id, name, price, stripe_product_id)    # Product catalog
admins(id, email, password)                     # Optional JWT admins
```

## Common Tasks

### Adding New Gifts
1. Update `initialGifts` array in `GiftList.tsx`
2. Import gift images in assets structure  
3. Products auto-sync to Stripe on first admin configuration

### Stripe API Key Updates
1. Admin enters new key in settings panel
2. Triggers `/admin/stripe-config` endpoint
3. Backend validates and saves to database
4. **Automatic re-sync of all products**
5. Updates `stripe_product_id` for all gifts

### User vs Admin Access
- Users: Google login → gift browsing → Stripe checkout
- Admins: Token login → full panel → Stripe config → product management
- Critical: `StripeProductManager` component NEVER shown to users

## Security Implementation

### Route Protection
- Backend: `adminAuth` middleware validates token on sensitive endpoints
- Frontend: Conditional rendering based on `localStorage.getItem('adminToken')`
- Database: RLS policies protect admin and settings tables

### Key Files for Auth Flow
- `src/components/GiftList.tsx` - User/admin visibility logic
- `backend/src/index.ts` - Admin route protection  
- `src/hooks/useAuth.ts` - User authentication state
- `src/components/admin/AdminPanelComplete.tsx` - Stripe configuration UI