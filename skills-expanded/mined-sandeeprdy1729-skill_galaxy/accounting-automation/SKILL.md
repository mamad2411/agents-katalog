---
name: accounting-automation
description: "Automate accounting workflows using QuickBooks and Xero APIs. Covers invoicing, expense tracking, bank reconciliation, financial reporting, and AI-powered bookkeeping automation."
license: Apache 2.0
tags: ["accounting", "quickbooks", "xero", "invoicing", "bookkeeping", "fintech", "automation"]
difficulty: intermediate
time_to_master: "8-12 weeks"
version: "1.0.0"
---

# Accounting Automation

## Overview

QuickBooks (Intuit) and Xero dominate small-to-mid-market accounting with 10M+ combined customers. Their APIs enable AI agents to create invoices, categorize expenses, reconcile bank transactions, and generate financial reports — eliminating hours of manual bookkeeping. This skill covers both platforms' APIs and common automation patterns.

## When to Use This Skill

- Building MCP servers for automated bookkeeping
- Creating invoice generation and payment tracking workflows
- Automating expense categorization with AI
- Implementing bank reconciliation automation
- Generating financial reports (P&L, balance sheet, cash flow)
- Syncing accounting data with CRM or ERP systems

## Core Concepts

### Platform Comparison

| Feature | QuickBooks Online | Xero |
|---------|------------------|------|
| Market | US-dominant (80% SMB) | Strong in UK, AU, NZ |
| API Style | REST | REST |
| Auth | OAuth 2.0 | OAuth 2.0 |
| Webhooks | Yes | Yes |
| Sandbox | Yes (free) | Demo Company |
| Rate Limit | 500 req/min | 60 req/min |

### Core Accounting Objects

```
Chart of Accounts
  ├── Assets (bank accounts, receivables)
  ├── Liabilities (payables, loans)
  ├── Income (revenue accounts)
  ├── Expenses (cost categories)
  └── Equity (owner's equity)

Transactions
  ├── Invoices (money owed to you)
  ├── Bills (money you owe)
  ├── Payments (money received)
  ├── Expenses (money spent)
  ├── Journal Entries (manual adjustments)
  └── Bank Transactions (imported from bank)
```

## Implementation Guide

### QuickBooks Online API

```typescript
import OAuthClient from "intuit-oauth";

// Initialize OAuth client
const oauthClient = new OAuthClient({
  clientId: process.env.QBO_CLIENT_ID,
  clientSecret: process.env.QBO_CLIENT_SECRET,
  environment: "production", // or "sandbox"
  redirectUri: process.env.QBO_REDIRECT_URI,
});

// Create an invoice
async function createInvoice(customerId, lineItems) {
  const invoice = {
    CustomerRef: { value: customerId },
    Line: lineItems.map(item => ({
      DetailType: "SalesItemLineDetail",
      Amount: item.amount,
      SalesItemLineDetail: {
        ItemRef: { value: item.itemId },
        Qty: item.quantity,
        UnitPrice: item.unitPrice,
      },
    })),
    DueDate: new Date(Date.now() + 30 * 86400000).toISOString().split("T")[0],
  };

  const response = await qboClient.makeApiCall({
    url: `${baseUrl}/v3/company/${realmId}/invoice`,
    method: "POST",
    body: JSON.stringify(invoice),
  });

  return response.json.Invoice;
}

// Query invoices with SQL-like syntax
async function getOverdueInvoices() {
  const query = `SELECT * FROM Invoice WHERE DueDate < '${today}' AND Balance > '0'`;
  const response = await qboClient.makeApiCall({
    url: `${baseUrl}/v3/company/${realmId}/query?query=${encodeURIComponent(query)}`,
  });
  return response.json.QueryResponse.Invoice;
}
```

### Xero API

```typescript
import { XeroClient } from "xero-node";

const xero = new XeroClient({
  clientId: process.env.XERO_CLIENT_ID,
  clientSecret: process.env.XERO_CLIENT_SECRET,
  scopes: ["openid", "profile", "email", "accounting.transactions", "accounting.reports.read"],
});

// Create invoice in Xero
async function createXeroInvoice(contactId, items) {
  const invoice = {
    type: "ACCREC", // Accounts Receivable (sales invoice)
    contact: { contactID: contactId },
    lineItems: items.map(item => ({
      description: item.description,
      quantity: item.quantity,
      unitAmount: item.unitPrice,
      accountCode: "200", // Revenue account
      taxType: "OUTPUT2",
    })),
    date: new Date().toISOString().split("T")[0],
    dueDate: new Date(Date.now() + 30 * 86400000).toISOString().split("T")[0],
    status: "AUTHORISED",
  };

  const response = await xero.accountingApi.createInvoices(tenantId, { invoices: [invoice] });
  return response.body.invoices[0];
}

// Get Profit & Loss report
async function getProfitAndLoss(fromDate, toDate) {
  const report = await xero.accountingApi.getReportProfitAndLoss(
    tenantId, fromDate, toDate
  );
  return report.body.reports[0];
}
```

### Accounting MCP Server

```typescript
server.tool(
  "get_financial_summary",
  "Get a financial summary including revenue, expenses, and profit for a period",
  {
    period: z.enum(["this_month", "last_month", "this_quarter", "this_year"]),
    platform: z.enum(["quickbooks", "xero"]),
  },
  async ({ period, platform }) => {
    const { startDate, endDate } = resolvePeriod(period);
    const pnl = await getProfitAndLoss(platform, startDate, endDate);

    return {
      content: [{
        type: "text",
        text: `Financial Summary (${period}):\n` +
          `Revenue: $${pnl.totalIncome.toLocaleString()}\n` +
          `COGS: $${pnl.costOfSales.toLocaleString()}\n` +
          `Gross Profit: $${pnl.grossProfit.toLocaleString()} (${pnl.grossMargin.toFixed(1)}%)\n` +
          `Operating Expenses: $${pnl.totalExpenses.toLocaleString()}\n` +
          `Net Profit: $${pnl.netProfit.toLocaleString()} (${pnl.netMargin.toFixed(1)}%)\n`,
      }],
    };
  }
);

server.tool(
  "categorize_expenses",
  "Auto-categorize uncategorized bank transactions using AI",
  {
    limit: z.number().default(20),
  },
  async ({ limit }) => {
    const uncategorized = await getUncategorizedTransactions(limit);

    const categorized = uncategorized.map(txn => ({
      ...txn,
      suggestedCategory: categorizeTransaction(txn.description, txn.amount),
      confidence: calculateConfidence(txn),
    }));

    return {
      content: [{
        type: "text",
        text: `${categorized.length} transactions to categorize:\n\n` +
          categorized.map(t =>
            `${t.date} | ${t.description} | $${t.amount} → ${t.suggestedCategory} (${(t.confidence * 100).toFixed(0)}% confident)`
          ).join("\n"),
      }],
    };
  }
);
```

## Best Practices

1. **Use OAuth 2.0 with refresh tokens** — never store user passwords
2. **Sandbox first** — test all operations in sandbox before production
3. **Idempotent invoice creation** — use external IDs to prevent duplicates
4. **Respect rate limits** — QuickBooks: 500/min; Xero: 60/min
5. **Bank reconciliation should be human-approved** — AI suggests, human confirms
6. **Audit trail everything** — log every financial transaction modification
7. **Multi-currency handling** — always store and convert amounts explicitly

## Resources

- [QuickBooks Online API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [Xero API Documentation](https://developer.xero.com/documentation/api/accounting/overview)
- [Intuit Developer Portal](https://developer.intuit.com/)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |
