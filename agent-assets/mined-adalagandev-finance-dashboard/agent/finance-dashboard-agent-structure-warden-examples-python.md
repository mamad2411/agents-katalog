# Structure Rules — Backend (Python) Examples

**Framework basis:** Python 3.11+, a `src/`-layout package installed via
`pyproject.toml`, framework such as FastAPI/Flask/Django. The rules themselves
are framework-agnostic — these trees only show one concrete stack.
**Translation hints:** Django imposes its own app layout (`app/models.py`,
`app/views.py`) — treat each Django *app* as a feature module and apply Rule 2
within it. A flat layout (no `src/`) is acceptable if applied uniformly.
**Version-sensitive:** namespace packages vs. `__init__.py` marker packages both
work; whichever the repo uses, keep it uniform. `__init__.py` is the public
surface for Rule 5.

## Rule 1 — Location is derivable from role
Violation — catch-all module:
```
src/shop/
  utils.py            # unrelated helpers accrete here forever
  helpers.py
  misc.py
```
Correct — named, role-scoped modules:
```
src/shop/
  order/service.py
  pricing/calculator.py
  clock.py            # single-purpose, named
```

## Rule 2 — One organizing axis per tier
Violation — mixed axes at one level:
```
src/shop/
  routers/order.py    # layer-first...
  order/service.py    # ...and feature-first — inconsistent
  repositories/order.py
```
Correct (feature-first, uniform):
```
src/shop/
  order/    router.py  service.py  repository.py  schemas.py
  payment/  router.py  service.py  repository.py  schemas.py
```

## Rule 4 — The tree encodes dependency direction
Violation — domain imports the web/ORM layer:
```python
# src/shop/order/domain.py
from shop.order.router import OrderResponse      # domain -> transport
from shop.order.models import OrderRow           # domain -> ORM
```
Correct — inner layer defines a Protocol port; adapters implement it:
```
src/shop/order/
  domain.py         # Order, OrderService, OrderRepository (Protocol) — no outward imports
  router.py         # depends on domain
  repository.py     # implements the Protocol, depends on domain
```

## Rule 5 — One public entry per module
Violation — importing a private internal:
```python
from shop.order._internal.row_mapper import map_row   # reaching past the surface
```
Correct — `__init__.py` re-exports the public surface; `_`-prefixed modules are
internal:
```
src/shop/order/
  __init__.py       # exposes OrderService, OrderRepository — the entry point
  _row_mapper.py    # internal, not imported from outside the package
```

## Rule 6 — Co-locate by change cadence (test placement)
Two accepted conventions — detect which the repo uses, keep it uniform:
```
# Mirrored tests/ root
src/shop/order/service.py
tests/order/test_service.py

# Beside source (also valid if uniform)
src/shop/order/service.py
src/shop/order/test_service.py
```

## Rule 9 — Designated homes for non-source
```
project/
  pyproject.toml            # config at root
  migrations/               # Alembic/Django migrations (persistence-warden owns content)
  src/shop/static/          # assets, separated from logic
  .venv/  __pycache__/  *.egg-info/   # generated — .gitignore'd, never edited
```
