---
name: ecommerce-operations
description: Use when planning, reviewing, or improving ecommerce operations such as product listings, merchandising, conversion, promotions, order issue workflows, marketplace operations, inventory-facing summaries, customer FAQs, or store performance readouts. Prefer this Skill when the task needs SKU, offer, conversion, customer experience, operational risk, or marketplace-ready copy. Do not use for store admin actions, payments, inventory writes, or platform automation.
meta:
  version: 1
  display_name: 电商运营
---

# Ecommerce Operations

## Purpose

Improve ecommerce work by connecting product value, listing clarity, customer trust, promotions, operational constraints, and measurable conversion or retention outcomes.

## Use When

Use for:

- product listing copy
- merchandising and promotion planning
- marketplace listing review
- ecommerce FAQ or policy explanation
- order issue workflow drafts
- conversion improvement ideas
- store performance summaries

## Material Gate

Identify:

- product, audience, price, channel, SKU or category, and offer
- product facts, specifications, images, reviews, policy, inventory, and fulfillment constraints
- conversion goal, customer objections, and marketplace rules

Do not invent product specs, inventory, shipping promises, discounts, reviews, or compliance claims.

## Workflow

1. Clarify customer use case and buying objection.
2. Turn product facts into benefit-led listing structure.
3. Improve title, bullets, description, FAQ, and CTA when requested.
4. Identify trust signals, missing evidence, and risk claims.
5. Map promotion or merchandising idea to customer segment and metric.
6. Separate customer-facing copy from internal operations notes.
7. Use `html-report-builder` for ecommerce audit or performance reports.

## Checks

- Product claims match provided facts.
- Customer objections are answered.
- Shipping, returns, and discounts are not invented.
- Marketplace or policy constraints are respected when provided.
- Recommendations include measurement ideas.

## Outputs

- product listing draft
- listing critique
- promotion plan
- merchandising brief
- ecommerce FAQ
- order issue workflow
- store performance readout

## Boundary

This Skill owns ecommerce messaging, merchandising reasoning, operations framing, and customer experience review. It does not own store admin changes, payment actions, inventory updates, marketplace submission, legal approval, or ad buying.

It must not run shell, Python, Node, npm, curl, MCP, ecommerce platform, marketplace, payment, inventory, shipping, ads, package install, publish, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
