---
name: customer-support-kb
description: "Builds a complete customer support knowledge base with tiered FAQs, canned response templates, troubleshooting decision trees, and escalation protocols. Use when a user needs to systematize customer support, reduce response times, onboard support staff, or stop answering the same questions repeatedly."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Customer Support KB

## When to Use This Skill

Use this skill when you need to:
- Build a customer support knowledge base from scratch for your business
- Systematize answers to questions you keep getting asked over and over
- Onboard a VA, support hire, or team member who needs to handle customer inquiries
- Reduce your personal response time by creating self-service resources
- Create escalation rules so you only get pulled in when it truly requires you

**DO NOT** use this skill for creating marketing copy, sales FAQs, or public-facing help center content meant for SEO. This builds an internal operational support system.

## How It Works

EVERY SUPPORT RESPONSE MUST SOUND LIKE A REAL HUMAN WHO KNOWS THE BUSINESS — NEVER LIKE A BOT READING A SCRIPT.

---

### Phase 1: Gather — Collect Support Scenarios

Pull together every question, complaint, and support scenario the business handles.

1. **Ask the user for their business type and primary offering** (product, service, course, coaching, SaaS, etc.)
2. **Request their top 10-20 most common customer questions** — if they cannot list them, prompt with these categories:
   - Pre-purchase questions (pricing, features, how it works)
   - Account and access issues (login, password, billing)
   - Product or service problems (defects, bugs, delivery issues)
   - Refund and cancellation requests
   - How-to and usage questions
   - Complaints and negative feedback
3. **Ask for existing support material** — email threads, DM screenshots, help docs, Notion pages, or any files they have. Read them with `Read` or `Glob` if file paths are provided.
4. **Identify the support channels** they use (email, DM, live chat, phone, helpdesk tool)
5. **Ask about their current pain points** — what takes the most time, what gets escalated unnecessarily, what falls through the cracks

Present a summary back to the user:

```
## Support Landscape

**Business:** Handmade candle e-commerce store
**Channels:** Email, Instagram DM, Etsy messages
**Volume:** ~40 inquiries/week

**Top Issues Identified:**
1. "Where is my order?" — 35% of all inquiries
2. "Can I change/cancel my order?" — 15%
3. "This arrived damaged" — 12%
4. "Do you offer custom scents?" — 10%
5. "How do I use the subscription?" — 8%
6. "I want a refund" — 7%
7. "Wholesale inquiry" — 5%
8. "Other" — 8%

**Pain Points:**
- Owner personally answers every DM and email
- No templates — every response written from scratch
- Damaged item process is inconsistent
- No clear escalation rules for VA
```

**GATE: Do not proceed until the user confirms the support landscape is accurate and complete.**

---

### Phase 2: Organize — Tier the Issues

Sort every identified issue into one of four tiers based on complexity and who should handle it.

1. **Assign each issue to a tier:**

| Tier | What It Covers | Who Handles It | Target Response |
|------|---------------|----------------|-----------------|
| Tier 1 | Self-service / FAQ | Customer (no staff needed) | Instant |
| Tier 2 | Canned responses | VA or support staff | Under 2 hours |
| Tier 3 | Troubleshooting trees | Trained support staff | Under 24 hours |
| Tier 4 | Escalation | Business owner | Under 48 hours |

2. **Apply the 80/20 rule** — Tier 1 and Tier 2 should handle at least 80% of inquiries. If they do not, re-examine whether some Tier 3 issues can be simplified into Tier 2 templates.

3. **Present the tier map to the user:**

```
## Tier Map

### Tier 1 — Self-Service FAQ (customers answer themselves)
- Where is my order? → tracking page link
- What are your shipping times? → shipping policy
- Do you ship internationally? → shipping policy
- What is your return policy? → returns page

### Tier 2 — Canned Responses (VA sends with minor personalization)
- Can I change/cancel my order?
- Do you offer custom scents?
- How do I use the subscription?
- General product questions

### Tier 3 — Troubleshooting Trees (VA follows decision tree)
- Item arrived damaged → photo required → replace or refund flow
- Wrong item received → verify order → reship flow
- Subscription billing issue → check payment status → retry or cancel

### Tier 4 — Escalation to Owner
- Refund requests over $75
- Legal threats or chargebacks
- Wholesale/partnership inquiries
- Complaints posted publicly on social media
- Anything unresolved after 2 back-and-forth exchanges
```

**GATE: User must approve the tier assignments before writing begins.**

---

### Phase 3: Write — Create All KB Content

Build out the full content for each tier. Work through them in order.

#### Step 1: Write Tier 1 FAQ Entries

For each FAQ item, write:
- **Question** as the customer would phrase it (conversational, not formal)
- **Short answer** (1-3 sentences, direct)
- **Detailed answer** (if needed, with links or steps)

Format:

```markdown
### Where is my order?

**Quick answer:** You can track your order anytime using the tracking link in your shipping confirmation email.

**Details:** After you place an order, you will receive a confirmation email within 1 hour. Once your order ships (1-2 business days for in-stock items), you will get a second email with a tracking number and link. If you did not receive either email, check your spam folder first, then contact us at support@example.com.
```

Write 8-15 FAQ entries depending on the business. **Every answer must include a specific next step** — never end with "contact us" as the only option.

#### Step 2: Write Tier 2 Canned Response Templates

For each canned response, write:
- **Trigger** — the situation that calls for this template
- **Tone note** — one-line guidance (e.g., "warm and apologetic" or "friendly but firm")
- **Template** with `{variables}` for personalization points
- **When NOT to use** — edge cases where this template is wrong

Format:

```markdown
### Order Change/Cancellation Request

**Trigger:** Customer wants to modify or cancel an order that has not shipped yet.
**Tone:** Helpful, no friction — make it easy.

**Template:**
Hi {first_name},

Thanks for reaching out! I checked on your order #{order_number} and it has not shipped yet, so we can absolutely {change/cancel} it for you.

{If change: Here is what I have updated: [describe change]. Your new total is {amount}. Everything else stays the same.}

{If cancel: I have canceled the order and your refund of {amount} will hit your account within 3-5 business days.}

Let me know if there is anything else I can help with!

{sign_off}

**Do NOT use when:** Order has already shipped. Switch to the "Order Already Shipped" template instead.
```

Write 6-12 canned response templates. **Every template must include at least one personalization variable** — no fully generic copy-paste blocks.

#### Step 3: Write Tier 3 Troubleshooting Decision Trees

For each troubleshooting scenario, write a clear if/then decision tree that a support agent can follow without guessing.

Format:

```markdown
### Damaged Item Resolution

**Start here:** Customer reports a damaged or defective item.

1. Ask the customer to send 1-2 photos of the damage.
   - **If photos received and damage is confirmed** → go to step 2
   - **If photos are unclear** → reply: "Thanks for sending that. Could you take one more photo in good lighting showing the damaged area? That helps me get this resolved faster for you."
   - **If customer refuses to send photos** → go to step 4

2. Check the order value.
   - **If order value is under $50** → send replacement immediately, no return required. Use the "Free Replacement" template.
   - **If order value is $50-$150** → offer choice: replacement or full refund. Use the "Damage Resolution Options" template.
   - **If order value is over $150** → escalate to owner (Tier 4).

3. Process the resolution.
   - Log the issue in the support tracker with: order number, damage description, photo links, resolution chosen.
   - Send confirmation to the customer using the appropriate template.
   - Flag the supplier/production batch if this is the third damage report on the same product in 30 days.

4. No-photo exception.
   - If the customer is a repeat buyer (3+ orders) → trust them and offer replacement.
   - If the customer is a first-time buyer → explain that photos are needed for quality tracking and offer to help them take one. If they still refuse after one follow-up, escalate to owner.
```

Write 3-6 decision trees. **Every branch must end with a specific action** — no dead ends.

#### Step 4: Write Tier 4 Escalation Protocol

Define exactly when and how issues reach the business owner.

