---
name: purchase-order-tracker
description: Tracks every purchase order referenced in email — what has been ordered, from which supplier, at what price, whether it has been confirmed, shipped, delivered, or invoiced. Use when a procurement manager wants a real-time view of all active POs without checking a separate system. Triggers on "purchase order status", "PO tracker", "what orders are outstanding", "order status", "has my order been confirmed", "purchase orders".
metadata:
  version: 1.0.0
---

# Purchase Order Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all procurement email threads to find every purchase order referenced —
extracting the supplier, items ordered, value, confirmation status, expected
delivery date, and whether invoicing has been received — and returns a
structured PO status view.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since the budget cycle"). Default: the last 90 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [supplier_scope] — either "all" (default) or a specific supplier
     or category to focus on.
   - [supplier_clause] — derived. When [supplier_scope] is not "all",
     set to " for [supplier_scope]". When [supplier_scope] is "all",
     set to empty string.

2. Call search with:
   - query: purchase order PO order confirmation delivery invoice shipment
     dispatch expected arrival goods services
     (if [supplier_scope] is not "all", append the supplier or category to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all procurement and supplier email threads from [time_range][supplier_clause]. Find every purchase order referenced or implied — identify the supplier, what was ordered, the PO number if mentioned, the total value, the order date, whether the order was confirmed by the supplier, the expected delivery date, and whether delivery confirmation or an invoice has been received.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Purchase order tracker across all active procurement activity",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "purchase_orders": {
           "type": "array",
           "description": "List of every purchase order found in email",
           "items": {
             "type": "object",
             "description": "A single purchase order with full status tracking",
             "additionalProperties": false,
             "properties": {
               "supplier": {
                 "type": "string",
                 "description": "Name of the supplier the order was placed with"
               },
               "po_number": {
                 "type": "string",
                 "description": "Purchase order number or reference, empty string if not found"
               },
               "description": {
                 "type": "string",
                 "description": "Description of goods or services ordered"
               },
               "order_date": {
                 "type": "string",
                 "description": "ISO8601 date the order was placed"
               },
               "order_value": {
                 "type": "number",
                 "description": "Total value of the order, 0 if not found"
               },
               "currency": {
                 "type": "string",
                 "description": "Currency of the order value"
               },
               "status": {
                 "type": "string",
                 "description": "Current status of this purchase order",
                 "enum": [
                   "placed_awaiting_confirmation", "confirmed", "in_production",
                   "shipped", "partially_delivered", "delivered", "invoiced",
                   "paid", "cancelled", "disputed", "unknown"
                 ]
               },
               "expected_delivery_date": {
                 "type": "string",
                 "description": "ISO8601 expected delivery date, empty string if not confirmed"
               },
               "days_until_delivery": {
                 "type": "number",
                 "description": "Number of days until expected delivery, negative if overdue, -1 if unknown"
               },
               "invoice_received": {
                 "type": "boolean",
                 "description": "Whether an invoice for this order has been received in email"
               },
               "issues": {
                 "type": "array",
                 "description": "Any issues, discrepancies, or concerns raised about this order",
                 "items": {
                   "type": "string",
                   "description": "A single issue or concern with this order"
                 }
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended next step for this purchase order"
               }
             },
             "required": [
               "supplier", "po_number", "description", "order_date",
               "order_value", "currency", "status", "expected_delivery_date",
               "days_until_delivery", "invoice_received", "issues",
               "recommended_action"
             ]
           }
         },
         "awaiting_confirmation_count": {
           "type": "number",
           "description": "Number of orders placed but not yet confirmed by the supplier"
         },
         "overdue_delivery_count": {
           "type": "number",
           "description": "Number of orders past their expected delivery date"
         },
         "total_outstanding_value": {
           "type": "number",
           "description": "Total value of all orders that have not yet been delivered or invoiced"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of active PO status and most urgent items"
         }
       },
       "required": [
         "as_of", "purchase_orders", "awaiting_confirmation_count",
         "overdue_delivery_count", "total_outstanding_value", "summary"
       ]
     }
   }

4. Present overdue deliveries and unconfirmed orders first. Lead with
   overdue_delivery count and awaiting_confirmation count.

5. Ask: "Would you like me to draft a supplier chase email for any
   overdue or unconfirmed orders?"
