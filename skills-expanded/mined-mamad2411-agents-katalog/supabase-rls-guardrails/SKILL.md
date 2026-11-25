---
name: supabase-rls-guardrails
description: Row Level Security and anon-access checklist for any Supabase schema, policy, or Storage bucket change. Use whenever writing a migration, adding a table/bucket, adding or editing an RLS policy, or writing a SECURITY DEFINER function — before applying it, not just when asked to audit security.
---

# Supabase RLS Guardrails

This app has multiple anonymous, no-login write surfaces (`/f/:shareId`, `/c/:portalId`, client file uploads). The client is never a trust boundary — every guarantee has to live in the policy or function itself. Check this before applying any migration, not after.

## Before writing a policy

- **RLS must be enabled on the table**, not just have policies attached. A table with RLS off and policies defined enforces nothing.
- **Anon access is scoped by an unguessable id**, never `true` or a guessable value. If a policy needs to check "does this row/folder belong to a real share/portal," write it as a `SECURITY DEFINER` function so anon never touches the underlying table directly — mirror the existing `get_discovery_share`/`is_client_upload_target` pattern.
- **Insert-only when only inserts are needed.** Don't grant update/delete to `anon` by default — a stranger with one valid link should not be able to overwrite or destroy someone else's row.

## Inside a SECURITY DEFINER function

- `set search_path = public, pg_temp` — always, no exceptions.
- `revoke all ... from public` then explicit `grant execute ... to anon, authenticated` — never rely on the default grant.
- **Validate input before using it in a query.** Casting an arbitrary string to `::uuid` throws if it isn't one — that surfaces as a 500 to an anonymous caller instead of a clean "no". Regex-check the shape first, return false/null on a miss.
- Single-use tokens (share status, form submission) must be checked and flipped **inside** the function, atomically — never trust the client to only call it once.

## Before shipping

- Read the actual policy back with `execute_sql` against `pg_policies` — don't trust what the migration file says was intended; confirm what's actually live.
- If a new anon-write surface is added, re-run through this whole list for it specifically — each one is a fresh trust boundary, not a copy that inherits safety from an existing one.
