---
name: interswitch-transaction-search
description: >-
  Interswitch Transaction Search API — quick search, reference lookup, bulk search,
  and detailed transaction reporting. Use this skill whenever looking up transaction
  details, performing reconciliation, searching transactions by reference, date range,
  or status, building transaction reports, or debugging payment issues. Also use when
  you see references to transaction search, transaction lookup, quick search, bulk
  search, or /api/v1/transactions/search endpoints.
---

# Interswitch Transaction Search API

Search and retrieve transaction details for reconciliation, reporting, and dispute resolution.

## Search Types

| Type | Use Case |
| --- | --- |
| Quick Search | Fast lookup by transaction reference |
| Reference Search | Search by merchant or payment reference |
| Bulk Search | Multiple transactions by criteria |
| Date Range Search | Transactions within a time period |

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/transactions/search/quick` | GET | Quick single-ref lookup |
| `/api/v1/transactions/search/reference` | GET | Search by reference |
| `/api/v1/transactions/search` | POST | Advanced/bulk search |

## Quick Search

```typescript
interface TransactionDetail {
  transactionRef: string;
  paymentReference: string;
  amount: number;
  currency: string;
  responseCode: string;
  responseDescription: string;
  transactionDate: string;
  channel: string;
  cardNumber?: string;        // Masked
  customerEmail?: string;
  merchantCode: string;
  payItemId: string;
  settlementStatus: string;
}

async function quickSearch(
  transactionRef: string
): Promise<TransactionDetail> {
  const headers = await getAuthHeaders();

  const url = new URL(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/transactions/search/quick`
  );
  url.searchParams.set('transactionRef', transactionRef);

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers,
  });

  return response.json();
}
```

## Reference Search

```typescript
async function searchByReference(
  reference: string,
  referenceType: 'MERCHANT' | 'PAYMENT' = 'MERCHANT'
): Promise<TransactionDetail[]> {
  const headers = await getAuthHeaders();

  const url = new URL(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/transactions/search/reference`
  );
  url.searchParams.set('reference', reference);
  url.searchParams.set('referenceType', referenceType);

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers,
  });

  const data = await response.json();
  return data.transactions;
}
```

## Advanced Search (Bulk)

```typescript
interface TransactionSearchRequest {
  startDate: string;          // YYYY-MM-DD
  endDate: string;            // YYYY-MM-DD
  status?: 'SUCCESS' | 'FAILED' | 'PENDING' | 'ALL';
  channel?: 'WEB' | 'POS' | 'ATM' | 'MOBILE' | 'ALL';
  minAmount?: number;         // In kobo
  maxAmount?: number;
  merchantCode?: string;
  page?: number;
  pageSize?: number;          // Max 100
}

interface SearchResponse {
  transactions: TransactionDetail[];
  totalCount: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

async function searchTransactions(
  criteria: TransactionSearchRequest
): Promise<SearchResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/transactions/search`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(criteria),
    }
  );

  return response.json();
}
```

## Complete Search Examples

```typescript
// Quick single lookup
const txn = await quickSearch('TXN_1234567890');
console.log('Status:', txn.responseCode, txn.responseDescription);
console.log('Amount:', txn.amount / 100);

// Search by merchant reference
const byRef = await searchByReference('ORDER_001', 'MERCHANT');
console.log('Found:', byRef.length, 'transactions');

// Advanced search: all successful transactions this month
const results = await searchTransactions({
  startDate: '2024-12-01',
  endDate: '2024-12-31',
  status: 'SUCCESS',
  channel: 'WEB',
  page: 1,
  pageSize: 50,
});

console.log(`Page ${results.page} of ${results.totalPages}`);
console.log(`Total: ${results.totalCount} transactions`);
results.transactions.forEach((txn) => {
  console.log(`${txn.transactionRef}: ₦${txn.amount / 100} - ${txn.responseDescription}`);
});

// Paginate through all results
let allTransactions: TransactionDetail[] = [];
let page = 1;
let hasMore = true;

while (hasMore) {
  const pageResults = await searchTransactions({
    startDate: '2024-12-01',
    endDate: '2024-12-31',
    status: 'SUCCESS',
    page,
    pageSize: 100,
  });

  allTransactions = [...allTransactions, ...pageResults.transactions];
  hasMore = page < pageResults.totalPages;
  page++;
}

console.log('Total fetched:', allTransactions.length);
```

## Reconciliation Pattern

```typescript
interface ReconciliationResult {
  matched: number;
  unmatched: string[];        // Transaction refs not found
  discrepancies: {
    transactionRef: string;
    expectedAmount: number;
    actualAmount: number;
  }[];
}

async function reconcileTransactions(
  localRecords: { ref: string; amount: number }[],
  startDate: string,
  endDate: string
): Promise<ReconciliationResult> {
  // Fetch all Interswitch transactions for the period
  const iswTransactions = await searchTransactions({
    startDate,
    endDate,
    status: 'SUCCESS',
    pageSize: 100,
  });

  const iswMap = new Map(
    iswTransactions.transactions.map((t) => [t.transactionRef, t])
  );

  const result: ReconciliationResult = {
    matched: 0,
    unmatched: [],
    discrepancies: [],
  };

  for (const record of localRecords) {
    const iswTxn = iswMap.get(record.ref);
    if (!iswTxn) {
      result.unmatched.push(record.ref);
    } else if (iswTxn.amount !== record.amount) {
      result.discrepancies.push({
        transactionRef: record.ref,
        expectedAmount: record.amount,
        actualAmount: iswTxn.amount,
      });
    } else {
      result.matched++;
    }
  }

  return result;
}
```

## Best Practices

1. **Use quick search** for single transaction lookups — faster response
2. **Paginate bulk searches** — Don't request all at once
3. **Cache search results** — Avoid repeated API calls for the same data
4. **Implement reconciliation** — Run daily to catch discrepancies
5. **Filter by status** — Reduce response size by filtering upfront
6. **Date range limits** — Keep ranges narrow (max 30 days recommended)
