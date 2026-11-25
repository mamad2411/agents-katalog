---
name: printkk-print-on-demand
description: >
  Domain knowledge for using PrintKK print-on-demand API tools effectively.
  PrintKK is a print-on-demand platform that lets sellers create custom products,
  manage designs, upload images, and fulfill orders via API.
  Use this skill whenever the user wants to interact with PrintKK — browsing products,
  creating designs, placing orders, managing images, or building integrations with the
  PrintKK API. Also trigger when the user mentions "PrintKK", "print on demand",
  "POD fulfillment", custom product design workflows, or wants to automate their
  PrintKK store operations.
---

# PrintKK

PrintKK is a print-on-demand platform that connects sellers with production and fulfillment for custom products — apparel, home decor, accessories, and more. Use the API to automate design creation, product browsing, order placement, and image management.

**Base URL:** `https://api.printkk.com/pkk-openapi`

## API Scope & Limitations

The API covers **internal PrintKK operations only**:
- ✅ Image upload & management
- ✅ Design creation & editing
- ✅ Order creation, payment, tracking
- ✅ Product catalog browsing
- ❌ **No publishing** — you cannot publish designs to external sales channels (Shopify, Etsy, etc.) via API. Publishing must be done through the PrintKK Dashboard.
- ❌ **No shop/store management** — the API does not expose multi-shop operations. Although PrintKK accounts support multiple stores, the API operates at the account level without shop scoping.
- ❌ **No print provider selection** — PrintKK uses its own production network. Unlike marketplace-model platforms, there is no API for choosing print providers. Production routing is handled internally by PrintKK.

## Authentication

All requests require an `Api-Key` header.

- Get your key: PrintKK Dashboard → **Settings** → **Api Management**
- Keys expire — validity extends 90 days per renewal
- Renewal only allowed when remaining validity ≤ 7 days
- Expired keys cannot be renewed; generate a new one

```
Api-Key: <your-api-key>
```

## Response Format

All responses follow this structure:

```json
{
  "code": 200,
  "success": true,
  "msg": "OK",
  "data": { ... }
}
```

Check `success` field first, not just HTTP status code.

## Data Model

```
Product (catalog)          Image (media library)
  ├── productCode             ├── imageId
  ├── printAreas[]            ├── folderId
  └── specifications[]        └── keywords
         │                         │
         ▼                         ▼
      Design ◄────────────── uses imageId per printArea
        ├── designCode
        ├── designSpecifications[]
        │     └── designSpecificationCode
        └── taskId (async creation)
                │
                ▼
            Order
              ├── orderId
              ├── designSpecificationCode + quantity
              ├── shippingAddress
              └── shippingType priority list
                      │
                      ▼
                  Payment (wallet)
```

**Key relationships:**
- A **Product** is a catalog template (e.g. "Unisex T-Shirt"). You don't create products — you browse them.
- A **Design** applies your images to a Product's print areas. Creating a design is **async** — you get a `taskId`, then poll for completion.
- An **Order** references `designSpecificationCode` (a specific size/color variant of your design), NOT the product directly.
- **Images** must be uploaded before creating designs. The `imageId` returned from upload is used in design creation.

## Core Workflows

### Workflow 1: Create a Design and Place an Order

This is the most common end-to-end flow. Follow these steps **in order** — skipping steps will fail.

```
1. Browse products     GET  /api/v1/product/page
2. Get product detail  GET  /api/v1/product/{productCode}
   → Note the printAreas and their printAreaCodes
   → Note isWhole (1=full coverage, 0=fragment/placement)
3. Upload image        POST /api/v1/image
   → Returns imageId
4. Create design       POST /api/v1/design
   → Returns taskId (NOT designCode yet!)
5. Poll task status    GET  /api/v1/design/task/{taskId}
   → Wait for designTaskStatus = "completed"
   → Now you have designCode
6. Get design detail   GET  /api/v1/design/{designCode}
   → Get designSpecificationCode for the variant you want
7. Create order        POST /api/v1/order
   → Use designSpecificationCode + quantity
8. Pay with wallet     POST /api/v1/pay/wallet
   → orderId required, wallet must have sufficient balance
```

### Workflow 2: Brand Design Flow

For sellers with branded product lines:

```
1. List brand groups       GET  /api/v1/design/brand-group/list
2. Browse brand designs    GET  /api/v1/design/brand/page
3. Create brand design     POST /api/v1/design/brand
   → Requires brandName (max 50 chars)
   → Same async flow: returns taskId, poll for completion
```

### Workflow 3: Image Management

```
Create folder    POST   /api/v1/image/folder
List folders     GET    /api/v1/image/folder/list
Upload image     POST   /api/v1/image          (multipart/form-data)
Browse images    GET    /api/v1/image/page
Update metadata  PUT    /api/v1/image/{imageId}
```

## Gotchas & Constraints

