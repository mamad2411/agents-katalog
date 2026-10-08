---
name: doordash-order
description: Order food via Doordash using browser automation
metadata:
  {
    "openclaw":
      {
        "requires": { "config": ["browser.enabled"] },
        "user-invocable": true,
        "emoji": "🍔"
      }
  }
---

# Doordash Order Skill

You can order food through Doordash using browser automation.

## Authentication

Uses the OpenClaw managed browser with a dedicated profile:

1. Open `doordash.com` in the browser
2. User logs in once (session and cookies are persisted)
3. Use browser automation to navigate and order

## Commands

### Order Food
Parse natural language to place orders:
- "Order me a burger from McDonald's"
- "Get pizza from Domino's"
- "I want tacos from Taco Bell"

### Specify Address
- "Order to my office"
- "Deliver to home"
- Use default address if not specified

### Check Order Status
- "Where's my order?"
- "Check my Doordash order"

## Order Flow

1. **Confirm Request**
   - Parse restaurant name and food items
   - Ask for clarification if items are ambiguous

2. **Search Restaurant**
   - Use browser to search for restaurant on Doordash
   - Verify restaurant is available in user's area

3. **Add Items**
   - Navigate menu to find requested items
   - Handle customizations if mentioned (e.g., "no onions", "extra cheese")
   - Add items to cart

4. **Review Order**
   - Show order summary to user
   - Confirm delivery address
   - Ask for explicit confirmation before placing

5. **Checkout**
   - Proceed to checkout
   - Select delivery address (default or specified)
   - Use saved payment method
   - Place order

6. **Confirm**
   - Report order confirmation number
   - Provide estimated delivery time

## Browser Automation Tips

- Use `browser snapshot` frequently to see page state
- Wait for page loads before acting
- Handle popups (location permission, promotions)
- Take screenshots if uncertain about page state

## Safety & Confirmation

- **Always** confirm order details before placing
- Show item names, quantities, and prices
- Display delivery address clearly
- Ask "Place this order?" before final submission

## Address Handling

- Default: User's default Doordash address
- Override: Parse address from chat context
- Always show delivery address before placing

## Error Handling

- Restaurant closed: Suggest alternatives
- Item unavailable: Ask for substitute
- Delivery unavailable: Inform user, suggest pickup
- Payment failed: Ask user to check Doordash app

## Important Notes

- Never place orders without explicit user confirmation
- Keep orders simple; ask for clarification on complex requests
- Report any issues immediately
- Provide order tracking link when available
