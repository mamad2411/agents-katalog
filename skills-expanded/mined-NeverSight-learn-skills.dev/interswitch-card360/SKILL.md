---
name: interswitch-card360
description: >-
  Interswitch Card 360 API — create, manage, block/unblock, set PINs, and check
  balances for debit cards. Use this skill whenever implementing card issuance,
  card lifecycle management, PIN management flows, card blocking/unblocking, or
  balance inquiries on Interswitch-issued cards. Also use when you see references
  to Card 360, card management, card issuance, PIN reset, or /api/v1/cards endpoints.
---

# Interswitch Card 360 API

Manage the complete lifecycle of debit cards — issuance, PIN management, blocking/unblocking, and balance inquiries.

## Card Lifecycle

```
Create Card → Set PIN → Activate → Use → Block/Unblock → Expire/Renew
```

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/cards` | POST | Create/issue a new card |
| `/api/v1/cards/{cardId}` | GET | Get card details |
| `/api/v1/cards/{cardId}/balance` | GET | Check card balance |
| `/api/v1/cards/{cardId}/pin` | PUT | Set or reset PIN |
| `/api/v1/cards/{cardId}/block` | POST | Block a card |
| `/api/v1/cards/{cardId}/unblock` | POST | Unblock a card |
| `/api/v1/cards/{cardId}/status` | GET | Get card status |

## Create Card

```typescript
interface CreateCardRequest {
  customerId: string;
  cardType: 'VIRTUAL' | 'PHYSICAL';
  cardScheme: 'VERVE' | 'VISA' | 'MASTERCARD';
  currency: string;           // e.g., 'NGN'
  accountNumber: string;
  bankCode: string;
  firstName: string;
  lastName: string;
  phoneNumber: string;
  email: string;
  dateOfBirth: string;        // YYYY-MM-DD
  address?: string;
}

interface CardResponse {
  responseCode: string;
  cardId: string;
  pan: string;                // Masked PAN (e.g., 506105****7864)
  expiryDate: string;         // YYMM
  cardType: string;
  cardScheme: string;
  status: string;
  createdAt: string;
}

async function createCard(
  data: CreateCardRequest
): Promise<CardResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/cards`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Get Card Details

```typescript
async function getCardDetails(
  cardId: string
): Promise<CardResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/cards/${encodeURIComponent(cardId)}`,
    { method: 'GET', headers }
  );

  return response.json();
}
```

## Check Card Balance

```typescript
interface CardBalance {
  availableBalance: number;
  ledgerBalance: number;
  currency: string;
}

async function getCardBalance(
  cardId: string
): Promise<CardBalance> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/cards/${encodeURIComponent(cardId)}/balance`,
    { method: 'GET', headers }
  );

  return response.json();
}
```

## Set / Reset PIN

```typescript
interface SetPinRequest {
  oldPin?: string;            // Required for PIN change (not initial set)
  newPin: string;             // 4-digit PIN
  confirmPin: string;         // Must match newPin
}

async function setCardPin(
  cardId: string,
  data: SetPinRequest
): Promise<{ responseCode: string; responseDescription: string }> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/cards/${encodeURIComponent(cardId)}/pin`,
    {
      method: 'PUT',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Block Card

```typescript
interface BlockCardRequest {
  reason: string;             // Reason for blocking
  blockType: 'TEMPORARY' | 'PERMANENT';
}

async function blockCard(
  cardId: string,
  data: BlockCardRequest
): Promise<{ responseCode: string; responseDescription: string }> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/cards/${encodeURIComponent(cardId)}/block`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Unblock Card

```typescript
async function unblockCard(
  cardId: string
): Promise<{ responseCode: string; responseDescription: string }> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/cards/${encodeURIComponent(cardId)}/unblock`,
    {
      method: 'POST',
      headers,
    }
  );

  return response.json();
}
```

## Complete Card Management Flow

```typescript
// 1. Issue a virtual card
const card = await createCard({
  customerId: 'CUST_001',
  cardType: 'VIRTUAL',
  cardScheme: 'VERVE',
  currency: 'NGN',
  accountNumber: '0123456789',
  bankCode: '058',
  firstName: 'John',
  lastName: 'Doe',
  phoneNumber: '+2348012345678',
  email: 'john@example.com',
  dateOfBirth: '1990-01-15',
});

console.log('Card ID:', card.cardId);
console.log('PAN:', card.pan);

// 2. Set PIN
await setCardPin(card.cardId, {
  newPin: '1234',
  confirmPin: '1234',
});

// 3. Check balance
const balance = await getCardBalance(card.cardId);
console.log('Balance:', balance.availableBalance / 100);

// 4. Block card if compromised
await blockCard(card.cardId, {
  reason: 'Suspected fraud',
  blockType: 'TEMPORARY',
});

// 5. Unblock after investigation
await unblockCard(card.cardId);

// 6. Change PIN
await setCardPin(card.cardId, {
  oldPin: '1234',
  newPin: '5678',
  confirmPin: '5678',
});
```

## Card Statuses

| Status | Description |
| --- | --- |
| `ACTIVE` | Card is usable |
| `INACTIVE` | Card created but not activated |
| `BLOCKED` | Card is temporarily blocked |
| `EXPIRED` | Card has expired |
| `CLOSED` | Card permanently deactivated |

## Best Practices

1. **Never log full PAN** — Only use masked versions
2. **PIN handling** — Never store or log PINs
3. **Block immediately** on fraud suspicion
4. **Implement PIN retry limits** — Lock after 3 failed attempts
5. **Use virtual cards** for online-only use cases
6. **Monitor card status** — Set up alerts for status changes
