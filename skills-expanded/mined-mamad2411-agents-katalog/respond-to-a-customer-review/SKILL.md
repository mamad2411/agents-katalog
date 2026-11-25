---
name: respond-to-a-customer-review
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Post a professional response to a customer review without exposing private customer information.

## Preconditions

- You have access to the review platform or business profile.
- You know the business response policy.
- You can verify whether the reviewer is a customer if needed.

## Steps

1. **Read the full review.** Note rating, issue, date, product or location, and tone. → *Expect:* the customer's main point is clear.
2. **Check internal context.** Look up the order or visit only if policy allows and access is needed. → *Expect:* you know whether a specific recovery path exists.
3. **Choose response type.** [BRANCH: positive | negative | inaccurate] thank, apologize and route to support, or correct facts briefly. → *Expect:* the response matches the review.
4. **Draft a public reply.** Keep it short, respectful, and free of private account or order details. → *Expect:* the reply can stand in public.
5. **Offer a support path.** For unresolved issues, invite the customer to contact an official support channel. → *Expect:* the customer has a next step outside the public thread.
6. **Post the response.** ⚠️ *Irreversible:* before posting, confirm tone, facts, and privacy because public replies may be screenshotted or indexed. → *Expect:* the reply appears under the review.
7. **Log follow-up if needed.** Create a support task for issues that require internal action. → *Expect:* public response and private resolution are connected.

## Decision points

- If the review includes threats, harassment, or prohibited content → report it through the platform instead of arguing.
- If the complaint is valid → acknowledge the experience and move resolution to support.
- If you cannot verify details → avoid saying the customer is wrong.

## Failure modes & recovery

- **F1 Privacy leak:** detect reply includes order, health, payment, or personal details → edit or remove the reply immediately if possible.
- **F2 Defensive tone:** detect the reply argues with the customer → replace it with a calm factual response.
- **F3 No follow-up:** detect a promised support action was not logged → create the task and assign an owner.

## Verification

The public response is posted, addresses the review's main point, contains no private data, and routes unresolved issues to an official support channel.

## Variations

- App store review: ask for diagnostic details through support rather than in the review.
- Marketplace product review: focus on product experience and policy-compliant support options.
- Local business review: include the location manager or store contact if approved.

## Safety & privacy

Low risk. Never disclose customer identity, order history, payment status, medical details, or internal notes in a public review response.
