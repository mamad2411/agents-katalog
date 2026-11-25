---
name: shiprocket
description: Use this skill whenever the user wants to integrate Shiprocket logistics APIs. Triggers include: creating shipment orders, generating AWB numbers, tracking parcels by AWB or order ID, checking courier serviceability between pincodes, calculating shipping rates, generating shipping labels, handling NDR (Non-Delivery Reports), cancelling orders, requesting pickups, or building any eCommerce shipping workflow using Shiprocket. Also trigger when user mentions Shiprocket courier, logistics API, AWB tracking, or delivery partner selection.
---

## Source
- Official docs: https://apidocs.shiprocket.in/
- Base URL (confirmed across all implementations): `https://apiv2.shiprocket.in/v1/external/`
- Auth: Bearer token (JWT), expires every 24 hours — must refresh daily

## Bundled Files
| File | Purpose |
|---|---|
| `scripts/shiprocket_client.py` | Reusable Python client — import in any project |
| `scripts/test_shiprocket.py` | Smoke-test script |
| `scripts/requirements.txt` | Python dependencies |
| `references/endpoints.md` | Full endpoint reference table |

---

## Step 0 — Get Credentials

1. Sign up at https://app.shiprocket.in/register
2. Go to **Settings → API → Configure → Create an API User**
3. Enter email + password → these are your API credentials (separate from login)
4. Max 4 API users allowed per account

```
SHIPROCKET_EMAIL=your_api_user@email.com
SHIPROCKET_PASSWORD=your_api_password
```

---

## Authentication — Generate Token

**Every request needs a Bearer token. Token expires in 24 hours.**

```
POST https://apiv2.shiprocket.in/v1/external/auth/login
```

```python
import requests, os

BASE = "https://apiv2.shiprocket.in/v1/external"

def get_token(email: str, password: str) -> str:
    res = requests.post(f"{BASE}/auth/login", json={
        "email": email,
        "password": password
    })
    return res.json()["token"]

TOKEN = get_token(os.environ["SHIPROCKET_EMAIL"], os.environ["SHIPROCKET_PASSWORD"])
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
```

> ⚠️ Token is valid for 24 hrs. Cache it; don't generate a new one per request.

---

## Core Flow

```
1. Check Serviceability  →  Is delivery possible between 2 pincodes?
2. Create Order          →  Register order in Shiprocket
3. Generate AWB          →  Assign courier + get AWB number
4. Request Pickup        →  Schedule courier to collect
5. Generate Label        →  Print shipping label (PDF)
6. Track Shipment        →  Live tracking by AWB or order ID
7. Handle NDR            →  Re-attempt failed deliveries
```

---

## 1. Check Courier Serviceability

```
GET https://apiv2.shiprocket.in/v1/external/courier/serviceability/
```

```python
params = {
    "pickup_postcode":   "110001",   # seller pincode
    "delivery_postcode": "400001",   # buyer pincode
    "weight":            0.5,        # kg
    "cod":               0           # 0=prepaid, 1=COD
}
res = requests.get(f"{BASE}/courier/serviceability/", headers=HEADERS, params=params)
couriers = res.json()["data"]["available_courier_companies"]
# Pick cheapest:
best = min(couriers, key=lambda c: c["rate"])
courier_id = best["courier_company_id"]
print(f"Best courier: {best['courier_name']} @ ₹{best['rate']}")
```

---

## 2. Create an Order

```
POST https://apiv2.shiprocket.in/v1/external/orders/create/adhoc
```

