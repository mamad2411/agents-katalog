---
name: tax-deduction-finder
description: Identifies commonly missed business tax deductions by industry and entity type with category lists and documentation requirements. Use this skill when a freelancer or small business owner is preparing for tax season, wants to reduce their tax bill, or needs to know what business expenses are deductible.
allowed-tools: Read Write Bash(ls)
---

# Tax Deduction Finder

## When to Use This Skill

- User is preparing for tax season and wants to maximize deductions
- User is a freelancer or solopreneur unsure what they can deduct
- User wants a checklist of commonly missed deductions for their industry
- User needs to know documentation requirements for specific deductions
- User recently started a business and does not know what qualifies as a business expense

## Core Principle

EVERY LEGITIMATE DEDUCTION MISSED IS MONEY LEFT ON THE TABLE — BUT EVERY UNSUPPORTED DEDUCTION IS AN AUDIT RISK. DOCUMENT EVERYTHING.

## Tax Disclaimer

**IMPORTANT: This skill provides general educational information about common business deductions. It does not constitute tax advice. Tax laws vary by jurisdiction, change frequently, and depend on individual circumstances. Always consult a qualified CPA or tax professional before claiming deductions. The information here is based on general US federal tax principles and may not apply to your specific situation.**

## Workflow

### Phase 1: Profile the Business

1. Determine the business type and entity structure:
   - Sole proprietor / Single-member LLC (Schedule C)
   - Partnership / Multi-member LLC (Form 1065)
   - S-Corporation (Form 1120-S)
   - C-Corporation (Form 1120)
2. Identify the industry/niche (freelancer, e-commerce, consultant, content creator, etc.)
3. Ask if the user works from home (home office deduction eligibility)
4. Ask if the user uses a personal vehicle for business

### Phase 2: Generate Deduction Checklist

5. Present the universal deduction checklist (applies to most businesses):

**Commonly Missed Deductions — Universal:**

| Category | Examples | Often Missed? |
|----------|----------|---------------|
| Home Office | Dedicated workspace, percentage of rent/mortgage, utilities, internet | YES — many skip this |
| Vehicle/Mileage | Business miles at IRS standard rate, parking, tolls | YES — fail to track miles |
| Health Insurance | Self-employed health insurance premium deduction (Schedule 1) | YES — sole proprietors miss this |
| Retirement Contributions | SEP-IRA, Solo 401(k), SIMPLE IRA | YES — huge tax savings ignored |
| Self-Employment Tax | Deduct 50% of SE tax on Schedule 1 | YES — automatic but often unknown |
| Professional Development | Courses, certifications, conferences, books related to business | YES |
| Software & Subscriptions | SaaS tools, design apps, project management, accounting software | Sometimes |
| Business Insurance | Liability, E&O, professional indemnity, cyber insurance | Sometimes |
| Professional Services | CPA fees, legal fees, bookkeeping, business coaching | Sometimes |
| Bank & Processing Fees | Stripe fees, PayPal fees, merchant account fees, business bank fees | YES |
| Marketing & Advertising | Ads, sponsorships, business cards, website hosting, domain names | Rarely missed |
| Office Supplies & Equipment | Computers, desks, chairs, printers (Section 179 for big items) | Sometimes |
| Travel | Business flights, hotels, 50% of business meals | Sometimes |
| Phone & Internet | Business percentage of personal phone/internet bill | YES |
| Startup Costs | Up to $5,000 in first-year startup expenses (if under $50K total) | YES |
| Bad Debt | Invoices you were unable to collect on | YES |
| Continuing Education | Courses and training that maintain or improve current skills | Sometimes |

6. Add industry-specific deductions based on the user's business type

### Phase 3: Industry-Specific Deductions

7. Present relevant additions:

**Content Creators (YouTube, Podcast, Social Media):**
- Camera, lighting, microphone, and audio equipment
- Editing software (Final Cut Pro, Adobe Premiere, Descript)
- Props, backgrounds, and set materials
- Studio or recording space (rent or home office portion)
- Thumbnail design tools or freelance designer fees
- Products purchased for review (if required for content)
- Music licensing fees (Epidemic Sound, Artlist)

