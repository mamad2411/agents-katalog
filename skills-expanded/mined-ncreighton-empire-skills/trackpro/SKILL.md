---
name: trackpro
description: "Automate supply chain visibility and tracking with real-time data aggregation, customizable workflows, and compliance reporting. Use when the user needs inventory tracking, shipment monitoring, supplier compliance, or supply chain analytics."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["TRACKPRO_API_KEY", "SLACK_WEBHOOK_URL", "GOOGLE_SHEETS_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📦"
    }
  }
---

# TrackPro: Automated Supply Chain Visibility & Tracking

## Overview

TrackPro is an enterprise-grade supply chain automation skill that transforms manual tracking into real-time visibility. Supply chain managers spend 30-40% of their time on data entry, manual status updates, and compliance reporting. TrackPro eliminates this friction by:

- **Automating data import** from ERP systems, shipping APIs (FedEx, UPS, DHL), and supplier portals
- **Providing real-time visibility** into shipments, inventory levels, and supplier performance
- **Generating compliance reports** automatically for regulatory requirements (FDA, ITAR, RoHS)
- **Triggering workflows** based on supply chain events (delays, quality issues, threshold breaches)

### Why It Matters

Supply chain disruptions cost companies an average of $250K per incident. Real-time visibility reduces incident response time by 60% and improves on-time delivery rates by 15-20%. TrackPro integrates with **Slack**, **Google Sheets**, **SAP**, **Oracle NetSuite**, **Shopify**, and major shipping carriers to create a unified tracking ecosystem.

---

## Quick Start

Try these example prompts immediately:

### Example 1: Track Active Shipments
```
Track all shipments in transit from our top 5 suppliers, 
show current location, ETA, and any delays. 
Alert me in Slack if any shipment is delayed by more than 2 hours.
```

### Example 2: Generate Weekly Compliance Report
```
Create a compliance report for the week showing:
- All shipments by supplier with certifications
- Quality issues or failed inspections
- Regulatory violations (if any)
- Supplier performance scores
Export to Google Sheets and email summary to compliance@company.com
```

### Example 3: Automated Inventory Threshold Alerts
```
Monitor inventory levels for SKU-2847 and SKU-3921.
If stock falls below 50 units, automatically:
1. Create a purchase order from backup supplier
2. Notify procurement team via Slack
3. Log event in Google Sheets
4. Escalate to manager if 2+ items hit critical levels
```

### Example 4: Supplier Performance Dashboard
```
Build a real-time dashboard showing:
- On-time delivery % by supplier (last 30 days)
- Average lead time vs. contracted lead time
- Quality defect rates
- Cost variance (actual vs. budgeted)
Refresh every 4 hours and alert if any supplier drops below 85% on-time delivery.
```

---

## Capabilities

### 1. **Automated Data Aggregation**
- **ERP Integration**: Connect to SAP, Oracle NetSuite, Microsoft Dynamics 365
- **Shipping APIs**: Real-time tracking from FedEx, UPS, DHL, Amazon Logistics
- **Supplier Portals**: Auto-import from EDI, custom APIs, or web scraping
- **Inventory Systems**: Sync with WMS (Warehouse Management System) platforms
- **Data Normalization**: Standardize formats across 50+ data sources

**Usage Example:**
```
Aggregate shipment data from FedEx API, Shopify inventory, 
and SAP purchase orders. Merge by tracking number and PO, 
dedup, and store in real-time database. Refresh every 30 minutes.
```

### 2. **Real-Time Tracking & Visibility**
- **GPS-Level Tracking**: Show shipment location on interactive map
- **Multi-leg Tracking**: Follow shipments across multiple carriers/handoffs
- **Predictive ETAs**: ML-powered arrival predictions accounting for traffic, weather
- **Status Notifications**: Automatic alerts for pickup, in-transit, customs, delivery
- **Exception Management**: Flag delays, damage, lost shipments, quality issues

**Usage Example:**
```
Show all shipments in-transit on a map. Highlight shipments 
that are 4+ hours behind schedule. Display customer name, 
tracking number, current location, ETA, and last update time.
```

### 3. **Customizable Workflows & Automation**
- **Event-Driven Actions**: Trigger workflows on shipment milestones, inventory changes, quality issues
- **Conditional Logic**: IF supplier_delay > 6_hours THEN escalate AND notify_customer
- **Multi-Step Automation**: Chain actions (create PO → notify supplier → log in system → update customer)
- **Approval Workflows**: Route exceptions to appropriate manager for review
- **Scheduled Reports**: Daily/weekly/monthly snapshots with trends and anomalies

**Usage Example:**
```
When a shipment is delayed by 4+ hours:
1. Create incident ticket in Jira
2. Notify customer via email with revised ETA
3. Alert procurement in Slack
4. Log to Google Sheets for root cause analysis
5. Trigger backup supplier evaluation
```

### 4. **Compliance & Regulatory Reporting**
- **Automated Audits**: Track certifications, inspections, compliance status
- **Regulatory Templates**: FDA, ITAR, RoHS, GDPR, ISO compliance reports
- **Document Management**: Store certificates, test reports, quality records
- **Audit Trails**: Complete chain of custody for regulated industries
- **Threshold Monitoring**: Alert on compliance violations or expiring certifications

**Usage Example:**
```
Generate ITAR compliance report showing all shipments to 
restricted countries, supplier security clearances, and 
export license status. Flag any missing certifications.
```

### 5. **Integration with Slack, Google Sheets, Email**
- **Slack Alerts**: Real-time notifications with rich formatting and action buttons
- **Google Sheets Export**: Automatic weekly/monthly data dumps for analysis
- **Email Reports**: Scheduled summaries to stakeholders
- **Webhook Support**: Send data to custom tools or dashboards
- **API Access**: Query TrackPro data programmatically

---

## Configuration

### Required Environment Variables

Set these in your `.env` file or ClawHub secrets manager:

```bash
# TrackPro Core
TRACKPRO_API_KEY=your_trackpro_api_key_here
TRACKPRO_WORKSPACE_ID=workspace_12345

# Shipping Carriers
FEDEX_API_KEY=your_fedex_key
UPS_API_KEY=your_ups_key
DHL_API_KEY=your_dhl_key

# ERP Systems (choose what you use)
SAP_API_KEY=your_sap_key
NETSUITE_API_KEY=your_netsuite_key
SHOPIFY_API_KEY=your_shopify_key

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
GOOGLE_SHEETS_API_KEY=your_google_api_key
SENDGRID_API_KEY=your_sendgrid_key

# Optional: Advanced Features
GOOGLE_MAPS_API_KEY=for_location_mapping
TWILIO_ACCOUNT_SID=for_sms_alerts
```

### Setup Instructions

1. **Create TrackPro Account**: Sign up at trackpro.io and generate API key
2. **Connect Data Sources**: Add credentials for your ERP, shipping carriers, and suppliers
3. **Set Slack Webhook**: Create incoming webhook in Slack workspace settings
4. **Enable Google Sheets**: Use Google Cloud Console to enable Sheets API and generate credentials
5. **Configure Workflows**: Define your custom automation rules (see Capabilities section)
6. **Test Integration**: Run a sample import to verify all connections

### Optional Configuration

```yaml
# Tracking refresh intervals (in minutes)
tracking_refresh_interval: 30
inventory_refresh_interval: 60
supplier_performance_refresh_interval: 1440  # daily

# Alert thresholds
delay_alert_threshold_hours: 4
inventory_critical_level: 50
quality_defect_rate_threshold: 0.02  # 2%

# Report schedules
daily_report_time: "06:00"  # 6 AM UTC
weekly_report_day: "monday"
monthly_report_day: "1"     # 1st of month

# Data retention (days)
tracking_data_retention: 90
audit_log_retention: 365
```

---

## Example Outputs

### Real-Time Shipment Tracking Report

```
📦 ACTIVE SHIPMENTS (Updated: 2024-01-15 14:32 UTC)

SHIPMENT 1: FDX-9847-2024
├─ Status: IN TRANSIT
├─ From: Shanghai Port → To: Los Angeles Port
├─ Current Location: Pacific Ocean (15.2°N, 142.8°E)
├─ Progress: 62% complete
├─ ETA: 2024-01-22 09:00 UTC (on schedule)
├─ Carrier: FedEx International
└─ Items: 500 units SKU-2847, 250 units SKU-3921

SHIPMENT 2: UPS-5632-2024
├─ Status: ⚠️ DELAYED
├─ From: Chicago Distribution Center → To: New York
├─ Current Location: Indianapolis, IN
├─ Progress: 45% complete
├─ ETA: 2024-01-16 18:00 UTC (6 hours behind schedule)
├─ Delay Reason: Weather-related traffic in Ohio
├─ Carrier: UPS Ground
└─ Items: 100 units SKU-1234

SHIPMENT 3: DHL-7891-2024
├─ Status: CUSTOMS CLEARANCE
├─ From: Mexico City → To: Houston
├─ Current Location: Customs Facility, Laredo, TX
├─ ETA: 2024-01-17 14:00 UTC
├─ Documents: Pending customs broker review
└─ Items: 750 units SKU-4456

⚠️ ALERTS:
• UPS-5632 is 6 hours delayed - Slack notification sent to #supply-chain
• DHL-7891 customs docs incomplete - Action required from procurement team
```

### Weekly Compliance Report (Google Sheets)

