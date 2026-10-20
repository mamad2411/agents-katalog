---
name: backup-recovery-design
description: "Design or review backup and disaster-recovery architecture for production services, databases, object stores and control planes. Turns business impact into workload-specific RTO, RPO and retention targets; maps recoverable state and dependencies; chooses consistent backup, replication, immutability, encryption and isolation patterns; defines identity bootstrap, restore order, acceptance evidence, ownership and cost. Use for backup strategy, DR architecture, ransomware recovery, regional-loss planning, restore design, backup coverage reviews, or questions such as \"what must we back up\" and \"can we meet a four-hour RTO\". For a restore-from-copy rehearsal with measured outcomes use disaster-recovery-exercise; for live failover experiments use game-day."
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Backup and Recovery Design

A backup is useful only when a named service can be restored, by an authorised person,
within a business deadline, to a known point whose loss the business accepts. Design
backwards from that claim. A schedule and a retention number alone describe stored
copies, not recoverability.

## Hard gates

1. **The business owns recovery objectives.** Engineering may measure feasibility, but
   cannot silently choose how much transaction loss or outage the business accepts.
2. **Replication is not the only recovery copy.** Deletion, corruption, ransomware and
   bad writes replicate too. Preserve versioned, point-in-time copies in an independently
   administered failure domain.
3. **Every retained copy has a restore path.** Capture schema, configuration, identity,
   keys and dependency versions needed to read it. Data without its decoder is not a
   recovery copy.
4. **Recovery identity survives the event.** A plan that requires the failed identity
   provider, production secrets manager or one administrator's account is circular.
5. **Evidence closes the claim.** Job success, object count and provider durability are
   evidence that copies exist. Only a restore plus workload-level validation supports an
   RTO or RPO claim.

## Workflow

### 1. Start with business impact

Partition the service into business capabilities rather than assigning one target to an
entire estate. For each capability record:

| Field | Decision |
| --- | --- |
| Consequence | What happens after 15 minutes, 4 hours, 24 hours and 7 days unavailable? |
| RTO | Maximum time from service disruption to accepted service restoration |
| RPO | Maximum age of the accepted recovery point at the incident boundary |
| Integrity | Which invariants must hold: balances, uniqueness, ordering, referential integrity? |
| Retention | Operational rollback window, audit or legal period, and required expiry |
| Degraded mode | Minimum capability that may satisfy the first recovery milestone |
| Authority | Business owner who accepts the target and residual loss |

Default RTO to the full outage: disruption, detection, declaration, decision, provisioning,
transfer, replay, validation and traffic readiness through business acceptance. If a
technical restore duration starts later or stops earlier, label it separately. Convert
RPO into the maximum transactions exposed at peak write rate and get explicit acceptance.
Zero RPO needs failure semantics that backups alone cannot provide.

### 2. Inventory the recovery set

Trace one business transaction and list every stateful component needed to serve and
prove it afterward:

- data stores, logs, queues, indexes and their schemas;
- application artefacts, runtime images, infrastructure and network configuration;
- DNS, identity, certificates, secrets, encryption keys and key policy;
- tenant mappings, feature flags, external-provider state, observability and audit data.

For each item record owner, writer, source of truth, protection mechanism, frequency,
retention, storage location, administrator boundary, encryption dependency, restore
method and last accepted restore. Mark derived data with its rebuild source and measured
rebuild duration. “Rebuildable” does not satisfy a short RTO without that measurement.

Draw a coverage matrix: capabilities as rows, recovery-set items as columns. Any blank
cell is either a documented exclusion with a rebuild path or a design gap.

### 3. Choose a consistent recovery point

Select consistency to match the invariant:

| Pattern | Appropriate when | Required evidence |
| --- | --- | --- |
| Crash-consistent snapshot | The workload can replay logs and repair after abrupt stop | Recovery and integrity checks from that snapshot |
| Application-consistent copy | In-memory or cross-volume state must be quiesced | Quiesce completed, copy boundary recorded, application validation passed |
| Database-native backup plus logs | Point-in-time recovery is required | Base backup and uninterrupted log chain cover the target time |
| Coordinated multi-system point | A transaction spans stores without a replayable event source | Shared boundary, fencing or reconciliation rule |
| Independent copies plus replay | Events are durable and consumers are idempotent | Replay cursor, ordering rule and duplicate handling verified |

Do not call independently timed snapshots “consistent” because their timestamps are
close. Define the write fence, transaction boundary, log position or reconciliation
procedure that makes them one recoverable state. Account for backup duration: a daily job
that runs for six hours may expose more than one day of loss depending on when the usable
recovery point is established.

### 4. Separate failure domains

Model threats, not just locations: operator error, compromised production identity,
software defect, provider account suspension, zone loss, region loss and provider-wide
dependency loss. For each threat, show which copy and control plane remain reachable.
For regional promotion, name the authority that chooses the writable side, how the old
side is fenced, how traffic and DNS follow authority, and how authoritative data is
chosen and reconciled before failback. Two writable regions without a conflict rule are
not recovery.

Place at least one recovery copy outside the production administration path. Use a
separate account, project or organisation boundary where the threat warrants it; a
different bucket in the same compromised project is only a storage location. Restrict
production writers from deleting backups or shortening retention. Require separate,
audited recovery roles for destructive policy changes.

Immutability has a lifecycle: lock period, legal holds, expiry, deletion and exceptional
release. Verify whether a platform setting can be reduced, bypassed by an administrator,
or becomes irreversible once locked. Versioning and soft deletion protect different
mistakes from retention lock; name which layers handle overwrite, deletion and account
compromise.

### 5. Design encryption and identity bootstrap together

Record for every copy the encryption mode, key, key location, key administrator and
recovery dependency. A customer-managed key improves separation only if the key remains
available during the same disaster. Preserve key metadata and policy; ensure the chosen
key service and location match the recovery scope. Never place exported secrets beside
the encrypted backup under the same access path.

Create a small, controlled bootstrap path that does not depend on production SSO, DNS,
network or secrets. Define break-glass custodians, strong authentication, access logging,
approval, periodic credential rotation and a way to establish recovery roles in the
target environment. Keep privileges narrow enough to restore the control plane first;
normal workload access follows through restored identity.

### 6. Build the dependency restore graph

Express dependencies as a directed graph and restore in topological order. A common
shape is:

1. recovery identity, keys, organisation policy and audit sink;
2. network, DNS prerequisites and the recovery control plane;
3. foundational data stores and transaction logs;
4. schemas, applications and internal dependencies;
5. derived indexes, caches and asynchronous consumers;
6. observability, external integrations and traffic readiness.

Replace this generic order with the actual graph. Identify cycles such as identity
requiring DNS while DNS administration requires identity, then add a bootstrap edge that
breaks each cycle. For parallel branches, budget the critical path rather than summing
every duration. Include data transfer, quota increases, key access, replay, validation
and approval in the RTO calculation.

Read `references/design-patterns.md` when choosing copy topology, tiering workloads,
calculating the recovery timeline or writing acceptance tests.

### 7. Define acceptance before selecting products

For every recovery tier, write an acceptance contract:

- a recovery point at or newer than the RPO boundary is selectable;
- restoration completes within the component budget on production-scale data;
- integrity invariants, record counts and domain reconciliations pass;
- applications start from pinned, compatible artefacts and schema;
- synthetic business transactions succeed in an isolated target;
- security controls, audit logging and least-privilege access are present;
- the business owner accepts any known loss before traffic is enabled.

Attach evidence: recovery-point identifier and timestamp, source and target scope, data
volume, elapsed times by phase, validation results, exceptions and approver. Set an
evidence freshness requirement based on change rate and risk. Hand the contract to
`disaster-recovery-exercise` for a restore-from-copy rehearsal; feed measured timings and failures back into this design. Use `game-day` for live failover experiments without restoration from a copy.

### 8. Reconcile objectives, evidence and cost

Cost the complete design: copy storage by retention tier, change-log growth, cross-region
and restore egress, API operations, immutable duplicate data, reserved recovery capacity,
licences, key and audit services, and recurring restore exercises. Include the cost of
meeting RTO during a regional capacity shortage; “provision on demand” is an assumption,
not reserved capacity.

If the design misses an objective, present explicit choices: fund faster protection or
warm capacity, reduce the protected scope, accept a longer RTO/RPO, or redesign the
application. Do not hide the gap behind a provider feature name. Deduplicate only after
confirming it does not couple independent copies to one failure domain.

### 9. Produce the recovery design record

Deliver the approved capability tiers; recovery-set inventory and coverage matrix;
consistency boundaries and copy topology by threat; retention and administrator controls;
key and identity bootstrap dependencies; restore graph and critical path; acceptance
contract and evidence freshness; annualised cost, gaps, owners and review date.
For regional recovery, include promotion authority, write fencing, traffic movement and
the return or failback design; execution belongs in `cutover`.

Read `references/gcp-recovery-pitfalls.md` when the design uses Google Cloud. It limits
claims to documented platform behaviour that changes retention, consistency, key or
regional-loss decisions.
