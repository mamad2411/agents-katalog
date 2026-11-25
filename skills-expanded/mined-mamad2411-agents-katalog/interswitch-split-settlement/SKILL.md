---
name: interswitch-split-settlement
description: >-
  Interswitch Split Settlement API — distribute payments across multiple beneficiary
  accounts using wallet-pay with passport-v2 authentication. Use this skill whenever
  implementing marketplace payments, multi-party settlement, revenue sharing between
  vendors, split payment configurations, or wallet-pay flows. Also use when you see
  references to /api/v2/wallet-pay/initialize, splitSettlement, passport-v2, or
  beneficiary percentage splits.
---

# Interswitch Split Settlement API

Split payments across multiple beneficiary accounts using the wallet-pay system with Passport v2 authentication.

## Split Settlement Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v2/wallet-pay/initialize` | POST | Initialize a split payment |
| `/api/v2/wallet-pay/status` | POST | Check split payment status |

## Authentication

Split settlement uses **Passport v2** (Collections Passport). See `interswitch-setup` skill for `getCollectionsAuthHeaders()`.

```typescript
// Base URL for split settlement
const COLLECTIONS_BASE_URL = process.env.INTERSWITCH_SPLIT_PASSPORT_URL;
// Test: https://qa.interswitchng.com
// Live: https://saturn.interswitchng.com
```

## Split Settlement Data Model

```typescript
interface SplitSettlementItem {
  accountId: string;       // Beneficiary account ID
  accountType: string;     // 'BANK' or 'WALLET'
  bankCode?: string;       // Required if accountType is 'BANK'
  accountNumber?: string;  // Required if accountType is 'BANK'
  percentage: number;      // Settlement percentage (0-100)
  splitPercentage: number; // Split percentage share
}

interface DebitWalletWithSplitDto {
  customerId: string;             // Wallet PAN or customer ID
  amount: number;                 // Total amount in kobo
  currency: string;               // '566' for NGN
  transactionRef: string;         // Unique reference
  pin: string;                    // Customer wallet PIN
  splitSettlement: SplitSettlementItem[];
  requestorId?: string;
  paymentCode?: string;
}

interface WalletPayResponse {
  responseCode: string;
  responseDescription: string;
  amount: number;
  transactionRef: string;
  paymentId: string;
  splitDetails?: SplitSettlementItem[];
}
```

## Initialize Split Payment

```typescript
async function debitWalletWithSplit(
  data: DebitWalletWithSplitDto
): Promise<WalletPayResponse> {
  // Uses Collections Passport v2 authentication
  const headers = await getCollectionsAuthHeaders();

  const response = await fetch(
    `${COLLECTIONS_BASE_URL}/api/v2/wallet-pay/initialize`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(`Split payment failed: ${response.status}`);
  }

  return response.json();
}
```

## Check Split Payment Status

```typescript
interface WalletPayStatusRequest {
  transactionRef: string;
  amount: number;
}

async function getWalletPayStatus(
  data: WalletPayStatusRequest
): Promise<WalletPayResponse> {
  const headers = await getCollectionsAuthHeaders();

  const response = await fetch(
    `${COLLECTIONS_BASE_URL}/api/v2/wallet-pay/status`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(`Status check failed: ${response.status}`);
  }

  return response.json();
}
```

## Get Settlement Accounts

```typescript
interface SettlementAccount {
  accountId: string;
  accountName: string;
  accountNumber: string;
  bankCode: string;
  bankName: string;
}

async function getSettlementAccounts(): Promise<SettlementAccount[]> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_WALLET_BASE_URL}/api/v1/settlement/accounts`,
    {
      method: 'GET',
      headers,
    }
  );

  if (!response.ok) {
    throw new Error(`Get settlement accounts failed: ${response.status}`);
  }

  return response.json();
}
```

## Complete Split Payment Example

```typescript
// Marketplace: 70% to vendor, 20% to platform, 10% to logistics
const splitPayment = await debitWalletWithSplit({
  customerId: customerWalletPan,
  amount: 100000, // ₦1,000.00
  currency: '566',
  transactionRef: `SPLIT_${Date.now()}_${crypto.randomUUID().slice(0, 8)}`,
  pin: customerPin,
  splitSettlement: [
    {
      accountId: 'vendor-001',
      accountType: 'BANK',
      bankCode: '058',
      accountNumber: '0123456789',
      percentage: 70,
      splitPercentage: 70,
    },
    {
      accountId: 'platform-001',
      accountType: 'WALLET',
      percentage: 20,
      splitPercentage: 20,
    },
    {
      accountId: 'logistics-001',
      accountType: 'BANK',
      bankCode: '044',
      accountNumber: '9876543210',
      percentage: 10,
      splitPercentage: 10,
    },
  ],
});

if (splitPayment.responseCode === '00') {
  console.log('Split payment successful');

  // Verify status
  const status = await getWalletPayStatus({
    transactionRef: splitPayment.transactionRef,
    amount: 100000,
  });
  console.log('Settlement status:', status.responseCode);
}
```

## Configuration-Based Splits

For consistent splits (e.g., levy systems), define split configurations:

```typescript
interface SplitConfig {
  name: string;
  beneficiaries: {
    name: string;
    accountId: string;
    accountType: 'BANK' | 'WALLET';
    bankCode?: string;
    accountNumber?: string;
    percentage: number;
  }[];
}

// Example: State levy split configuration
const levySplitConfig: SplitConfig = {
  name: 'State Levy Collection',
  beneficiaries: [
    { name: 'State Government', accountId: 'state-001', accountType: 'BANK', bankCode: '058', accountNumber: '0123456789', percentage: 60 },
    { name: 'Local Government', accountId: 'lga-001', accountType: 'BANK', bankCode: '044', accountNumber: '9876543210', percentage: 25 },
    { name: 'Collection Agent', accountId: 'agent-001', accountType: 'WALLET', percentage: 15 },
  ],
};

function buildSplitSettlement(
  config: SplitConfig
): SplitSettlementItem[] {
  const total = config.beneficiaries.reduce((sum, b) => sum + b.percentage, 0);
  if (total !== 100) {
    throw new Error(`Split percentages must total 100, got ${total}`);
  }

  return config.beneficiaries.map((b) => ({
    accountId: b.accountId,
    accountType: b.accountType,
    bankCode: b.bankCode,
    accountNumber: b.accountNumber,
    percentage: b.percentage,
    splitPercentage: b.percentage,
  }));
}
```

## Best Practices

1. **Percentages must total 100%** — Validate before submission
2. **Use Passport v2** — Split settlements require collections passport-v2 auth
3. **Verify all beneficiary accounts** before configuring splits
4. **Always check status** — Use `getWalletPayStatus` to confirm settlement
5. **Handle partial failures** — Some beneficiaries may fail while others succeed
