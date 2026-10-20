---
name: threat-model-stride
description: Produces a design-level STRIDE threat model — decomposes the architecture into a data-flow diagram with trust boundaries, enumerates threats per element, rates them by likelihood × impact, and records mitigations and signed-off residual risk. Use before building or substantially changing a system that handles untrusted input, secrets, money, or PII.
when_to_use: A new service, public API, auth flow, multi-tenant boundary, or agent/tool surface is being designed and you need "what could go wrong here?" answered before code exists. Distinct from security-review (audits an already-written diff line by line) and write-rfc (proposes the design itself).
---

## When to Use

Reach for this when the question is **what an adversary could do to a design**, before the design is built:

- "Threat model this new payments/checkout service"
- "We're adding a multi-tenant boundary — where can one tenant reach another's data?"
- "New public API / webhook ingress / agent tool surface — enumerate the attack surface"
- "The security RFC needs a threats section and a residual-risk register"
- "What trust boundaries does this auth flow cross, and what crosses each one?"

NOT this skill:
- Auditing already-written code for injection/SSRF/secrets line by line → security-review (this skill works on a diagram, not a diff)
- Writing the design/proposal itself (motivation, alternatives, rollout) → write-rfc (threat-model is one section feeding it)
- Implementing the login/JWT/session controls a threat surfaces → auth-jwt-session
- Storing/rotating the secrets a threat targets → secrets-management
- Hardening one webhook endpoint's signature/replay handling → ingest-webhook-secure
- Responding to an attack happening **now** → incident-response-sre

## Steps

1. **Define scope, assets, and adversaries first — never enumerate threats against an unbounded system.** Write three lists before drawing anything:
   - **Assets** — what you protect, by category: *confidentiality* (PII, secrets, tokens), *integrity* (balances, order state, audit log), *availability* (checkout, login). Name the concrete data, not "the database."
   - **Adversaries** — pick from this set and state each one's starting position:

     | Adversary | Starts with | Typically drives |
     |---|---|---|
     | Anonymous internet | Network reachability only | S, D, I (info disclosure via errors) |
     | Authenticated user | Valid session, own tenant | E (priv-esc), tenant-boundary I/T |
     | Malicious tenant (multi-tenant) | Valid account, own data | Cross-tenant I (read), T (write) |
     | Insider / operator | Prod console, some creds | R (repudiation), I, E |
     | Compromised dependency | Code execution in one process | S, T, E across the process boundary |
     | Stolen credential / token | One leaked secret | S, blast-radius of that secret |

   - **In/out of scope** — explicitly list what you will NOT model (e.g. "physical datacenter security: out; we trust the cloud provider's hypervisor"). Unstated scope = infinite scope.

2. **Draw the data-flow diagram as validated Mermaid — four element types plus boundaries, no more.** DFD elements: **External Entity** (square — user, third-party API), **Process** (round — your service/lambda), **Data Store** (cylinder — DB, queue, bucket, cache), **Data Flow** (arrow, labeled with protocol + what data). A **trust boundary** is a dashed box crossing one or more flows where the privilege/trust level changes. The four boundaries to always look for: **network edge** (internet → DMZ), **authz** (unauthenticated → authenticated), **tenant** (tenant A → shared/tenant B), **process** (your code → third-party/dependency code).

   ```mermaid
   flowchart LR
     subgraph edge["Network edge — untrusted"]
       user["Browser (external entity)"]
     end
     subgraph trusted["Authenticated · single-tenant"]
       api("API service")
       worker("Async worker")
     end
     db[("Orders DB")]
     pay["Stripe API (external entity)"]
     user -->|"HTTPS · login creds"| api
     api -->|"SQL · tenant_id scoped"| db
     api -->|"enqueue · job payload"| worker
     worker -->|"HTTPS · card token"| pay
   ```

   Shapes match the legend above: `[ ]` square = external entity, `( )` round = process, `[( )]` cylinder = data store, `-->|label|` = data flow. Each `subgraph` is a trust boundary (Mermaid renders dashed boxes). `db` and `pay` sit outside both boundaries on purpose — that's the point where trust changes.

   Validate it before continuing: `npx -y @mermaid-js/mermaid-cli -i model.mmd -o model.svg` (or paste into mermaid.live). A diagram that doesn't render isn't a deliverable. If the system is large, model **one boundary-crossing flow per diagram** rather than one unreadable mega-graph.

3. **Walk every flow that crosses a boundary and apply STRIDE per element.** Do not brainstorm freely — march the checklist. STRIDE maps to the property each threat violates:

   | Letter | Threat | Violates | Ask at this element |
   |---|---|---|---|
   | **S** | Spoofing | Authentication | Can the caller forge who they are? (no/weak auth, replayable token) |
   | **T** | Tampering | Integrity | Can data in transit or at rest be altered? (no TLS, no signature, mutable audit log) |
   | **R** | Repudiation | Non-repudiation | Can an actor deny an action? (no/forgeable logs, shared accounts) |
   | **I** | Information disclosure | Confidentiality | Can data leak? (verbose errors, missing authz check, IDOR, unencrypted store) |
   | **D** | Denial of service | Availability | Can it be exhausted? (unbounded input, no rate limit, amplification) |
   | **E** | Elevation of privilege | Authorization | Can a lower-privilege actor gain higher rights? (missing tenant scope, broken RBAC, injection → RCE) |

   Apply the elements-affected rule to save time: **External entities** → S, R. **Processes** → all six. **Data stores** → T, I, D (and R if it's the audit log). **Data flows** → T, I, D. Record each threat as one row: `<element> | <STRIDE letter> | <concrete attack> | <adversary from step 1>`. Concrete means "authenticated user changes `tenant_id` in the path param and reads another tenant's orders (I via IDOR)", not "data could leak."

4. **Rate each threat likelihood × impact, then rank.** Use a 3×3 so disagreements are cheap:

   | | Impact: Low | Impact: Med | Impact: High |
   |---|---|---|---|
   | **Likelihood: High** | Medium | High | **Critical** |
   | **Likelihood: Med** | Low | Medium | High |
   | **Likelihood: Low** | Low | Low | Medium |

   Likelihood = how exposed + how easy (anonymous-reachable + no skill = High; insider-only + needs prod creds = Low). Impact = blast radius on the asset (all-tenant PII dump = High; one user's display name = Low). Sort the threat table by rating, Critical first. Rate on the controls that *exist today*, never on ones you plan to build — planned controls earn their reduction in the disposition step (5), not here.

5. **Disposition every threat — exactly one of four, no threat left unrated or "noted."**
   - **Mitigate** — name the *specific* control (e.g. "scope every query by `tenant_id` from the session, never from the request; add a row-level-security policy as defense-in-depth"). A mitigation without a named control is not a mitigation.
   - **Eliminate** — remove the feature/flow/data that creates the threat (don't store the PAN; tokenize at the edge so the card number never enters scope).
   - **Transfer** — push to a party who owns it (offload card storage to a PCI-compliant processor; buy insurance). Note who now owns it.
   - **Accept** — only with a named sign-off and an expiry. An accepted risk needs an owner, a date, and a re-review trigger; otherwise it's a silent gap.

   Default bias: **Critical/High must be mitigated or eliminated before ship.** Medium may be accepted with sign-off. Low may be accepted by the team lead.

6. **Map each mitigation to a real engineering task and link existing controls.** For every "mitigate," produce a tracked task (`SEC-123: enforce tenant_id from session in OrderRepository`) and point at the control that delivers it — frequently a sibling skill: rate limiting (D) → rate-limiting; auth/RBAC/IDOR (S/E) → auth-jwt-session; secret handling (S, I) → secrets-management; webhook signature/replay (S/T) → ingest-webhook-secure. Mark which controls **already exist** (TLS everywhere, WAF) vs **must be built** so the model doubles as a backlog.

7. **Emit the deliverables — the model is the artifact, not the conversation.** Write a `threat-model.md` containing: scope/assets/adversaries (step 1), the validated DFD (step 2), the rated threat table with dispositions (steps 3–5), an explicit **abuse-cases** list (the top attacker stories: "as a malicious tenant I enumerate IDs to read others' invoices"), and a **residual-risk register** (every Accept row: threat, rating, owner, sign-off, expiry). Finish with **re-model triggers** — the events that invalidate this model and require a redo (new trust boundary, new external integration, auth model change, new class of PII, major arch change). A threat model with no expiry condition rots silently.

## Common Errors

- **Listing threats with no diagram.** Without the DFD you miss the boundary-crossing flows that produce the real threats. Draw and validate the diagram first; enumerate per element second.
- **Missing trust boundaries entirely (or only drawing the network edge).** The expensive bugs live at the *authz* and *tenant* boundaries, not the firewall. Every place trust level changes gets a dashed box.
- **Vague threats: "data could be leaked."** Unactionable and unrateable. Write the concrete path: which actor, which element, which parameter, which STRIDE letter.
- **Skipping STRIDE letters because they "feel unlikely."** That's what rating is for — enumerate all applicable letters per element, then let likelihood × impact triage. Skipping at enumeration time hides the threat; skipping at rating time is a defensible decision.
- **Accepting risk with no owner/expiry.** "We'll accept that" in a meeting evaporates. An accepted risk is only accepted when it's in the register with a name, a date, and a re-review trigger.
- **Modeling the whole company.** Scope creep makes the model useless. Bound it to the one service/flow/change and explicitly list what's out of scope (step 1).
- **Rating on aspirational controls.** Rating a threat "Low" because of a mitigation you *plan* to build inflates safety. Rate on what exists today; the disposition step is where planned controls earn their reduction.
- **Mitigation = "add validation" / "we'll be careful."** Not a control. Name the mechanism (RLS policy, signed token with `aud` check, allowlist, rate limiter) and the task that builds it.
- **Treating it as one-and-done.** A model with no re-model triggers is stale the next time a boundary moves. List the triggers that force a redo.
- **Confusing this with a code audit.** STRIDE on a diagram finds design flaws (missing boundary, IDOR by design); it will not find a SQL-injection typo in line 88 — that's security-review on the diff.

## Verify

1. **Diagram renders:** `npx -y @mermaid-js/mermaid-cli -i model.mmd -o model.svg` exits 0 and the SVG shows every external entity, process, store, flow, and at least one dashed trust boundary.
2. **Boundary coverage:** Every flow that crosses a trust boundary has at least one threat row. Pick any boundary-crossing arrow at random — it must appear in the threat table.
3. **STRIDE coverage:** Each process element was evaluated against all six letters (each letter either has a threat row or an explicit "N/A — why"); stores and flows covered for T/I/D.
4. **Every threat is concrete and rated:** No row reads "data could leak"; each names actor + element + attack, carries a likelihood × impact rating, and is sorted Critical-first.
5. **Every threat is dispositioned:** Each row is exactly one of mitigate / eliminate / transfer / accept — zero "noted" or blank. Mitigations name a control and link a tracked task.
6. **Residual register complete:** Every Accept appears in the residual-risk register with owner, sign-off, and expiry. No Critical/High is in Accept without explicit named sign-off.
7. **Abuse cases + re-model triggers present:** The doc lists the top attacker stories and the events that invalidate the model.

Done = the Mermaid DFD renders with explicit trust boundaries, every boundary-crossing flow has STRIDE-enumerated threats that are each rated and dispositioned, no Critical/High sits in Accept without named sign-off, and the doc ships a residual-risk register plus re-model triggers.
