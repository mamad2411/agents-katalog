---
name: supplychainvision
description: "Monitor and automate supply chain operations with real-time tracking, analytics dashboards, and customizable workflows. Use when the user needs supply chain visibility, inventory alerts, or shipment monitoring across multiple vendors and locations."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["SUPPLYCHAINVISION_API_KEY", "SLACK_WEBHOOK_URL", "GOOGLE_SHEETS_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📦"
    }
  }
---

## Overview

SupplyChainVision automates supply chain visibility and monitoring across your entire network of vendors, warehouses, and distribution centers. This skill transforms fragmented data sources into actionable insights, enabling real-time tracking, predictive analytics, and intelligent workflow automation.

**Why it matters:** Supply chain disruptions cost businesses an average of $184M annually. Manual tracking across spreadsheets, emails, and vendor portals creates blind spots, delays, and inefficiencies. SupplyChainVision consolidates this chaos into a single source of truth with automated alerts, custom rules, and seamless integrations with Slack, Google Sheets, Shopify, and enterprise ERP systems.

**Key integrations:** Slack (notifications), Google Sheets (data sync), Shopify (order tracking), SAP/NetSuite (ERP data), AWS S3 (document storage), Twilio (SMS alerts), Stripe (payment verification).

---

## Quick Start

Try these prompts immediately to see SupplyChainVision in action:

### Example 1: Real-Time Shipment Monitoring
```
Monitor all shipments in transit from our top 5 suppliers. 
Alert me on Slack if any shipment is delayed by more than 2 hours 
from the estimated delivery window. Include tracking number and 
current location in the alert.
```

### Example 2: Automated Inventory Reorder Rules
```
Create a workflow that automatically triggers a purchase order 
when inventory of SKU-4521 drops below 50 units. Email the 
procurement team and log the PO in Google Sheets with timestamp 
and supplier details.
```

### Example 3: Supply Chain Analytics Dashboard
```
Generate a weekly supply chain health report showing: on-time 
delivery rate by supplier, inventory turnover ratio, average 
lead time, and cost per unit. Include year-over-year comparison 
and flag any suppliers below 90% on-time performance.
```

### Example 4: Vendor Performance Scorecard
```
Analyze the last 90 days of shipments from our top 10 suppliers. 
Calculate quality score, delivery reliability, responsiveness, 
and cost competitiveness. Rank vendors and recommend which ones 
to consolidate or renegotiate with.
```

### Example 5: Automated Compliance Monitoring
```
Monitor all incoming shipments for customs documentation. 
Flag any international orders missing required certificates, 
invoices, or permits. Send automated follow-up emails to vendors 
with missing documents and escalate to compliance team if unresolved 
after 24 hours.
```

---

## Capabilities

### 1. Real-Time Supply Chain Tracking
- **Multi-carrier integration:** Automatically pull tracking data from FedEx, UPS, DHL, XPO, and 50+ carriers
- **Geolocation mapping:** Visualize shipment locations on interactive maps with ETA predictions
- **Delay detection:** Proactive alerts when shipments fall outside expected delivery windows
- **Exception management:** Automatic escalation workflows for lost, damaged, or held shipments

**Usage example:**
```
Track all POs with status="in_transit". If any shipment's 
ETA slips by >4 hours, create a Jira ticket for supply chain 
team and notify the downstream warehouse manager.
```

### 2. Inventory Analytics & Forecasting
- **Stock level monitoring:** Real-time visibility into inventory across all locations (warehouses, stores, 3PLs)
- **Demand forecasting:** Predictive algorithms using historical sales, seasonality, and market trends
- **Safety stock optimization:** Automatic calculation of reorder points to minimize stockouts while reducing carrying costs
- **ABC analysis:** Classify inventory by value and movement to optimize warehouse space and cash flow

**Usage example:**
```
Calculate optimal reorder points for all SKUs in Category A 
(high-value, fast-moving). Factor in 30-day lead time from 
China suppliers and 15% demand volatility. Generate POs 
automatically when stock hits reorder point.
```

### 3. Customizable Workflows & Rules Engine
- **If-then automation:** Define custom rules without coding (e.g., "If supplier response time > 4 hours, escalate to VP Procurement")
- **Multi-step workflows:** Chain actions together (detect issue → notify team → create ticket → log to database → send customer update)
- **Conditional branching:** Route decisions based on supplier tier, order value, product category, or geography
- **Scheduled triggers:** Run reports, audits, or reconciliations on daily/weekly/monthly cadence

**Usage example:**
```
IF supplier_rating < 85% AND order_value > $50,000 
THEN require_secondary_approval AND notify_CFO 
AND log_to_risk_register AND schedule_vendor_review_call
```

### 4. Vendor Performance Management
- **Scorecards:** Track on-time delivery %, quality (defect rate), responsiveness (email response time), and cost competitiveness
- **Trend analysis:** Identify improving vs. declining vendors over rolling 30/60/90-day windows
- **Benchmarking:** Compare vendor metrics against industry standards and peer suppliers
- **Automated reviews:** Schedule quarterly business reviews with performance data pre-populated

