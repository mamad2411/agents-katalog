---
name: interswitch-lending
description: >-
  Interswitch Lending API — nano loans, salary lending, and value financing products.
  Use this skill whenever implementing micro-lending, salary advance features, product
  financing, loan origination, or repayment processing through Interswitch. Also use
  when you see references to nano-loans, salary lending, value financing, credit scoring,
  or loan disbursement via Interswitch APIs.
---

# Interswitch Lending API

Access lending products including nano loans, salary lending, and value financing through the Interswitch platform.

## Lending Products

| Product | Description | Typical Amount |
| --- | --- | --- |
| Nano Loans | Micro-loans for instant cash needs | ₦1,000 – ₦50,000 |
| Salary Lending | Salary advance for employed individuals | Up to 50% of salary |
| Value Financing | Product/asset financing | ₦50,000 – ₦5,000,000 |

## Nano Loans

### Loan Eligibility Check

```typescript
interface LoanEligibilityRequest {
  customerId: string;        // Customer identifier
  phoneNumber: string;       // +234XXXXXXXXXX
  bvn?: string;              // Bank Verification Number
  employerId?: string;
}

interface LoanEligibilityResponse {
  eligible: boolean;
  maxAmount: number;         // Maximum loan amount in kobo
  tenor: number[];           // Available tenure options (days)
  interestRate: number;      // Percentage
  reasons?: string[];        // If not eligible, reasons why
}

async function checkLoanEligibility(
  data: LoanEligibilityRequest
): Promise<LoanEligibilityResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/lending/eligibility`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

### Request Nano Loan

```typescript
interface NanoLoanRequest {
  customerId: string;
  amount: number;              // In kobo
  tenor: number;               // Days
  phoneNumber: string;
  disbursementAccount: {
    accountNumber: string;
    bankCode: string;
  };
  transactionRef: string;
}

interface LoanResponse {
  responseCode: string;
  responseDescription: string;
  loanId: string;
  amount: number;
  tenor: number;
  interestAmount: number;
  totalRepayment: number;
  disbursementDate: string;
  repaymentDate: string;
  status: string;
}

async function requestNanoLoan(
  data: NanoLoanRequest
): Promise<LoanResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/lending/nano-loans`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Salary Lending

```typescript
interface SalaryLoanRequest {
  customerId: string;
  employerId: string;          // Registered employer ID
  amount: number;              // In kobo
  tenor: number;               // Months
  phoneNumber: string;
  accountNumber: string;
  bankCode: string;
  transactionRef: string;
}

async function requestSalaryLoan(
  data: SalaryLoanRequest
): Promise<LoanResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/lending/salary-loans`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Value Financing

```typescript
interface ValueFinanceRequest {
  customerId: string;
  amount: number;              // Product/asset value in kobo
  downPayment: number;         // Down payment in kobo
  tenor: number;               // Months
  productDescription: string;
  merchantId: string;          // Vendor/merchant providing the product
  phoneNumber: string;
  transactionRef: string;
}

async function requestValueFinancing(
  data: ValueFinanceRequest
): Promise<LoanResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/lending/value-financing`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Loan Status & Repayment

```typescript
// Check loan status
async function getLoanStatus(loanId: string): Promise<LoanResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/lending/loans/${encodeURIComponent(loanId)}`,
    { method: 'GET', headers }
  );

  return response.json();
}

// Process repayment
interface RepaymentRequest {
  loanId: string;
  amount: number;             // Repayment amount in kobo
  transactionRef: string;
  paymentMethod: 'WALLET' | 'CARD' | 'BANK_TRANSFER';
}

async function processRepayment(
  data: RepaymentRequest
): Promise<{ responseCode: string; responseDescription: string }> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/lending/repayments`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Complete Nano Loan Flow

```typescript
// 1. Check eligibility
const eligibility = await checkLoanEligibility({
  customerId: 'CUST_001',
  phoneNumber: '+2348012345678',
});

if (!eligibility.eligible) {
  console.log('Not eligible:', eligibility.reasons);
  return;
}

console.log('Max amount:', eligibility.maxAmount / 100);
console.log('Available tenors:', eligibility.tenor);

// 2. Request loan
const loan = await requestNanoLoan({
  customerId: 'CUST_001',
  amount: 2000000,           // ₦20,000
  tenor: 30,                 // 30 days
  phoneNumber: '+2348012345678',
  disbursementAccount: {
    accountNumber: '0123456789',
    bankCode: '058',
  },
  transactionRef: `LOAN_${Date.now()}`,
});

console.log('Loan ID:', loan.loanId);
console.log('Repayment:', loan.totalRepayment / 100);
console.log('Due date:', loan.repaymentDate);

// 3. Check status later
const status = await getLoanStatus(loan.loanId);
console.log('Status:', status.status);

// 4. Process repayment
const repayment = await processRepayment({
  loanId: loan.loanId,
  amount: loan.totalRepayment,
  transactionRef: `REPAY_${Date.now()}`,
  paymentMethod: 'WALLET',
});

console.log('Repayment status:', repayment.responseCode);
```

## Best Practices

1. **Always check eligibility** before requesting a loan
2. **Display total repayment** clearly to customers (including interest)
3. **Implement repayment reminders** — Notify before due dates
4. **Track loan status** — Monitor disbursement and repayment states
5. **Comply with lending regulations** — CBN consumer credit guidelines apply
6. **Secure BVN data** — Handle as sensitive PII, encrypt at rest
