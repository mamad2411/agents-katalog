---
name: food-ecommerce-ui
description: >
  Premium food e-commerce UI generator inspired by the "Mesa" design system.
  Use this skill whenever the user asks to build any food delivery, restaurant,
  or food-commerce interface — including landing pages, product grids, food cards,
  carts, checkout flows, dashboards, category rails, search palettes, navbars,
  profile screens, login/register modals, or any other screen typical of a food
  tech startup. Also trigger for requests like "build me a food app", "design a
  restaurant UI", "create a delivery app screen", "make a food ordering interface",
  or "build something like Uber Eats / DoorDash". This skill ensures all output
  follows the Mesa design language: Apple-inspired minimalism, warm orange brand,
  glassmorphism navbar, Inter Tight display font, and production-ready React/JSX
  with smooth microinteractions — fully responsive from 375px mobile to 1280px desktop.
---

# Food E-commerce UI — Mesa Design System
## Version 2.0 — Full Responsive + Configurable

Generate premium, production-ready food e-commerce interfaces in the **Mesa** design language.
Every view is responsive: mobile-first layouts that scale gracefully to desktop.

**Before coding always read:**
- `references/design-tokens.md` — CSS tokens, keyframes, utility classes
- `references/components.md` — Visual components (cards, navbar, hero, etc.)
- `references/interactive-patterns.md` — Forms, inputs, cart, auth, toasts

---

## 1. Brand Configuration

Every generated interface declares a `CONFIG` object at the top of the file.
Always use its values — never hardcode brand strings, colors, or prices.

```js
const CONFIG = {
  // Brand
  brand:        "FoodStore",
  brandTagline: "La cocina de Mendoza, en tu mesa.",
  logoChar:     "·",

  // Locale & currency
  locale:       "es-AR",
  currency:     "$",
  currencyCode: "ARS",

  // Delivery
  deliveryFee:    450,
  freeDeliveryAt: 5000,
  deliveryLabel:  "Envío",

  // Colors — override brand tokens here
  brandColor:      "#FF7A00",   // --brand
  brandColorHover: "#FF8A1F",   // --brand-hover
  brandSoft:       "#FFE9D5",   // --brand-soft
  brandInk:        "#2D1804",   // --brand-ink

  // Feature flags — toggle sections on/off
  features: {
    googleAuth:    true,
    guestCheckout: false,
    tipping:       true,
    wineParings:   true,
    searchPalette: true,
    dashboard:     false,
  },

  // Payment methods shown in checkout
  paymentMethods: ["mercadopago", "card", "cash", "transfer"],

  // Tip percentages
  tipOptions: [0, 10, 15, 20],
};
```

**Inject CONFIG colors into CSS at runtime:**
```jsx
useEffect(() => {
  const r = document.documentElement;
  r.style.setProperty("--brand",      CONFIG.brandColor);
  r.style.setProperty("--brand-h",    CONFIG.brandColorHover);
  r.style.setProperty("--brand-soft", CONFIG.brandSoft);
  r.style.setProperty("--brand-ink",  CONFIG.brandInk);
}, []);
```

---

## 2. Responsive System

### Breakpoints
```
xs:  0–479px     single column, full-width panels, bottom sheets
sm:  480–767px   slightly wider, still single column
md:  768–1023px  two-column grids, sidebar starts appearing
lg:  1024–1279px full multi-column layout, sidebar fixed
xl:  1280px+     max-width container, generous spacing
```

### useBreakpoint hook — include in every multi-layout file
```jsx
function useBreakpoint() {
  const [w, setW] = useState(() => window.innerWidth);
  useEffect(() => {
    const fn = () => setW(window.innerWidth);
    window.addEventListener("resize", fn, { passive: true });
    return () => window.removeEventListener("resize", fn);
  }, []);
  return {
    isMobile:  w < 768,
    isTablet:  w >= 768 && w < 1024,
    isDesktop: w >= 1024,
    width: w,
  };
}
```

### Layout switch pattern
```jsx
function SomeScreen() {
  const { isMobile } = useBreakpoint();
  return isMobile ? <SomeMobileLayout /> : <SomeDesktopLayout />;
}
```