### 5. Cost Optimization & Spend Analysis
- **Landed cost tracking:** Calculate true cost per unit including freight, duties, tariffs, and handling
- **Spend consolidation:** Identify opportunities to consolidate volume with fewer suppliers for better rates
- **Contract compliance:** Monitor if suppliers are adhering to negotiated terms (pricing, MOQs, lead times)
- **Savings tracking:** Quantify cost reductions from process improvements and renegotiations

### 6. Integration Hub
- **ERP sync:** Two-way sync with SAP, NetSuite, Oracle for PO/receipt data
- **Slack notifications:** Customizable alerts for delays, exceptions, and threshold breaches
- **Google Sheets export:** Automatic weekly/monthly reports with charts and pivot tables
- **Webhook support:** Send supply chain events to custom systems or data warehouses
- **API access:** RESTful API for building custom dashboards and third-party integrations

---

## Configuration

### Required Environment Variables
```bash
# Core API credentials
SUPPLYCHAINVISION_API_KEY=your_api_key_here
SUPPLYCHAINVISION_WORKSPACE_ID=your_workspace_id

# Integration credentials
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
GOOGLE_SHEETS_API_KEY=your_google_sheets_api_key
SHOPIFY_API_TOKEN=your_shopify_token
SHOPIFY_STORE_URL=your-store.myshopify.com

# Optional integrations
SAP_API_ENDPOINT=https://your-sap-instance.com/api
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
```

### Setup Instructions

**Step 1: Authenticate**
```bash
# Initialize with your API key
supplychainvision auth --api-key $SUPPLYCHAINVISION_API_KEY
```

**Step 2: Connect Data Sources**
```bash
# Link your ERP or inventory system
supplychainvision connect --source shopify --token $SHOPIFY_API_TOKEN
supplychainvision connect --source google-sheets --spreadsheet-id ABC123XYZ
```

**Step 3: Configure Alerts**
```bash
# Set up Slack notifications
supplychainvision config alerts --channel #supply-chain --severity high,critical
```

**Step 4: Define Workflows**
```bash
# Create custom automation rules (via web UI or API)
supplychainvision workflow create --name "auto-reorder" --trigger inventory_low --action create_po
```

### Configuration Options
- **Alert thresholds:** Customizable delays (2h, 4h, 24h), inventory levels, cost variances
- **Reporting frequency:** Daily, weekly, monthly, or on-demand
- **Data retention:** 90 days (default) to 2 years (enterprise)
- **Timezone handling:** Automatic conversion for global operations
- **Currency support:** Multi-currency tracking with real-time FX rates

---

## Example Outputs

### Real-Time Alert (Slack)
```
🚨 SHIPMENT DELAYED
Tracking: 1Z999AA10123456784
Supplier: SunTrust Electronics (Tier 1)
Route: Shanghai → Los Angeles
Current Location: Pacific Ocean (145.2°E, 23.1°N)
Original ETA: 2024-01-15 14:00 PST
Updated ETA: 2024-01-16 08:00 PST (+18 hours)
Reason: Port congestion in LA
Action: PO-2024-001234 pushed to 2024-01-17
Customer Impact: 12 orders affected, notified
```

### Weekly Supply Chain Health Report
```
📊 SUPPLY CHAIN HEALTH REPORT
Week of Jan 8-14, 2024

DELIVERY PERFORMANCE
├─ On-Time Rate: 94.2% (↑2.1% vs last week)
├─ Average Lead Time: 18.3 days (↓0.5 days)
└─ Critical Delays: 3 (resolved same-day)

INVENTORY STATUS
├─ Total SKUs: 2,847
├─ Out of Stock: 12 (0.4%)
├─ Overstock (>180 days): 34 SKUs (flagged for clearance)
└─ Inventory Turnover: 8.2x annually

TOP VENDORS
1. SunTrust Electronics: 98% on-time, $847K spend
2. Pacific Logistics: 96% on-time, $623K spend
3. Global Parts Co: 91% on-time, $412K spend

COST ANALYSIS
├─ Total Spend: $2.1M (↓3.2% vs budget)
├─ Freight Cost: $187K (8.9% of spend)
├─ Savings Achieved: $42K (renegotiated rates)
└─ Projected Annual Savings: $504K

ALERTS & ACTIONS
⚠️ 2 vendors below 90% on-time threshold
🔄 8 POs at risk of delay (proactive action taken)
✅ Compliance: 100% (all certifications current)
```

