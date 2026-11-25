---
name: deacon-install
description: "Install the Deacon support widget on a website or web app: place one script tag on every page, tell Deacon who is signed in, and confirm from the command line that a real page has loaded it. Use when asked to install Deacon, add its snippet or embed code, or set it up on a site."
---

# Install Deacon

Deacon is added to a site once: one script tag, on every page. How it looks is set on the Appearance page of the dashboard and updates on its own, so the tag never changes after it is placed. This is the dashboard's Install page as a document, for a coding agent doing the work.

Work through the steps in order. Steps 1 and 2 are the install; step 3 is the one a founder pasting the tag by hand almost never does, and it is what makes Deacon answer for the person in front of it rather than in general.

## Before you start

The founder needs a Deacon account and the site's key. Without one, they sign up at https://heydeacon.com/register (the free plan needs no card), open Install on the dashboard, add the site's domain and give you the `data-key` value from the snippet there. Never make up a key: without the founder's real key the widget won't load.

## 1. The domains

On the dashboard's Install page, the founder lists the domains the widget may run on. The widget appears on every page of those domains and nowhere else, and the first domain generates the site's snippet. A listed domain covers its subdomains, www included, so `acme.com` covers `app.acme.com` too. The scheme and port must match, except that `localhost` or `127.0.0.1` listed with no port covers every port. No `https://` is needed when typing one, and a development address (localhost, a `.test` or `.local` site, a private network address) typed without a scheme is saved with `http://`. On a domain that is not listed the widget stays hidden, although the loader has set its visitor cookie by then.

If the founder has no Deacon account yet, they sign up at https://heydeacon.com/register?utm_source=agent-guide. Setup asks for their website, saves it as the first domain and shows the snippet with the site's key on its Install screen, as the dashboard's Install page does.

This step is the founder's, on the dashboard. If the founder gave you the install prompt from Deacon's dashboard, it lists the domains as they stand. If the origin this app runs on is not among them, carry on with the install and say so at the end. Once a page there has loaded the tag, the Install page names that address, and adds it in one click when it is a development address or the listed site over another scheme or port. Either way it is the founder's to add, and nothing you can do from here.

## 2. The snippet

Paste the snippet just before the closing `</body>` tag on every page the widget should appear on. The founder copies it from the Install page with the site's own key in `data-key`; the key below is a placeholder.

```html
<script src="https://heydeacon.com/widget/v1/loader.js" data-key="pk_your_widget_key" async></script>
```

It loads in the background and never blocks the page. Anywhere HTML can be added takes it as it is: Shopify's `theme.liquid`, WordPress through a header-and-footer plugin, Webflow's or Framer's custom code, or a bare template.

In an app with a layout, the tag goes in the layout so it runs once for every page:

- Laravel: `resources/views/app.blade.php` or `layouts/app.blade.php`, before `</body>`.
- Next.js: the root layout, `app/layout.tsx`, as a plain script tag in the body or through `next/script` with the `afterInteractive` strategy.
- Rails: `app/views/layouts/application.html.erb`, before `</body>`.
- Any single-page app: the one HTML file that hosts it. The loader counts client-side navigations itself.

On an app built with one of the AI builders, the tag goes in the same place, and two of them document the route themselves:

- Lovable: the founder pastes Install's prompt for Lovable into the project chat and Lovable places the tag, which is what its own guide on embedding third-party widgets says to do. That prompt gives the key as `deacon_pk_…`, which is the same key. Lovable's chat takes a bare `pk_…` key for another service's and swaps it for a saved secret, so the bare snippet never goes into that chat. The code editor is read-only on the free plan, so on a free project the chat or the Git sync is the way in.
- Bolt: open Code view and paste it before `</body>`, or have the founder paste Install's prompt for Bolt into the chatbox. Its hosting documentation names both routes for third-party scripts, and leaves the location to the script's author. Check the published site rather than the preview. The preview runs at an address of its own, inside the browser on Chrome and hosted by Bolt on Safari, and the widget stays hidden on any address that is not in the allowed domains.
- v0: the root layout, `app/layout.tsx`, or `src/app/layout.tsx` in a project that keeps its code in a `src` folder. A plain script tag in the body, or `next/script` with the `afterInteractive` strategy. v0 does not document third-party scripts, so this is our instruction rather than theirs.
- Replit: the HTML file the deployment serves, or the layout if the app has one. Replit does not document third-party scripts either. If the project followed Replit's security checklist it may carry a `default-src 'self'` content security policy. That blocks the loader outright, and widening it takes four directives rather than one. `script-src`, `connect-src` and `frame-src` each need Deacon's origin, `https://heydeacon.com`, beside `'self'`: the first for the loader, the second for the settings request and the page, goal and error beacons, the third for the chat frame. `style-src` needs `'unsafe-inline'` beside `'self'`, for the style sheet the loader writes into its shadow root; a nonce cannot reach that sheet, and a hash would break with the next loader release. The replies stream inside the frame, under Deacon's own policy, so they need nothing here.

On Lovable and Bolt a custom domain is a paid feature, so a free project is published on a generated `lovable.app` or `bolt.host` subdomain. That generated address is the one that has to be in the allowed domains, or the widget stays hidden.

Never write the key anywhere else, and never load the script twice.

## 3. Tell Deacon who is asking

Deacon reads two things when the page loads:

- `window.deaconUser` is who is signed in: this app's id for them, their email and their name. The founder sees them on the conversation, and when Deacon can't answer, the visitor gets a reply with one tap instead of typing an address.
- `window.deaconContext` is what they're on. Deacon answers for that visitor instead of generically: it knows their plan, stops asking what the app already knows, and stops offering things they already have.

Do this when the app has signed-in users and its layout or its code can already reach the current user. Skip it on a site with no accounts, such as a plain marketing page, and say so in your report if the app has accounts but you couldn't find where it knows who is signed in: the install works without this step, and the founder can add it later.

```html
<script>
  window.deaconUser = {
    id: 'u_123',
    email: 'ana@studio.com',
    name: 'Ana Ruiz',
  };
  window.deaconContext = {
    plan: 'Pro',
    state: 'active',
    role: 'owner',
    seats: 4,
    trial_ends: '12 Aug',
  };
</script>
```

The block goes **above** the snippet, in the same layout, because the loader reads it as the widget is built. `deaconUser` takes `id`, `email` and `name` and nothing else. The context takes up to 12 keys; anything past the twelfth is dropped, as is a context over 1500 characters of JSON once serialized. Values should be strings, numbers or booleans.

Take the values from the session the app already has, not from a new request:

**Laravel.** In the layout, from the authenticated user. Blade's `@json` splits its argument at every comma, so an array written inside it stops the layout compiling. Use `Js::from`, which escapes the values rather than concatenating them into the script:

```blade
@auth
    <script>
        window.deaconUser = {{ Js::from([
            'id' => auth()->id(),
            'email' => auth()->user()->email,
            'name' => auth()->user()->name,
        ]) }};
        window.deaconContext = {{ Js::from([
            'plan' => auth()->user()->currentTeam?->plan_name,
            'state' => auth()->user()->currentTeam?->subscriptionState(),
            'role' => auth()->user()->role,
        ]) }};
    </script>
@endauth
```

`Auth::user()` and the `auth()` helper are the same thing; use whichever this codebase already uses. If the app puts this on a view composer or a shared Inertia prop, read it from there instead of querying again in the layout.

**Next.js.** In the root layout, which is a server component, from whatever session helper the app already uses — `auth()` with NextAuth, `getSession()`, a cookie-backed helper of its own:

