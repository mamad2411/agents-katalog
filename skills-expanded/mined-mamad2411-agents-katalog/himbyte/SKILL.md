# Himbyte OS: Project Rules & Standards

## 🚀 Project Context
You are an expert AI developer at **Himbyte**, building a premier "Restaurant Operating System" for the Nepali market. This is a Multi-Tenant SaaS designed to handle QR-based ordering, staff-approval workflows, and hotel concierge services.

## 🛠 Tech Stack
- **Frontend:** React (Vite), Tailwind CSS v4, Framer Motion, Lucide React, Zustand, react-hot-toast.
- **Backend:** Node.js (Express, ESM modules), Supabase (Auth & Database).
- **Realtime:** Supabase Realtime (Critical for the "Staff Approval" gate — subscribed on `orders` table).
- **Deployment:** Vercel (Frontend), Railway (Backend).

## 🏛 Multi-Tenancy & Security
- **Data Isolation:** Every table MUST include a `restaurant_id`. Use Row Level Security (RLS) policies in Supabase to enforce this at the database level.
- **The "Staff Gate" Logic:** Orders start with `status: 'pending'`. Only authenticated users with `role: 'staff'` or `'restaurant_admin'` can PATCH the status to `'approved'`.
- **Global Context:** The `restaurant_id` is derived from the Auth session (staff) or the URL slug (guests).
- **Never** perform an update/delete without a `restaurant_id` filter.

## 🎨 Design System: "Rara Blue" (Himbyte's own identity — NOT RestroX)
Himbyte uses a premium Himalayan palette inspired by Rara Lake and temple gold. This is distinct from any other Nepali POS product.

### Color Tokens (defined in `@theme` inside `client/src/index.css`)
```
Primary  — Rara Lake Blue
  --color-primary:        #1B5E8A   → bg-primary, text-primary
  --color-primary-light:  #2E86C1   → bg-primary-light
  --color-primary-dark:   #0D2B3E   → bg-primary-dark, hover states
  --color-primary-soft:   #E8F4FD   → bg-primary-soft (light tinted backgrounds)

Accent  — Marigold / Temple Gold
  --color-gold:           #E8A820   → bg-gold, text-gold
  --color-gold-light:     #F5C842   → bg-gold-light
  --color-gold-dark:      #B37D0E   → text-gold-dark
  --color-gold-soft:      #FEF5E7   → bg-gold-soft

Semantic
  --color-success:        #16A34A   → bg-success, text-success
  --color-success-soft:   #DCFCE7
  --color-warning:        #D97706
  --color-warning-soft:   #FEF3C7
  --color-danger:         #DC2626
  --color-danger-soft:    #FEE2E2

Neutrals (high contrast — readable in restaurant low-light)
  --color-ink:            #0F172A   → primary text, headings
  --color-body:           #334155   → body copy
  --color-muted:          #64748B   → labels, placeholders
  --color-border:         #CBD5E1   → dividers, card borders
  --color-surface:        #FFFFFF   → card backgrounds
  --color-canvas:         #F4F8FB   → page background (light blue-tinted white)
  --color-canvas-dark:    #E2EBF3   → hover backgrounds

Brand Sidebar (dark navy)
  --color-sidebar:        #0D2540
  --color-sidebar-hover:  #1B3F6B
```

### Visuals
- Use `rounded-2xl` for all cards and buttons.
- Page backgrounds use `bg-canvas` (`#F4F8FB`).
- Card surfaces use `bg-surface` (`#FFFFFF`) with `border border-border`.
- Sidebar uses `bg-sidebar` (`#0D2540`) with the `bg-dhaka` CSS utility (Dhaka Topi SVG pattern, gold strokes at low opacity).
- Customer pages use `bg-mandala` CSS utility (Mandala SVG, primary-blue strokes at low opacity).
- Font: `Inter` via Google Fonts (loaded in `index.html`).

### Animations
- Use Framer Motion with **spring physics** (`type: 'spring', damping: 25-28, stiffness: 300-350`).
- Bottom sheet drawers: `initial={{ y: '100%' }}` → `animate={{ y: 0 }}`.
- List items: staggered `initial={{ opacity: 0, y: 16 }}` with `transition={{ delay: i * 0.07 }}`.
- Avoid `initial={{ opacity: 0 }}` on above-the-fold content (causes blank flash).
- `AnimatePresence mode="popLayout"` for order list updates.

## 📂 Naming Conventions
- **Files:** `kebab-case.jsx` (React), `camelCase.js` (utils/stores/hooks)
- **React Components:** `PascalCase`
- **Variables/Functions:** `camelCase`
- **Database Tables/Columns:** `snake_case`

