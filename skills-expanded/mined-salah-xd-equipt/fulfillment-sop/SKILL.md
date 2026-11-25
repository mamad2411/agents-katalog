---
name: fulfillment-sop
description: "Creates order fulfillment SOPs with picking, packing, shipping procedures, quality control checkpoints, and error handling. Use when standardizing your shipping operations."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Fulfillment SOP

## When to Use This Skill

Use this skill when you need to:
- Create standard operating procedures for order fulfillment
- Document picking, packing, and shipping workflows
- Establish quality control checkpoints to reduce shipping errors
- Train new team members or fulfill prep for outsourcing to a 3PL

**DO NOT** use this skill for warehouse layout design, inventory management systems, or shipping rate negotiations. This is for the order-to-shipment process documentation.

---

## Core Principle

EVERY ORDER SHOULD BE FULFILLED IDENTICALLY REGARDLESS OF WHO DOES IT — AN SOP ELIMINATES VARIATION AND ENSURES EVERY CUSTOMER GETS THE SAME EXPERIENCE.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Order volume** | "How many orders per day/week do you ship?" | 5-20/day |
| **Product types** | "What do you ship? (single SKU, multiple SKUs, fragile, heavy, custom)" | Multiple SKUs, standard shipping |
| **Fulfillment location** | "Where do you fulfill? (home, office, warehouse, 3PL)" | Home or small office |
| **Current process** | "Describe how you currently fulfill orders." | Ad hoc, no documentation |
| **Shipping carriers** | "Which carriers? (USPS, UPS, FedEx, DHL)" | USPS and UPS |
| **Packaging** | "Describe your packaging materials and options." | Standard boxes and poly mailers |
| **Special requirements** | "Any custom inserts, gift options, or special handling?" | Thank-you card insert |

**GATE: Confirm brief before documenting the SOP.**

---

## Phase 2: Map

### Fulfillment Workflow Steps

1. **Order received** — notification triggers the process
2. **Order review** — verify order details, flag anomalies
3. **Pick** — gather products from inventory
4. **Quality check** — inspect items before packing
5. **Pack** — assemble order with packaging and inserts
6. **Label** — generate and apply shipping label
7. **Ship** — hand off to carrier or schedule pickup
8. **Confirm** — mark as shipped, send tracking to customer
9. **Exception handling** — process for issues (out of stock, address errors, damaged items)

### Quality Control Checkpoints

| Checkpoint | When | What to Verify |
|-----------|------|----------------|
| Pick check | After picking | Correct SKU, correct quantity, no damage |
| Pack check | Before sealing | All items present, inserts included, correct box size |
| Label check | Before shipping | Correct address, correct shipping method, weight matches |

**GATE: Present the workflow map for approval before writing the detailed SOP.**

---

## Phase 3: Build

### Deliverables

**1. Complete Fulfillment SOP**
- Step-by-step procedures for each workflow stage
- Decision trees for exceptions and edge cases
- Photos or descriptions of correct packaging for each product type
- Time estimates per step (for capacity planning)

**2. Picking Guide**
- Inventory location map (where each SKU is stored)
- Pick list format and sorting logic
- Batch picking instructions (for multiple orders at once)
- Out-of-stock procedure

**3. Packing Guide**
- Box/mailer selection by product type and size
- Packing sequence (product → protection → inserts → seal)
- Void fill and protection guidelines by product fragility
- Insert checklist (thank-you card, care instructions, promo)

**4. Shipping and Labeling Guide**
- Label generation process per carrier
- Shipping method selection rules (by weight, destination, speed)
- International shipping requirements (customs forms, documentation)
- Carrier pickup schedule or drop-off locations

**5. Error Handling Procedures**
- Wrong item shipped: immediate replacement + prepaid return label
- Address undeliverable: contact customer within 24 hours
- Damaged in transit: file carrier claim + reship to customer
- Out of stock: notify customer, offer alternatives or estimated restock date

---

## Phase 4: Polish

### Training Checklist

- [ ] New team member reads full SOP
- [ ] Shadows experienced fulfiller for 5 orders
- [ ] Completes 5 orders independently with quality checks reviewed
- [ ] Signs off on SOP understanding

### Performance Metrics

Track weekly:
- Orders shipped per hour (efficiency)
- Error rate (wrong item, missing insert, wrong address)
- Average ship time (order placed to carrier scan)
- Customer complaints related to fulfillment

### SOP Review Schedule

- Monthly: review error log and update procedures for recurring issues
- Quarterly: full SOP review for accuracy and completeness
- On trigger: update immediately when products, packaging, or carriers change

---

## Example 1: Home-Based Fulfillment (10 orders/day)

**Daily workflow:** Download orders at 9am → batch pick all orders → quality check → pack with inserts → print labels → drop off at USPS by 3pm. One person handles the full process.

## Example 2: Small Warehouse (50 orders/day, 2 staff)

**Daily workflow:** Person A picks and quality checks. Person B packs, labels, and stages for carrier pickup at 4pm. Orders downloaded in batches every 2 hours. End-of-day reconciliation against order count.

---

## Anti-Patterns

- **No written process** — "Just do what I do" does not scale. When the founder is sick or on vacation, orders stop or go wrong.
- **Skipping quality checks** — saving 30 seconds per order by skipping checks costs 30 minutes per reshipped wrong order.
- **No exception procedures** — when something goes wrong (and it will), staff should not have to improvise. Document the plan for common problems.
- **Optimizing too early** — perfect the basic process before adding complexity. Batch picking for 5 orders/day is overhead, not optimization.
- **Ignoring packing consistency** — one order beautifully packed and the next thrown in a bag destroys brand consistency.

---

## Recovery

- **Errors keep happening at one step:** Add a second verification at that step or simplify the process. Errors cluster where procedures are unclear.
- **Volume exceeds capacity:** Calculate current orders-per-hour and identify the bottleneck step. Usually it is packing or label printing.
- **Transitioning to a 3PL:** This SOP becomes the handoff document. Share with the 3PL and verify they can match your quality standards.
- **Seasonal volume spikes:** Document a "surge mode" SOP with simplified procedures and temporary staff training guides.