```markdown
## Escalation Protocol

### When to Escalate
- Refund requests exceeding {amount threshold set by user}
- Legal language, chargeback threats, or lawyer mentions
- Public complaints on social media or review platforms
- Customer requests to "speak to the owner/manager"
- Any issue unresolved after 2 exchanges between support and customer
- Wholesale, partnership, or media inquiries

### How to Escalate
1. Write a brief summary: customer name, order number (if applicable), issue, what has been tried so far.
2. Forward the full conversation thread — do not summarize the customer's words, include them verbatim.
3. Tag as URGENT if it involves: legal threats, public complaints, or orders over {high_value_threshold}.
4. Expected owner response time: 24 hours (URGENT: 4 hours).

### What to Tell the Customer
Use this template while escalating:

"Hi {first_name}, I want to make sure this gets the attention it deserves, so I have looped in {owner_name} who will personally follow up with you within {timeframe}. Thank you for your patience."

**NEVER** say "I am just the support person" or "I cannot help you with that." Always frame the escalation as getting them better/faster help.
```

**GATE: Present the complete draft of all four tiers to the user. Get approval or revision requests before delivering final files.**

---

### Phase 4: Deliver — Organize into Structured Files

Write the knowledge base to organized files the user can reference, share with staff, or load into a helpdesk tool.

1. **Create the directory structure:**

```
support-kb/
├── README.md                          # Overview, tier summary, quick reference
├── tier-1-faq/
│   └── faq.md                         # All FAQ entries
├── tier-2-templates/
│   └── canned-responses.md            # All response templates
├── tier-3-troubleshooting/
│   └── decision-trees.md              # All troubleshooting trees
├── tier-4-escalation/
│   └── escalation-protocol.md         # Escalation rules and templates
└── support-guide.md                   # Complete single-file version for quick onboarding
```

2. **Write the README.md** with:
   - Business name and support channel list
   - Tier summary table (copy from Phase 2)
   - Quick-reference links to each file
   - Last-updated date

3. **Write support-guide.md** as a single combined document containing all four tiers — this is the "hand this to a new hire on day one" file.

4. **Confirm all files written** and provide a summary:

```
## Knowledge Base Complete

**Files created:**
- support-kb/README.md — overview and quick reference
- support-kb/tier-1-faq/faq.md — 12 FAQ entries
- support-kb/tier-2-templates/canned-responses.md — 8 response templates
- support-kb/tier-3-troubleshooting/decision-trees.md — 4 decision trees
- support-kb/tier-4-escalation/escalation-protocol.md — escalation rules
- support-kb/support-guide.md — complete single-file onboarding guide

**Coverage:** Tier 1 + Tier 2 handle an estimated 82% of inquiries.
**Next step:** Review each file and customize the {variables} with your real business details.
```

---

## Concrete Example 1: E-Commerce Store (Handmade Candles)

**User says:** "I sell handmade candles on Etsy and my own Shopify store. I get about 40 messages a week and I answer every single one myself. I am hiring a VA next month and need a support system."

**Phase 1 output (excerpt):**
```
## Support Landscape

**Business:** Handmade soy candle shop (Etsy + Shopify)
**Channels:** Etsy messages, Shopify email, Instagram DM
**Volume:** ~40 inquiries/week

**Top Issues:**
1. Where is my order / tracking request — 35%
2. Order change or cancellation — 15%
3. Damaged item on arrival — 12%
4. Custom scent or bulk order questions — 10%
5. Subscription management — 8%
6. Refund requests — 7%
7. Wholesale inquiries — 5%
8. Candle care / burn time questions — 5%
9. Gift wrapping / special packaging — 3%
```

**Phase 4 output (excerpt from canned-responses.md):**
```markdown
### Custom Scent Inquiry

**Trigger:** Customer asks if you make custom scents or can modify an existing candle.
**Tone:** Enthusiastic but honest about what is possible.

Hi {first_name},

I love that you are interested in a custom scent! Here is how it works:

I offer custom blends for orders of 6 or more candles. You pick up to 3 fragrance notes from our scent menu (I will send you the link), and I blend a custom combination just for you. Turnaround is 7-10 business days since each batch is hand-poured.

For single candles, I am not able to do full custom blends, but I am happy to recommend the closest match from our current collection if you tell me what vibes you are going for.

Want me to send over the scent menu?

{sign_off}

**Do NOT use when:** Customer is asking about wholesale custom scents (50+ units). Escalate to owner.
```

---

## Concrete Example 2: SaaS / Online Coaching Business

