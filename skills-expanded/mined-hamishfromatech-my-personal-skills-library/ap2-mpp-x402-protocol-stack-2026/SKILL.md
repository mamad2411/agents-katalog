---
name: ap2-mpp-x402-protocol-stack-2026
description: Applies Inriver's August 31, 2026 protocol guide comparing AP2 (Google, authorization), MPP (Stripe+Tempo, settlement), and x402 (Coinbase, web-native charging) — the three functions are complementary, not competing: "a wrong specification travels through every protocol intact and comes out the other side as an authorized, settled, wrong transaction." Includes the standardization timeline (AP2 → FIDO Alliance April 2026; x402 Foundation under Linux Foundation July 14 2026 with 40 members; MPP as the youngest with no neutral body), the Visa-participates-in-all-three signal, and the merchant decision framework (who's buying / what your PSP supports / what you can defer). Use when [explaining the agent-payment protocol landscape to businesses, deciding which protocols affect a given merchant, briefing on standards-body governance of agent commerce, or composing a protocol stack design]. NOT for [protocol security analysis — use x402-free-riding-attack-surface — or escrow design — use agent-settlement-protocol-asp-2026].
---

# AP2, MPP, x402: Three Functions, One Purchase

## The separation of concerns

AI agents don't pay the way people do — no card form, no checkout, no "buy" click. Three open protocols now standardize the layer instead, and the core insight of the Inriver comparison is that **they solve different problems and are frequently misread as competitors**:

| Protocol | Function | Created by | Governance |
|---|---|---|---|
| **AP2** (Agent Payments Protocol) | **Authorization** — cryptographically proves the buyer approved the agent's transaction | Google (Sept 2025, 60+ partners) → donated to **FIDO Alliance April 28, 2026**; v0.2 adds "Human Not Present" purchases; Verifiable Intent co-developed with Mastercard | FIDO; two technical working groups (chairs incl. Google, OpenAI, CVS Health, Mastercard, Visa) |
| **MPP** (Machine Payments Protocol) | **Settlement** — how agents pay businesses over card and stablecoin rails | Stripe + Tempo (launched March 18, 2026, with Tempo mainnet) | Open standard, co-authored by Stripe/Tempo — **no neutral standards body** |
| **x402** | **Web-native charging** — payment embedded in the HTTP request via the long-dormant 402 status code | Coinbase → **x402 Foundation under Linux Foundation, operational July 14, 2026**, 40 members (premier: Visa, Mastercard, Amex, Stripe, Adyen, Fiserv, Google, AWS, Shopify, Cloudflare, Coinbase) | Linux Foundation |

The market-structure tell: **Visa participates in all three** (card specs contributed to MPP; premier x402 membership; AP2 working-group co-chair) — the same payment network hedging across all functions simultaneously. The specs also reference each other: AP2's docs include an x402 settlement integration guide; the Universal Commerce Protocol designates AP2 as its payment method.

## How one purchase traverses all of them

A contractor tells their AI assistant: "Reorder the 240V compressor motor we bought in March, under $300, by Friday."
1. The agent finds the product through the merchant's **MCP** server.
2. Confirms specifications and stock through **UCP** catalog capabilities.
3. Initiates checkout through the merchant's **ACP** endpoints.
4. Presents an **AP2** Intent Mandate proving pre-authorization within the price ceiling and deadline.
5. Payment settles over **MPP**.

Five protocols, one purchase, no human clicking anything — **and every layer trusted one input, none verified: the product record.** If that record is wrong, MCP serves it, UCP confirms it, ACP transacts on it, AP2 binds the buyer to it, and MPP settles it. The stack moves the data faithfully; it does not check it. That's the comparison's load-bearing warning: a wrong specification becomes an authorized, settled, wrong transaction — and at x402's machine speed and sub-cent cost, an agent transacting on bad data does so thousands of times before anyone notices.

## What each protocol ideal-for/use-case mapping says

- **AP2:** consumer purchases through AI assistants (UCP-designated payment method); "Human Not Present" autonomous buying within pre-authorized limits — the design answer to Visa's own research (58% of Americans comfortable with AI comparing prices; 38% with autonomous purchase; **60% unwilling to let an agent spend without prior approval** — mandates bridge exactly that gap).
- **MPP:** agent-to-business purchases at conventional transaction sizes (goods, services, software); Stripe merchants accept via the existing PaymentIntents API; rail-agnostic by design (fiat + stablecoins + Visa-contributed card specs).
- **x402:** high-frequency, sub-dollar machine-to-machine payments — per-request API access, data queries, compute.

## The merchant decision framework

Most brands don't choose a protocol — implementation falls to payment providers, AI platforms, and infrastructure vendors. Three questions determine which reach your business, and through which vendor:
1. **Who is buying from you?** Consumers via AI assistants → AP2 (bundled). Agents buying goods/services/software at conventional sizes → MPP. Machine-to-machine sub-dollar → x402.
2. **What does your payment provider already support?** Check your PSP, commerce platform, and card networks' shipped integrations.
3. **What can you defer?** Most of it — the protocols interoperate by design, so an early wrong bet is cheap to correct. What must be ready from day one is the input every protocol transacts on: **your product data.**

## The shifts already underway

- **Discovery compresses:** AI-source traffic to US retail sites +393% YoY (Q1 2026, Adobe, trillion-visit base); Gartner expects SEO/PPC to give way to agent-engine optimization — agents evaluate structured product data and return a shortlist; brands compete to be in it.
- **Transactions happen without shopping sessions:** AP2's Human-Not-Present support exists because buyers want delegation with boundaries; inside a mandate, **the product record is the entire customer experience** — no human sees a product page.
- **The layers standardize at different speeds:** payments went from vendor projects to two standards bodies inside a year; **product data has no standards body coming** — Adobe's content-visibility analysis found retail product pages average 66% readable to the AI models driving that traffic. Transaction infrastructure is built industry-wide; data readiness is built merchant by merchant.

## Honest caveats

- The source is a product-data platform's guide (Inriver) — the "product data is the unverified layer" thesis is its commercial thesis, though the protocol mechanics are documented accurately against primary sources.
- MPP mainnet was weeks old at launch coverage; adoption curves and the missing-neutral-body question are live risks.
- Adobe/Gartner/Visa figures are third-party research cited secondhand; the 66% readability average is a modeled estimate.
- The protocol set will keep multiplying (the guide's own prediction) — treat this as a snapshot of a still-forming stack.

## Pairs with

`x402-production-checklist` (the seller-side operational layer), `x402-free-riding-attack-surface` (the security layer the guide doesn't cover), `agent-settlement-protocol-asp-2026` (the commerce escrow layer above all three), `agentic-payment-protocol-convergence-2026`, `agent-economy-payment-protocols`, `agent-native-advertising-economics`, `ai-native-product-discovery` (the discovery-compression counterpart).

## A-Tech alignment

- **Open source:** all three are free open specifications; governance diversity (FIDO/Linux Foundation/vendor-led) is itself a lesson in standards strategy for open protocols.
- **Privacy:** AP2 mandates and Verifiable Intent create an auditable consent chain for agent purchases — a privacy-positive architecture worth highlighting; conversely, product-data readability pressure may push merchants toward richer machine-readable exposure of (sometimes sensitive) catalog data.
- **Financial freedom:** the merchant framework ("what can you defer: most of it") keeps small-business protocol adoption cheap; the data-readiness gap is a service opportunity for solo consultants.
- **Practical:** the five-layer purchase walkthrough, three-question framework, and the "wrong record travels through every layer" warning are a complete explainer kit — the clearest teaching sequence published for the agent-payment stack.