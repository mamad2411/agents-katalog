---
name: inventory-management
description: "Sets up inventory tracking systems with reorder points, supplier management, and stockout prevention for product-based businesses."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Inventory Management

## When to Use This Skill

Use this skill when you need to:
- Set up an inventory tracking system for a product-based business
- Calculate reorder points and safety stock levels
- Create supplier management frameworks with lead time tracking
- Build stockout prevention systems and demand forecasting templates

**DO NOT** use this skill for warehouse layout design, shipping logistics, or supply chain optimization at enterprise scale. This is for solopreneurs and small businesses managing product inventory.

---

## Core Principle

INVENTORY MANAGEMENT IS A CASH FLOW DECISION — TOO MUCH INVENTORY TIES UP CAPITAL, TOO LITTLE LOSES SALES. THE GOAL IS FINDING THE MINIMUM STOCK THAT PREVENTS STOCKOUTS.

---

## Phase 1: Inventory Assessment

Understand the current inventory situation before building a system.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product count** | "How many unique products/SKUs do you carry?" | Under 50 |
| **Sales volume** | "Roughly how many units do you sell per month?" | Varies |
| **Current tracking** | "How do you track inventory now? (spreadsheet, software, memory)" | Spreadsheet or none |
| **Supplier count** | "How many suppliers do you work with?" | 1-3 |
| **Lead times** | "How long from order to delivery for your main products?" | 2-4 weeks |
| **Storage** | "Where do you store inventory? (home, warehouse, 3PL, dropship)" | Home or small warehouse |

**GATE: Confirm assessment before designing the system.**

---

## Phase 2: System Design

Build the inventory tracking framework.

### Product Catalog Template

```
## Product Catalog

| SKU | Product Name | Category | Unit Cost | Sell Price | Margin | Supplier | Lead Time |
|-----|-------------|----------|-----------|------------|--------|----------|-----------|
| [SKU-001] | [Name] | [Category] | $[X] | $[X] | [X]% | [Name] | [X] days |
```

### Reorder Point Calculation

For each product, calculate the reorder point:

**Formula:** Reorder Point = (Average Daily Sales x Lead Time in Days) + Safety Stock

**Safety Stock:** Average Daily Sales x Safety Days (typically 7-14 days for solopreneurs)

```
## Reorder Points

| Product | Daily Sales | Lead Time | Safety Stock | Reorder Point | Reorder Qty |
|---------|------------|-----------|-------------|---------------|-------------|
| [Name] | 5 units | 14 days | 35 units | 105 units | 150 units |
```

### ABC Classification

Categorize products by revenue contribution:
- **A items (top 20% of products, ~80% of revenue):** Tight control, frequent counting, optimized reorder points
- **B items (next 30%, ~15% of revenue):** Moderate control, monthly review
- **C items (bottom 50%, ~5% of revenue):** Loose control, quarterly review, consider discontinuing low performers

**GATE: Present the system design for review.**

---

## Phase 3: Tracking Setup

Create the operational tracking templates.

### Inventory Tracker Template

```
## Inventory Tracker

| SKU | Product | On Hand | On Order | Reorder Point | Status | Last Counted |
|-----|---------|---------|----------|---------------|--------|-------------|
| [SKU] | [Name] | [qty] | [qty] | [qty] | OK / LOW / REORDER | [date] |
```

### Supplier Management

```
## Supplier Directory

| Supplier | Products | Lead Time | Min Order | Payment Terms | Contact | Reliability Score |
|----------|----------|-----------|-----------|--------------|---------|------------------|
| [Name] | [SKUs] | [days] | $[X] | [Net 30] | [email] | [1-5] |
```

### Stock Alert System

Define alert thresholds:
- **Green:** Stock above reorder point — no action needed
- **Yellow:** Stock within 20% of reorder point — place order soon
- **Red:** Stock at or below reorder point — order immediately
- **Critical:** Stockout — activate backup plan

---

## Phase 4: Prevention and Optimization

Deliver ongoing management frameworks.

### Monthly Inventory Review Checklist

```
- [ ] Count A-items and reconcile with tracker
- [ ] Review products approaching reorder points
- [ ] Check supplier lead times (have any changed?)
- [ ] Review slow-moving C-items for discontinuation
- [ ] Update demand forecasts based on last 30 days
- [ ] Review cash tied up in inventory
```

### Demand Forecasting (Simple)

Provide a basic forecasting approach:
- Use 3-month rolling average for stable products
- Apply seasonal multipliers for seasonal products
- Flag any product where actual sales deviate more than 30% from forecast

### Stockout Prevention Checklist

- Maintain backup supplier contacts for A-items
- Keep safety stock at minimum 7 days for bestsellers
- Set calendar reminders for reorders based on lead times
- Create a "what to sell when out of stock" list (alternatives, bundles, pre-orders)

---

## Anti-Patterns

- **Not tracking at all** — "I know what I have" stops working past 20 SKUs. Track everything.
- **Over-ordering to feel safe** — excess inventory is dead cash. Calculate reorder points, do not guess.
- **Single supplier dependency** — if your only supplier is delayed, you are out of business. Have backups for A-items.
- **Ignoring slow movers** — C-items that sit for 6+ months should be discounted, bundled, or discontinued.
- **Manual counting without schedule** — if you do not count regularly, your tracker becomes fiction.

---

## Recovery

- **User has no sales data:** Start with best estimates and refine after 30 days of tracking. Any estimate beats no system.
- **User is already experiencing stockouts:** Prioritize the top 5 revenue products. Calculate reorder points for those first, handle the rest later.
- **User has too many SKUs to track manually:** Recommend inventory management software (Sortly, inFlow, or Shopify inventory for e-commerce).
- **Supplier lead times are unpredictable:** Increase safety stock to 21 days and track actual lead times to find the real average.
- **User does dropshipping:** Adjust the framework — focus on supplier reliability monitoring rather than physical stock tracking.