**User says:** "I run an online coaching program with a membership site. Members pay monthly. My biggest headaches are login issues, people wanting to cancel, and questions about what is included in their tier."

**Phase 1 output (excerpt):**
```
## Support Landscape

**Business:** Online coaching membership (3 tiers: Starter, Pro, Elite)
**Channels:** Email (support@), in-app chat widget, Facebook group DMs
**Volume:** ~60 inquiries/week

**Top Issues:**
1. Cannot log in / password reset not working — 25%
2. What is included in my tier / upgrade questions — 20%
3. Cancellation and refund requests — 15%
4. Billing errors or double charges — 10%
5. How to access specific course module — 10%
6. Technical issues with video playback — 8%
7. Requests for 1-on-1 coaching (Elite only) — 7%
8. Community guidelines / reported posts — 5%
```

**Phase 3 output (excerpt from decision-trees.md):**
```markdown
### Login / Access Troubleshooting

**Start here:** Member reports they cannot log in or access content.

1. Ask which email address they are using to log in.
   - **If they provide an email** → check if it matches their membership email on file.
     - **Match found** → go to step 2
     - **No match** → reply: "It looks like your membership is under a different email. Try logging in with {correct_email}. If that does not work, let me know and I will sort it out."
   - **If they are unsure which email** → look up by name in the member database.
     - **Found** → provide their email (masked: j***n@gmail.com) and ask them to try again.
     - **Not found** → ask for the email used at purchase and check payment processor records.

2. Confirm their subscription status.
   - **Active** → send password reset link manually. Reply: "I just sent a fresh password reset to {email}. Check your inbox (and spam folder). The link expires in 1 hour."
   - **Expired/canceled** → reply: "It looks like your membership ended on {date}. Would you like to reactivate? I can send you a direct link."
   - **Payment failed** → reply: "Your last payment on {date} did not go through. Want to update your card on file? Here is the link: {billing_link}"

3. If password reset does not work after 2 attempts:
   - Clear their session manually in the admin panel.
   - Send a new temporary password via email.
   - **If still locked out** → escalate to owner with a note: "Possible platform-side issue, manual reset failed twice."
```

---

## Anti-Patterns

- **DO NOT** use robotic corporate language. Write "I am happy to help" not "Your inquiry has been received and will be processed accordingly." Customers can tell the difference.
- **DO NOT** create one-size-fits-all templates. A refund request from a loyal repeat customer and a refund request from a first-time buyer on day one require different tones and different policies. Build branching logic.
- **DO NOT** skip edge cases in decision trees. If a branch can happen, document it. Every "what if" a support agent might ask should have an answer in the tree.
- **DO NOT** bury the answer behind unnecessary pleasantries. The customer wants the answer first, then the warmth. Lead with the resolution: "Your refund has been processed" not "Thank you so much for reaching out to us today, we really appreciate your patience and understanding..."
- **DO NOT** write FAQ answers that just say "contact us." Every FAQ entry must attempt to answer the question directly. "Contact us" is only the fallback after the answer.
- **DO NOT** create templates with zero personalization variables. If a response could be sent to any customer without changing a single word, it will feel like spam.

---

## Recovery

- **User cannot identify their top questions:** Ask them to forward or paste their last 10-15 customer messages. Extract patterns from the raw conversations instead.
- **User has no existing support material:** Start from their product/service page and generate likely questions based on what a customer would need to know before buying, during delivery, and after using the product.
- **Decision tree gets too complex (more than 5 branches deep):** Split it into two separate trees. One tree should handle the common path, and a second tree handles the edge-case path.
- **User wants to support a channel not covered:** Ask for the channel's constraints (response length, formatting, whether attachments are supported) and adapt the templates accordingly.
- **If 3 attempts to gather requirements fail** (user is unsure, gives vague answers, or keeps changing scope): Stop and reassess. Suggest the user spend one week logging every customer inquiry in a simple spreadsheet before building the KB. Provide a logging template:

```
| Date | Channel | Customer Question (verbatim) | Category | Time to Resolve | Resolved By |
|------|---------|------------------------------|----------|-----------------|-------------|
```

This gives real data to build from instead of guessing.