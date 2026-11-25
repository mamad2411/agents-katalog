---
name: erp-integration
description: "Integrate with enterprise resource planning systems including SAP S/4HANA, Oracle NetSuite, and Microsoft Dynamics 365. Covers procurement, supply chain, financials, and manufacturing data flows."
license: Apache 2.0
tags: ["erp", "sap", "netsuite", "dynamics-365", "enterprise", "supply-chain", "procurement"]
difficulty: advanced
time_to_master: "14-24 weeks"
version: "1.0.0"
---

# ERP Integration

## Overview

Enterprise Resource Planning (ERP) systems are the operational backbone of large organizations, managing financials, procurement, inventory, manufacturing, and HR. SAP, Oracle NetSuite, and Microsoft Dynamics 365 collectively serve 80%+ of the enterprise market. Integrating AI agents with ERP systems unlocks intelligent procurement, demand forecasting, and real-time operational visibility.

## When to Use This Skill

- Building connectors between AI agents and SAP/NetSuite/Dynamics 365
- Automating procurement workflows (purchase orders, vendor management)
- Implementing real-time inventory and supply chain visibility
- Creating financial consolidation and reporting integrations
- Designing data pipelines from ERP to data warehouses

## Core Concepts

### ERP Platform Comparison

| Platform | Market | API Style | Auth | Best For |
|----------|--------|-----------|------|----------|
| SAP S/4HANA | Enterprise | OData v4, REST | OAuth 2.0, X.509 | Manufacturing, logistics |
| Oracle NetSuite | Mid-market | SuiteTalk (SOAP), REST | Token-Based Auth | Growing companies |
| Dynamics 365 | Mid-enterprise | OData v4, REST | Azure AD OAuth | Microsoft ecosystem |

### Core ERP Modules

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Financials │   │ Procurement │   │Manufacturing│
│  (GL, AP,   │   │ (PO, Vendor,│   │ (BOM, Work  │
│   AR)       │   │  Sourcing)  │   │  Orders)    │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌────────────────────────────────────────────────┐
│            Shared Data Layer                    │
│  (Materials, Vendors, Customers, Cost Centers) │
└────────────────────────────────────────────────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Inventory  │   │   Supply    │   │    HR &     │
│  Management │   │   Chain     │   │   Payroll   │
└─────────────┘   └─────────────┘   └─────────────┘
```

### Integration Architecture

```
┌──────────┐     ┌──────────────┐     ┌───────────┐
│ AI Agent │────►│ Integration  │────►│   ERP     │
│ (MCP)    │     │  Layer       │     │  System   │
└──────────┘     │ (API Gateway)│     └───────────┘
                 │              │
                 │ • Auth mgmt  │
                 │ • Rate limit │
                 │ • Transform  │
                 │ • Caching    │
                 └──────────────┘
```

## Implementation Guide

### SAP S/4HANA OData API

```typescript
// Query purchase orders via OData
const purchaseOrders = await fetch(
  `${sapBaseUrl}/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder?` +
  new URLSearchParams({
    "$filter": `PurchaseOrderDate ge datetime'${startDate}' and PurchasingOrganization eq '1000'`,
    "$select": "PurchaseOrder,PurchaseOrderDate,Supplier,PurchaseOrderNetAmount,Currency",
    "$orderby": "PurchaseOrderDate desc",
    "$top": "20",
  }),
  {
    headers: {
      Authorization: `Bearer ${sapToken}`,
      Accept: "application/json",
    },
  }
);

