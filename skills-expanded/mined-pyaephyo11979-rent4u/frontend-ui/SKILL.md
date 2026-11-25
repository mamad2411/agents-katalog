# Frontend UI Skill

Component architecture, styling, and UX guidelines for the Rent4U frontend.

## Stack

- **Framework:** React 19 + TypeScript 6
- **Styling:** Tailwind CSS v4 (CSS-first config)
- **Routing:** react-router-dom v7
- **State:** React Context + hooks (no external state library yet)
- **Build:** Vite 8

## Directory Structure

```
frontend/src/
├── components/
│   ├── ui/                    # Primitive building blocks
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   ├── Skeleton.tsx
│   │   └── index.ts           # Barrel export
│   ├── layout/                # Page structure
│   │   ├── Navbar.tsx
│   │   ├── Footer.tsx
│   │   ├── Sidebar.tsx
│   │   └── Layout.tsx         # Wraps Navbar + main + Footer
│   ├── forms/                 # Form-specific components
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── HouseForm.tsx
│   └── features/              # Domain-specific composites
│       ├── house/
│       │   ├── HouseCard.tsx
│       │   ├── HouseGrid.tsx
│       │   ├── HouseDetail.tsx
│       │   └── HouseFilters.tsx
│       ├── booking/
│       │   ├── BookingCard.tsx
│       │   ├── BookingForm.tsx
│       │   └── BookingCalendar.tsx
│       └── auth/
│           ├── ProtectedRoute.tsx
│           └── AuthProvider.tsx
├── pages/
│   ├── HomePage.tsx
│   ├── LoginPage.tsx
│   ├── RegisterPage.tsx
│   ├── SearchPage.tsx
│   ├── HouseDetailPage.tsx
│   ├── DashboardPage.tsx
│   └── NotFoundPage.tsx
├── hooks/
│   ├── useAuth.ts
│   ├── useHouses.ts
│   └── useDebounce.ts
├── services/
│   └── api.ts                 # Axios/fetch wrapper
├── types/
│   └── global.d.ts
├── index.css
├── main.tsx
└── App.tsx
```

## Component Rules

### 1. One Component Per File
```tsx
// Good: HouseCard.tsx
export function HouseCard({ house }: { house: House }) {
  return (
    <div className="rounded-2xl border border-gray-200 overflow-hidden">
      <img src={house.images[0]?.url} alt={house.name} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h3 className="font-semibold text-lg">{house.name}</h3>
        <p className="text-gray-500 text-sm">{house.city}</p>
        <p className="mt-2 font-bold">{formatPrice(house.price)} / night</p>
      </div>
    </div>
  );
}
```

### 2. Props Over Context
Pass data down via props. Use Context only for truly global state (auth, theme).

```tsx
// Good — explicit data flow
<HouseCard house={house} onSelect={handleSelect} />

// Bad — implicit, hard to trace
<HouseCard houseId={house.id} />  // component fetches its own data
```

### 3. Composition Over Configuration
```tsx
// Good — composable
<Card>
  <Card.Image src={url} />
  <Card.Title>{name}</Card.Title>
  <Card.Body>{description}</Card.Body>
</Card>

// Bad — prop soup
<Card image={url} title={name} body={description} footer={...} />
```

### 4. Naming Conventions
| Thing | Convention | Example |
|-------|-----------|---------|
| Components | PascalCase | `HouseCard` |
| Hooks | `use` prefix | `useAuth` |
| Helpers | camelCase | `formatPrice` |
| Types/Interfaces | PascalCase | `House`, `BookingStatus` |
| CSS classes | Tailwind utilities | `className="mt-4 text-lg"` |
| Test IDs | kebab-case with prefix | `data-testid="house-card"` |

## Styling Rules

### Tailwind Only — No Inline Styles, No CSS Modules
```tsx
// Good
<div className="flex items-center gap-4 p-6 bg-white rounded-xl shadow-sm">

// Bad
<div style={{ display: 'flex', padding: '24px' }}>
```