### Responsive behavior per view
| View | Mobile (< 768px) | Desktop (≥ 1024px) |
|------|-----------------|-------------------|
| Landing | Single-column hero, stacked sections | 2-col hero, 3-4 col product grid |
| Navbar | Compact pill, hide nav links | Full links + inline search bar |
| Product Grid | 1–2 cols `minmax(160px,1fr)` | 3–4 cols `minmax(248px,1fr)` |
| Cart | Full-screen page (tab) | Right drawer 460px + backdrop |
| Login/Register | Full-screen page | Centered modal 420px + backdrop blur |
| Profile | Full-screen tabbed page | 2-col: sidebar nav 240px + content |
| Checkout | Step accordion full screen | 2-col: form left + sticky summary right |
| Product Detail | Bottom sheet 90vh | Centered modal 680px |
| Search Palette | Full-screen overlay | Centered modal 560px |
| Dashboard | Stacked cards | Sidebar nav + grid KPIs |

### Container classes
```css
.container       { max-width: 1280px; margin: 0 auto; padding: 0 28px; }
.container-sm    { max-width: 640px;  margin: 0 auto; padding: 0 20px; }
@media (max-width: 767px) {
  .container, .container-sm { padding: 0 18px; }
}
```

---

## 3. Complete View Inventory

### VIEW 01 — Landing Page (`screen: "home"`)
**Purpose:** Marketing, conversion-focused, first impression.

Sections (top to bottom):
1. `<Navbar>` — floating glass pill, scroll-reactive shadow
2. `<Hero>` — display headline + hero visual card + floating chips
3. `<TrustStrip>` — 4 stat cards (delivery time, rating, chef count, origin)
4. `<CategoryRail>` — horizontal scroll category pills
5. `<FiltersRow>` — toggle chips (fast/vegan/trending/new) + sort
6. `<ProductGrid>` — staggered cards
7. `<ChefsRail>` — chef profile cards grid
8. `<CtaBanner>` — dark full-width CTA (wine/pairing/seasonal theme)
9. `<Footer>` — links, copyright, location badge

Mobile: hero stacks (copy → visual), product grid 1-2 cols, hero chips hidden  
Desktop: hero 2-col side by side, product grid 3-4 cols, all floating chips visible

---

### VIEW 02 — Menu / Product Listing (`screen: "menu"`)
**Purpose:** Browse, filter, and search all products.

Structure:
1. `<Navbar>` (shared)
2. Sticky bar: `<CategoryRail>` + `<FiltersRow>`
3. `<SearchInput>` (if `CONFIG.features.searchPalette`)
4. `<ProductGrid>` — filtered results with stagger animation
5. `<ProductModal>` on card click (see VIEW 07)

Mobile: search full-width below navbar, grid 1-2 cols, modal = bottom sheet  
Desktop: search embedded in navbar, grid 3-4 cols, modal = centered overlay

---

### VIEW 03 — Cart (`screen: "cart"` / `ui.cartOpen`)
**Purpose:** Review items, set options, initiate checkout.

Content:
- Item rows: `<FoodArt>` thumb + name + chef + price + `<Counter>` + remove
- `<ShippingBar>` — live free delivery progress
- Delivery speed toggle: Standard / Express
- `<PaymentSelector>` — collapsed accordion
- `<TipSelector>` (if `CONFIG.features.tipping`)
- Fee breakdown: subtotal, delivery, tip, total
- CTA: "Confirmar pedido" → checkout or login prompt
- Empty state: `<EmptyState type="cart">` + 3 quick-add suggestions

Mobile: full-screen page, sticky footer with total + CTA button  
Desktop: `position:fixed; right:0; width:460px` drawer, `slide-in-right` animation, backdrop

---

### VIEW 04 — Checkout (`screen: "checkout"`)
**Purpose:** Complete the purchase in 3 steps.

Steps:
1. **Entrega** — `<AddressForm>` + Standard ($450) vs Express ($850) radio
2. **Pago** — `<PaymentSelector>` → conditional `<CardForm>` + `<TipSelector>`
3. **Resumen** — order item list, address + payment summary, grand total, confirm button

Mobile: vertical accordion — each step numbered, expands below previous  
Desktop: left col (steps 1-2 as form) + right col (sticky order summary card, 360px wide)

After confirm → VIEW 09 (Order Confirmation)

---

### VIEW 05 — Auth / Login & Register (`screen: "auth"` / `ui.loginOpen`)
**Purpose:** Login, register, forgot password.

Modes: `"login"` | `"register"` | `"forgot"`

Login includes:
- Logo + headline
- Mode toggle pills
- Google OAuth button (if `CONFIG.features.googleAuth`)
- Email + Password (with show/hide toggle)
- "¿Olvidaste tu contraseña?" link → forgot mode
- `apiError` inline below form
- Spinner in button while loading