```
COMPLIANCE SUMMARY - Week of Jan 8-14, 2024

Total Shipments: 47
Compliant: 45 (95.7%)
Non-Compliant: 2 (4.3%)

By Supplier:
├─ Supplier A (12 shipments): 100% compliant ✓
├─ Supplier B (18 shipments): 94% compliant (1 missing cert)
├─ Supplier C (10 shipments): 90% compliant (2 quality issues)
└─ Supplier D (7 shipments): 100% compliant ✓

Issues Requiring Action:
1. Supplier B - Export License expires 2024-02-28 (45 days)
2. Supplier C - Quality defect rate 3.2% (threshold: 2%)
3. Shipment FDX-9847 - RoHS certification missing for 50 units

Recommendations:
• Renew Supplier B export license immediately
• Schedule quality audit with Supplier C
• Request RoHS cert from Supplier A for future shipments
```

### Supplier Performance Scorecard

```
SUPPLIER PERFORMANCE - January 2024

Supplier A:
├─ On-Time Delivery: 98.5% (target: 95%) ✓
├─ Lead Time: 12.3 days (contracted: 14 days) ✓
├─ Quality: 0.8% defect rate (threshold: 2%) ✓
├─ Cost Variance: -2.1% (under budget) ✓
└─ Overall Score: 4.8/5.0 (EXCELLENT)

Supplier B:
├─ On-Time Delivery: 87.2% (target: 95%) ⚠️
├─ Lead Time: 16.8 days (contracted: 14 days) ⚠️
├─ Quality: 1.9% defect rate (threshold: 2%) ✓
├─ Cost Variance: +5.3% (over budget) ⚠️
└─ Overall Score: 3.1/5.0 (NEEDS IMPROVEMENT)

Supplier C:
├─ On-Time Delivery: 92.1% (target: 95%)
├─ Lead Time: 13.5 days (contracted: 14 days) ✓
├─ Quality: 3.2% defect rate (threshold: 2%) ✗
├─ Cost Variance: +1.8% (slightly over)
└─ Overall Score: 2.8/5.0 (ACTION REQUIRED)
```

---

## Tips & Best Practices

### 1. **Optimize Data Import Frequency**
- **High-velocity items**: Refresh every 15-30 minutes (critical inventory)
- **Standard items**: Refresh hourly (regular stock)
- **Slow-moving items**: Refresh daily (low-priority SKUs)
- Use intelligent caching to avoid API rate limits

### 2. **Set Smart Alert Thresholds**
- Don't alert on every delay—set thresholds that matter (4+ hours, not 30 minutes)
- Use supplier-specific thresholds (critical supplier = 2-hour alert, others = 6-hour)
- Avoid alert fatigue: consolidate related alerts into single notifications

### 3. **Leverage Predictive ETAs**
- Machine learning improves ETA accuracy over time; trust it after 2-3 weeks of data
- Account for seasonality (holiday peaks, weather patterns) in your thresholds
- Use predictive delays to proactively notify customers before they ask

### 4. **Automate Supplier Communication**
- Send customers revised ETAs automatically when delays exceed 4 hours
- Use templated emails to maintain consistency
- Include tracking links so customers can self-serve

### 5. **Build Dashboards for Different Audiences**
- **Executive**: High-level KPIs (on-time %, cost variance, supplier scores)
- **Operations**: Real-time shipment status, exceptions, workload
- **Finance**: Cost variance, budget tracking, supplier invoices
- **Compliance**: Audit trails, certifications, regulatory status

### 6. **Schedule Reports at Off-Peak Hours**
- Run heavy exports during night hours to avoid impacting live tracking
- Stagger report generation (don't run all at once)
- Use incremental exports for large datasets

### 7. **Monitor Integration Health**
- Set up alerts for API failures or data sync delays
- Log all integration errors for troubleshooting
- Test failover to backup data sources quarterly

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **No Manual Shipping**: This skill tracks shipments; it does not physically ship items
- **No Price Negotiation**: Cannot automatically renegotiate supplier contracts or rates
- **No Inventory Procurement**: Will NOT place purchase orders without explicit user approval
- **No Customs Clearance**: Cannot clear customs or handle regulatory compliance filings (alerts only)
- **No Data Deletion**: All tracking data is immutable for audit compliance; cannot be deleted retroactively

### Security & Compliance Boundaries

- **API Keys**: Never logs or transmits API keys in plain text; uses encrypted storage
- **PII Protection**: Removes customer names/addresses from logs if configured
- **Data Residency**: Respects data residency requirements (GDPR, CCPA); does not export to unauthorized regions
- **Audit Trails**: Maintains complete audit logs for regulatory compliance; cannot be tampered with
- **Rate Limiting**: Respects carrier API rate limits; will queue requests if limits are exceeded

### Limitations

- **Real-time Accuracy**: Tracking data is updated every 15-60 minutes (not millisecond-level)
- **Carrier Coverage**: Only supports major carriers (FedEx, UPS, DHL, Amazon); local carriers may not be available
- **ERP Integration**: Requires API access; cannot work with systems that only offer EDI or manual uploads
- **Historical Data**: Only retains data for 90 days (configurable); older data is archived
- **Predictive Accuracy**: ETA predictions are 85-95