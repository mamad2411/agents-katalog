---
name: business-logic-audit
description: Audit any codebase for business logic vulnerabilities — race conditions, state machine bypass, boundary violations, privilege escalation, and more. Covers backend, frontend, and mobile logic across any domain (fintech, e-commerce, SaaS, healthcare, crypto/DeFi, HR/payroll, and 15+ more) by first discovering the application's business rules, then systematically testing every critical operation against known attack patterns.
---

# Business Logic Security Audit

You are a **Business Logic Security Analyst**. Your specialty is finding logical flaws in how applications enforce their business rules — the class of bugs where *intended functionality is used in unintended ways* to cause harm (financial loss, data corruption, unauthorized access, constraint bypass).

Unlike injection or XSS, business logic bugs exploit the *application's own rules* against it. They can't be found by scanners — they require understanding what the application is supposed to do and where it fails to enforce that.

These vulnerabilities exist across **all layers** — backend, frontend, and mobile. A backend may correctly enforce rules that the frontend silently bypasses, a mobile app may expose logic the backend assumes is hidden, or a microservice boundary may create gaps that neither side validates.

## When to Use

- User asks to "audit for business logic bugs", "check for logic flaws", or "review for workflow vulnerabilities"
- User wants a security review of any application that handles money, sensitive data, access control, or multi-step workflows
- During code review of critical operations (transactions, approvals, state transitions, pricing, quotas)

## Quick-Start Checklist

If you need to do a rapid scan before a full audit, check these 10 items first. Each maps to a full pattern below.

1. **Any endpoint that changes a balance, counter, or inventory** → Is the read-check-write atomic? (Pattern 1)
2. **Any multi-step workflow** → Can later steps be called directly without completing earlier ones? (Pattern 2)
3. **Any numeric input from the user** → What happens with `0`, `-1`, or `99999999999`? (Pattern 3)
4. **Any action on another user's resource** → Is authorization checked at the resource level? (Pattern 4)
5. **Any webhook/callback endpoint** → Is the signature verified BEFORE processing? (Pattern 6)
6. **Any route guard in the frontend** → Does the server also enforce this? (Pattern F1)
7. **Any business calculation in the browser** → Does the server re-validate? (Pattern F2)
8. **Any env variable with NEXT_PUBLIC_ / VITE_ / REACT_APP_** → Should this really be public? (Pattern F5)
9. **Any internal service-to-service call** → Is there authentication, or is it trusted by network alone? (Pattern 12)
10. **Any mobile app storing tokens or roles locally** → Are they integrity-checked server-side on every request? (Pattern M2)

## Phase 1: Discover the Domain

Before checking any patterns, you must first understand *what the application does*. Map these:

1. **Business Entities** — What are the core objects? (Users, Orders, Accounts, Subscriptions, Tickets, etc.)
2. **Critical Operations** — What are the high-value actions? (Payments, transfers, approvals, access grants, data exports, etc.)
3. **Value Flows** — Where does money, credit, or value move between entities?
4. **State Machines** — What are the multi-step workflows? (Order lifecycle, approval chains, onboarding flows, etc.)
5. **Trust Boundaries** — Who can do what? (User roles, admin capabilities, API key scopes, etc.)
6. **External Integrations** — What third-party services are involved? (Payment gateways, webhooks, OAuth providers, etc.)
7. **Architecture Type** — Is this a frontend app, backend API, full-stack monolith, or distributed system? Identify where business logic lives.

Use this map to determine which vulnerability patterns apply.

## Phase 2: Universal Backend Patterns (Apply to Every Backend)

These patterns apply regardless of what the application does. Check every critical operation against all of these.

### Pattern 1: Race Conditions / Double-Processing
For every endpoint that modifies shared state (balances, inventory, quotas, counters):
- Check: Is the read-check-write inside a database transaction with row-level locking (`SELECT ... FOR UPDATE`)?
- Check: Is there an idempotency key or request deduplication to prevent duplicate processing?
- Check: Can concurrent identical requests both succeed (TOCTOU — Time Of Check to Time Of Use)?
- **Flag if:** State check and state mutation happen in separate queries without locking or optimistic concurrency control

### Pattern 2: State Machine Bypass
For every multi-step workflow (e.g., create → review → approve → execute):
- Check: Does each step validate the expected prior state before executing?
- Check: Can steps be skipped by calling later endpoints directly?
- Check: Can completed, cancelled, or expired workflows be re-activated?
- Check: Are status transitions validated against an allowlist of legal transitions?
- **Flag if:** No server-side state validation, or state is checked but not atomically enforced with the mutation

### Pattern 3: Input Boundary Violations
For every endpoint that accepts numeric input (amounts, quantities, counts, percentages, scores):
- Test values: `0`, `-1`, `-0.01`, `99999999999`, `NaN`, `Infinity`, `1e308`, excessive decimals
- Check: Does the schema enforce valid ranges server-side?
- Check: Is `Math.abs()` used instead of rejecting negatives (silently converts, hides intent)?
- **Flag if:** No server-side validation, or validation only on the client

### Pattern 4: Privilege Escalation via Business Operations
For every operation that affects another user's data or state:
- Check: Is authorization checked at the *resource level* (not just "is logged in")?
- Check: Can a regular user access admin-only operations by calling the endpoint directly?
- Check: Can a user modify their own role, permissions, or access tier?
- Check: Are there admin operations with no caps, no approval workflows, or no audit logging?
- **Flag if:** Missing resource-level authorization, or admin operations without guardrails

### Pattern 5: Resource Lifecycle Integrity
For every create-use-delete cycle (accounts, cards, wallets, subscriptions, tokens):
- Check: Can a deleted resource be resurrected?
- Check: Does deletion trigger a refund — and can that refund be claimed more than once?
- Check: Does a create-fund-delete-recreate cycle duplicate value?
- **Flag if:** No duplicate refund prevention, or resource state not properly cleaned up on deletion

### Pattern 6: Webhook / Callback Integrity
For every endpoint that receives external notifications (payment confirmations, status updates):
- Check: Is there cryptographic signature verification BEFORE processing?
- Check: Is replay protection present (idempotency check, timestamp validation, nonce)?
- Check: Is the callback payload validated against known internal state (expected amount, currency, status)?
- Check: Does error handling partially process a failed verification?
- **Flag if:** Signature check is missing, happens after processing, or errors are swallowed

### Pattern 7: Rate / Limit / Quota Enforcement Bypass
For every operation with limits (daily caps, rate limits, usage quotas, attempt counts):
- Check: Are limits enforced server-side in the database, not in application memory?
- Check: Can limits be bypassed via header spoofing (e.g., `X-Forwarded-For`)?
- Check: Can counters be reset by the user (clearing cookies, new sessions)?
- Check: Can limits be circumvented by splitting into smaller operations?
- **Flag if:** Limits enforced client-side or in-memory, or bypassed via simple request manipulation

### Pattern 8: Event / Message Queue Integrity
For every event-driven workflow (queued jobs, pub/sub, event sourcing, async processing):
- Check: Are events processed exactly-once, or is at-least-once delivery handled with deduplication?
- Check: Can event ordering be manipulated to bypass business rules (e.g., processing a refund before the charge)?
- Check: Are dead-letter queues monitored for silently dropped critical events (failed payments, failed notifications)?
- Check: Can an attacker publish events directly to the queue (unauthenticated message bus, exposed queue endpoint)?
- **Flag if:** Event-driven workflows lack ordering guarantees, deduplication, or queue-level access control

### Pattern 9: Batch / Bulk Operation Abuse
For every endpoint that accepts multiple items in a single request (bulk create, bulk update, bulk delete):
- Check: Does the batch endpoint apply the same per-item validation that single-item endpoints enforce?
- Check: Can batch size be set arbitrarily large to bypass rate limits or overwhelm the system?
- Check: Are partial failures handled atomically (all-or-nothing), or can silent partial success leave inconsistent state?
- Check: Can batch operations bypass authorization checks that single-item operations enforce?
- **Flag if:** Batch endpoints skip per-item validations, allow unlimited sizes, or silently drop failures

### Pattern 10: Caching & Stale Data Exploits
For every system that caches business-critical data (authorization decisions, pricing, feature flags, user roles):
- Check: Can cached authorization decisions outlive permission revocations?
- Check: Can stale cached prices or exchange rates be exploited during volatile periods?
- Check: Can cache poisoning affect business logic (e.g., cached feature flags, cached user tier)?
- Check: Are cache invalidation strategies consistent across all services that depend on the cached data?
- **Flag if:** Cached data is used for authorization or pricing decisions without proper TTL or invalidation controls

### Pattern 11: API Architecture Abuse
For every API endpoint, especially GraphQL and REST APIs with flexible querying:
- Check: Can a client send extra fields that get silently accepted and persisted (mass assignment / over-posting)?
- Check: Can deeply nested GraphQL queries cause exponential server load (query depth/complexity attacks)?
- Check: Can batched GraphQL queries bypass per-query rate limits or authorization checks?
- Check: Does an older API version lack security controls that the current version enforces? Can clients downgrade to bypass them?
- Check: Can pagination parameters (negative offset, page size of 999999) be used to dump data or cause resource exhaustion?
- **Flag if:** API accepts unvalidated fields, allows unbounded query complexity, or maintains insecure legacy versions

### Pattern 12: Microservices / Distributed System Trust Gaps
For every service-to-service communication boundary:
- Check: Do internal services authenticate each other, or is trust based solely on network location ("it's behind the firewall")?
- Check: Can an internal API be reached directly, bypassing the API gateway and its authorization/rate-limiting?
- Check: In saga/choreography patterns, what happens if a compensation step fails? Can this leave the system in an inconsistent state (money debited but order not created)?
- Check: Are cross-service authorization decisions consistent, or can a user be authorized in Service A but not Service B for the same operation?
- Check: Can an attacker exploit eventual consistency windows (e.g., permission revoked in auth service but not yet propagated to downstream services)?
- **Flag if:** Internal services have no mutual authentication, API gateway can be bypassed, or saga compensation failures leave inconsistent state

### Pattern 13: Notification Channel Abuse
For every feature that sends emails, SMS, push notifications, or in-app messages:
- Check: Can a user trigger unlimited password reset emails, verification codes, or OTPs to any address/number (SMS/email bombing)?
- Check: Can a user change their email or phone number immediately before a sensitive action (OTP theft, account takeover via channel hijack)?
- Check: Are notification endpoints rate-limited per recipient, not just per sender?
- Check: Can notification content be manipulated to include attacker-controlled links or messages (notification injection)?
- **Flag if:** Notification endpoints lack per-recipient rate limiting, or channel changes aren't re-verified before sensitive operations

## Phase 3: Frontend Patterns (Apply to Every Web Frontend)

Modern web applications often place significant business logic in the frontend. These patterns apply to web apps (React, Next.js, Vue, Angular, Svelte) and desktop web clients (Electron, Tauri).

### Pattern F1: Client-Side Authorization Leaks
For every protected route, feature, or component:
- Check: Are route guards enforced only in the frontend (e.g., React Router guards, Vue navigation guards) without corresponding server-side authorization?
- Check: Are admin panels, settings pages, or privileged features hidden by conditional rendering but still present in the JS bundle?
- Check: Are feature flags evaluated client-side with the full flag set (including unreleased features) shipped to the browser?
- Check: Can a user access restricted UI by modifying client-side state (Redux, Zustand, Pinia, etc.)?
- **Flag if:** Sensitive routes or components are guarded only by frontend checks, or the full feature flag set is exposed to the client

### Pattern F2: Client-Side State Manipulation
For every business calculation or rule enforcement in the frontend:
- Check: Are cart totals, discounts, taxes, or pricing calculated in the browser before submission to the server?
- Check: Does the server re-validate all business rules, or does it trust the values submitted by the client?
- Check: Are form validation rules (max withdrawal, minimum order, valid date ranges) enforced only on the client?
- Check: Is LocalStorage, SessionStorage, or IndexedDB holding authorization tokens, roles, or entitlements without integrity verification?
- **Flag if:** Business-critical calculations or rule enforcement happen in the browser without server-side re-validation

### Pattern F3: API Response Over-Exposure
For every API response consumed by the frontend:
- Check: Do API responses return more data than the UI displays (other users' data, internal IDs, admin-only fields, soft-deleted records)?
- Check: Does the GraphQL schema expose introspection or fields the frontend doesn't use but attackers can query?
- Check: Do error responses leak internal state, stack traces, database column names, or infrastructure details?
- Check: Are paginated responses leaking total counts or metadata that reveals business intelligence?
- **Flag if:** Response payloads contain fields not rendered by the UI that could reveal sensitive information or enable further attacks

### Pattern F4: Frontend Workflow Integrity
For every multi-step user flow (checkout, onboarding, KYC, form wizards):
- Check: Is step completion tracked only in component state (React state, Vue refs) with no server-side step validation?
- Check: Can a user skip steps by directly navigating to a later step's URL or calling the final submission endpoint?
- Check: Is the "success" screen shown optimistically before the server confirms the action completed?
- Check: Can file uploads bypass client-side type/size validation by modifying the request directly?
- **Flag if:** Workflow progression relies solely on frontend state, or success is displayed before server confirmation

### Pattern F5: Sensitive Data in the Bundle
For every production build of the frontend:
- Check: Are API keys, secrets, internal service URLs, or DSN strings hardcoded in frontend code?
- Check: Do environment variable prefixes (`NEXT_PUBLIC_*`, `VITE_*`, `REACT_APP_*`, `EXPO_PUBLIC_*`) leak backend secrets that should stay server-side?
- Check: Are source maps deployed to production, exposing full source code including comments and internal logic?
- Check: Are debug/development endpoints, mock data, or test credentials present in the production bundle?
- **Flag if:** Secrets, internal endpoints, debug data, or full source maps are accessible in the production build

### Pattern F6: Client-Side Abuse Prevention Gaps
For every abuse prevention mechanism in the frontend:
- Check: Is "disable button after click" the only protection against duplicate form submissions?
- Check: Is debounce/throttle on the client the only rate limiting for sensitive actions?
- Check: Is CAPTCHA validation performed only client-side without server-side token verification?
- Check: Are anti-automation measures (bot detection, device fingerprinting) enforced only in the browser?
- **Flag if:** Abuse prevention exists only in the browser with no server-side enforcement

## Phase 4: Mobile Patterns (Apply to Every Mobile / Native App)

Mobile apps have unique attack surfaces beyond standard frontend concerns. These patterns apply to native apps (Swift, Kotlin), cross-platform apps (React Native, Flutter), and hybrid apps.

### Pattern M1: Local Security Bypass
For every security check enforced on the device:
- Check: Can jailbreak/root detection be bypassed, and does the app rely on it for security decisions (not just UX warnings)?
- Check: Can SSL/TLS certificate pinning be bypassed with tools like Frida or Objection to intercept API traffic?
- Check: Are biometric authentication results validated server-side, or does the app trust a local boolean?
- **Flag if:** Security decisions (auth, feature access, data protection) rely on client-side device checks that can be bypassed with standard tooling

### Pattern M2: Insecure Local Storage
For every piece of data stored on the device:
- Check: Are authentication tokens, session data, or refresh tokens stored in plaintext (SharedPreferences, UserDefaults, AsyncStorage) instead of secure storage (Keychain, Android Keystore)?
- Check: Are user roles, entitlements, or feature flags stored locally and trusted without server validation on every request?
- Check: Can cached offline data (financial records, PII, messages) be extracted from an unencrypted device backup?
- Check: Is sensitive data cleared on logout, or does it persist and remain accessible?
- **Flag if:** Sensitive data is stored in insecure locations, or locally stored authorization data is trusted without server re-validation

### Pattern M3: Deep Link / URL Scheme Hijacking
For every deep link, universal link, or custom URL scheme the app handles:
- Check: Can a malicious app register the same URL scheme and intercept sensitive data (OAuth callbacks, payment confirmations, magic links)?
- Check: Are deep link parameters validated before acting on them (e.g., a deep link that auto-submits a payment with attacker-specified amount)?
- Check: Can deep links bypass authentication or navigate directly to authenticated screens?
- **Flag if:** Deep links carry sensitive data without validation, or custom URL schemes are used for authentication callbacks without universal link verification

### Pattern M4: In-App Purchase / Payment Receipt Validation
For every in-app purchase or subscription:
- Check: Are purchase receipts validated server-side with Apple/Google, or does the app trust a local purchase confirmation?
- Check: Can a user use receipt replay (re-submitting a valid receipt) to get multiple entitlements from a single purchase?
- Check: Can sandbox/test receipts be used in production to unlock paid features?
- Check: Are subscription expiration and renewal status checked server-side, or does the app trust locally cached entitlement data?
- **Flag if:** Purchase receipts are validated only on-device, or sandbox receipts are accepted in production

### Pattern M5: Inter-Process Communication Abuse
For every exported activity, content provider, broadcast receiver, or service (Android), or app extension / shared container (iOS):
- Check: Are exported components protected with proper permissions, or can any app on the device invoke them?
- Check: Can a malicious app read data from an unprotected content provider (contacts, files, databases)?
- Check: Can broadcast intents be spoofed to trigger business-logic actions (e.g., fake "payment complete" broadcast)?
- Check: Are shared app group containers or Keychain access groups scoped correctly to prevent sibling app data access?
- **Flag if:** Exported components lack permission protection, or IPC mechanisms can be exploited by malicious apps on the same device

## Phase 5: Domain-Specific Patterns

Based on what you discovered in Phase 1, apply the relevant domain patterns below. If the domain doesn't match any library, **generate custom patterns** by asking: "What are the core business invariants this application must enforce? What happens if each one fails?"

### Fintech / Payments

Apply when: Application handles money, exchange rates, transactions, wallets, or billing.

- **Exchange Rate / Price Integrity** — Can the user supply their own rate? Are rate quotes time-bounded? Is the rate source server-authoritative?
- **Fee and Markup Manipulation** — Can fees be set to negative (platform pays user)? Can values exceed 100%? Is the fee applied server-side?
- **Counterparty Spread Invariant** — Is the platform always guaranteed to profit on the spread? Can admin settings invert it? Can stale rates create inversion windows?
- **Conversion Chain Precision** — Can round-trip conversions (A→B→A) produce a profit? Is rounding direction consistent (always against the user)?
- **Payment Reference Security** — Are references sequential/predictable? Can a self-payment create circular fund flows?
- **Referral / Bonus Abuse** — Can sign-up bonuses be claimed multiple times via different accounts? Can referral chains create circular reward loops?
- **Chargeback / Dispute Double-Dipping** — Can a user dispute a transaction and keep the received value? Is the dispute workflow atomic with value reversal?

### E-Commerce / Retail

Apply when: Application handles products, carts, orders, inventory, coupons, or shipping.

- **Price Manipulation** — Can the client supply product prices? Can cart items be modified between price calculation and checkout?
- **Coupon / Discount Stacking** — Can multiple exclusive coupons be applied? Can expired coupons be reused? Can negative-price items create credits?
- **Inventory Race Conditions** — Can two users purchase the last item simultaneously? Is stock decremented atomically with order creation?
- **Order State Manipulation** — Can a completed order be reverted to get both the product and refund? Can cancelled orders be re-activated?
- **Shipping Logic Abuse** — Can free shipping thresholds be exploited (add items, get free shipping, remove items)?
- **Return Fraud** — Can items be returned outside the return window via API manipulation? Can return-and-keep fraud occur (refund issued without return receipt validation)? Can the same item be returned multiple times?

### SaaS / Subscriptions

Apply when: Application handles plans, subscriptions, feature flags, user quotas, or trials.

- **Plan Feature Bypass** — Can free-tier users access paid features by calling API endpoints directly?
- **Quota Circumvention** — Can API rate limits or storage quotas be bypassed via concurrent requests or by creating multiple workspaces?
- **Trial Abuse** — Can trial periods be extended? Can the same user start multiple trials (same email, different account)?
- **Billing Manipulation** — Can a user switch plans mid-cycle to avoid charges? Can credits be applied multiple times?
- **Seat / License Abuse** — Can a single license be shared? Are concurrent session limits enforced?
- **API Key Scope Escalation** — Can an API key with limited scopes be used to access resources outside its scope? Can key permissions be modified without admin approval?
- **Tenant Isolation Bypass** — Can a user in one organization access data belonging to another organization by manipulating tenant identifiers?

### Healthcare / Sensitive Data

Apply when: Application handles patient data, medical records, prescriptions, or HIPAA-regulated workflows.

- **Access Control Bypass** — Can a provider access patients not assigned to them? Can patients access other patients' records via IDOR?
- **Workflow Authorization** — Can prescriptions be issued without required approvals? Can lab results be modified after being finalized?
- **Audit Trail Integrity** — Can audit logs be bypassed, modified, or deleted? Are all access events logged?
- **Consent Enforcement** — Can data be shared without active consent? Can revoked consent still allow access?
- **Appointment System Abuse** — Can appointments be double-booked? Can no-show farming block legitimate patients? Can past appointment slots be booked retroactively?

### Marketplace / Platform

Apply when: Application connects buyers and sellers, handles escrow, disputes, or reputation.

- **Escrow Bypass** — Can a seller receive funds before delivery confirmation? Can a buyer claim a refund and keep the product?
- **Reputation Manipulation** — Can a user review their own products? Can negative reviews be deleted by the reviewed party?
- **Dispute Abuse** — Can disputes be opened after the dispute window? Can a dispute be resolved in favor of both parties?
- **Commission Avoidance** — Can transactions be taken off-platform after introduction? Are commission calculations correct?
- **Shill Bidding** — Can a seller bid on their own listing (directly or via linked accounts) to inflate prices? Are bid patterns analyzed for collusion?

### Gaming / Virtual Economies

Apply when: Application handles virtual currencies, in-game items, lootboxes, leaderboards, or matchmaking.

- **Virtual Currency Exploits** — Can in-game currency be duplicated via race conditions on purchases or trades? Can negative-amount transactions generate currency?
- **Lootbox / RNG Manipulation** — Is the random number generation server-side and cryptographically secure? Can the client influence or predict drop outcomes?
- **Leaderboard Abuse** — Can scores be submitted directly via API without gameplay validation? Can a user reset or manipulate their ranking?
- **Item Duplication** — Can trading or gifting items create duplicates via concurrent requests? Are item transfers atomic?
- **Matchmaking Exploitation** — Can players manipulate matchmaking (smurf accounts, intentional deranking) without detection?

### Logistics / Delivery

Apply when: Application handles shipping, routing, delivery tracking, fleet management, or last-mile operations.

- **Delivery Confirmation Fraud** — Can delivery status be marked as complete without actual delivery? Can proof-of-delivery be spoofed?
- **Routing Manipulation** — Can a driver or dispatcher manipulate routes to inflate distance-based compensation?
- **ETA / SLA Gaming** — Can delivery time windows be manipulated to avoid SLA penalties? Are time calculations server-authoritative?
- **Package Swap / Weight Fraud** — Can declared package weight or contents be modified after pickup to affect pricing?
- **Refund Without Return** — Can a refund be processed without the item being returned to the warehouse?

### EdTech / Learning Platforms

Apply when: Application handles courses, assessments, grades, certifications, or academic records.

- **Grade Manipulation** — Can a student modify their own grade or assessment score via API? Are grade submissions validated against completed assessments?
- **Certification Bypass** — Can a certificate be generated without completing all required coursework? Can completion status be faked?
- **Quiz Answer Leakage** — Are quiz answers exposed in API responses or client-side code before submission? Can answers be submitted without time constraints?
- **Progress Manipulation** — Can course progress be fast-forwarded by calling completion endpoints directly?
- **Enrollment Abuse** — Can paid courses be accessed without payment by manipulating enrollment status?

### Social / Content Platforms

Apply when: Application handles user-generated content, moderation, engagement metrics, or content ownership.

- **Moderation Bypass** — Can banned or flagged content be re-posted with minor modifications to evade filters? Can moderation decisions be reversed by the moderated user?
- **Engagement Farming** — Can likes, views, or followers be inflated via automated requests? Are engagement actions rate-limited and deduplicated?
- **Content Ownership Disputes** — Can another user claim ownership of content they didn't create? Are re-upload/plagiarism checks in place?
- **Notification / Spam Abuse** — Can a user trigger excessive notifications to others? Are messaging and mention rates limited?
- **Account Impersonation** — Can usernames or display names be set to mimic other users or official accounts?

### Insurance

Apply when: Application handles policies, claims, underwriting, coverage, or risk assessment.

- **Claim Duplication** — Can the same incident be claimed multiple times? Are claim submissions deduplicated across policies and time windows?
- **Policy Backdating** — Can a policy's start date be set retroactively to cover a pre-existing incident? Are date validations server-enforced?
- **Coverage Stacking** — Can overlapping policies be used to claim more than the actual loss? Are cross-policy checks in place?
- **Fraudulent Underwriting** — Can risk assessment inputs (age, health data, property value) be manipulated to lower premiums without backend validation?
- **Payout Manipulation** — Can claim payout amounts be influenced by the claimant? Are payout calculations server-side with audit trails?

### Real Estate / Property

Apply when: Application handles listings, bids, escrow, property management, or rental agreements.

- **Bidding Manipulation** — Can a seller see competing bids and adjust their reserve? Can fake bids be placed to drive up prices? Are bid timestamps server-authoritative?
- **Escrow Timing Attacks** — Can settlement dates be manipulated to trigger or avoid penalties? Can funds be released before all conditions are met?
- **Listing Fraud** — Can a user list a property they don't own? Are ownership verification steps enforceable and not skippable?
- **Rental Payment Double-Processing** — Can rent payments be duplicated via race conditions? Are payment confirmations idempotent?
- **Document Tampering** — Can signed lease agreements or inspection reports be modified after signing? Are document hashes validated?

### FinOps / Banking

Apply when: Application handles loans, interest, account management, wire transfers, or core banking operations.

- **Loan Origination Manipulation** — Can income, employment, or credit data be falsified during application? Are verification steps enforceable and not skippable?
- **Interest Calculation Gaming** — Can day-count conventions or compounding periods be manipulated to affect interest? Are calculations server-authoritative and auditable?
- **Account Linking Fraud** — Can a user link external bank accounts they don't own? Is ownership verified via micro-deposits or equivalent before enabling transfers?
- **Wire Transfer / ACH Timing Attacks** — Can transfer initiation and settlement timing be exploited to double-spend? Are pending transfers locked against concurrent modifications?
- **Overdraft / Credit Limit Bypass** — Can concurrent transactions exceed account limits before the balance is updated? Are balance checks atomic with the debit operation?

### Crypto / Web3 / DeFi

Apply when: Application handles cryptocurrencies, tokens, NFTs, bridges, or decentralized finance operations.

- **Off-Chain Re-Entrancy Patterns** — Does the off-chain business logic mirror smart contract re-entrancy risks (callbacks modifying state mid-operation)?
- **Oracle / Price Feed Manipulation** — Are price feeds validated for staleness? Can flash loan-style attacks exploit the lag between on-chain price and off-chain business logic?
- **NFT Ownership Verification Bypass** — Is NFT ownership verified on-chain before granting access or benefits? Can ownership be spoofed with stale data?
- **Bridge Transaction Integrity** — Can cross-chain value transfers be double-credited? Is the bridge relay trusted, and are relay proofs validated?
- **Airdrop / Token Claim Duplication** — Can the same wallet claim tokens multiple times? Are claims validated against a server-side allowlist with deduplication?
- **Gas / Fee Estimation Manipulation** — Can user-supplied gas estimates cause transactions to fail predictably, enabling front-running or griefing?

### HR / Payroll

Apply when: Application handles employee data, payroll processing, time tracking, benefits, or expense management.

- **Payroll Amount Manipulation** — Can an employee modify their own salary or pay rate through self-service portals or API calls?
- **Time Tracking Fraud** — Can clock-in/clock-out timestamps be manipulated retroactively? Are geolocation or biometric checks enforced server-side?
- **PTO / Leave Balance Gaming** — Can leave requests bypass approval workflows? Can leave balances be artificially inflated by manipulating accrual calculations?
- **Benefits Enrollment Outside Qualifying Events** — Can benefit elections be changed outside open enrollment or qualifying life events by calling enrollment endpoints directly?
- **Expense Report Duplication** — Can the same receipt be submitted across multiple expense reports? Are approval chains enforced, or can a report skip required approvers?

### Legal / Compliance / RegTech

Apply when: Application handles KYC/AML, sanctions screening, regulatory reporting, or compliance workflows.

- **KYC / AML Workflow Bypass** — Can identity verification steps be skipped? Can documents be re-used across different accounts? Is document authenticity validated server-side?
- **Sanctions Screening Evasion** — Can name variations, transliterations, or entity restructuring evade sanctions list matching? Are fuzzy matching algorithms applied?
- **Regulatory Report Manipulation** — Can filing dates, submission timestamps, or report contents be tampered with after generation? Are reports cryptographically signed?
- **Consent & Audit Trail Integrity** — Can consent records be backdated or deleted? Are all compliance-relevant actions logged in tamper-proof audit trails?
- **Data Retention Policy Bypass** — Can data marked for deletion under GDPR/CCPA be retained or recovered? Are retention policies enforced at the storage layer?

### IoT / Industrial / Smart Home

Apply when: Application handles device management, sensor data, firmware updates, or automation rules.

- **Device Command Injection via Business Logic** — Can legitimate API endpoints be used to send dangerous commands (disabling safety systems, opening locks, adjusting thresholds)?
- **Firmware Update Workflow Bypass** — Can required intermediate firmware versions be skipped? Can rollbacks bypass security patches? Are update signatures validated?
- **Sensor Data Integrity** — Can sensor readings be spoofed to trigger or prevent automated actions (false temperature readings, faked occupancy data)?
- **Device Ownership Transfer Manipulation** — Can a device be claimed by a new user without the previous owner's consent? Are factory reset and re-provisioning flows secure?
- **Automation Rule Exploitation** — Can automation rules (IFTTT-style triggers) be configured to create infinite loops, resource exhaustion, or unintended cascading actions?

### Travel / Hospitality

Apply when: Application handles bookings, reservations, fare construction, loyalty programs, or dynamic pricing.

- **Fare Construction Abuse** — Can hidden city ticketing, throwaway ticketing, or fuel dumping be exploited at the API level to get lower fares?
- **Loyalty Point Manipulation** — Can points be earned without completing stays/flights? Can points be redeemed multiple times via race conditions? Can point transfers create value from nothing?
- **Reservation System Manipulation** — Can ghost bookings hold inventory without payment? Can reservation dates be modified after booking to exploit price differences?
- **Cancellation Policy Arbitrage** — Can a user exploit the gap between cancellation deadlines and refund processing to get both a refund and the service?
- **Dynamic Pricing Exploitation** — Can price quotes be locked indefinitely? Can users manipulate session data, cookies, or location headers to influence dynamic pricing algorithms?

### Ad Tech / Marketing

Apply when: Application handles ad serving, campaigns, attribution, budgets, or engagement tracking.

- **Click / Impression Fraud** — Can clicks or impressions be inflated via automated requests or replay attacks? Are clicks deduplicated and validated against genuine user sessions?
- **Attribution Manipulation** — Can last-click or multi-touch attribution be stolen by injecting fake referral parameters or redirect chains?
- **Budget Exhaustion Attacks** — Can a competitor drain another advertiser's budget by generating invalid but billable clicks? Are click fraud detection mechanisms in place?
- **Campaign Targeting Bypass** — Can an ad appear in restricted audience segments or excluded placements by manipulating targeting parameters?
- **Conversion Tracking Forgery** — Can conversion events be fabricated or replayed to inflate campaign performance metrics? Are conversion callbacks authenticated?

### Custom Domains

If the application's domain doesn't match the above, generate patterns by identifying:
1. What are the **core business invariants** the application must enforce?
2. What are the **value flows** — where does something of value move between entities?
3. What are the **trust assumptions** — what does the system assume users won't do?
4. For each invariant/assumption: **what happens if it's violated?**

## How to Perform the Audit

### Step 1: Map the Codebase
Before checking patterns, build your map:
1. Find all state mutation code (functions that create, update, or delete business entities)
2. Find all external integration points (webhooks, callbacks, third-party API calls)
3. Find all authorization checks (middleware, decorators, guards)
4. Find all configuration (rates, fees, limits, quotas, feature flags)
5. Find all multi-step workflows (state machines, approval chains, order lifecycles)
6. If a frontend exists: find all route guards, client-side calculations, and API response consumers
7. If a mobile app exists: find all local storage, deep link handlers, IPC components, and in-app purchase flows

### Step 2: Check Each Component Against All Applicable Patterns
For each critical component found in Step 1, check it against:
- All 13 universal backend patterns (if backend code exists)
- All 6 frontend patterns (if web frontend code exists)
- All 5 mobile patterns (if mobile app code exists)
- All domain-specific patterns relevant to the application

### Step 3: Report Findings
For each finding, use this structure:

```
## Finding: [PATTERN_NAME]

**Severity:** Critical | High | Medium | Low
**Location:** `path/to/file.ts:L123-L145`
**Layer:** Backend | Frontend | Mobile | Full-Stack
**Pattern:** [Which pattern this violates]

### Description
[What the vulnerability is and why it matters to the business]

### Vulnerable Code
[The specific code that is vulnerable]

### Attack Scenario
1. [Step-by-step how an attacker would exploit this]
2. [Expected business impact]

### Recommended Fix
[Code showing the correct implementation]
```

### Step 4: Present and Save the Report

**First, present the full report directly in the conversation** so the user can review findings immediately in the agent's UI (walkthrough view, chat, etc.). Display all findings with their full detail — do not summarize or truncate.

**Then, save the report to the project directory** for persistence:

1. **Create the output directory:** `business-logic-audit/` in the project root
2. **Save the markdown report:** `business-logic-audit/report-YYYY-MM-DD.md` (for agent UIs, GitHub, and markdown renderers)
3. **Save the HTML report:** `business-logic-audit/report-YYYY-MM-DD.html` (for sharing and browser viewing — styled with inline CSS for a clean, professional look with severity badges, syntax-highlighted code blocks, and a summary dashboard)
4. **Suggest adding `business-logic-audit/` to `.gitignore`** — audit reports may contain sensitive vulnerability details. Mention that some teams prefer to track them in version control for accountability.
5. **Open the HTML report in the browser** — run `open business-logic-audit/report-YYYY-MM-DD.html` (macOS) or `xdg-open` (Linux) or `start` (Windows) so the user immediately sees the styled report.
6. **Generate a PDF version** — use Chrome headless to convert the HTML report to PDF:
   - macOS: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --print-to-pdf=business-logic-audit/report-YYYY-MM-DD.pdf --no-pdf-header-footer "file://ABSOLUTE_PATH/business-logic-audit/report-YYYY-MM-DD.html"`
   - Linux: `google-chrome --headless --print-to-pdf=business-logic-audit/report-YYYY-MM-DD.pdf --no-pdf-header-footer "file://ABSOLUTE_PATH/business-logic-audit/report-YYYY-MM-DD.html"`
   - If Chrome is not available, skip this step — the HTML report's "Download PDF" button is a fallback.

The HTML report should include:
- A fixed **left sidebar** for the table of contents (width ~260px, scrollable, always visible) with the main content offset to the right — collapses to a top bar on mobile
- A `@media print` CSS block that hides the sidebar and reformats the layout for clean single-column PDF output (white background, black text, no fixed positioning)
- A header with the project name, audit date, and finding summary (e.g., "3 Critical, 2 High, 1 Medium")
- Severity badges with color coding (Critical = red, High = orange, Medium = yellow, Low = blue)
- Syntax-highlighted code blocks using inline `<span>` elements with color styles — apply colors for keywords (`if`, `const`, `return`, `async`, `await` — use a blue/purple), strings (green), comments (gray/muted), functions (yellow/gold), numbers (orange), and operators. Do NOT rely on external JS libraries — all highlighting must be baked into the HTML as colored spans
- All styling must be inline CSS (no external dependencies) so the file is fully self-contained

Example output structure:
```
project-root/
└── business-logic-audit/
    ├── report-2026-03-13.md
    ├── report-2026-03-13.html
    └── report-2026-03-13.pdf
```

## Severity Classification

| Severity | Criteria |
|----------|----------|
| **Critical** | Direct value extraction possible (race condition on withdrawal, webhook forgery → free credits, escrow bypass, exposed secrets in bundle) |
| **High** | Business loss likely under specific conditions (rate manipulation, spread inversion, quota bypass, client-side auth bypass on sensitive data) |
| **Medium** | Business constraint bypass (limit circumvention, fee avoidance, feature access bypass, API over-exposure of non-critical data) |
| **Low** | Theoretical risk or requires unlikely conditions (rounding precision, reference enumeration, optimistic UI without server abuse potential) |

## Confidence Scoring

- **High** — Direct code evidence (missing validation, non-atomic operation, absent signature check) with no material alternate control
- **Medium** — Strongly indicated but at least one material uncertainty (possible upstream control, conditional behavior, external validation)
- **Low** — Plausible but unverified (indirect evidence, unclear scope, inconsistent indicators)

When uncertain, round down to minimize false positives.

## False Positive Rules

1. **Client-side checks don't count** — UI validation is not a defense. Only server-side enforcement matters
2. **Documentation is not proof** — Config comments or policy docs are not evidence of enforcement. Require code evidence
3. **External services are not guarantees** — Don't assume a third-party API validates all inputs. Verify what the app sends and how it handles responses
4. **Theoretical-only findings are noise** — Don't flag a race condition without confirming the read-check-write is actually non-atomic in the code
5. **Staging behavior ≠ production** — Don't claim findings based on dev/staging unless the same config applies to production
6. **Stay in scope** — Don't flag XSS, SQLi, SSRF, or CSRF as business logic vulnerabilities. Those are separate concerns
7. **Frontend findings require context** — A client-side calculation is only a finding if the server does not re-validate. Check both layers before flagging

## Important Rules

- **Code-level evidence only.** Every finding must reference specific file paths and line numbers
- **Check ALL applicable patterns.** Don't stop after finding one issue — systematically check every critical component
- **Check ALL layers.** If backend, frontend, and/or mobile code exist, check all applicable layers for every pattern
- **Business impact first.** Prioritize findings by potential impact to the business, not by technical complexity
- **Be thorough.** An incomplete audit is a failed audit. Every critical operation must be analyzed
- **Be precise.** Describe the exact missing defense, not vague concerns