Register adds:
- Full name field
- Confirm password field
- Password strength bar (4 segments, color fills as length grows)
- Terms acceptance note

Forgot password:
- Info callout (brand-soft background)
- Email field
- "← Volver al login" text button

Mobile: full-screen page with top logo  
Desktop: centered modal 420px, `backdrop-filter: blur(6px)` overlay, `float-up` entry animation

---

### VIEW 06 — User Profile (`screen: "profile"`)
**Purpose:** Account management — orders, addresses, settings.

Structure:
- **Avatar card**: initials circle + name + email + member since + stats (orders / favorites / rating)
- **Edit form** (inline expand on pencil click): name, email, phone, address — `useForm` validated
- **Tab: Mis pedidos** — order history cards: order ID + status badge + items + date + total
- **Tab: Direcciones** — address cards (primary badge) + "Agregar dirección" dashed button
- **Tab: Ajustes** — preference rows (notifications, emails, privacy, biometrics)
- **Logout** button — red border + text on hover, bottom of page

Mobile: horizontal scrollable tabs, full-width content below  
Desktop: left sidebar 240px with vertical tab nav (fixed), right scrollable content area

---

### VIEW 07 — Product Detail (`productModal` / `screen: "product"`)
**Purpose:** Full product info + quantity before adding to cart.

Content:
- `<FoodArt>` large display area
- Chef name + avatar chip + `<Stars>` rating + review count
- Product name in display type + full description
- Tag badges (Vegano, Premium, Temporada, etc.)
- Ingredient/allergen chips
- `<Counter>` quantity selector
- Price + "Agregar al carrito" CTA (brand primary button full-width)

Mobile: bottom sheet, `border-radius: 28px 28px 0 0`, slides up from bottom, 90vh  
Desktop: centered overlay modal 680px, `float-up` animation, backdrop

---

### VIEW 08 — Search Palette (`ui.searchOpen`)
**Purpose:** Fast product/chef search — command palette style.

Content:
- Search input (autofocus on open)
- Live results debounced 220ms
- Results grouped: **Platos** / **Chefs** / **Categorías**
- Keyboard: ↑↓ to navigate, Enter to select, Esc to close
- Empty state: "Sin resultados para «X»"
- Recent searches (last 5, from state)

Mobile: full-screen overlay  
Desktop: centered floating panel 560px, `float-up` spring animation, backdrop

---

### VIEW 09 — Order Confirmation (`screen: "confirmed"`)
**Purpose:** Post-purchase success screen.

Content:
- Animated ✓ in green circle (scale-up spring animation)
- Order number (mono font)
- Estimated delivery time
- Delivery address summary
- "Seguir comprando" CTA → screen: "menu"
- "Ver mis pedidos" ghost button → screen: "profile"

Layout: full-screen centered column, no navbar, ambient background

---

### VIEW 10 — Dashboard (`screen: "dashboard"`, only if `CONFIG.features.dashboard`)
**Purpose:** Chef / admin analytics view.

Content:
- KPI row (4 cards): Ingresos hoy / Pedidos / Ticket promedio / Tiempo entrega
- Revenue sparkline (7-day bar chart or SVG line)
- Recent orders table: ID, customer, items, status, total
- Top products ranking
- Quick actions: mark as ready, update availability

Mobile: stacked cards + bottom tab nav  
Desktop: left sidebar nav 220px + main content grid

---

## 4. Shared Components Reference

| Component | Views | Mobile | Desktop |
|-----------|-------|--------|---------|
| `<Navbar>` | All | Compact pill, bag icon | Full pill + nav links + search |
| `<SearchPalette>` | Landing, Menu | Full-screen | Centered modal 560px |
| `<ProductCard>` | Landing, Menu | Compact, hover lift | Full card, hover lift |
| `<CartDrawer>` | All | Full-screen page | Right drawer 460px |
| `<LoginModal>` | Navbar, Checkout | Full-screen | Centered modal 420px |
| `<ProductModal>` | Menu | Bottom sheet | Centered modal 680px |
| `<ToastStack>` | All | Bottom-center | Bottom-center |
| `<FoodArt>` | All | Inline | Inline |
| `<Badge>` | Cards, orders | Inline | Inline |
| `<Counter>` | Product, Cart | Pill row | Pill row |
| `<ShippingBar>` | Cart, Checkout | Full-width | Full-width |
| `<EmptyState>` | Cart, Search, Orders, Favorites | Centered column | Centered column |
| `<Spinner>` | Buttons, loaders | Inline | Inline |
| `<SkeletonCard>` | Product grid | 1-2 col shimmer | 3-4 col shimmer |

