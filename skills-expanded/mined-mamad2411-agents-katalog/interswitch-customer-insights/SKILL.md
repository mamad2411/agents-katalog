---
name: interswitch-customer-insights
description: >-
  Interswitch Customer Insights API — access customer demographics, financial history,
  and spending habits for KYC, credit scoring, and personalization. Use this skill
  whenever performing KYC checks, building credit scoring models, analyzing customer
  financial behavior, verifying customer identity, or implementing data-driven
  personalization. Also use when you see references to customer demographics, financial
  history, spending habits, or /api/v1/customer-insights endpoints.
---

# Interswitch Customer Insights API

Access customer demographics, financial transaction history, and spending patterns for KYC verification, credit scoring, and service personalization.

## Insight Categories

| Category | Data Available |
| --- | --- |
| Demographics | Name, age, gender, location, phone, email |
| Financial History | Transaction history, account balances, income patterns |
| Financial Habits | Spending categories, frequency, average amounts |

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/customer-insights/demographics` | POST | Get demographic data |
| `/api/v1/customer-insights/financial-history` | POST | Get transaction history |
| `/api/v1/customer-insights/financial-habits` | POST | Get spending patterns |

## Customer Demographics

```typescript
interface DemographicsRequest {
  customerId: string;         // BVN, phone, or account number
  idType: 'BVN' | 'PHONE' | 'ACCOUNT';
  consent: boolean;           // Customer consent required
}

interface DemographicsResponse {
  responseCode: string;
  data: {
    firstName: string;
    lastName: string;
    middleName?: string;
    dateOfBirth: string;
    gender: string;
    phoneNumber: string;
    email?: string;
    address?: string;
    state?: string;
    lga?: string;
    nationality: string;
    bvn?: string;
  };
}

async function getCustomerDemographics(
  data: DemographicsRequest
): Promise<DemographicsResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/customer-insights/demographics`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Financial History

```typescript
interface FinancialHistoryRequest {
  customerId: string;
  idType: 'BVN' | 'PHONE' | 'ACCOUNT';
  startDate: string;          // YYYY-MM-DD
  endDate: string;            // YYYY-MM-DD
  consent: boolean;
}

interface TransactionRecord {
  date: string;
  amount: number;
  type: 'CREDIT' | 'DEBIT';
  description: string;
  category: string;
  channel: string;
  balance?: number;
}

interface FinancialHistoryResponse {
  responseCode: string;
  data: {
    totalCredits: number;
    totalDebits: number;
    averageBalance: number;
    transactions: TransactionRecord[];
    incomePattern: {
      averageMonthlyIncome: number;
      incomeFrequency: string;
      primaryIncomeSource: string;
    };
  };
}

async function getFinancialHistory(
  data: FinancialHistoryRequest
): Promise<FinancialHistoryResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/customer-insights/financial-history`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Financial Habits

```typescript
interface FinancialHabitsRequest {
  customerId: string;
  idType: 'BVN' | 'PHONE' | 'ACCOUNT';
  period: number;             // Months to analyze
  consent: boolean;
}

interface SpendingCategory {
  category: string;           // e.g., 'Food', 'Transport', 'Bills'
  totalAmount: number;
  percentage: number;
  transactionCount: number;
  averageAmount: number;
}

interface FinancialHabitsResponse {
  responseCode: string;
  data: {
    spendingCategories: SpendingCategory[];
    savingsRate: number;
    transactionFrequency: {
      daily: number;
      weekly: number;
      monthly: number;
    };
    preferredChannels: {
      channel: string;        // 'POS', 'ATM', 'Web', 'Mobile'
      percentage: number;
    }[];
    riskScore: number;        // 0-100 risk assessment
  };
}

async function getFinancialHabits(
  data: FinancialHabitsRequest
): Promise<FinancialHabitsResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/customer-insights/financial-habits`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Complete KYC Flow

```typescript
// 1. Get demographics for identity verification
const demographics = await getCustomerDemographics({
  customerId: '22123456789',  // BVN
  idType: 'BVN',
  consent: true,
});

console.log('Customer:', demographics.data.firstName, demographics.data.lastName);

// 2. Get financial history for credit assessment
const history = await getFinancialHistory({
  customerId: '22123456789',
  idType: 'BVN',
  startDate: '2024-01-01',
  endDate: '2024-12-31',
  consent: true,
});

console.log('Monthly income:', history.data.incomePattern.averageMonthlyIncome / 100);
console.log('Total credits:', history.data.totalCredits / 100);

// 3. Get spending habits for risk profiling
const habits = await getFinancialHabits({
  customerId: '22123456789',
  idType: 'BVN',
  period: 6,
  consent: true,
});

console.log('Risk score:', habits.data.riskScore);
console.log('Top spending:', habits.data.spendingCategories[0]);
```

## Data Privacy & Compliance

1. **Customer consent is mandatory** — Always set `consent: true` only after explicit consent
2. **NDPR compliance** — Follow Nigeria Data Protection Regulation
3. **Data minimization** — Only request data you actually need
4. **Secure storage** — Encrypt all customer insight data at rest
5. **Access logging** — Log all data access for audit trails
6. **Data retention** — Implement retention policies per regulatory requirements
7. **Right to erasure** — Honor customer requests to delete their data
