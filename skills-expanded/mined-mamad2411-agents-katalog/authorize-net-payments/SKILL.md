---
name: authorize-net-payments
description: Activate when implementing Authorize.net payment processing, tokenization, Accept.js integration, or posting payment results back to the POS tblPayment table. Covers the tokenization-only flow (no card data on our servers), the Accept.js web flow, and the React Native SDK mobile flow.
---

# Authorize.net Payments Skill

## Critical Rule: Tokenization Only

This project **never stores raw card numbers** on IMIDUS servers. The flow is:

1. Browser/app collects card details using Authorize.net's hosted UI (Accept.js / Accept In-App)
2. Authorize.net returns an **opaque token** (nonce)
3. Our backend charges the token via the Authorize.net API
4. Only the **last 4 digits + masked number** are stored in `tblPayment.CardNumber` (encrypted via `dbo.EncryptString`)

---

## Environment Variables (Never Hardcode)

```bash
AUTHNET_API_LOGIN_ID=...       # From Authorize.net merchant account
AUTHNET_TRANSACTION_KEY=...    # From Authorize.net merchant account
AUTHNET_CLIENT_KEY=...         # For Accept.js (public key)
AUTHNET_ENVIRONMENT=sandbox    # or "production"
```

Loaded in `appsettings.json`:

```json
"AuthorizeNet": {
  "ApiLoginId":     "",
  "TransactionKey": "",
  "ClientKey":      "",
  "Environment":    "sandbox"
}
```

---

## Backend: Charge a Payment Token

```csharp
// AuthorizeNetService.cs (IntegrationService.Infrastructure/Services/)
using AuthorizeNet.Api.Contracts.V1;
using AuthorizeNet.Api.Controllers;

public async Task<PaymentResult> ChargeTokenAsync(string nonce, decimal amount, string description)
{
    ApiOperationBase<ANetApiRequest, ANetApiResponse>.RunEnvironment =
        _config["AuthorizeNet:Environment"] == "production"
            ? AuthorizeNet.Environment.PRODUCTION
            : AuthorizeNet.Environment.SANDBOX;

    var merchantAuth = new merchantAuthenticationType
    {
        name           = _config["AuthorizeNet:ApiLoginId"],
        ItemElementName = ItemChoiceType.transactionKey,
        Item           = _config["AuthorizeNet:TransactionKey"]
    };

    var opaqueData = new opaqueDataType
    {
        dataDescriptor = "COMMON.ACCEPT.INAPP.PAYMENT",
        dataValue      = nonce
    };

    var paymentType = new paymentType { Item = opaqueData };

    var transactionRequest = new createTransactionRequest
    {
        merchantAuthentication = merchantAuth,
        transactionRequest     = new transactionRequestType
        {
            transactionType = transactionTypeEnum.authCaptureTransaction.ToString(),
            amount          = amount,
            payment         = paymentType,
            order           = new orderType { description = description }
        }
    };

    var controller = new createTransactionController(transactionRequest);
    controller.Execute();

    var response = controller.GetApiResponse();
    if (response?.messages.resultCode == messageTypeEnum.Ok)
    {
        var txn = response.transactionResponse;
        return new PaymentResult
        {
            Success       = true,
            TransactionId = txn.transId,
            AuthCode      = txn.authCode,
            LastFour      = txn.accountNumber?.Replace("XXXX", "").Trim(),
            CardType      = txn.accountType
        };
    }

    var error = response?.transactionResponse?.errors?.FirstOrDefault()?.errorText
             ?? response?.messages?.message?.FirstOrDefault()?.text
             ?? "Unknown error";
    return new PaymentResult { Success = false, ErrorMessage = error };
}
```

---

## Web Frontend: Accept.js Integration (Next.js)

```tsx
// components/checkout/PaymentForm.tsx
export function PaymentForm({ onToken }: { onToken: (nonce: string) => void }) {
  const handleSubmit = () => {
    window.Accept.dispatchData(
      {
        authData: {
          clientKey: process.env.NEXT_PUBLIC_AUTHNET_CLIENT_KEY!,
          apiLoginID: process.env.NEXT_PUBLIC_AUTHNET_API_LOGIN!,
        },
        cardData: {
          cardNumber: cardNumber.replace(/\s/g, ""),
          month: expMonth,
          year: expYear,
          cardCode: cvv,
        },
      },
      (response) => {
        if (response.messages.resultCode === "Ok") {
          onToken(response.opaqueData.dataValue);
        } else {
          setError(response.messages.message[0].text);
        }
      },
    );
  };

  return (
    <>
      {/* Load Accept.js — sandbox or production */}
      <Script src="https://jstest.authorize.net/v1/Accept.js" />
      {/* Card input fields */}
      {/* ... */}
    </>
  );
}
```

Required env vars in `.env.local`:

```
NEXT_PUBLIC_AUTHNET_CLIENT_KEY=...
NEXT_PUBLIC_AUTHNET_API_LOGIN=...
```

---

## Mobile: Accept In-App SDK (React Native)

```tsx
// screens/CheckoutScreen.tsx
import { AuthNet } from "react-native-authnet"; // or direct REST call

const handlePayment = async () => {
  const result = await AuthNet.getToken({
    apiLoginId: AUTHNET_API_LOGIN_ID,
    clientKey: AUTHNET_CLIENT_KEY,
    cardNumber: cardNumber,
    expirationMonth: month,
    expirationYear: year,
    cvv: cvv,
  });

  if (result.success) {
    await api.post("/orders", {
      ...orderData,
      paymentNonce: result.token,
    });
  }
};
```

---

## Posting Payment to POS (After Successful Charge)

After a successful Authorize.net charge, the backend inserts into `tblPayment`:

```csharp
var tender = new PosTender
{
    SalesID         = salesId,
    PaymentTypeID   = MapCardType(paymentResult.CardType), // 3=Visa,4=MC,5=Amex
    Amount          = chargeAmount,
    CardNumber      = $"XXXX{paymentResult.LastFour}",     // Encrypted by SQL: dbo.EncryptString()
    AuthCode        = paymentResult.AuthCode,
    RefNum          = paymentResult.TransactionId,
    PaymentDateTime = DateTime.UtcNow
};
await _posRepo.InsertPaymentAsync(tender, transaction);
```

The SQL insert uses `dbo.EncryptString(@CardNumber)` directly in the query — never pass the raw number to any other column.

---

## Verifone/Ingenico Bridge (Milestone 5 — BLOCKED)

The client will provide API docs for the in-store card reader bridge. When available:

- Consume bridge events from Verifone/Ingenico webhook/API
- Map results to same `PosTender` model
- Post to POS via same `InsertPaymentAsync` path
- Bridge integration UI goes in Admin Portal (Phase 15)

Do NOT implement this until client provides documentation.

---

## Error Handling

```csharp
// In OrdersController.cs
try
{
    var result = await _authNetService.ChargeTokenAsync(nonce, total, "IMIDUS Online Order");
    if (!result.Success)
        return BadRequest(new { error = result.ErrorMessage });

    // Continue with POS write steps...
}
catch (Exception ex)
{
    _logger.LogError(ex, "Payment failed for order {IdempotencyKey}", idempotencyKey);
    return StatusCode(500, new { error = "Payment processing failed" });
}
```

- Never expose Authorize.net error codes directly to the frontend
- Log the full error server-side, return a clean user message
- On payment failure, do NOT create the POS ticket — fail before Step 1