---

## 5. App State Architecture

```jsx
const initialState = {
  user:  null,         // null = guest | { id, name, email, avatar, joined, orders, fav }
  cart:  [],           // [{ ...product, qty }]
  ui: {
    screen:      "home",
    cartOpen:    false,   // desktop drawer
    loginOpen:   false,   // desktop modal
    searchOpen:  false,
    productOpen: null,    // product id or null
  },
};

function reducer(state, action) {
  switch (action.type) {
    case "LOGIN":        return { ...state, user: action.payload, ui: { ...state.ui, loginOpen: false, screen: "profile" } };
    case "LOGOUT":       return { ...state, user: null, cart: [] };
    case "CART_ADD": {
      const ex = state.cart.find(i => i.id === action.payload.id);
      return { ...state, cart: ex
        ? state.cart.map(i => i.id === action.payload.id ? { ...i, qty: i.qty + 1 } : i)
        : [...state.cart, { ...action.payload, qty: 1 }] };
    }
    case "CART_REMOVE":  return { ...state, cart: state.cart.filter(i => i.id !== action.payload) };
    case "CART_SET_QTY": return { ...state, cart: state.cart.map(i => i.id === action.payload.id ? { ...i, qty: action.payload.qty } : i).filter(i => i.qty > 0) };
    case "CART_CLEAR":   return { ...state, cart: [] };
    case "SCREEN":       return { ...state, ui: { ...state.ui, screen: action.payload } };
    case "UI_SET":       return { ...state, ui: { ...state.ui, ...action.payload } };
    default:             return state;
  }
}
```

---

## 6. Implementation Rules

### Always
- Declare `CONFIG` at file top, use it everywhere
- Include `useBreakpoint()` in any multi-layout file
- Use `CONFIG.locale` in `.toLocaleString()` for all prices
- Prefix all prices with `CONFIG.currency`
- Use `var(--token)` for colors, radii, shadows, easing
- Add `transition` to every interactive element
- Use `.stagger` on product grids for entry animation
- Import Google Fonts: Inter Tight + Inter (400/500/600)

### Never
- Hardcode hex colors, font names, brand strings, prices, delivery fees
- Use `outline` for focus — use `box-shadow: 0 0 0 4px rgba(255,122,0,0.12)`
- Use `localStorage` / `sessionStorage`
- Use `position: fixed` inside widget/iframe contexts
- Build desktop-only or mobile-only layouts — always handle both with `useBreakpoint()`

### Responsive rules
- Write base styles for mobile, override for desktop
- Drawers (desktop) → full-screen sheets (mobile)
- Modals (desktop) → full-screen pages (mobile)
- Multi-column grids (desktop) → 1-2 cols (mobile)
- Sidebar nav (desktop) → horizontal tabs (mobile)

---

## 7. Code Output Format

Every output is a **single self-contained HTML file**:

```
<style>
  1. Google Fonts @import
  2. :root CSS token block
  3. Reset + base body styles
  4. Keyframes (float-up, spin, shimmer, toast-in, slide-in-right)
  5. Utility classes (.t-d, .eyebrow, .num, .glass, .food-art + variants, .stagger, .container)
</style>

<script type="text/babel">
  1.  CONFIG
  2.  useBreakpoint
  3.  useForm + validators
  4.  useToasts
  5.  useCart (or useReducer for full apps)
  6.  Icons (inline SVG object)
  7.  Atoms: FoodArt, Badge, Stars, Price, Counter, Spinner, SkeletonCard
  8.  Inputs: Input, PwInput, Textarea, Select
  9.  Shared: Navbar, SearchPalette, ToastStack, EmptyState, ShippingBar
  10. Screen components (each view as a named function)
  11. App root with state + screen router + useBreakpoint layout switch
  12. ReactDOM.createRoot(...).render(<App/>)
</script>
```

---

## 8. Reference Files

| File | Contents |
|------|----------|
| `references/design-tokens.md` | Full CSS `:root` block, keyframes, utility classes, all food-art variants |
| `references/components.md` | Visual components: Navbar, Hero, ProductCard, CategoryRail, CartDrawer, CheckoutScreen, ChefsRail, Footer |
| `references/interactive-patterns.md` | useForm, validators, useCart, auth modals, AddressForm, PaymentSelector, CardForm, TipSelector, SearchInput, ToastStack, Spinner, SkeletonCard, EmptyState, appReducer |
