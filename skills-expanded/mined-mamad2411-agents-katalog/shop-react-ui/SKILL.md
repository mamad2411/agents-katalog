---
name: shop-react-ui
description: Builds ShopFlow React UI with Vite, TypeScript, API client module, and data-testid attributes. Use when implementing catalog, cart, checkout, or order pages.
---

# ShopFlow React UI

## Structure

```
frontend/src/
  lib/api.ts
  features/catalog/
  features/product/
  features/cart/
  features/checkout/
  features/orders/
  components/   # shared UI
```

## Rules

- Pages compose feature components; data fetching in hooks (`useProducts`, `useCart`)
- Every button/link in demo flows has `data-testid`
- Loading and error states required
- Use React Router for `/`, `/products/:id`, `/checkout`, `/orders`

## API client

Centralize base URL and error parsing in `lib/api.ts`.

## Styling

Keep CSS minimal (CSS modules or a single `index.css`) — demo focuses on Cursor workflow, not design polish.

## Vite proxy

`vite.config.ts` should proxy `/api` to `http://localhost:8080` when using `make dev`.