**E-Commerce Sellers:**
- Cost of goods sold (materials, manufacturing, wholesale)
- Packaging and shipping supplies
- Product photography
- Inventory storage (warehouse, self-storage unit)
- Returns and refunds (adjusts revenue, not a deduction per se)
- Product samples
- Trade show and market booth fees

**Freelancers & Consultants:**
- Coworking space membership
- Client entertainment (50% of meals with documented business purpose)
- Portfolio website hosting and design
- Professional association memberships
- Certification and license renewal fees
- Gifts to clients (up to $25 per person per year)

**Coaches & Course Creators:**
- Course platform fees (Teachable, Kajabi, Thinkific)
- Webinar software (Zoom Pro, Crowdcast)
- Community platform costs (Circle, Slack paid plans)
- Student materials and workbooks
- Certification program costs (if required for coaching)

### Phase 4: Documentation Requirements

8. For each deduction category, specify what records to keep:

| Deduction | Required Documentation |
|-----------|----------------------|
| Home Office | Square footage of office vs. total home, lease/mortgage statements, utility bills |
| Vehicle/Mileage | Mileage log (date, destination, business purpose, miles), gas receipts if using actual expense method |
| Meals | Receipt + note of who attended and business purpose discussed |
| Travel | Itinerary, receipts, business purpose documentation |
| Equipment (>$2,500) | Purchase receipt, date placed in service, business use percentage |
| Professional Development | Course receipt, description of how it relates to current business |
| All expenses | Receipt or bank/credit card statement showing amount, date, and vendor |

9. **CRITICAL: Recommend the user keep receipts for a minimum of 3 years (IRS statute of limitations), ideally 7 years**

### Phase 5: Deliver

10. Output the personalized deduction checklist
11. Output documentation requirements
12. Provide estimated tax savings range if the user shares their tax bracket
13. Remind them to consult a CPA

## Example 1: Freelance Graphic Designer (Sole Proprietor)

**Profile:** Solo graphic designer, works from home, earns $85,000/year, uses personal car for client meetings, pays for own health insurance.

**Your Personalized Deduction Checklist:**

```
TAX DEDUCTION CHECKLIST
Business: Freelance Graphic Design (Schedule C)
Tax Year: 2025

COMMONLY MISSED (check these first):
[x] Home Office Deduction
    - Office: 150 sq ft of 1,200 sq ft apartment = 12.5%
    - Simplified method: $5/sq ft x 150 = $750
    - Regular method: 12.5% of rent ($1,800/mo x 12 = $21,600)
      = $2,700 + 12.5% of utilities
    - USE REGULAR METHOD: saves ~$1,950 more

[x] Self-Employed Health Insurance
    - Monthly premium: $420/mo = $5,040/year
    - Deducted on Schedule 1 (above-the-line, reduces AGI)
    - This is NOT an itemized deduction — it reduces taxable income directly

[x] Retirement: SEP-IRA Contribution
    - Can contribute up to 25% of net self-employment income
    - On $85,000 net income: up to ~$17,700
    - Deadline: tax filing deadline (including extensions)

[x] Vehicle Mileage
    - 2,400 business miles x $0.70/mile (2025 rate) = $1,680
    - Keep a mileage log app (MileIQ, Everlance, or manual)

[x] Self-Employment Tax Deduction
    - Automatic: deduct 50% of SE tax on Schedule 1
    - On $85K: SE tax ~$12,010, deduction = ~$6,005

[x] Phone & Internet (business percentage)
    - Phone: 60% business use x $85/mo x 12 = $612
    - Internet: 50% business use x $70/mo x 12 = $420

STANDARD DEDUCTIONS:
[x] Software: Adobe CC ($55/mo), Figma ($15/mo), Notion ($8/mo)
    = $936/year
[x] Hardware: MacBook Pro purchased March 2025 ($2,499)
    — Section 179: deduct full amount in year of purchase
[x] Professional development: Design conference ($800),
    online course ($297) = $1,097
[x] Marketing: Portfolio hosting ($200), domain ($15),
    LinkedIn Premium ($360) = $575
[x] Bank & processing fees: Stripe fees on invoices
    ~2.9% of $85,000 = $2,465
[x] Professional services: Bookkeeper ($150/mo x 12) = $1,800
[x] Office supplies: Paper, ink, external drive = ~$350

ESTIMATED TOTAL DEDUCTIONS: $41,329
AT 22% TAX BRACKET: ~$9,092 in federal tax savings
AT 15.3% SE TAX: additional ~$6,323 in SE tax savings
```