### Design Tokens (via Tailwind v4 theme)
```css
/* index.css — extend the default theme */
@theme {
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-secondary: #059669;
  --color-danger: #dc2626;
  --color-muted: #6b7280;
  --radius-card: 1rem;
  --shadow-card: 0 1px 3px rgb(0 0 0 / 0.1);
}
```

### Responsive Pattern — Mobile First
```tsx
// Always start with mobile layout, add breakpoints
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {houses.map(h => <HouseCard key={h.id} house={h} />)}
</div>
```

### Spacing Scale
Use Tailwind's default spacing. Common patterns:
- **Page padding:** `px-4 md:px-8 lg:px-16`
- **Section gap:** `space-y-8` or `gap-8`
- **Card padding:** `p-4` or `p-6`
- **Inline gap:** `gap-2` (tight) or `gap-4` (normal)

## UI Component Library

### Button
```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

const variants = {
  primary: 'bg-primary text-white hover:bg-primary-hover',
  secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
  ghost: 'bg-transparent text-gray-600 hover:bg-gray-100',
  danger: 'bg-danger text-white hover:bg-red-700',
};

export function Button({ variant = 'primary', size = 'md', loading, children, className, ...props }: ButtonProps) {
  return (
    <button
      className={cn('rounded-lg font-medium transition-colors disabled:opacity-50', variants[variant], sizes[size], className)}
      disabled={loading || props.disabled}
      {...props}
    >
      {loading ? <Spinner size={size} /> : children}
    </button>
  );
}
```

### Input
```tsx
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({ label, error, className, ...props }: InputProps) {
  return (
    <div className="space-y-1">
      {label && <label className="text-sm font-medium text-gray-700">{label}</label>}
      <input
        className={cn(
          'w-full rounded-lg border px-3 py-2 text-sm transition-colors',
          error ? 'border-danger focus:ring-danger' : 'border-gray-300 focus:ring-primary',
          className
        )}
        {...props}
      />
      {error && <p className="text-xs text-danger">{error}</p>}
    </div>
  );
}
```

### Card
```tsx
export function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('rounded-2xl border border-gray-200 bg-white shadow-card overflow-hidden', className)}>
      {children}
    </div>
  );
}
```

### Skeleton (Loading State)
```tsx
export function Skeleton({ className }: { className?: string }) {
  return <div className={cn('animate-pulse rounded-lg bg-gray-200', className)} />;
}

// Usage
<Skeleton className="h-48 w-full" />   // image placeholder
<Skeleton className="h-4 w-3/4" />     // text line
```

## Page Structure

Every page follows this pattern:
```tsx
export function SearchPage() {
  return (
    <Layout>
      <section className="px-4 md:px-8 lg:px-16 py-8">
        <h1 className="text-2xl font-bold mb-6">Find a Place to Stay</h1>
        <HouseFilters onFilter={handleFilter} />
        <HouseGrid houses={houses} loading={loading} />
      </section>
    </Layout>
  );
}
```

## Loading & Error States

Every data-fetching component must handle 3 states:
```tsx
function HouseGrid({ houses, loading, error }: Props) {
  if (loading) return <HouseGridSkeleton />;
  if (error) return <ErrorMessage message={error} onRetry={refetch} />;
  if (houses.length === 0) return <EmptyState message="No houses found" />;
  return <div className="grid ...">{houses.map(...)}</div>;
}
```

## Accessibility

- All images have `alt` text
- Interactive elements are `<button>` or `<a>`, not `<div onClick>`
- Form inputs have associated `<label>`
- Color contrast meets WCAG AA (4.5:1 for text)
- Focus visible on all interactive elements
- Modals trap focus and close on Escape

## Quality Checklist

- [ ] One component per file
- [ ] Props typed with TypeScript interfaces
- [ ] No inline styles — Tailwind only
- [ ] Mobile-first responsive layout
- [ ] Loading skeleton for every async state
- [ ] Empty state for every list
- [ ] Error state with retry option
- [ ] `data-testid` on interactive elements
- [ ] Accessible: labels, alt text, keyboard nav
- [ ] Consistent spacing with Tailwind scale
