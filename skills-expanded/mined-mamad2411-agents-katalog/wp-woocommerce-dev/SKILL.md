---
name: wp-woocommerce-dev
description: WooCommerce extension review for Codex. Use when reviewing HPOS compatibility, CRUD usage, payment gateway safety patterns, cart fragments, template overrides, Action Scheduler usage, and WooCommerce block integrations.
---

# Codex WooCommerce Development Review

## Purpose

Use this skill when Codex should review WooCommerce-specific code with attention to HPOS, CRUD APIs, payment gateways, template overrides, scheduling, and extension compatibility.

## Focus Areas

- HPOS compatibility declarations and CRUD-only order access
- Payment gateway and webhook safety patterns
- Template overrides and hook preservation
- Cart fragments, performance traps, and scheduling work
- WooCommerce Blocks and Store API integration
- Shipping methods, product types, and extension architecture

## Workflow

1. Detect the WooCommerce context: extension, gateway, shipping method, theme integration, or block integration.
2. Check HPOS and order access patterns first.
3. Review payment, webhook, template, and performance-sensitive flows.
4. Use the shared WooCommerce references only where deeper analysis is needed.
5. Report findings with severity, file references, impact, and WooCommerce-appropriate fixes.

## Reference Files

Load only the references you need from:

- `../../claude-skills/wp-woocommerce-dev/references/wc-extension-guide.md`
- `../../claude-skills/wp-woocommerce-dev/references/wc-template-guide.md`
- `../../claude-skills/wp-woocommerce-dev/references/wc-performance-guide.md`

## Output

- Group findings by severity
- Include file references and WooCommerce context
- Explain whether the issue affects HPOS, compatibility, security, or performance
- Recommend fixes that preserve WooCommerce hooks and supported APIs