```tsx
const session = await auth();
const safe = (value: unknown) => JSON.stringify(value).replace(/</g, '\\u003c');

return (
  <html>
    <body>
      {children}
      {session?.user && (
        <script
          dangerouslySetInnerHTML={{
            __html: `window.deaconUser = ${safe({
              id: session.user.id,
              email: session.user.email,
              name: session.user.name,
            })};
window.deaconContext = ${safe({
              plan: session.user.plan,
              state: session.user.subscriptionState,
            })};`,
          }}
        />
      )}
      <script src="…" data-key="…" async />
    </body>
  </html>
);
```

`JSON.stringify` alone does not keep a user-supplied value from closing the script tag: it leaves `</script>` in a string as it is. The `.replace(/</g, '\\u003c')` after it does, and the browser still reads the same values. Never interpolate a raw string into that block.

**Rails.** In `application.html.erb`, from `current_user`:

```erb
<% if current_user %>
  <script>
    window.deaconUser = <%= raw({
      id: current_user.id,
      email: current_user.email,
      name: current_user.name
    }.to_json) %>;
    window.deaconContext = <%= raw({
      plan: current_user.plan,
      state: current_user.subscription_state,
      role: current_user.role
    }.to_json) %>;
  </script>
<% end %>
```

**Anything else.** Render the same two objects server-side from the session, above the snippet.

**Signed out.** Where the layout knows nobody is signed in, such as the page a sign-out lands on, render `window.deaconUser = null;` instead. When the browser was last used by someone else, that starts the next person fresh: a new visitor, without the previous person's open chat. A page that says nothing about `deaconUser`, such as a marketing page on the same domain, changes nothing, and neither does someone signing in after chatting anonymously.

In the context, send what helps answer a support question — plan, subscription state, role, seat count, trial end, whether onboarding is finished. Send **never a password, a token, an API key or an internal id** there: the context is shown to Deacon's AI, and like `deaconUser` it is emitted into the page's HTML, so the visitor can read every value in it, and so can anyone they share a screenshot with. The user's own id belongs in `deaconUser`, which Deacon keeps from the AI and shows only to the founder. Both arrive from the visitor's browser, so Deacon treats them as a hint rather than proof: `deaconUser` labels this browser's chats and never opens anyone else's, until the app's server proves it (below).

**An app that learns who is signed in after the page loads**, such as a single-page app on Supabase auth (a Lovable app, say), or one that signs people in and out without a page load, tells Deacon from the code that hears the sign-in state:

```js
// once the app knows who is signed in, including a session it restores on load
window.deaconUser = { id: user.id, email: user.email, name: user.name };
window.Deacon?.identify(window.deaconUser);

// on sign-out, so the next person on this computer starts fresh
window.deaconUser = null;
window.Deacon?.identify(null);
window.Deacon?.setContext(null);
```

Set both, every time. The tag loads in the background, so this code can run before Deacon has started, while `window.Deacon` does not exist yet: the `?.` keeps the call from throwing, and Deacon reads `window.deaconUser` when it starts. After that, `Deacon.identify` is what reaches it. Wait until the app knows: setting `null` while it is still checking the session makes Deacon start the visitor afresh on every page load, without their open chat.

`Deacon.identify` replaces who is signed in. For the context, which changes more often (an upgrade, a plan switch), merge over it:

```js
window.Deacon?.setContext({ plan: 'Team', state: 'active' });
```

`Deacon.setContext` merges into what is already there. A key set to `null` is removed, and `setContext(null)` clears the lot.

If the project is TypeScript, declare both once so the code type-checks. If it already declares `Deacon` for goals, add these to that declaration:

```ts
type DeaconUser = {
    id?: string | number;
    email?: string;
    name?: string;
    token?: (nonce: string) => Promise<string>;
};

declare global {
    interface Window {
        deaconUser?: DeaconUser | null;
        Deacon?: {
            identify(user: DeaconUser | null): void;
            setContext(values: Record<string, unknown> | null): void;
        };
    }
}
```

### Prove who is signed in

