---
name: schedule-effective-dated-changes
description: Use when a change must take effect LATER (a future-dated plan/tier/price change, a scheduled deactivation, an end-of-cycle update) or must be visible / cancellable / auditable before it applies — model it as a pending-changes table (the change payload + an effective date + a status), swept by a scheduled job that applies DUE rows in a transaction, snapshots prior state to a history table, and marks them done. Covers when to use this vs a Redis delayed job. NestJS/TypeORM reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Schedule effective-dated changes

Applying a change at a **future effective date** (plan/tier/price changes, scheduled deactivations,
end-of-billing-cycle updates) without mutating now. The Redis *delayed job* alternative (and the cron +
overlap lock) is `background-jobs-and-caching`; transactions are `write-service-code` §9.

## Core principle
**Persist the *intended change* as a row with an effective date — don't mutate now, and don't bury the
timer in memory.** A pending-changes table makes a future change **queryable** ("what's scheduled?"),
**cancellable** (the user changes their mind), and **auditable** (history of what applied when). A
scheduled sweep applies the **due** ones transactionally and records history.

## 1. Store the intent, not the mutation
A `pending_changes` table holds the change payload + when it takes effect + its lifecycle status —
instead of writing the change to the live row immediately:
```ts
@Entity() class PendingChange extends BaseEntity {
  @Column() targetId!: string;                 // the entity to change
  @Column({ type: 'jsonb' }) data!: ChangePayload;   // WHAT changes (new tier, new price, …)
  @Column() effectiveAt!: Date;                // WHEN it takes effect
  @Column({ type: 'enum', enum: PendingStatus, default: PendingStatus.PENDING }) status!: PendingStatus;
  @Column({ nullable: true }) reason!: Nullable<string>;   // why it FAILED / was CANCELLED
}
// PENDING → COMPLETED | FAILED | CANCELLED
```
Now "show my scheduled changes" is a query, and cancelling is `status = CANCELLED` — no timer to chase.

## 2. Sweep DUE changes (push the filter into SQL, in batches)
A scheduled job (a cron processor — `background-jobs-and-caching`) fetches only what's **due and still
pending**, ordered by effective date, **paginated** for large sets. Never fetch everything then filter
in code (global *Database & Migration Rules*).
```ts
this.repo.find({
  where: { effectiveAt: LessThanOrEqual(now), status: PendingStatus.PENDING },  // due + pending, in SQL
  order: { effectiveAt: 'ASC', createdAt: 'ASC' },
  take: BATCH,
});
```
Guard the sweep against **overlap** (a slow run must not double-apply) with the Redis `SET NX` lock from
`background-jobs-and-caching`.

## 3. Apply transactionally + snapshot prior state to history
In one transaction: snapshot the **current** state into a `*_history` table (audit/rollback trail),
apply the change, then mark the pending row **COMPLETED**. On failure, mark **FAILED + reason** (keep
the record — don't lose it) so it's visible and retriable. Make apply **idempotent** (a re-run of a
COMPLETED row is a no-op).
```ts
await this.dataSource.transaction(async (em) => {
  const prior = await em.findBy(Target, { id: In(ids) });
  await em.insert(TargetHistory, prior.map(({ id, ...rest }) => rest));   // snapshot BEFORE overwrite
  await applyChanges(em, dueChanges);                                     // the actual mutation(s)
  await em.update(PendingChange, { id: In(dueIds) }, { status: PendingStatus.COMPLETED });
});
```

## 4. When to use this vs a delayed job
- **Redis delayed job** (`background-jobs-and-caching`): ephemeral, fire-and-forget **timers** — send a
  reminder, expire a hold, retry. No need to see/cancel/report it.
- **Pending-changes table** (this skill): a **business state change** that must be **visible,
  cancellable, reportable, or audited**, or applied at a **wall-clock boundary** for many records at
  once (end of cycle). The change is data you query, not a job you can't see.
They compose — the table is the source of truth; a cron is just the trigger.
▸ *Other stacks:* SQL **temporal / effective-dated (bitemporal)** tables; an "outbox"-style scheduled-
changes table + a worker; an effective-dated rate/price table read at `now`. Principle: persist the
future change as data with an effective date; a sweep applies due rows + keeps history.

## Verification
- A future change is a **row** (`data` + `effectiveAt` + `status`), not an immediate mutation or an in-memory timer.
- The sweep filters **due + pending in SQL**, batches, and is **overlap-guarded**.
- Apply is **transactional**, snapshots prior state to **history**, marks COMPLETED, and records FAILED + reason on error; re-runs are idempotent.
- Cancelling is a status change; "what's scheduled" is a query.

## Related
- `background-jobs-and-caching` — the cron + Redis overlap lock that triggers the sweep; the delayed-job alternative (§4).
- `write-service-code` §9 (the transaction + multi-repo write) · `database-migrations` (the pending + history tables; push filters into SQL).
- `release-safety` (effective-dating a change is a safe way to roll one out) · `use-feature-flags` (the runtime-toggle alternative).
