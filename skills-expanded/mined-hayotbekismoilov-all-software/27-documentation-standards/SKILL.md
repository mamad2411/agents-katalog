---
name: documentation-standards
description: |
  Code and API documentation standards. Apply when writing docstrings, README files,
  API docs, or architecture documents. Covers OpenAPI/Swagger setup, JSDoc/TSDoc patterns,
  README structure, and ADR (Architecture Decision Records).
---

# Documentation Standards

## OpenAPI / Swagger (FastAPI auto-docs)
```python
from fastapi import FastAPI
from drf_spectacular.utils import extend_schema, OpenApiParameter

app = FastAPI(
    title="MyWeb API",
    version="1.0.0",
    description="MyWeb Digital Agency — Client Projects API",
    contact={"name": "Hayotbek", "email": "hello@myweb.uz"},
)

# Document every endpoint
@extend_schema(
    summary="Create a new order",
    description="Creates an order with the provided items. Requires authentication.",
    request=OrderCreateSerializer,
    responses={
        201: OrderResponseSerializer,
        400: ErrorResponseSerializer,
        422: ErrorResponseSerializer,
    },
    tags=["Orders"],
)
@router.post("/orders")
async def create_order(data: OrderCreate, user = Depends(get_current_user)):
    ...
```

## Python Docstrings (Google Style)
```python
def calculate_order_total(items: list[OrderItem], discount: Discount | None = None) -> OrderTotal:
    """Calculate the total price for an order, applying discounts if eligible.

    Args:
        items: List of order items with price and quantity.
        discount: Optional discount to apply. Applied after subtotal is calculated.

    Returns:
        OrderTotal with subtotal, discount_amount, and total fields.

    Raises:
        ValueError: If items list is empty.
        InsufficientStockError: If any item's quantity exceeds available stock.

    Example:
        >>> items = [OrderItem(product_id="p1", price=100, quantity=2)]
        >>> result = calculate_order_total(items)
        >>> result.total
        Decimal('200.00')
    """
```

## TypeScript TSDoc
```typescript
/**
 * Formats a price value for display in Uzbek Som.
 *
 * @param amount - The price amount in regular sum (not tiyins)
 * @param options - Formatting options
 * @param options.compact - If true, uses compact notation (1.2M so'm)
 * @returns Formatted price string with currency symbol
 *
 * @example
 * formatPrice(125000) // "125 000 so'm"
 * formatPrice(1250000, { compact: true }) // "1.25M so'm"
 */
export function formatPrice(amount: number, options: { compact?: boolean } = {}): string { ... }
```

## README Template
```markdown
# Project Name

Brief description of what this project does and who it's for.

## Quick Start
\`\`\`bash
git clone ...
cp .env.example .env
docker compose up -d
\`\`\`

## Tech Stack
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Backend**: Django 4.2 + DRF + Celery
- **Database**: PostgreSQL + Redis
- **Deploy**: Docker + Nginx

## Project Structure
\`\`\`
├── frontend/    # React application
├── backend/     # Django API
├── nginx/       # Reverse proxy config
└── docker-compose.yml
\`\`\`

## Environment Variables
See `.env.example` for all required variables.

## API Documentation
Running locally: http://localhost:8000/api/docs

## Contributing
1. Branch naming: `feature/`, `fix/`, `chore/`
2. Commit format: `feat: add payment integration`
3. All PRs require passing tests
```

## ADR (Architecture Decision Records)
```markdown
# ADR-001: Use polling instead of webhooks for Telegram bot

**Date**: 2024-12-01
**Status**: Accepted

## Context
We need to deploy a Telegram bot without a public HTTPS endpoint.

## Decision
Use aiogram polling instead of webhook mode.

## Consequences
- ✅ Simpler deployment — no SSL cert or public IP needed
- ✅ Works on development machines
- ❌ Slightly higher latency (~1-3s vs instant for webhooks)
- ❌ Not suitable for >10,000 messages/day (consider webhook at scale)
```