### Vendor Scorecard
```
VENDOR PERFORMANCE SCORECARD (90-day rolling)

SunTrust Electronics
├─ On-Time Delivery: 98% (Target: 95%) ✅
├─ Quality (Defect Rate): 0.3% (Target: <1%) ✅
├─ Responsiveness (Avg Response Time): 2.1 hrs (Target: <4 hrs) ✅
├─ Cost Competitiveness: $12.45/unit (Market avg: $13.20) ✅
├─ Documentation Compliance: 100% ✅
└─ Overall Score: 98/100 (Tier 1 - Strategic Partner)

Pacific Logistics
├─ On-Time Delivery: 91% (Target: 95%) ⚠️
├─ Quality: 2.1% (Target: <1%) ❌
├─ Responsiveness: 5.3 hrs (Target: <4 hrs) ⚠️
├─ Cost Competitiveness: $14.10/unit (Market avg: $13.20) ⚠️
└─ Overall Score: 78/100 (Tier 2 - Renegotiate or Replace)
```

---

## Tips & Best Practices

### 1. Optimize Reorder Points
- Factor in supplier lead time variability (don't just use average)
- Account for seasonal demand spikes (e.g., +40% in Q4)
- Set separate thresholds for fast-moving vs. slow-moving SKUs
- Review and adjust quarterly based on actual performance data

### 2. Automate Exception Handling
- Define clear escalation paths: first alert → team manager → director → executive
- Use conditional logic to route issues (e.g., international delays → compliance team)
- Set time-based escalations (if unresolved after 4 hours, escalate)
- Log all exceptions for post-mortems and process improvement

### 3. Vendor Relationship Management
- Schedule quarterly business reviews with top suppliers using automated data
- Share performance scorecards transparently (builds trust and accountability)
- Recognize top performers with volume commitments or preferred pricing
- Create development plans for underperforming vendors before terminating

### 4. Data Quality & Hygiene
- Standardize supplier names, SKU codes, and location names across all systems
- Validate tracking numbers in real-time (catch data entry errors early)
- Reconcile inventory counts monthly against system records
- Audit PO-to-receipt matching weekly (catch missing receipts)

### 5. Forecasting Accuracy
- Incorporate external factors (weather, holidays, geopolitical events, competitor actions)
- Use ensemble methods (combine multiple forecasting models for better accuracy)
- Segment demand by customer type, geography, and product category
- Review forecast accuracy monthly and adjust models based on forecast errors

### 6. Cost Optimization
- Negotiate volume discounts based on 12-month forecast data
- Consolidate shipments to reduce freight costs (combine orders from same supplier)
- Explore alternative suppliers for high-spend categories
- Track landed cost (not just unit price) to make true apples-to-apples comparisons

---

## Safety & Guardrails

### What This Skill Will NOT Do

**SupplyChainVision respects these boundaries:**

1. **No unauthorized access:** Cannot access supplier systems, bank accounts, or confidential data without explicit API credentials and permissions
2. **No financial transactions:** Will not execute payments, initiate wire transfers, or modify financial records; only creates purchase orders for human approval
3. **No data retention beyond policy:** Automatically purges data according to your configured retention policy (90 days default); compliant with GDPR, CCPA, and data privacy laws
4. **No external data sharing:** Never sells, shares, or exports your supply chain data to third parties without explicit consent
5. **No override of business rules:** Workflows respect your configured approval thresholds; high-value or sensitive orders always require human review
6. **No predictive hiring/firing:** Cannot make vendor termination decisions; only provides performance data for human decision-makers
7. **No manipulation of supplier data:** Cannot alter PO quantities, pricing, or terms without explicit user action and audit trail
8. **No cross-company data mixing:** Maintains strict data isolation in multi-tenant environments; your data is yours alone

### Limitations

- **Tracking data lag:** Real-time tracking may have 15-30 minute delays from carrier systems
- **Forecast accuracy:** Predictions degrade during supply chain disruptions (pandemics, wars, natural disasters)
- **Carrier coverage:** Some regional carriers or specialized logistics (air charter, hazmat) may not be supported
- **Historical data:** Only processes data from connection date forward; cannot backfill historical data
- **API rate limits:** Enforces fair-use limits to prevent abuse (10,000 API calls/hour, 1M/month)

### Compliance & Auditing

- All actions logged with timestamp, user ID, and change details
- Audit trail immutable and retained per your data retention policy
- Supports SOC 2, ISO 27001, and HIPAA compliance requirements
- PII handling: Automatically masks sensitive data (SSN, credit card, passport numbers)
- Export compliance: Respects export controls for sanctioned countries

---

## Troubleshooting

### Common Issues & Solutions

**Issue: "Shipment tracking not updating"**
- **Cause:** Carrier API timeout or tracking number not yet in system
- **Solution:** 
  1. Verify tracking number format matches carrier requirements
  2. Wait 2-4 hours after shipment pickup (carriers need time to sync)
  3. Check if carrier is supported: `supplychainvision carriers list`
  4. Manually add tracking URL if auto-detection fails: `supplychainvision track --manual --url https://...`

**Issue: "Inventory alerts firing constantly"**
- **Cause:** Reorder point set too high or real-time sync lagging