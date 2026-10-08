---
name: sentry-issue-resolution
description: Fetch and resolve Sentry issues using the Sentry MCP. Use when given a Sentry issue ID, a production error report, a Sentry URL, a stack trace from Sentry, or when the user asks to investigate or fix a Sentry error.
---

# Sentry Issue Resolution

Diagnose and fix production errors reported in Sentry by fetching issue details via the Sentry MCP, tracing root causes through the codebase, and delivering validated patches.

## When to Use This Skill

- The user provides a **Sentry issue ID** (e.g., `6987204440`)
- The user shares a **Sentry URL** (e.g., `https://sentry.io/dh-pv-epaper/.../issues/...`)
- The user pastes a **stack trace** originating from Sentry
- The user asks to investigate a **production error** or **runtime exception**
- The user asks to triage or resolve **Sentry alerts**

---

## Step-by-Step Debugging Workflow

Copy this checklist and track progress:

```
Sentry Resolution Progress:
- [ ] Step 1: Fetch Sentry issue via MCP
- [ ] Step 2: Enter plan mode
- [ ] Step 3: Inspect stack traces
- [ ] Step 4: Identify the failing line of code
- [ ] Step 5: Analyze related files and dependencies
- [ ] Step 6: Determine root cause
- [ ] Step 7: Reproduce locally (if possible)
- [ ] Step 8: Write the patch
- [ ] Step 9: Run validation commands
- [ ] Step 10: Verify the fix
- [ ] Step 11: Summarize resolution
```

### Step 1: Fetch the Sentry Issue via MCP

Use the Sentry MCP to retrieve issue details. This MCP interaction is read-only and safe to perform before entering plan mode because it only gathers context and does not modify code or configuration. Typical MCP calls:

1. **Get issue details** — Retrieve the issue title, status, first/last seen timestamps, event count, and assigned tags.
2. **Get latest event** — Fetch the most recent event for the issue, which includes the full stack trace, request data, breadcrumbs, and context.

Extract and record:

- **Error type and message** (e.g., `TypeError: Cannot read properties of undefined (reading 'emails')`)
- **Environment** (DH_prod, PV_prod, DH_dev, PV_dev)
- **Browser/OS** from tags
- **Release version** if available
- **User impact** (event count, affected users)

### Step 2: Enter Plan Mode

After you have fetched and reviewed the basic Sentry issue details, **switch to plan mode before proposing or implementing any code changes.** Plan mode is required for all debugging and implementation work so the problem is fully understood first.

Announce the transition to plan mode and state the objective clearly, for example:

> "Investigating Sentry issue [ISSUE_ID]. Entering plan mode to analyze before making changes."

### Step 3: Inspect Stack Traces

From the event data, examine the stack trace carefully:

1. **Filter to application frames** — focus on frames inside `src/`, ignore `node_modules` and browser internals.
2. **Read top-down** — the topmost application frame is usually where the error manifests.
3. **Note the exact file path, function name, and line number** for each relevant frame.
4. **Check breadcrumbs** — Sentry breadcrumbs show the sequence of events (navigations, API calls, console logs) leading up to the error.

### Step 4: Identify the Failing Line of Code

Read the file indicated by the top application frame in the stack trace:

```
Read the file at the line number from the stack trace.
Include ±30 lines of context around the failing line.
```

Determine:

- What variable or property is null/undefined?
- What condition was not met?
- What API response shape was unexpected?

### Step 5: Analyze Related Files and Dependencies

Trace the data flow backwards from the failing point:

| Failing Area     | Files to Check                                                              |
| ---------------- | --------------------------------------------------------------------------- |
| Component render | The component file → its parent → props being passed                        |
| Hook logic       | The hook → context providers → API response types                           |
| API response     | Axios instance → API endpoint → response type definition in `src/types/`    |
| Auth/session     | `useAuth.ts` → `axiosSupertokensInstance` → SuperTokens config in `App.tsx` |
| State            | Context provider → reducer/setter → consumers                               |
| Payment          | `usePaymentHandler.ts` → `axiosAccessTypeInterface` → subscription types    |

Also check:

- **Type definitions** in `src/types/` — does the type match what the API actually returns?
- **Error boundaries** — is there a missing catch or fallback?
- **Optional chaining** — are null checks missing on data access paths?

### Step 6: Determine Root Cause

Categorize the root cause:

| Category                  | Common Causes                                                   |
| ------------------------- | --------------------------------------------------------------- |
| **Null/undefined access** | Missing optional chaining, API returning unexpected shape       |
| **Type mismatch**         | API response changed, type definition outdated                  |
| **Race condition**        | Component unmounted before async completes, stale closure       |
| **Auth failure**          | Session expired, token refresh failed, interceptor not catching |
| **Network error**         | API unreachable, CORS, timeout not handled                      |
| **Render error**          | Invalid JSX, missing key prop, conditional render on undefined  |

