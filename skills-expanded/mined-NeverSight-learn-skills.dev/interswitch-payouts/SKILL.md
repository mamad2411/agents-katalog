---
name: interswitch-payouts
description: >-
  Interswitch Payouts API — look up receiving institutions, discover payout channels,
  and route disbursements. Use this skill whenever building payout infrastructure,
  discovering available disbursement channels, resolving receiving institutions, or
  implementing multi-channel payout routing. Also use when you see references to
  payout channels, receiving institutions, disbursement routing, or
  /api/v1/payouts endpoints.
---

# Interswitch Payouts API

Discover available payout channels and receiving institutions for routing disbursements across Nigeria.

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/payouts/channels` | GET | List available payout channels |
| `/api/v1/payouts/institutions` | GET | List receiving institutions |
| `/api/v1/payouts/institutions/{code}` | GET | Get institution details |

## Payout Channels

```typescript
interface PayoutChannel {
  channelCode: string;
  channelName: string;
  description: string;
  supportedCurrencies: string[];
  isActive: boolean;
}

async function getPayoutChannels(): Promise<PayoutChannel[]> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/payouts/channels`,
    { method: 'GET', headers }
  );

  const data = await response.json();
  return data.channels;
}
```

### Available Channels

| Channel | Code | Description |
| --- | --- | --- |
| Bank Transfer | `BANK` | Direct bank account transfer |
| Mobile Money | `MOBILE_MONEY` | Mobile wallet payout |
| Card | `CARD` | Card-based disbursement |
| Paycode | `PAYCODE` | ATM cardless withdrawal |

## Receiving Institutions

```typescript
interface ReceivingInstitution {
  institutionCode: string;
  institutionName: string;
  type: 'BANK' | 'MICROFINANCE' | 'MOBILE_MONEY';
  isActive: boolean;
  supportedChannels: string[];
  nipCode?: string;
}

async function getReceivingInstitutions(
  channel?: string
): Promise<ReceivingInstitution[]> {
  const headers = await getAuthHeaders();

  const url = new URL(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/payouts/institutions`
  );
  if (channel) url.searchParams.set('channel', channel);

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers,
  });

  const data = await response.json();
  return data.institutions;
}
```

## Get Institution Details

```typescript
async function getInstitutionDetails(
  institutionCode: string
): Promise<ReceivingInstitution> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/payouts/institutions/${encodeURIComponent(institutionCode)}`,
    { method: 'GET', headers }
  );

  return response.json();
}
```

## Payout Routing

```typescript
// Build a payout router that selects the best channel
interface PayoutRequest {
  recipientAccount: string;
  recipientInstitution: string;
  amount: number;
  currency: string;
}

async function routePayout(request: PayoutRequest): Promise<string> {
  // 1. Get institution details
  const institution = await getInstitutionDetails(request.recipientInstitution);

  // 2. Find available channels for this institution
  const channels = await getPayoutChannels();
  const activeChannels = channels.filter(
    (c) => c.isActive && institution.supportedChannels.includes(c.channelCode)
  );

  if (activeChannels.length === 0) {
    throw new Error(`No active payout channels for ${institution.institutionName}`);
  }

  // 3. Prefer bank transfer, fall back to others
  const preferred = activeChannels.find((c) => c.channelCode === 'BANK')
    || activeChannels[0];

  return preferred.channelCode;
}
```

## Complete Payout Discovery Flow

```typescript
// 1. Discover channels
const channels = await getPayoutChannels();
console.log('Available channels:', channels.map((c) => c.channelName));

// 2. List bank institutions
const banks = await getReceivingInstitutions('BANK');
console.log('Banks:', banks.length);
banks.forEach((bank) => {
  console.log(`${bank.institutionCode}: ${bank.institutionName}`);
});

// 3. Get specific bank details
const gtbank = await getInstitutionDetails('058');
console.log('GTBank channels:', gtbank.supportedChannels);

// 4. Use with transfers
// Once you have the institution code, use the interswitch-transfers skill
// to initiate the actual transfer
```

## Best Practices

1. **Cache institution lists** — They don't change often (refresh daily)
2. **Check `isActive` status** — Only route to active institutions
3. **Implement fallback channels** — Route to alternative if primary fails
4. **Validate institution codes** — Confirm before initiating transfers
5. **Monitor channel availability** — Set up alerts for channel status changes
