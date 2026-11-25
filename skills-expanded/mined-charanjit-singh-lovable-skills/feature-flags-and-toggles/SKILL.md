---
name: feature-flags-and-toggles
description: >-
  Use when adding feature flags, gradual rollouts, beta features, kill switches,
  or per-user/per-org feature toggles. Not for plan-based gating (use
  pricing-and-billing) unless flags wrap plan checks too.
---

# Feature flags and toggles

Ship code dark, enable per user/org/percentage, kill instantly when broken.

## Storage

| Option | When |
|--------|------|
| Env var (`VITE_FEATURE_X`) | Static, build-time toggles |
| DB table `feature_flags` | Dynamic, per user/org, no extra vendor |
| PostHog / LaunchDarkly / Statsig | Targeting, gradual rollout, A/B |

For most Lovable apps, start with a DB table and graduate to a vendor if you need targeting.

## DB-backed flags

```sql
create table public.feature_flags (
  key text primary key,
  enabled_globally boolean not null default false,
  enabled_user_ids uuid[] not null default array[]::uuid[],
  enabled_org_ids uuid[] not null default array[]::uuid[],
  rollout_percent int not null default 0 check (rollout_percent between 0 and 100),
  updated_at timestamptz not null default now()
);

alter table public.feature_flags enable row level security;
create policy "anyone_authenticated_can_read_flags" on public.feature_flags
  for select to authenticated using (true);
```

Write access via service role only (admin UI / SQL editor).

## Resolver

```ts
export function isFlagOn(flag: FeatureFlag, ctx: { userId?: string; orgId?: string }): boolean {
  if (flag.enabled_globally) return true;
  if (ctx.userId && flag.enabled_user_ids.includes(ctx.userId)) return true;
  if (ctx.orgId && flag.enabled_org_ids.includes(ctx.orgId)) return true;
  if (flag.rollout_percent > 0 && ctx.userId) {
    return hashPercent(`${flag.key}:${ctx.userId}`) < flag.rollout_percent;
  }
  return false;
}
```

`hashPercent` should be a stable hash (e.g. djb2 mod 100) so the same user keeps the same bucket.

## Hook

```ts
export function useFlag(key: string) {
  const { user } = useUser();
  const { flags } = useFlags();
  return useMemo(
    () => isFlagOn(flags[key] ?? defaultFor(key), { userId: user?.id, orgId: user?.org_id }),
    [flags, key, user],
  );
}
```

Use:

```tsx
{useFlag("new_dashboard") ? <NewDashboard /> : <OldDashboard />}
```

## Rules

- **Default off** in production; default on only after rollout finishes.
- Remove the old branch within 2–4 weeks of 100% rollout — flags accumulate as tech debt.
- Server-side gating for security-sensitive flags (don't trust the client).
- Document the flag key, owner, and expected removal date in code or a `FLAGS.md`.

## Kill switch

For features that can break the app (new payment flow, new auth provider), ensure the flag check happens **before** the risky code path so flipping the flag instantly reverts behavior.

## Avoid

- Hundreds of long-lived flags — clean up after rollout.
- Different flag keys for the same concept across client and server.
- Targeting by email substring in production code.
- Flags that gate styling only — use CSS instead.

## Checklist

- [ ] Flag has a default and an owner.
- [ ] Old branch removed after 100% rollout.
- [ ] Server enforces security-sensitive flags.
- [ ] Toggle works without a deploy.
