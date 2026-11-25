---
name: marketplace-trust
version: 1.0.0
min_mindforge_version: 10.2.0
status: stable
triggers: marketplace trust system, reputation scoring, fraud detection marketplace, dispute resolution workflow, escrow payment pattern, trust and safety, content moderation marketplace, seller verification, buyer protection, platform integrity, transaction dispute, marketplace fraud prevention
---

# Skill — Marketplace Trust

## When this skill activates
This skill activates when building reputation systems, fraud detection, dispute resolution workflows, escrow payment patterns, trust and safety mechanisms, content moderation, seller verification, buyer protection, or platform integrity features for marketplaces.

## Mandatory actions when this skill is active

### Before writing any code
1. Design reputation scoring system: aggregate trust signals (completion rate, average rating, response time, dispute rate, tenure, transaction volume), weight recent activity higher (exponential decay: last 30 days = 50%, 30-90 days = 30%, 90+ days = 20%), normalize to 0-100 scale, segment by buyer/seller roles (separate scores)
2. Model dispute resolution workflow: buyer opens dispute (order not received, item not as described, damaged) → seller responds within 48 hours → platform mediator reviews evidence (messages, photos, tracking) → decision rendered (refund, partial refund, favor seller) → appeal window (7 days) → final resolution → reputation impact recorded
3. Map escrow payment flow: buyer pays platform (funds held) → seller notified (order confirmed) → seller ships item → buyer receives and inspects (3-7 day review period) → buyer approves (funds released to seller) OR buyer disputes (funds held until resolution) → platform fee deducted (10-20%) → seller payout (ACH, wire, PayPal)

### During implementation
- Implement fraud detection with multi-signal analysis: velocity checks (too many orders in 1 hour, new account with high-value purchase), device fingerprinting (IP geolocation mismatch with shipping address, VPN detection), behavioral anomalies (first order is expensive electronics), content analysis (listing description contains phishing keywords), ML scoring (ensemble model: random forest + gradient boosting, threshold tuning for precision/recall)
- Build reputation system with decay and recovery: store transaction outcomes (completed, disputed, refunded), calculate rolling metrics (30-day completion rate, 90-day avg rating), apply penalty for disputes (temporary score reduction, recovers over 6 months with good behavior), prevent review manipulation (verified purchase only, rate limiting 1 review per transaction, detect suspicious patterns like coordinated 5-star reviews from new accounts)
- Design dispute resolution dashboard: queue disputes by age (SLA: respond within 24 hours), display conversation history with timestamps, attach evidence (photos, tracking numbers, payment receipts), automated suggestions (refund amount calculator based on depreciation, precedent from similar disputes), escalation to human moderator for complex cases, decision audit trail (who decided, when, rationale)
- Implement content moderation pipeline: user-generated content (listings, reviews, messages) → automated filters (profanity, prohibited items like weapons/drugs, spam detection via regex and ML) → flagged content queued for human review → moderator approves/rejects with reason → user notification (content removed, account warning, suspension on repeat violations) → appeal process
- Build seller verification with identity proofing: phone verification (SMS OTP), email verification (link click), government ID upload (passport, driver's license → OCR extraction, face matching via liveness check), business registration documents (tax ID, incorporation certificate → third-party verification API), bank account linking (micro-deposit verification)

### After implementation
- Validate reputation accuracy: measure correlation with actual outcomes (high-rated sellers have <2% dispute rate, low-rated >10%), test decay mechanism (old bad reviews eventually expire), verify manipulation resistance (fake review rings detected and removed), ensure fairness (new sellers can build reputation within 30 days with 10+ successful transactions)
- Test fraud detection effectiveness: simulate known fraud patterns (account takeover, credit card fraud, fake listings), measure detection rate (>95% of known fraud blocked), false positive rate (<1% of legit transactions flagged), detection latency (<1 second at transaction time), monitor feedback loop (fraud analysts label misses, retrain model monthly)
- Execute dispute resolution fairness audit: measure resolution time (median <72 hours), appeal rate (<5% of decisions), appeal overturn rate (10-15% indicates healthy calibration), sentiment analysis of user feedback (post-resolution satisfaction), detect bias (outcomes should not correlate with user demographics)

## Self-check before task completion
- [ ] Reputation scoring functional: aggregates trust signals (completion rate, rating, disputes), weights recent activity higher (exponential decay), normalized 0-100 score
- [ ] Fraud detection multi-signal: velocity checks, device fingerprinting, behavioral anomalies, content analysis, ML scoring with tuned threshold
- [ ] Dispute resolution workflow: buyer opens, seller responds (48h SLA), evidence review, decision rendered, appeal window (7 days), reputation impact
- [ ] Escrow payment implemented: funds held by platform, released on buyer approval or dispute resolution, seller payout with fee deduction
- [ ] Content moderation active: automated filters (profanity, prohibited items), human review queue, moderator actions (approve/reject/suspend), appeal process
- [ ] Seller verification robust: phone/email verification, government ID with OCR + liveness, business documents, bank account linking
- [ ] Fairness metrics tracked: resolution time <72h, appeal rate <5%, no bias in outcomes, new sellers can build reputation within 30 days