## 📊 Database Schema (exact — always follow this)
```sql
CREATE TYPE order_status   AS ENUM ('pending','approved','preparing','ready','served','cancelled');
CREATE TYPE service_status AS ENUM ('requested','in_progress','completed','cancelled');
CREATE TYPE user_role      AS ENUM ('super_admin','restaurant_admin','staff');
CREATE TYPE location_type  AS ENUM ('table','room');

-- 1. Restaurants (tenants)
CREATE TABLE restaurants (
  id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name           TEXT NOT NULL,
  slug           TEXT UNIQUE NOT NULL,
  logo_url       TEXT,
  address        TEXT,
  phone          TEXT,
  vat_pan_number TEXT,        -- Nepal IRD compliance (single field)
  is_active      BOOLEAN DEFAULT true,
  created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Profiles (linked to auth.users)
CREATE TABLE profiles (
  id            UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  restaurant_id UUID REFERENCES restaurants(id),
  full_name     TEXT,
  role          user_role DEFAULT 'staff',
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Categories
CREATE TABLE categories (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  restaurant_id       UUID REFERENCES restaurants(id) ON DELETE CASCADE,
  name                TEXT NOT NULL,
  description         TEXT,
  priority            INTEGER DEFAULT 0,
  is_service_category BOOLEAN DEFAULT false,  -- true = hotel services (towels, DND etc.)
  created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Menu Items
CREATE TABLE menu_items (
  id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  category_id   UUID REFERENCES categories(id) ON DELETE CASCADE,
  restaurant_id UUID REFERENCES restaurants(id) ON DELETE CASCADE,
  name          TEXT NOT NULL,
  description   TEXT,
  price         DECIMAL(10,2) NOT NULL,
  image_url     TEXT,
  is_available  BOOLEAN DEFAULT true,
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Tables & Rooms (unified)
CREATE TABLE tables_rooms (
  id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  restaurant_id UUID REFERENCES restaurants(id) ON DELETE CASCADE,
  identifier    TEXT NOT NULL,      -- e.g. "Table 1", "Room 101"
  type          location_type DEFAULT 'table',
  qr_code_url   TEXT,
  UNIQUE(restaurant_id, identifier)
);

-- 6. Orders
CREATE TABLE orders (
  id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  restaurant_id UUID REFERENCES restaurants(id) ON DELETE CASCADE,
  table_room_id UUID REFERENCES tables_rooms(id),   -- NOT table_id or room_id
  status        order_status DEFAULT 'pending',
  total_price   DECIMAL(10,2) DEFAULT 0,             -- NOT "total" or "subtotal"
  notes         TEXT,
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Order Items
CREATE TABLE order_items (
  id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id      UUID REFERENCES orders(id) ON DELETE CASCADE,
  menu_item_id  UUID REFERENCES menu_items(id),
  quantity      INTEGER NOT NULL DEFAULT 1,
  price_at_time DECIMAL(10,2) NOT NULL   -- NOT unit_price
);

-- 8. Hotel Service Requests
CREATE TABLE service_requests (
  id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  restaurant_id UUID REFERENCES restaurants(id) ON DELETE CASCADE,
  table_room_id UUID REFERENCES tables_rooms(id),
  service_type  TEXT NOT NULL,    -- 'clean_room' | 'towels' | 'dnd' | 'other'
  status        service_status DEFAULT 'requested',
  created_at    TIMESTAMPTZ DEFAULT NOW()
);
```

## 📝 Critical Coding Rules
1. **Multi-tenancy:** Every query must be filtered by `restaurant_id` — no exceptions.
2. **Order fields:** Use `total_price` (not `total`), `price_at_time` (not `unit_price`), `table_room_id` (not `table_id`/`room_id`).
3. **Realtime:** Always clean up Supabase channel subscriptions in the `useEffect` return function to prevent memory leaks. Skip subscriptions when `DEMO_MODE` is true.
4. **Guest Access:** Guests are identified by URL `?r=slug&table=X` or `?r=slug&room=Y`. No login required. Orders are placed via the backend using the service role key.
5. **Color classes:** Use `bg-primary`, `text-primary`, `bg-gold`, `text-gold`, `bg-sidebar`, `text-ink`, `text-muted`, `bg-canvas`, `bg-surface`, `border-border` — never hardcode hex values in JSX.
6. **Demo mode:** The server auto-detects missing `SUPABASE_URL` and loads `routes/demo.js` with in-memory seed data. Demo restaurant ID: `a0000000-0000-0000-0000-000000000001`, slug: `himalayan-kitchen`.
7. **Framer Motion:** Never use `initial={{ opacity: 0 }}` on content that is visible on first load — use CSS `animate-slide-up` instead.