### Design Creation is Async
This is the #1 mistake. `POST /api/v1/design` does NOT return a design — it returns a `taskId`. You **must** poll `GET /api/v1/design/task/{taskId}` until `designTaskStatus` is `"completed"` before you can use the design. Status progression: `pending` → `generating` → `completed`.

### isWhole Matters
When creating a design, `isWhole` must match the product's print area type:
- `1` = whole (full-surface print, e.g. all-over print t-shirt)
- `0` = fragment (placement print, e.g. logo on chest)

Using the wrong value will produce incorrect output.

### imageFillingMode
Each print area requires an `imageFillingMode`:
- `cover` — image fills the entire area, may crop edges
- `contain` — image fits within the area, may have blank space
- `fill` — image stretches to fill exactly, may distort

### Shipping Type is a Priority List
`shippingType` in order creation is **not** a single choice — it's an ordered array of all three options. The order determines fallback priority:
```json
"shippingType": ["economy", "standard", "express"]
```
All three values must be present. Put your preferred option first.

### Order Can Only Be Modified When Pending
- `Order Address Update` and `Order Cancel` only work on orders with status `pendingPayment`
- Once paid (`waitingForFulfillment` and beyond), the order is locked

### Design Immutability
Once a design has been ordered, exported, or published, its status becomes `immutable`. You can no longer update it — you'd need to create a new design.

### Pagination Defaults
All paginated endpoints default to `current=1`, `size=10`, max `size=50`. If you need all records, loop through pages.

### Image Upload Constraints
- Accepted formats: JPG, JPEG, PNG only
- Max file size: 100MB
- fileName max length: 50 characters
- Upload is `multipart/form-data`, not JSON

### Order Status Lifecycle

```
pendingPayment → waitingForFulfillment → beingFulfilled → partiallyShipped → shipped → completed
       │
       └→ canceled → closed
```

### Rate Limit
Default: **60 requests/minute**. Exceeding this returns `Too Many Requests`. When polling design task status, add reasonable delays (2–3 seconds) between calls.

### No Webhooks
PrintKK does not provide webhooks. To track order status or design task completion, you must **poll** the relevant endpoints. Design task polling is mandatory; order status polling is optional but recommended for automation.

### Timestamps
All timestamps are in **fixed UTC-8 timezone** (does NOT follow daylight saving). Response format: `MM/dd/yyyy HH:mm:ss`. Date filter params in order pagination use `yyyy-MM-dd HH:mm:ss` format — note the inconsistency between input and output formats.

### Product Types
Two product types exist:
- `template` — regular catalog products
- `brand` — brand-specific products (requires separate brand design flow)

## Quick Reference: All Endpoints

| Module  | Method | Path | Summary |
|---------|--------|------|---------|
| General | GET | `/api/v1/general/ping` | Health check |
| General | GET | `/api/v1/general/time` | Server timestamp |
| General | GET | `/api/v1/general/country-list` | Country list (ISO codes) |
| Auth | PUT | `/api/v1/auth/renewal` | Renew API key (≤7 days remaining) |
| Image | POST | `/api/v1/image` | Upload image (multipart) |
| Image | GET | `/api/v1/image/page` | List images (paginated) |
| Image | PUT | `/api/v1/image/{imageId}` | Update image metadata |
| Image | POST | `/api/v1/image/folder` | Create folder |
| Image | GET | `/api/v1/image/folder/list` | List all folders |
| Image | PUT | `/api/v1/image/folder/{folderId}` | Update folder |
| Image | DELETE | `/api/v1/image/folder/{folderId}` | Delete folder |
| Product | GET | `/api/v1/product/category` | Product categories |
| Product | GET | `/api/v1/product/page` | List products (paginated) |
| Product | GET | `/api/v1/product/{productCode}` | Product detail |
| Design | POST | `/api/v1/design` | Create design (async) |
| Design | GET | `/api/v1/design/page` | List designs (paginated) |
| Design | GET | `/api/v1/design/{designCode}` | Design detail |
| Design | PUT | `/api/v1/design/{designCode}` | Update design |
| Design | GET | `/api/v1/design/task/{taskId}` | Poll design task |
| Design | POST | `/api/v1/design/brand` | Create brand design |
| Design | GET | `/api/v1/design/brand/page` | List brand designs |
| Design | GET | `/api/v1/design/brand-group/list` | List brand groups |
| Order | POST | `/api/v1/order` | Create order |
| Order | GET | `/api/v1/order/page` | List orders (paginated) |
| Order | GET | `/api/v1/order/{orderId}` | Order detail |
| Order | PUT | `/api/v1/order/address/{orderId}` | Update address |
| Order | PUT | `/api/v1/order/cancel/{orderId}` | Cancel order |
| Order | POST | `/api/v1/pay/wallet` | Pay with wallet |
| Order | GET | `/api/v1/pay/{orderId}` | Query payment status |