// Create a purchase order
const newPO = await fetch(
  `${sapBaseUrl}/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder`,
  {
    method: "POST",
    headers: {
      Authorization: `Bearer ${sapToken}`,
      "Content-Type": "application/json",
      "X-CSRF-Token": csrfToken,
    },
    body: JSON.stringify({
      PurchaseOrderType: "NB",
      Supplier: "VENDOR001",
      PurchasingOrganization: "1000",
      PurchasingGroup: "001",
      CompanyCode: "1000",
      to_PurchaseOrderItem: [{
        PurchaseOrderItem: "10",
        Material: "MAT001",
        OrderQuantity: "100",
        PurchaseOrderQuantityUnit: "EA",
        NetPriceAmount: "25.00",
        NetPriceQuantity: "1",
      }],
    }),
  }
);
```

### Oracle NetSuite SuiteQL

```typescript
// Query with SuiteQL (SQL-like)
const query = `
  SELECT
    t.tranid AS po_number,
    t.trandate,
    e.companyname AS vendor,
    t.foreigntotal AS amount,
    t.status
  FROM transaction t
  JOIN entity e ON t.entity = e.id
  WHERE t.type = 'PurchOrd'
    AND t.trandate >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
  ORDER BY t.trandate DESC
  FETCH FIRST 20 ROWS ONLY
`;

const results = await fetch(`${nsBaseUrl}/services/rest/query/v1/suiteql`, {
  method: "POST",
  headers: {
    Authorization: nsAuthHeader,  // Token-Based Auth
    "Content-Type": "application/json",
    Prefer: "transient",
  },
  body: JSON.stringify({ q: query }),
});
```

### ERP MCP Server Pattern

```typescript
server.tool(
  "get_purchase_orders",
  "Query recent purchase orders with status and amounts",
  {
    status: z.enum(["open", "approved", "received", "closed", "all"]).default("open"),
    vendor: z.string().optional(),
    minAmount: z.number().optional(),
    limit: z.number().default(10),
  },
  async ({ status, vendor, minAmount, limit }) => {
    const orders = await erpClient.queryPurchaseOrders({
      status, vendor, minAmount, limit,
    });

    const totalValue = orders.reduce((sum, po) => sum + po.amount, 0);

    return {
      content: [{
        type: "text",
        text: `${orders.length} Purchase Orders (${status}) | Total: $${totalValue.toLocaleString()}\n\n` +
          orders.map(po =>
            `PO-${po.number} | ${po.vendor} | $${po.amount.toLocaleString()} | ${po.status} | ${po.date}`
          ).join("\n"),
      }],
    };
  }
);

server.tool(
  "check_inventory_levels",
  "Check inventory levels across warehouses for specific materials",
  {
    materialId: z.string().optional(),
    warehouse: z.string().optional(),
    belowReorderPoint: z.boolean().default(false),
  },
  async ({ materialId, warehouse, belowReorderPoint }) => {
    const inventory = await erpClient.getInventory({
      materialId, warehouse, belowReorderPoint,
    });

    return {
      content: [{
        type: "text",
        text: inventory.map(item =>
          `${item.material} | ${item.warehouse}: ${item.quantity} ${item.unit} ` +
          `(Reorder: ${item.reorderPoint}) ${item.quantity < item.reorderPoint ? "⚠️ LOW" : "✓"}`
        ).join("\n"),
      }],
    };
  }
);
```

## Common Integration Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Real-time sync** | Webhooks/events for immediate updates | Order status changes |
| **Batch ETL** | Scheduled bulk data extraction | Nightly financial sync |
| **Request-reply** | On-demand queries | AI agent asks for PO status |
| **Event-driven** | Publish events for downstream consumption | New PO triggers approval workflow |

## Best Practices

1. **Never bypass ERP business logic** — always use the API, not direct DB access
2. **Cache master data** — materials, vendors, and cost centers change infrequently
3. **Handle SAP CSRF tokens** — fetch token before each write operation
4. **Use batch APIs for bulk operations** — individual calls are rate-limited
5. **Map custom fields carefully** — ERP systems are heavily customized per organization
6. **Test in sandbox/QA** — ERP changes can cascade across modules

## Resources

- [SAP API Business Hub](https://api.sap.com/)
- [NetSuite REST API](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/)
- [Dynamics 365 Web API](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |
