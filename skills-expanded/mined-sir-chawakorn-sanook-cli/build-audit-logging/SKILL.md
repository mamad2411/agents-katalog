---
name: build-audit-logging
description: Builds tamper-evident audit logging — structured actor/action/target/result records for security-relevant events, append-only hash-chained or WORM/object-lock storage, PII-safe payloads that log references not raw data, and regulation-driven retention — to satisfy SOC2/HIPAA-style controls and support incident forensics.
when_to_use: A system needs a defensible, queryable record of sensitive actions (access, permission/config changes, admin ops) for compliance or forensics. Distinct from observability-instrument (operational logs/metrics/traces for debugging) and map-privacy-data-gdpr (data-subject rights and lawful-basis mapping).
---

## When to Use

Reach for this skill when the requirement is a **defensible record of who did what to whom**, not operational telemetry:

- "We need an audit trail for SOC2 / HIPAA / PCI — access, admin actions, config changes"
- "Auditors want to know who changed this permission / exported this report / read this patient record"
- "After the breach, prove what the attacker touched and that nobody edited the logs"
- "Log every admin override / impersonation / data export, immutably"
- "Make sensitive-action history queryable for investigations and legal hold"

NOT this skill:
- Debugging latency/errors with logs, metrics, traces, dashboards → observability-instrument (operational, sampled, short-retention — the opposite of an audit log)
- Data-subject access/erasure requests, consent, lawful basis, retention *policy* for personal data → map-privacy-data-gdpr
- *Deciding* whether an action is allowed (the policy engine itself) → design-authorization-model (audit logging records the decision; it does not make it)
- An immutable append-only store as the system of record for business state (rebuildable projections) → design-event-sourcing-cqrs
- Storing/rotating the secrets and signing keys this log references → secrets-management
- Running the actual breach investigation/postmortem → incident-response-sre (this skill makes that investigation *possible*)

## Steps

1. **Enumerate auditable events first — code to a closed list, not "log everything."** An audit log with too much noise is as useless as one with gaps. Audit exactly the security-relevant control points:

   | Category | Examples | SOC2 (TSC) | HIPAA |
   |---|---|---|---|
   | Authentication | login success/fail, MFA, logout, password/key change, session revoke | CC6.1 | §164.312(b) |
   | Authorization decisions | access denied, privilege grant/revoke, role change, impersonation start/stop | CC6.3 | §164.308(a)(4) |
   | Sensitive data access | read/export/print of PII/PHI/financial records, bulk query, report download | CC6.1 / CC7.2 | §164.312(b) audit controls |
   | Config / security changes | feature flag, retention policy, encryption setting, integration/webhook, IAM policy | CC8.1 | §164.308(a)(1) |
   | Admin / break-glass ops | user delete, data purge, override, prod DB access, support impersonation | CC6.1 | §164.308(a)(3) |

   Define this list with security/compliance, not ad hoc per feature. Each event gets a stable `action` constant (e.g. `user.role.granted`, `record.exported`) — never a free-text string you can't query or version.

2. **Fix one structured schema and emit it everywhere.** Required fields, machine-parseable (JSON), one shape across services:

   ```json
   {
     "id": "01J8...ULID",                  // unique, sortable, dedup key
     "ts": "2026-06-15T09:41:02.117Z",     // UTC, ISO-8601, ms precision, server clock
     "action": "record.exported",          // from the closed list, dotted, versioned
     "actor": { "type": "user", "id": "u_8821", "auth": "session", "on_behalf_of": "support_agent_31" },
     "target": { "type": "patient_record", "id": "p_5567" },   // id/reference ONLY
     "result": "allow",                     // allow | deny | error
     "reason": "policy:export.phi.granted", // why, esp. for deny
     "source_ip": "203.0.113.7",            // normalized from trusted proxy header
     "user_agent": "...",
     "request_id": "req_9f3c",              // correlation id → ties to app/trace logs
     "tenant": "org_204",
     "meta": { "row_count": 1420, "format": "csv" }  // counts/refs, NEVER raw payload
   }
   ```
   Use **ULID/UUIDv7** for `id` (sortable + a natural dedup key for at-least-once emitters). `on_behalf_of` is mandatory whenever an admin/support acts as another user — impersonation without it is an audit gap auditors will flag.

3. **Keep the audit log physically separate from application logs.** Different store, different write credentials, different retention. App logs are mutable, sampled, debug-grade; audit logs are not. Mixing them means a developer with log-write access can forge or delete audit history. Ship audit events to a **dedicated append-only sink** (dedicated Postgres table with revoked UPDATE/DELETE, a WORM object store, or a managed audit service) — never the same index/bucket as `console.log` output.

4. **Make tamper-evidence structural, not a promise. Pick by threat model:**

   | Mechanism | Detects | Use when | Cost |
   |---|---|---|---|
   | **Hash chain** (each row stores `hash(prev_hash + entry)`) | any edit/delete/reorder of past rows | default — works in any DB, cheap, verifiable offline | 1 hash/write + periodic verify job |
   | **WORM / object-lock** (S3 Object Lock COMPLIANCE, GCS retention lock) | deletion/overwrite before retention expiry, even by root | regulated retention, untrusted operators | storage + immutable retention window |
   | **Per-entry digital signature** (HSM/KMS sign each batch) | forgery + proves origin/non-repudiation | strict non-repudiation, third-party verifier | KMS calls, key mgmt |
   | **External anchoring** (periodic chain-head to a notary/transparency log) | insider with full DB+app access rewriting the whole chain | high-value targets, hostile-insider model | scheduled external write |

   **Default: hash chain + WORM storage.** The chain proves *no row was altered*; object-lock proves *no row was deleted*. Hash chain alone doesn't stop a truncate-and-rebuild by someone with full write access — pair it with object-lock or external anchoring for that threat. Restrict write access to an **append-only path** (DB role with `INSERT` only; bucket policy allowing `PutObject` but not `DeleteObject`/overwrite); **nobody — including the app service account — gets row-level update/delete.**

5. **Never log secrets or raw PII/PHI — log references and minimized metadata.** The audit log is high-value, long-retention, and widely readable by auditors; a raw payload in it is a second copy of your most sensitive data with the worst blast radius. Log the *id* of the record touched, not its contents. For changes, log a **field-name diff** (`changed: ["role","status"]`) or hashed before/after, never the literal old/new PII values. Run a serializer allowlist + a secret/PII scrubber on the `meta` object before write; drop anything not on the allowlist. Tokens, passwords, full card/SSN, message bodies, query result rows → never.

6. **Set retention per regulation, then enforce it in the store — don't rely on a cron `DELETE`.** Map each event category to its longest applicable requirement and configure the immutable window so deletion *can't* happen early and *does* happen on schedule:

   | Regime | Typical minimum | Enforce via |
   |---|---|---|
   | HIPAA | 6 years | object-lock retention 6y + lifecycle expiry |
   | SOC2 | 1 year (often 7 for evidence) | partition + lifecycle policy |
   | PCI-DSS | 1 year (3 months hot) | hot tier + cold archive |

   Use **time-partitioned tables or object lifecycle rules** so expiry is declarative and audited, not a script someone can disable. Don't over-retain past the requirement (that's its own liability under privacy law — see map-privacy-data-gdpr).

7. **Make it queryable for investigations.** A trail you can't search is forensically useless. Index `actor.id`, `target.id`, `action`, `ts`, `tenant`, `request_id`. The two queries every investigation needs: *"everything actor X did in window T"* and *"everyone who touched target Y."* Tie `request_id` back to operational traces (observability-instrument owns those) so an investigator can pivot from an audit entry to the full request. Provide a read-only investigator role separate from the write path.

8. **Emit exactly once, synchronously to the decision, fail-closed on sensitive actions.** Write the audit record **in the same transaction/critical path as the action it records** (or via a transactional outbox) so an action can never succeed without its record. For sensitive control points (data export, permission grant, break-glass), if the audit write fails, **deny the action** — an unlogged privileged action is worse than a blocked one. Dedup downstream consumers on `id`. Never fire-and-forget an audit write for a security-critical event.

## Common Errors

- **Audit log shares the store/credentials with app logs.** Anyone who can write debug logs can then forge or wipe audit history. Separate store, separate INSERT-only credential, separate retention.
- **Logging raw PII/PHI or secrets in the payload.** Creates a long-retention, broadly-read second copy of your crown jewels. Log ids and field-name diffs; scrub `meta` against an allowlist before write.
- **"Append-only" that the app account can still UPDATE/DELETE.** That's not append-only. Revoke update/delete at the DB-role / bucket-policy level; verify with an attempted delete that must fail.
- **Hash chain with no verification job.** An undetected break = no tamper evidence at all. Run a scheduled verifier that recomputes the chain and alerts on the first mismatch; anchor the chain head externally if insiders are in scope.
- **Async fire-and-forget emit.** The action commits, the audit write is dropped on a queue overflow or crash, and you have a silent gap. Write in-transaction or via outbox; fail-closed for sensitive actions.
- **Free-text `action` strings.** `"User exported the data"` can't be queried, aggregated, or mapped to a control. Use a versioned closed enum.
- **Trusting client-supplied `X-Forwarded-For` / actor id.** Both are spoofable. Take `source_ip` only from the header your trusted proxy sets; take `actor.id` from the authenticated session, never from the request body.
- **Missing impersonation provenance.** Support acts "as" a user and the log shows only the end user — auditors flag this as a control gap. Always populate `on_behalf_of`.
- **Cron-job retention instead of store-enforced.** A disabled or buggy cron either leaks data forever or deletes evidence early. Use object-lock / partition lifecycle so the store enforces it.
- **No timezone discipline.** Mixed local timestamps make a forensic timeline unreconstructable. UTC + ISO-8601 + ms, server clock, everywhere.
- **Recording allows but dropping denies.** Auditors and investigators care most about blocked attempts. Record `result: "deny"` with `reason`, not just successful actions.

## Verify

1. **Exactly-once coverage:** For each event in the closed list, perform the action and confirm **one** audit record is written with all required fields populated; perform a sensitive action whose audit write is forced to fail and confirm the action is **denied** (fail-closed), not silently completed.
2. **Tamper detection:** Directly mutate one stored row (or delete one), run the chain verifier → it flags the exact broken entry. Re-run on the untouched log → clean. This is the test that proves the tamper-evidence is real, not decorative.
3. **Immutability of the write path:** As the **application service account**, attempt `UPDATE`/`DELETE` on an audit row (and overwrite/delete on the object store) → both must be rejected by the role/bucket policy. Only `INSERT`/`PutObject` succeeds.
4. **No leakage:** Trigger actions involving secrets and PII/PHI (export a record, change a password, edit a profile), then grep the stored audit entries for the raw secret, the password, and the literal PII values → **zero hits**; only ids, field names, and counts appear.
5. **Retention enforced by the store:** Confirm the object-lock/partition policy is configured for the regulated window and that no role (including admin/root) can delete before expiry; confirm entries past the window expire automatically without a manual job.
6. **Investigation queries:** Run *"all actions by actor X in window T"* and *"all actors who touched target Y"* → both return correct, complete results in interactive time on indexed fields, and a `request_id` pivots to the matching operational trace.
7. **Provenance:** An impersonated action shows both the acting agent and `on_behalf_of`; a denied action shows `result: "deny"` + `reason`; `source_ip` matches the trusted-proxy value, not a spoofed body field.

Done = every event in the closed list emits exactly one complete record on a physically separate, INSERT-only, retention-locked store; the chain verifier detects any edit/delete; no secret or raw PII/PHI appears in any entry; and the two core investigation queries return complete, correct results mapped to their SOC2/HIPAA controls.