Document your finding clearly:

> Root cause: `useAuth` accesses `response.data.userData.emails[0]` without null-checking `userData`, which is `undefined` when the `/auth/me` endpoint returns a 204 with empty body.

### Step 7: Reproduce Locally (If Possible)

If the error is reproducible:

```bash
npm run start:dh   # or start:pv depending on the variant
```

Try to trigger the same code path:

- Navigate to the affected page/component.
- Simulate the conditions (e.g., logged-out user, expired session, empty API response).
- Check browser DevTools console for the same error.

If not reproducible (intermittent, environment-specific), proceed based on code analysis.

### Step 8: Write the Patch

Now switch to agent mode and implement the fix.

**Safe patching principles:**

- **Minimal change** — fix the root cause without refactoring unrelated code.
- **Defensive coding** — add null checks, optional chaining, or default values at the failure point.
- **Preserve existing behavior** — ensure all other code paths continue to work.
- **Match project conventions** — follow patterns from AGENTS.md (TypeScript strict mode, React Query for data fetching, TailwindCSS, etc.).
- **Error handling** — add try/catch or error state handling if missing. Log errors with `console.error` at minimum.
- **No silent failures** — if the error represents a user-facing problem, show a toast or fallback UI.

Example patterns for common fixes:

```typescript
// Null-safe property access
const email = apiUserData?.emails?.[0] ?? "";

// Default value for missing data
const userName = sanitizeName(fullName) || "User name";

// Guard clause in hook
if (!response?.data) {
  console.error("Empty response from /auth/me");
  return null;
}
```

### Step 9: Run Validation Commands

After implementing the fix, run all validation checks:

```bash
# Must all pass with zero errors/warnings
npm run type-check
npm run lint
npm run format

# Build verification
npm run build-local:dh
npm run build-local:pv
```

If any command fails, fix the issue before proceeding.

### Step 10: Verify the Fix

Confirm the fix addresses the root cause:

- [ ] The exact error scenario from the Sentry issue is handled.
- [ ] Edge cases are covered (null data, empty arrays, network failures).
- [ ] No regressions — related features still work correctly.
- [ ] Type safety — no new `any` types or type assertions introduced.
- [ ] The fix applies to both variants (dh and pv) if the affected code is shared.

### Step 11: Summarize the Resolution

Provide a structured summary:

```
## Sentry Issue Resolution

**Issue:** [ISSUE_ID] — [Error title]
**Environment:** [DH_prod / PV_prod / etc.]
**Root Cause:** [Concise explanation of why the error occurred]
**Fix:** [What was changed and why]
**Files Modified:** [List of changed files]
**Validation:** All type-check, lint, and build commands pass.
**Regression Risk:** [Low / Medium / High] — [brief justification]
**Follow-up:** [Any remaining work, monitoring, or related issues]
```

---

## Troubleshooting Guide

### Sentry MCP Not Responding

- Verify the Sentry MCP server is enabled in Cursor settings.
- Check that the Sentry auth token has the required scopes (`event:read`, `issue:read`, `project:read`).
- Try fetching the issue by direct Sentry API URL as a fallback.

### Stack Trace Points to Minified Code

- Check the Sentry release/source map configuration in the CI workflow.
- Look at the `environment` tag to determine which build produced the error.
- Use the error message and breadcrumbs to locate the source manually via grep.

### Issue Cannot Be Reproduced Locally

- Compare environment variables between local and production.
- Check if the issue is browser-specific (inspect Sentry's browser/OS tags).
- Look for timing-dependent issues (race conditions, slow network simulation).
- Check if the issue only occurs for specific user states (logged out, expired subscription, first visit).

### Multiple Errors in One Sentry Issue

- Sentry groups similar errors. Check the "Events" tab to see variations.
- The fix should handle all grouped variations, not just the most recent event.
- Verify by reviewing multiple events from the issue.

---

## Best Practices

1. **Never rush a fix** — understand the full context before changing code.
2. **Check event frequency** — high-frequency errors deserve more defensive handling.
3. **Consider user impact** — errors on payment or auth flows are higher priority.
4. **Update types** — if the API response shape doesn't match the TypeScript type, update the type definition in `src/types/`.
5. **Add breadcrumbs** — for complex flows, consider adding `Sentry.addBreadcrumb()` calls to improve future debugging.
6. **Monitor after deploy** — after the fix ships, check the Sentry issue to confirm the error rate drops to zero.
