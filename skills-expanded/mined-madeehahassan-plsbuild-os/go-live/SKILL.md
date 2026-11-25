---
name: Go-Live
description: Pre-launch checklist. Use before making any app public, sharing a link externally, or announcing a product launch. Adapts to Claude Code, claude.ai, and Cowork.
---

# /go-live

Run this before making any app public. Before sharing a link. Before announcing anything.

Work through each section in order. Don't mark things done until they actually are.

---

## Which surface are you on?

**Claude Code**
You can run the checks directly. Execute terminal commands (`npm run build`, `grep -r "sk-" src/`), read files, open URLs. Report back what you found. For anything that needs a browser (auth flow, mobile test, live URL), ask the user to do it and confirm.

**claude.ai chat**
You can't run commands or read files. Walk the user through each check. For terminal-style checks, give them the exact command to run and ask them to paste the output. For browser checks, give them the steps and ask them to confirm.

**Cowork**
You have access to the workspace files. Read code to verify things like API-key placement, try/catch coverage, and RLS policies. For terminal commands and live-URL tests, walk the user through them the way you would in chat.

Either way, work through the checklist one section at a time. Don't batch.

---

## Section 1: Auth and user data

- [ ] Sign up works
- [ ] Login works
- [ ] Session persists on page refresh
- [ ] Logout clears session completely
- [ ] Protected pages redirect to login if not authenticated
- [ ] Password reset flow works end to end
- [ ] Every user only sees their own data
- [ ] No data shared between users (test with two separate accounts)
- [ ] Empty state shown when user has no data yet
- [ ] If using Supabase: row-level security enabled and tested

These all require real browser testing. Walk the user through sign-up → login → refresh → logout → protected page → second-user-test. On Code/Cowork, you can read the RLS policies in the codebase to confirm they match; the user still tests the flows.

---

## Section 2: API security

- [ ] Zero API keys in client-side code
- [ ] Zero API keys in git (.env in .gitignore)
- [ ] All keys in environment variables in hosting dashboard
- [ ] Keys only accessed via server-side functions
- [ ] User inputs validated before hitting the database
- [ ] Per-user rate limiting in place if using an AI API

**The API-key scan:**

- **Code:** run `grep -rE "sk-|api[_-]?key" src/` and report what you find
- **Cowork:** search the open workspace files for the same patterns
- **Chat:** paste the command and ask the user to run it and paste the result

Anything returned that isn't a reference to `process.env` or a hosted-key pattern is a blocker.

---

## Section 3: Cost controls

- [ ] Free tier limits defined
- [ ] Usage tracked per user in database
- [ ] Spend alerts set up in AI API console
- [ ] Estimated cost per active user per month calculated

The user has to check the AI API console themselves on every surface. You can help them do the math on cost-per-user if they paste pricing + expected usage.

---

## Section 4: Error handling

- [ ] Every API call has try/catch
- [ ] Users see friendly error messages, never raw error text
- [ ] Every async operation shows a loading indicator
- [ ] Buttons disabled while loading (no double-submits)

On Code/Cowork, read the code. Grep for `fetch(` or `await ` and check each one has a catch path. On Chat, ask the user to paste the files that make API calls.

---

## Section 5: Performance

- [ ] Initial page load under 3 seconds
- [ ] Build completes with zero errors
- [ ] No console errors in production build

Build command and console check are browser/terminal work. On Code, run the build and report. On Chat/Cowork, give the user the command and ask them to paste output.

---

## Section 6: Mobile

- [ ] Test at 375px (iPhone SE)
- [ ] No horizontal scroll
- [ ] All tap targets at least 44x44px
- [ ] Forms usable with mobile keyboard open

Real device or devtools responsive mode. User runs the test. On Code/Cowork, you can scan the CSS for tap-target sizes and obvious mobile issues, but actual rendering has to be checked in a browser.

---

## Section 7: Legal minimum

- [ ] Privacy Policy page exists
- [ ] Terms of Service page exists
- [ ] If EU users: GDPR basics covered
- [ ] Any AI-generated content appropriately disclaimed

User confirms these exist by opening the URLs. You can draft the copy for any missing page if asked.

---

## Section 8: Production deploy

- [ ] All environment variables set in hosting dashboard
- [ ] HTTPS working
- [ ] Full end-to-end test on the production URL (not localhost)
- [ ] Test on mobile browser

Hosting dashboard check is always the user. End-to-end test is the user. You can help interpret any errors they paste back.

---

## Section 9: Soft launch

- [ ] App has run for at least a few days without breaking
- [ ] You've used it yourself daily and fixed rough edges
- [ ] Feedback mechanism exists
- [ ] You know the one thing you most want feedback on

This is calendar time and founder intuition. No code to check.

---

## Verdict

**Ready:** all sections complete, no blockers.
**Not ready:** list the blocking items with estimated effort to fix.
**Ready with caveats:** core is ready, non-critical items noted for v1.1.

Don't sugarcoat. If there's a blocker, say so clearly. The founder decides whether to ship anyway.
