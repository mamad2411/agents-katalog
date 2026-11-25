---
name: block-disposable-emails
description: >-
  Reject throwaway/disposable email addresses at signup by checking the domain
  against a maintained list, so spam accounts, trial-abuse, and fake signups
  drop sharply. Use this whenever the user is building or hardening a signup /
  registration / waitlist flow and mentions fake accounts, throwaway emails,
  mailinator / 10minutemail / temp-mail, trial abuse, bot signups, junk users,
  or wants to "improve signup quality" or "stop disposable emails." Reach for it
  when adding an auth/signup endpoint even if the user hasn't named disposable
  email yet — it's a cheap, high-leverage guard. Produces a server-side check
  (works on Node, edge runtimes like Cloudflare Workers, etc.) and the rules for
  layering it with a CAPTCHA and email verification.
---

# Block disposable emails at signup

If anyone can sign up with any email, a chunk of your "users" will be throwaway
inboxes — `mailinator.com`, `10minutemail.com`, and hundreds more. They're how
people farm free trials, dodge bans, and pad the numbers with accounts that
never convert. Checking the signup domain against a community-maintained list of
disposable domains takes minutes and cuts a surprising amount of junk.

## The check

Use the continuously-updated
[`disposable/disposable-email-domains`](https://github.com/disposable/disposable-email-domains)
list (`domains.json`, tens of thousands of domains). Fetch it, cache for a day,
load into a `Set`, and membership-test the domain after the `@`. A `Set` lookup
is O(1); the daily cache means you're not hammering the CDN.

```ts
const LIST =
  "https://rawcdn.githack.com/disposable/disposable-email-domains/master/domains.json";

let cache: Set<string> | null = null;
let fetchedAt = 0;

async function disposableDomains() {
  if (cache && Date.now() - fetchedAt < 86_400_000) return cache; // 1 day
  const res = await fetch(LIST);
  cache = new Set<string>(await res.json());
  fetchedAt = Date.now();
  return cache;
}

export async function isDisposableEmail(email: string) {
  const domain = email.split("@")[1]?.toLowerCase().trim();
  if (!domain) return false;
  return (await disposableDomains()).has(domain);
}
```

Guard the signup handler:

```ts
if (await isDisposableEmail(email)) {
  return new Response("Please use a permanent email address.", { status: 422 });
}
```

## Rules that make it actually work

- **Server-side only.** The check belongs at the signup endpoint. A client-only
  check is trivially skipped — never trust it.
- **Cache correctly for the runtime.** On an edge runtime like Cloudflare
  Workers, module-scope memory may not persist between requests; back the cache
  with KV (or similar) so you're not refetching the list constantly.
- **Use the maintained list, not a hand-rolled regex.** A regex of domains you
  remember goes stale the day after you write it. The list doesn't.
- **Layer it — no single signal is enough.** Stack cheap independent filters:
  a CAPTCHA (Cloudflare Turnstile / hCaptcha) stops bots before submit, the
  disposable-domain block stops throwaway humans, and a verification email at
  the end still requires a real, owned inbox. Each is minutes of work; together
  they compound.

---

From [seangeng.com/writing/block-disposable-emails](https://seangeng.com/writing/block-disposable-emails).
Part of [github.com/seangeng/skills](https://github.com/seangeng/skills).
Credit: [@venelinkochev](https://x.com/venelinkochev/status/2042573164245336451).