## Example 2: E-Commerce Candle Business (Single-Member LLC)

**Profile:** Handmade candle business, works from home studio, $48,000 revenue, attends 4 craft fairs per year.

**Your Personalized Deduction Checklist:**

```
TAX DEDUCTION CHECKLIST
Business: Ember & Sage Candle Co. (Schedule C / Single-Member LLC)
Tax Year: 2025

COMMONLY MISSED:
[x] Home Office (Studio Space)
    - Dedicated studio: 200 sq ft of 1,500 sq ft home = 13.3%
    - Regular method: 13.3% of mortgage interest, property tax,
      utilities, insurance, repairs
    - Estimated deduction: $3,200

[x] Startup Costs (if business started this year)
    - Can deduct up to $5,000 in startup costs immediately
    - Includes: market research, branding, initial inventory setup,
      legal fees for LLC formation

[x] Vehicle Mileage
    - Post office runs, supplier pickups, craft fair travel
    - Estimated 1,800 miles x $0.70 = $1,260

[x] Phone & Internet (40% business use)
    - $65/mo phone + $70/mo internet = $648/year

COST OF GOODS SOLD:
[x] Wax, fragrance oils, wicks, dyes = $8,400
[x] Jars, lids, labels = $3,200
[x] Packaging (boxes, tissue, stickers) = $1,400
[x] Shipping supplies = $1,100
    Total COGS: $14,100

OPERATING EXPENSES:
[x] Shopify subscription ($79/mo x 12) = $948
[x] Canva Pro ($13/mo x 12) = $156
[x] Email marketing (Mailchimp, $20/mo x 12) = $240
[x] Instagram/Facebook ads = $2,400
[x] Product photography session = $500
[x] Craft fair booth fees (4 x $200) = $800
[x] Craft fair travel (hotels, meals at 50%) = $1,100
[x] Product liability insurance = $500/year
[x] Business bank account fee ($10/mo x 12) = $120
[x] Payment processing fees (Stripe/Shopify ~2.9%) = $1,392
[x] LLC annual filing fee = $50
[x] Bookkeeper ($100/mo x 12) = $1,200

ESTIMATED TOTAL DEDUCTIONS: $29,564
ON $48,000 REVENUE: taxable income reduced to ~$18,436
```

## Recovery and Fallback

- If the user does not know their entity type, assume sole proprietor (Schedule C) unless they mention incorporating — this covers the majority of solopreneurs
- If the user is unsure whether something qualifies as a deduction, apply the "ordinary and necessary" test: Is it common in your industry? Is it helpful for your business? If both yes, it is likely deductible — but recommend confirming with a CPA
- If the user has no receipt for an expense, they can use bank or credit card statements as backup documentation — but original receipts are stronger
- If the user has not been tracking deductions all year, help them reconstruct from bank statements by categorizing the last 12 months of transactions

## Constraints

- **Always include the tax disclaimer** — this is educational, not tax advice
- Do not calculate exact tax liability — provide estimates as ranges and recommend a CPA for exact numbers
- Do not advise on audit defense strategies — that requires legal expertise
- Do not recommend aggressive or questionable deductions (100% personal vehicle as business, luxury items without clear business purpose)
- IRS mileage rates change annually — note that the user should verify the current rate
- Do not provide state-specific tax guidance — state deduction rules vary significantly
- Always recommend separating personal and business finances (dedicated business bank account)
- Retirement contribution limits change annually — recommend verifying current limits with the IRS or a CPA
