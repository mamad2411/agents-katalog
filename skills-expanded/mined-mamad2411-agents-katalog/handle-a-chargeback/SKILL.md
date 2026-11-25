---
name: handle-a-chargeback
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 30min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Review a chargeback and either accept it or submit evidence by the deadline.

## Preconditions

- You have access to the payment processor, store admin, and order records.
- A chargeback or dispute notice exists with a reason code and deadline.
- You know the business policy for contesting disputes.

## Steps

1. **Open the dispute.** Find the chargeback in the payment processor or store dispute center. → *Expect:* reason code, amount, deadline, and status are visible.
2. **Match the order.** Identify the order, payment, customer, fulfillment, refund, and communication records. → *Expect:* the disputed transaction is tied to one order.
3. **Assess the reason.** Determine whether the claim is fraud, not received, not as described, duplicate, canceled, or credit not processed. → *Expect:* evidence needs are clear.
4. **Decide response.** Choose to accept the chargeback or contest it based on policy, evidence strength, amount, and customer history. → *Expect:* the dispute has a documented strategy.
5. **Gather evidence.** Collect receipt, billing match, delivery proof, tracking, product description, refund policy, and customer messages. → *Expect:* evidence directly addresses the reason code.
6. **Prepare the response.** Write a brief factual statement and attach evidence in the required format. → *Expect:* the submission is complete and readable.
7. **Submit or accept before deadline.** ⚠️ *Irreversible:* before submitting or accepting, confirm amount, order, evidence, and policy because missed or accepted chargebacks usually cannot be reopened. → *Expect:* the processor shows submitted or accepted status.
8. **Record the outcome.** Note dispute status, deadline, expected decision date, and any order account action. → *Expect:* the business can track financial impact and follow-up.

## Decision points

- If evidence is weak or the order was clearly wrong → accept the chargeback and fix the root cause.
- If fraud is alleged but delivery proof exists → contest only with strong authorization and delivery evidence.
- If the customer is also asking support for a refund → coordinate before issuing duplicate credits.

## Failure modes & recovery

- **F1 Missed deadline:** detect the dispute is closed or expired → record the loss and improve alerts.
- **F2 Duplicate refund:** detect both refund and chargeback are active → contact processor or support lead before taking more money action.
- **F3 Irrelevant evidence:** detect evidence does not address the reason code → replace it with targeted proof before submission.

## Verification

The dispute record shows accepted or submitted status before the deadline, with order-linked evidence or a documented acceptance reason.

## Variations

- Digital goods: provide login, download, usage, IP, and terms acceptance evidence if allowed.
- Subscription dispute: include cancellation policy, renewal notices, and usage records.
- Marketplace order: follow the marketplace dispute portal rather than the payment processor directly.

## Safety & privacy

Medium risk because chargebacks involve money, identity, and payment data. Share only necessary evidence, redact unrelated personal data, and never include full card numbers.
