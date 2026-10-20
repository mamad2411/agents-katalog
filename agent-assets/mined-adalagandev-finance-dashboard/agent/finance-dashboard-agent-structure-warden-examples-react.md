# Structure Rules — Frontend (React) Examples

**Framework basis:** React 18 + Vite/CRA, ES modules under `frontend/src/`. The
rules themselves are framework-agnostic — these trees only show one concrete
stack.
**Translation hints:** Next.js adds a routing-driven `app/`/`pages/` tree — treat
route segments as the top tier and apply feature-folder rules beneath; Vue/Svelte
keep the same component-colocation shape with different file extensions.
**Version-sensitive:** a barrel `index.js` per feature is the public surface for
Rule 5; path aliases (`@/orders`) don't change the tree, only how it's imported.

## Rule 1 — Location is derivable from role
Violation — a grab-bag folder:
```
frontend/src/
  components/          # everything dumped flat, roles indistinguishable
    Thing.jsx  Stuff.jsx  utils.js  helpers.js
```
Correct — folders name the role:
```
frontend/src/
  features/order/OrderList.jsx
  components/ui/Button.jsx       # reusable primitives, named
  lib/formatCurrency.js          # named shared util, not "utils"
```

## Rule 2 — One organizing axis per tier
Violation — type-first and feature-first mixed:
```
frontend/src/
  components/OrderRow.jsx    # by type...
  hooks/useOrders.js
  order/OrderPage.jsx        # ...by feature — inconsistent
```
Correct (feature-first, uniform):
```
frontend/src/features/
  order/    OrderPage.jsx  OrderRow.jsx  useOrders.js  index.js
  payment/  PaymentPage.jsx PaymentForm.jsx usePayment.js index.js
```

## Rule 3 — Separate roots, mirrored shape
Backend and frontend name the same concept the same way and sit in parallel:
```
backend/  .../order/     OrderController  OrderService
frontend/ src/features/order/  OrderPage  useOrders   # same concept, same name
```
No shared mutable source straddling both roots; a shared *contract* (types) is a
published package, not an edited-in-place folder reached by `../../backend`.

## Rule 4 — The tree encodes dependency direction (the api.js seam)
Violation — a component reaches the network directly and imports upward:
```jsx
// features/order/OrderList.jsx
const res = await fetch('/api/orders');           // transport in the component
import { db } from '../../../backend/db';         // reaching into the backend
```
Correct — network access lives only in the api seam; features depend inward:
```
frontend/src/
  api.js                    # THE single backend seam (frontend-warden owns content)
  features/order/OrderList.jsx  ->  import { getOrders } from '../../api';
```

## Rule 5 — One public entry per feature (barrel)
Violation — importing a feature's internals from outside it:
```jsx
import { OrderRowInternal } from '../order/internal/OrderRowInternal'; // deep import
```
Correct — `index.js` is the feature's only surface:
```
frontend/src/features/order/
  index.js          # re-exports OrderPage — the one public entry
  OrderRow.jsx      # internal to the feature, imported via index only
```

## Rule 6 — Co-locate by change cadence
Component, its styles, and its test move together:
```
frontend/src/features/order/
  OrderRow.jsx
  OrderRow.module.css       # styles beside the component
  OrderRow.test.jsx         # test beside the component (if that's the repo convention)
```

## Rule 9 — Designated homes for non-source
```
frontend/
  public/           # static assets served as-is
  src/assets/       # imported assets (bundled)
  vite.config.js    # build config at root
  dist/  node_modules/   # generated/vendored — .gitignore'd, never hand-edited
```