```python
order_data = {
    # Order info
    "order_id":       "ORD-001",          # your unique ID
    "order_date":     "2025-04-25 10:00", # YYYY-MM-DD HH:MM
    "pickup_location": "Primary",          # warehouse name in Shiprocket

    # Billing / Customer
    "billing_customer_name": "Rahul Sharma",
    "billing_last_name":     "Sharma",
    "billing_address":       "123 MG Road",
    "billing_city":          "Mumbai",
    "billing_pincode":       "400001",
    "billing_state":         "Maharashtra",
    "billing_country":       "India",
    "billing_email":         "rahul@example.com",
    "billing_phone":         "9876543210",

    # Shipping = billing if same address
    "shipping_is_billing": True,

    # Items
    "order_items": [
        {
            "name":          "Cotton Kurta",
            "sku":           "KURTA-001",
            "units":         2,
            "selling_price": 499,
            "discount":      "",
            "tax":           "",
            "hsn":           620469        # HSN code for apparel
        }
    ],

    # Payment
    "payment_method": "Prepaid",   # or "COD"
    "sub_total":      998,

    # Package dimensions
    "length": 30,    # cm
    "breadth": 20,
    "height":  5,
    "weight":  0.5   # kg
}

res = requests.post(f"{BASE}/orders/create/adhoc", json=order_data, headers=HEADERS)
data = res.json()
order_id   = data["order_id"]
shipment_id = data["shipment_id"]
print(f"Order created: {order_id} | Shipment: {shipment_id}")
```

---

## 3. Generate AWB (Assign Courier)

```
POST https://apiv2.shiprocket.in/v1/external/courier/assign/awb
```

```python
res = requests.post(f"{BASE}/courier/assign/awb", headers=HEADERS, json={
    "shipment_id": shipment_id,
    "courier_id":  str(courier_id)   # from serviceability check
})
awb_code = res.json()["response"]["data"]["awb_code"]
print(f"AWB: {awb_code}")
```

---

## 4. Request Pickup

```
POST https://apiv2.shiprocket.in/v1/external/courier/generate/pickup
```

```python
res = requests.post(f"{BASE}/courier/generate/pickup", headers=HEADERS, json={
    "shipment_id": [shipment_id]   # list — can batch multiple
})
print(res.json())
```

---

## 5. Generate Shipping Label

```
POST https://apiv2.shiprocket.in/v1/external/courier/generate/label
```

```python
res = requests.post(f"{BASE}/courier/generate/label", headers=HEADERS, json={
    "shipment_id": [shipment_id]
})
label_url = res.json()["label_url"]   # PDF download URL
print(f"Label: {label_url}")
```

---

## 6. Track Shipment

### By AWB code
```
GET https://apiv2.shiprocket.in/v1/external/courier/track/awb/{awb}
```
```python
res = requests.get(f"{BASE}/courier/track/awb/{awb_code}", headers=HEADERS)
tracking = res.json()["tracking_data"]
print(tracking["shipment_track"][0]["current_status"])
```

### By Order ID
```
GET https://apiv2.shiprocket.in/v1/external/orders/show/{order_id}
```
```python
res = requests.get(f"{BASE}/orders/show/{order_id}", headers=HEADERS)
```

### Multiple AWBs (batch)
```
GET https://apiv2.shiprocket.in/v1/external/courier/track?awb=AWB1,AWB2,AWB3
```

---

## 7. Cancel Order

```
POST https://apiv2.shiprocket.in/v1/external/orders/cancel
```
```python
res = requests.post(f"{BASE}/orders/cancel", headers=HEADERS, json={
    "ids": [order_id]   # list of order IDs
})
```

---

## 8. NDR — Non-Delivery Report (Failed Delivery)

```python
# Get all NDR shipments
res = requests.get(f"{BASE}/ndr/all", headers=HEADERS)

# Get specific AWB in NDR
res = requests.get(f"{BASE}/ndr/{awb_code}", headers=HEADERS)

# Re-attempt delivery with updated address
res = requests.post(f"{BASE}/ndr/reattempt", headers=HEADERS, params={
    "awb":           awb_code,
    "address1":      "New Address Line 1",
    "address2":      "Landmark",
    "phone":         "9876543210",
    "deferred_date": "2025-04-30"   # YYYY-MM-DD
})
```

---

## Important Notes

| Rule | Detail |
|---|---|
| Token expiry | 24 hours — cache it, use env vars or Redis |
| `shipment_id` vs `order_id` | Shiprocket creates both; AWB needs `shipment_id` |
| Weight unit | Always **kilograms** (kg), not grams |
| Dimensions | Always **centimetres** (cm) |
| `payment_method` values | `"Prepaid"` or `"COD"` (case-sensitive) |
| `pickup_location` | Must match exact warehouse name in your Shiprocket panel |
| HSN code | Required for GST compliance on order items |
| COD charge | Shiprocket deducts COD fee from remittance automatically |
