---
name: amazon-shopping
description: Browse and purchase items on Amazon using a real browser. Use when shopping on Amazon, finding products, comparing options, or buying things online.
allowed-tools: Read, Bash
---

# Amazon Shopping — Browser-Driven Product Research & Purchase

## Goal
Take high-level directions on what you want to buy, do thorough research (reviews, comparisons, pricing), present a few product options, and then purchase the selected item. Drives a real Chrome browser via Chrome DevTools MCP.

## CRITICAL RULES
1. **NEVER place an order without explicit user approval.** Always stop before "Place your order" and confirm.
2. **NEVER store or log payment info, passwords, or personal details.**
3. **NEVER auto-fill payment methods** — let Amazon's saved defaults handle this.
4. **Always show the product, price, and quantity** before adding to cart.
5. **Always show the order total** (including tax/shipping) before final purchase.

## Inputs
- **What to buy**: High-level description (e.g., "a good USB-C hub with at least 3 ports")
- **Preferences**: Price range, brand preferences, Prime-only, minimum rating
- **Quantity**: How many (default: 1)

## Process

### 1. Open Amazon
```
mcp__chrome-devtools__new_page → url: "https://www.amazon.ca"
```

### 2. Check Login
Take a screenshot. Look for "Hello, [Name]" in nav. If not logged in, ask the user to log in manually — never type credentials.

### 3. Search & Research
Navigate to search results. For each promising product, check:
- Price and Prime eligibility
- Rating and review count
- Key specs matching the user's requirements
- Delivery estimate

**Prioritize Prime and Prime Today products.** Target delivery within 48 hours. Deprioritize or skip non-Prime listings unless they're clearly the best option with no Prime alternative.

Present the top 3-5 options in a comparison table in the chat, then open each finalist in its own browser tab so the user can review. The table must include:

| Product | Price | Rating | Delivery | Why Buy |
|---------|-------|--------|----------|---------|
| Name | $X.XX | ★ X.X (N reviews) | Prime Today / Tomorrow / Date | 1-2 sentence reason — what makes this the right pick, standout specs, value angle, or caveat |

**Always include clickable Amazon.ca links** for each product using the ASIN: `https://www.amazon.ca/dp/{ASIN}`. Extract the ASIN from the `data-asin` attribute on each search result element.

### 4. User Selects Product
Click into the selected product. Verify:
- Correct variant (size/color/model)
- Current price
- Stock availability

### 5. Add to Cart
Only after user confirms. Take screenshot of cart to verify.

### 6. Checkout
Show complete order summary:
- Items and quantities
- Subtotal, shipping, tax
- **Total price**
- Delivery date

### 7. MANDATORY — Get Purchase Approval
Ask: "Should I place this order for $X.XX total?"
**Only proceed if the user explicitly says yes.**

### 8. Place Order
Click "Place your order." Screenshot the confirmation. Share the order number.

## Tools
All interaction via Chrome DevTools MCP:
- `navigate_page`, `take_screenshot`, `click`, `type_text`
- `evaluate_script` for reading page data
- `fill` for search fields

## Notes
- Target: Amazon.ca (user is in Calgary, Canada)
- User has Prime
- Chrome profile at `~/.cache/chrome-devtools-mcp/chrome-profile` retains login
- Always take a screenshot after every major action to verify state
- No execution scripts — entirely browser-driven via MCP

## First-Run Setup

Before executing, check if the workspace has a `.gitignore` file. If it doesn't, assume the user is new to this skill. In that case:

1. Ask the user if this is their first time running this skill
2. If yes, walk them through how it works and what they need to configure/set up (API keys, env vars, dependencies, etc.)
3. Let them know that Nick wishes them the best!