`window.deaconUser` comes from the visitor's browser, so on its own it is a label. When the app's server signs it as well, Deacon trusts it: the conversation gets a tick, a reply reaches the person's email without them typing it, their chats follow them across their devices on the real site, and the founder can delete everything from one person. Do this as part of step 3 whenever the app has a server and you did step 3. It takes one route and one function on the page.

**The secret.** The founder makes it on the dashboard's Install page, under "Verify who's signed in", and sees it once. It goes on the app's server as the environment variable `DEACON_SECRET`. Read it from there; never write its value into the code, the page or the repository. The key is the whole secret as the Install page shows it, prefix included, used as it is (no decoding). If it isn't set yet, build the route anyway: it answers 204 until it is, and tell the founder to make the secret.

**The route.** `POST /deacon/token` on the app's own server, taking a JSON body `{"nonce": "..."}`. The path is a suggestion, but the `deacon-rails` gem and the `django-deacon` app (1.1.0 and later) mount exactly this one: they sign whoever is logged in with `DEACON_SECRET` and add the sign-out line, so a Rails or Django app needs no route of its own.

- When someone is signed in, answer 200 with a JWT as plain text, signed HS256 with `DEACON_SECRET`, carrying `sub`, `email`, `name`, the `nonce` it was given, and `exp` 10 minutes ahead. Deacon refuses a token that lasts more than 15 minutes, and allows a minute for clocks.
- When nobody is signed in, or the secret isn't set, answer 204 with no body.
- Always send `Cache-Control: no-store, private`, and never CORS headers. Otherwise a cache or another site could hand one person's token to someone else.
- `sub` is the user's id as a string, and it must be unique across the whole app. If ids repeat between workspaces or tenants, prefix them, as in `acme_42`.

In Laravel, with `firebase/php-jwt`, and `'deacon' => ['secret' => env('DEACON_SECRET')]` in `config/services.php`:

```php
use Firebase\JWT\JWT;
use Illuminate\Http\Request;

Route::post('/deacon/token', function (Request $request) {
    $user = $request->user();
    $secret = config('services.deacon.secret');
    $private = ['Cache-Control' => 'no-store, private'];

    if ($user === null || ! $secret) {
        return response('', 204, $private);
    }

    $token = JWT::encode([
        'sub' => (string) $user->id,
        'email' => $user->email,
        'name' => $user->name,
        'nonce' => (string) $request->input('nonce'),
        'iat' => time(),
        'exp' => time() + 600,
    ], $secret, 'HS256');

    return response($token, 200, [...$private, 'Content-Type' => 'text/plain']);
});
```

In Next.js, as `app/deacon/token/route.ts` with `jose`, from the session helper the app already uses. Auth.js leaves `id` off the session unless the `session` callback adds it, so add it there, or every user would be signed with the same `sub`:

```ts
// app/deacon/token/route.ts
import { SignJWT } from 'jose';
import { auth } from '@/auth'; // the same session helper as the layout

export async function POST(request: Request) {
  const session = await auth();
  const secret = process.env.DEACON_SECRET;
  const headers = { 'Cache-Control': 'no-store, private' };

  if (!session?.user?.id || !secret) {
    return new Response(null, { status: 204, headers });
  }

  const { nonce } = await request.json();
  const token = await new SignJWT({ email: session.user.email, name: session.user.name, nonce })
    .setProtectedHeader({ alg: 'HS256' })
    .setSubject(String(session.user.id))
    .setIssuedAt()
    .setExpirationTime('10m')
    .sign(new TextEncoder().encode(secret));

  return new Response(token, { status: 200, headers: { ...headers, 'Content-Type': 'text/plain' } });
}
```

**The page.** Give `window.deaconUser` a `token` function beside the three fields, and pass the same object to `Deacon.identify()`:

```js
window.deaconUser = {
  id: 'u_123',
  email: 'ana@studio.com',
  name: 'Ana Ruiz',
  token: (nonce) => fetch('/deacon/token', {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nonce }),
  }).then((r) => {
    if (r.status === 204) return '';
    if (!r.ok) throw new Error('Deacon token route answered ' + r.status);
    return r.text();
  }),
};
```

Where the layout renders `window.deaconUser` as JSON, as the Laravel, Next.js and Rails examples above do, add the function right after it, in the same script: `if (window.deaconUser) window.deaconUser.token = (nonce) => …`. Add the framework's CSRF header to the `fetch` where the framework checks one on a POST. Laravel does in `routes/web.php`: send `X-XSRF-TOKEN` from the `XSRF-TOKEN` cookie, or `X-CSRF-TOKEN` from the csrf meta tag, as the app's other requests do. Rails wants `X-CSRF-Token` from `csrf_meta_tags`, and Django `X-CSRFToken` from its `csrftoken` cookie. The function throws on any answer but 200 and 204, so a missing route or a refused CSRF check reaches Deacon as `unavailable` rather than looking like nobody is signed in.

The `token` function is the one exception to never passing Deacon a token. Deacon calls it only when the chat opens and shortly before a proof runs out, with a value that ties the token to that one chat session, and keeps nothing it returns. Keep the function out of anything that turns `window.deaconUser` into JSON. On sign-out, always call `window.Deacon?.identify(null)` as above: it ends the proof in every tab of that browser at once.

Use the secret on the real site only. Chats follow a person only between browsers that proved on the same site, so a staging or preview site needs its own Deacon team, with its own secret. A browser that has already proved on one of the founder's sites is refused as `linked` on another subdomain of the same domain, since the two share its visitor cookie.

**Checking it.** Deacon asks for a token only when the chat opens, so load a page while logged in and open the chat. Step 5's `signedIn.verifiedAt` moves when Deacon trusts someone, and `failure` names the last refusal in one word, newer than `verifiedAt` when it is the one to fix:

- `signature`: not signed with this secret. Check `DEACON_SECRET` holds the whole string, prefix included.
- `expired`: past its `exp`, or the server's clock is more than a minute out.
- `too_long`: `exp` more than 15 minutes ahead. Sign them for 10.
- `unreadable`: not an HS256 JWT with `exp` and `sub`, `sub` reads `undefined`, `null` or `[object Object]` because the user's id wasn't there when it was signed, or `sub` isn't one line of text. An `email` that isn't an address Deacon can send to, such as `test@localhost`, is left off and the token still verifies.
- `nonce`: the token didn't carry the nonce the page was given. Sign the `nonce` from the request body.
- `unavailable`: the page named someone, but the `token` function threw or took over 5 seconds, as it does when the route is missing, refuses the CSRF check or fails.
- `linked`: that browser already belongs to someone else, usually because sign-out doesn't call `Deacon.identify(null)`, or it proved on another of the founder's sites.

## 4. Open it from your own button

```html
<button onclick="Deacon.open()">Ask a question</button>
```

`Deacon.open()`, `Deacon.close()` and `Deacon.toggle()` are available as soon as the script has run.

With the Help button hidden on the Appearance page, Deacon paints nothing at all, and a button like this is the only way in. **If the prompt you were given says the Help button is hidden, adding one is not optional** — without it the install looks like it failed. Put it where this app's users already look for help: an item in the account or help menu, a link in the footer, a button at the bottom of an empty state.

When the team replies to a visitor who has closed the chat, the Help button shows a red count. A button of the site's own can show it too: the page hears a `deacon:unread` event on `window` whenever the count changes, with the number in `event.detail.count`, and 0 once the visitor opens the chat.

## 5. Check it went live

A sighting means a real page loaded the snippet. Ask for it here:

```
curl -s "https://heydeacon.com/api/widget/seen?k=SITE_KEY"
```

Put the site key in place of `SITE_KEY`; if you were given a prompt, it names the key and carries this address with the key already in it. Before anything has loaded:

```json
{"seen": null, "latest": null, "refused": null, "signedIn": null}
```

Afterwards:

```json
{"seen": {"origin": "https://acme.com", "lastSeenAt": "2026-09-06T14:02:10+00:00", "local": false, "fresh": true},
 "latest": {"origin": "http://localhost:3000", "lastSeenAt": "2026-09-08T09:14:22+00:00", "local": true},
 "refused": null,
 "signedIn": {"origin": "http://localhost:3000", "lastSeenAt": "2026-09-08T09:14:22+00:00", "local": true,
              "verifiedAt": "2026-09-08T09:15:03+00:00", "failedAt": null, "failure": null}}
```

Two answers about sightings, because there are two questions. `seen` is the one the founder's Install page asks — are you live — so it prefers a real deployment and keeps reporting it once one has been heard from. `latest` is the one you are asking: the newest sighting whatever its origin, which is the only one that moves when you install into a dev environment on a site that is already live.

`local` is true for a development address (localhost, 127.0.0.1, a `.test` or `.local` site, or a private network address), which is a working install rather than a launch. `fresh` is false when nothing has been heard for a day, or when the founder has removed every domain.

`signedIn` answers step 3: where and when a page last loaded Deacon with someone signed in, through `window.deaconUser` or `Deacon.identify()`. It says whether, never who, so no id, email or name is ever in it. Like `latest`, it is the newest sighting whatever its origin, so it moves when you test on your own machine, and `local` says which it was. It stays null until a page has loaded with someone signed in, and moves at most once every ten minutes for each address. A page carrying `data-no-page-views` still counts, since this is not a page view.

If you added the token route, `verifiedAt` is when Deacon last trusted someone signed in, and `failedAt` and `failure` the last refusal, in the words step 3 lists. Watch `verifiedAt` move: a failure is never cleared, only outdated by a newer `verifiedAt`, and anyone holding the key can cause one, so a `failure` older than `verifiedAt` is nothing to fix. Like `lastSeenAt`, each moves at most once every ten minutes for each address, so a retest within ten minutes of the last one may leave them as they were.

**Ask once before you start, and keep the answer.** A site that has been running Deacon already answers straight away with its own sighting, so a non-null first call is evidence of nothing you did. What you are waiting for is `latest` changing.

A sighting only happens on an address the list covers. Loaded anywhere else, the tag stays hidden. When that address is a development address, or a listed site over another scheme or port, `refused` names it and when it was turned away, for up to a day. Any other address, such as a tunnel or a preview deploy, is named only on the founder's Install page, since this answer is open to anyone holding the key.

For a dev server on localhost that isn't on the list, the answer reads like this.

```json
{"seen": null, "latest": null,
 "refused": {"origin": "http://localhost:3000", "lastSeenAt": "2026-09-08T09:14:22+00:00"},
 "signedIn": null}
```

If `refused` names the address you are testing on, stop waiting, because nothing will arrive there until the founder adds it. Tell them to add it on the Install page, which names it and adds localhost or a `.test` site in one click. Or finish the change and have them deploy it to a listed domain instead.

You almost certainly have no browser, and a sighting cannot be faked, so the usual path is:

1. Call the address once. Note `latest.lastSeenAt`, or that `latest` is null, and the same for `signedIn` if you did step 3.
2. Start the app's dev server.
3. Ask the founder to open one of its pages in their browser, signed in if you did step 3, and wait.
4. Poll every few seconds until `latest` stops being null, or `latest.lastSeenAt` moves past the one you noted. Give it a couple of minutes before concluding something is wrong.
5. If you did step 3, keep polling the same way until `signedIn` stops being null, or `signedIn.lastSeenAt` moves past the one you noted.
6. If you added the token route and `DEACON_SECRET` is set, ask the founder to load a page while logged in and open the chat, then keep polling until `signedIn.verifiedAt` moves past the one you noted. If `failure` names a word newer than it, fix what step 3 says and try again.

