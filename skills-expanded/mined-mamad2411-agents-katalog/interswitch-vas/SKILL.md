---
name: interswitch-vas
description: >-
  Interswitch Value Added Services API — bills payment, airtime recharge, customer
  validation, virtual top-up, and e-pins. Use this skill whenever implementing bill
  payments (electricity, TV, internet), buying airtime or data, validating customer
  accounts for billers, issuing e-pins, or building VAS aggregation platforms. Also
  use when you see references to /api/v2/quickteller, billers, categoryId, paymentCode,
  customer validation, or airtime recharge endpoints.
---

# Interswitch Value Added Services API

Integrate bills payment, airtime recharge, customer validation, and e-pin services through the Quickteller Business platform.

## VAS Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v2/quickteller/categorys` | GET | List biller categories |
| `/api/v2/quickteller/categorys/{id}/billers` | GET | Get billers in category |
| `/api/v2/quickteller/billers/{id}/paymentitems` | GET | Get biller payment items |
| `/api/v2/quickteller/customers/validations` | POST | Validate customer |
| `/api/v2/quickteller/payments/advices` | POST | Send payment |
| `/api/v2/quickteller/payments/recharges` | POST | Airtime/data recharge |

## List Biller Categories

```typescript
interface BillerCategory {
  categoryId: string;
  categoryName: string;
  categoryDescription: string;
}

async function getBillerCategories(): Promise<BillerCategory[]> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v2/quickteller/categorys`,
    { method: 'GET', headers }
  );

  const data = await response.json();
  return data.categorys;
}
```

## Get Billers by Category

```typescript
interface Biller {
  billerId: string;
  billerName: string;
  customerField1: string;
  supportedPaymentTypes: string[];
}

async function getBillersByCategory(
  categoryId: string
): Promise<Biller[]> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v2/quickteller/categorys/${encodeURIComponent(categoryId)}/billers`,
    { method: 'GET', headers }
  );

  const data = await response.json();
  return data.billers;
}
```

## Get Payment Items

```typescript
interface PaymentItem {
  paymentItemId: string;
  paymentItemName: string;
  amount: number;
  paymentCode: string;
  isAmountFixed: boolean;
  itemCurrencySymbol: string;
}

async function getPaymentItems(
  billerId: string
): Promise<PaymentItem[]> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v2/quickteller/billers/${encodeURIComponent(billerId)}/paymentitems`,
    { method: 'GET', headers }
  );

  const data = await response.json();
  return data.paymentitems;
}
```

## Customer Validation

Validate customer details with a biller before making payment:

```typescript
interface CustomerValidationRequest {
  customers: {
    customerId: string;     // Customer's account/meter number
    paymentCode: string;    // From payment items
  }[];
}

interface CustomerValidationResponse {
  customers: {
    customerId: string;
    responseCode: string;
    fullName: string;
    amount?: number;
    amountType?: string;
    amountTypeDescription?: string;
  }[];
}

async function validateCustomer(
  data: CustomerValidationRequest
): Promise<CustomerValidationResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v2/quickteller/customers/validations`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Send Payment (Bill Payment)

```typescript
interface PaymentAdviceRequest {
  terminalId: string;
  paymentCode: string;        // From payment items
  customerId: string;         // Validated customer ID
  customerMobile: string;
  customerEmail: string;
  amount: number;             // In kobo
  requestReference: string;   // Unique reference
}

interface PaymentAdviceResponse {
  responseCode: string;
  responseCodeGrouping: string;
  transactionRef: string;
  rechargePIN?: string;
  miscData?: string;
}

async function sendPayment(
  data: PaymentAdviceRequest
): Promise<PaymentAdviceResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v2/quickteller/payments/advices`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Airtime Recharge

```typescript
interface RechargeRequest {
  terminalId: string;
  paymentCode: string;        // Network-specific payment code
  customerId: string;         // Phone number
  amount: number;             // In kobo
  requestReference: string;
}

async function rechargeAirtime(
  data: RechargeRequest
): Promise<PaymentAdviceResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v2/quickteller/payments/recharges`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Common Biller Categories

| Category | Typical Billers |
| --- | --- |
| Utilities | PHCN (Electricity), Water Corp |
| Cable TV | DSTV, GOTV, StarTimes |
| Internet | Spectranet, Smile, Swift |
| Airtime | MTN, Airtel, Glo, 9mobile |
| Education | WAEC, JAMB |
| Insurance | Various providers |
| Government | Tax, Levies |

## Complete Bill Payment Flow

```typescript
// 1. Get categories
const categories = await getBillerCategories();
const utilityCat = categories.find(c => c.categoryName.includes('Utility'));

// 2. Get billers in category
const billers = await getBillersByCategory(utilityCat!.categoryId);
const electricityBiller = billers.find(b => b.billerName.includes('PHCN'));

// 3. Get payment items
const items = await getPaymentItems(electricityBiller!.billerId);
const prepaidItem = items.find(i => i.paymentItemName.includes('Prepaid'));

// 4. Validate customer meter number
const validation = await validateCustomer({
  customers: [{
    customerId: '45678901234',  // Meter number
    paymentCode: prepaidItem!.paymentCode,
  }],
});

if (validation.customers[0].responseCode !== '00') {
  throw new Error('Customer validation failed');
}

console.log('Customer:', validation.customers[0].fullName);

// 5. Make payment
const payment = await sendPayment({
  terminalId: 'TERM001',
  paymentCode: prepaidItem!.paymentCode,
  customerId: '45678901234',
  customerMobile: '08012345678',
  customerEmail: 'customer@email.com',
  amount: 500000, // ₦5,000
  requestReference: `BILL_${Date.now()}_${crypto.randomUUID().slice(0, 8)}`,
});

console.log('Payment status:', payment.responseCode);
if (payment.rechargePIN) {
  console.log('Token/PIN:', payment.rechargePIN);
}
```

## Best Practices

1. **Always validate customers** before sending payments
2. **Check supported payment types** for each biller
3. **Handle fixed vs variable amounts** — Some billers have fixed amounts
4. **Store payment references** for requery and reconciliation
5. **Display customer name** for confirmation before payment