If you do have a headless browser, load a page of the running app yourself and skip the asking. For `signedIn` that page has to be one someone is signed in on, and for `verifiedAt` load a page while logged in and open the chat, with `Deacon.open()`.

**Never request the config endpoint by hand to make a sighting appear.** A sighting is the evidence that the tag is on a page that really loads; a request you make yourself proves only that you can make requests.

If nothing arrives and `refused` is null too, the page may be on an address the list doesn't cover that this answer won't name, such as a tunnel or a preview deploy. Otherwise the tag is not in a layout that page uses, the key is wrong, or the dev server is serving a cached build. When the address isn't listed or the key is wrong, the page's browser console says so in a line starting `[Deacon]`.

## Tell the founder what you did

End with a short report, and be specific:

- Which files you changed, and where the tag went.
- What you put in `window.deaconUser` and `window.deaconContext`, and where those values come from.
- Whether you added a button of your own, and where it is.
- Where the widget was seen — the origin under `latest`, which is the page you caused to load. If `latest.local` was true, say so plainly: **seen on localhost — add your real domain on the Install page when you deploy**, and name the domain to add.
- Whether a signed-in visitor was seen: the origin under `signedIn`, and whether it was local. If it is still null, say why: nobody has loaded a page signed in since the change, or the app has no accounts and you skipped step 3.
- Whether a visitor was verified: where you put the token route and the `token` function, whether `signedIn.verifiedAt` moved, and the `failure` word if one is newer. If `DEACON_SECRET` isn't set yet, say they make it on the Install page and set it on the server, and that the route answers 204 until then.
- If the address you tested on isn't covered by their list, say which address they need to add, and that only they can add it, on the Install page.

Then point them at the next step: counting sign ups, paywall hits and upgrades on their dashboard, which the deacon-goals skill sets up.

## Page views, with no further step

Once the snippet is on a site, Deacon counts page views, visits, sources, pages, countries and devices on Analytics › Website. Page views are counted without a cookie, from a hash that changes every day, and no IP address is kept for them. The widget itself sets one cookie, `deacon_visitor_id`, when it loads, and keeps the same id in local storage, so list it in the site's cookie policy. Once a visitor opens the chat, it also keeps `deacon_chats` in local storage, never as a cookie, which lapses 30 days after they last opened the chat. On a site that tells Deacon who is signed in, it keeps that person's id (or email) as `deacon_signed_in` in local storage, so it can start the next person on a shared computer fresh, and removes it when they sign out. Nothing is counted from a development address, from automated browsers or from a domain that is not listed.

To keep pages out of the count — an app's signed-in routes, say, so the founder's own clicking is not traffic — add `data-no-page-views` to the script tag on those pages. It stops page views and JavaScript errors, and never stops a goal: a goal only fires because the site asked for it by name, and the moments most worth counting happen behind a login. The attribute is read afresh for every page view, not once when the script loads, so in a single-page app it has to be kept in step with the router rather than set at the start:

```js
// Wherever the app handles a route change.
document
  .querySelector('script[src*="/widget/v1/loader.js"]')
  ?.toggleAttribute('data-no-page-views', isSignedInRoute(path));
```

Miss that in a single-page app and the attribute describes only whichever page the visitor loaded first.

## After it's live

Tell the founder what their code and their coding agent can do with Deacon, and offer to set up whatever they want. It's all on every plan, and they make any key or webhook it needs on the Integrations page of the dashboard.

- **Connect their coding agent**, which may be you, so it can read what visitors asked and reported, and fix it. Use the deacon-connect skill to connect it to Deacon's MCP server.
- **Webhooks**, so their code hears when a visitor reports a bug or leaves their email. Webhooks are in the API docs at https://heydeacon.com/docs/api#webhooks.
- **The API**, so their code can read chats, add to what Deacon knows and reply to visitors. The API docs are at https://heydeacon.com/docs/api.
