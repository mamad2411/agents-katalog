---
name: setup-maple-org
description: Register and install the Maple GitHub App for an organisation, wire the SDK route to it, and verify that a reviewer can sign in from a preview and post a pull-request comment. Use when setting up Maple for the first time in an organisation, installing the Maple GitHub App, changing which repositories are reviewable, or working out how reviewers sign in to Maple.
---

# Set up Maple for an organisation

This is the one-time setup a person with organisation owner rights has to do.
Nothing here can be automated from inside a repository: creating a GitHub App
and installing it both need a browser and an owner.

It takes about fifteen minutes. Work top to bottom; later steps use values
earlier ones produce.

**Maple uses two GitHub Apps, and this file registers one of them.** The
comment App authenticates as the reviewer and carries `Pull requests`; the
gate App authenticates as itself and carries `Checks`.
They are separate because a user-to-server token carries every permission its
App holds, so merging them would hand each reviewer's token the gate's reach.
Section 6 says when to register the second one. Do not add `Checks` here.

On a personal account rather than an organisation, every path below is
**Settings → Developer settings** instead of **Organisation settings →
Developer settings**, and there is no organisation to choose when installing.
Nothing else differs.

Read `docs/github-auth.md` before or after, depending on whether you want the
reasoning first. This file is the sequence; that file is why the sequence is
this one. Every `docs/` path here is in the Maple repository, at
<https://github.com/maple-kit/maple/tree/main/docs>.

Throughout, `acme` is your organisation and `acme/web` a repository you want
reviewable. Substitute your own.

The CLI does the parts of this that can be generated: `npx @maple-kit/cli@0.24.0
setup app --owner=acme` prints the prefilled registration URL (`--gate` for the
gate App), `setup verify --client-id=<Iv…>` checks Device Flow, and `setup ci`
prints the gate workflow. Flags take `--flag=value` or `--flag value`.

## 1. Register the GitHub App

Go to **Organisation settings → Developer settings → GitHub Apps → New GitHub
App** and fill it in as follows.

| Field                                             | Value                                          |
| ------------------------------------------------- | ---------------------------------------------- |
| GitHub App name                                   | `Maple — acme`                                 |
| Homepage URL                                      | Your Maple deployment, or the Maple repository |
| Callback URL                                      | Your organisation's home page                  |
| Request user authorisation (OAuth) during install | Off                                            |
| Enable Device Flow                                | **On**                                         |
| Expire user authorisation tokens                  | **On** (recommended) or Off                    |
| Webhook → Active                                  | Off                                            |
| Where can this app be installed?                  | Only on this account                           |

Four of those need saying out loud.

**The App name has to be globally unique on GitHub.** `Maple` is taken.
Including your organisation in the name is the simplest way through, and
reviewers see it on the authorisation screen, so make it recognisable.

**The callback URL is never used.** Device Flow does not redirect anywhere, but
GitHub's form refuses to save without a value. Put your organisation's home page
in and ignore it.

**Device Flow must be on.** It is what lets a reviewer sign in from a preview
host whose URL is different on every deployment. Without it, the first sign-in
attempt fails with `device_flow_disabled` and nothing else about this setup
matters.

**Expire user authorisation tokens: on is recommended, off is supported.** On,
tokens die after eight hours (fixed by GitHub), nothing refreshes them, and the
reviewer signs in again with a new device code; drafts are kept. Refreshing
would need the App's `client_secret` in every preview, which this design
forbids. Needs `@maple-kit/core` 0.24.0 or later. Off, there is no re-sign-in,
but a leaked token works until the reviewer revokes it; the cookie is still
checked against `maxAgeSeconds`.

Then set **Repository permissions** to exactly this, and nothing more:

| Permission      | Access         |
| --------------- | -------------- |
| `Pull requests` | Read and write |

`Metadata: Read-only` is added by GitHub and cannot be removed. Leave every
other permission at **No access** — in particular `Contents`, which Maple does
not need because it never reads or writes repository code.

**`Issues` stays at No access, although the endpoints look like it needs it.**
A pull-request conversation comment _is_ an issue comment, so every call Maple
makes goes to `/repos/{owner}/{repo}/issues/…` and it is tempting to grant
`Issues: Read and write`. GitHub lists those endpoints under **both**
permissions and authorises a comment on a pull request under `Pull requests`,
so granting `Issues` would hand every reviewer's token write access to every
issue in the repository and buy nothing. `docs/github-auth.md` has the full
reasoning.

Create the App. You do not need to generate a private key: the private key is
for an App acting as itself, and Maple's comment path never does.

**Creating the App is not the end of this step.** GitHub drops you on a
settings page that looks like a finish line, and it is not one: an App that
exists but is installed nowhere can see no repository at all. Everything you
need for section 3 is on the screen in front of you, so it is possible to
configure Maple completely, sign a reviewer in successfully, and only find out
at the first comment. Keep going.

## 1a. Give it the Maple logo

Still on that settings page, under **Display information**: drag the Maple
avatar onto **Upload a logo**, click **Set new avatar**, and set **Badge
background colour** to `#fdf8e8`.

**The badge colour is the plate, not the leaf.** GitHub puts the square logo
inside a circle filled with that colour, and the leaf is green throughout, so
setting the plate to a green makes the leaf disappear into it — which is
exactly what it looks like in the corner of a reviewer's avatar on every
comment, at sixteen pixels. Cream is the contrast the mark was drawn for. The
field only appears once a logo is uploaded.

The avatar is `docs/assets/app-logo.png` in the Maple repository — the pixel
leaf, 1024 square on a transparent ground, well inside GitHub's 1 MB limit. It
is drawn to survive being shrunk: the whole square is leaf, because a margin
is the one thing a sixteen-pixel badge cannot afford. Download it without
cloning:

```
curl -O https://raw.githubusercontent.com/maple-kit/maple/main/docs/assets/app-logo.png
```

`docs/branding.md` records what it is drawn from and how to enlarge it, for an
organisation that would rather render its own.

**There is no other way to do this.** GitHub's App manifest has no logo field
and its REST API has no endpoint for an App's avatar, so it is a browser step
or it does not happen — which is why it is a step here rather than something
Maple configures for you.

Skipped, the App wears GitHub's grey default on the authorisation screen every
reviewer sees, which is the one moment Maple has to look like something a
person should hand their account to.

## 2. Install it on repositories

From the App's page, **Install App → acme**, then choose **Only select
repositories** and pick the ones that should be reviewable. The direct URL is
`https://github.com/apps/<slug>/installations/new`, where `<slug>` is the last
path segment of the App's public page — `Maple — acme` becomes `maple-acme`.

Install it on the repositories you actually review. The set you choose here is
the blast radius of every reviewer token Maple will ever issue, so keeping it
small is worth the minute it costs. You can add repositories later without
anyone signing in again.

Confirm it landed: the App should now appear under
**Settings → Applications → Installed GitHub Apps** (organisation owners see it
under the organisation's **Installed GitHub Apps** instead), listing the
repositories you picked.

## 3. Copy the client id and the slug

On the App's settings page, copy the **Client ID**. It starts with `Iv` and is
not the App ID printed above it — the two are easy to confuse and only one of
them works.

It is public. It appears in the authorisation URL every reviewer sees, and it is
safe in a preview environment, a build log and a configuration file in your
repository. It is the only GitHub identifier the preview needs.

Do not put an App ID, a private key or a client secret anywhere near a preview
environment.

Write down the **slug** beside it, from the App's public URL
(`https://github.com/apps/<slug>`). Nothing in Maple reads it, but every later
question about this App is answered through it: `gh api /apps/<slug>` describes
the App without credentials, `https://github.com/apps/<slug>/installations/new`
adds a repository, and there is no way to recover it from the Client ID — GitHub
publishes no mapping between the two.

## 4. Configure the SDK route

Set `MAPLE_GITHUB_CLIENT_ID` and `MAPLE_SESSION_SECRET` in the preview
environment. The secret is required: at least 32 random bytes
(`openssl rand -base64 48`), and it seals the reviewer's cookie so nobody can
read or forge a session. Both go in your host's preview environment variables,
not in a file in the repository. The client id is public and the session secret
is a secret; `docs/configuration.md` names every variable Maple's halves need and
which side of that line each falls on.

Mount the route behind your preview flag so it never exists in production:

```ts
import { createCommentStore } from "@maple-kit/core";
import { readGitHubSession } from "@maple-kit/core/auth";
import { createPullCache, githubStore } from "@maple-kit/core/connectors";
import { consoleSink, createLogger } from "@maple-kit/core/logger";
import { createMapleHandler } from "@maple-kit/core/route";

const secret = process.env.MAPLE_SESSION_SECRET!;
const logger = createLogger({ sinks: [consoleSink()] });
const pulls = createPullCache();

const mounted =
  process.env.MAPLE_PREVIEW === "1"
    ? createMapleHandler({
        logger,
        store: async (request) => {
          const session = await readGitHubSession(request, { secret });
          if (!session) return null;
          return createCommentStore(
            githubStore({
              owner: "acme",
              repo: "web",
              token: session.token,
              cache: pulls,
            }),
          );
        },
        githubAuth: {
          clientId: process.env.MAPLE_GITHUB_CLIENT_ID!,
          secret,
        },
      })
    : () => new Response("Not found", { status: 404 });

export { mounted as DELETE, mounted as GET, mounted as PATCH, mounted as POST };
```

`createCommentStore` is what the route takes: the connector is the backend, the
store around it is what carries Maple's retries, its timeout and its one error
type. The store is built per request from the reviewer's own token, which is
what makes the comment show up under their name rather than a bot's. Returning
`null` — nobody has linked yet — makes the route answer `401`, and the overlay
offers **Link GitHub** rather than writing the comment as somebody else.

**Both of the other two arguments earn their place.** A connector's message is
deliberately kept out of the browser, so without `logger` every failure below
is a `500` with its cause recorded nowhere — which is most of this file's
troubleshooting turned into guesswork. And a store built per request gets a
new closure every time, so `cache` is where a resolved pull request is
remembered; without it every call asks GitHub which pull request the branch
belongs to, again.

`githubAuth` is what serves the three link endpoints. Without it they answer
`404`, which is the right shape for a deployment that stores comments some
other way and needs no GitHub sign-in at all.

### The assist tier, if you want it

Maple can score a comment against five pillars as the reviewer types it. It is
advice and never a gate — it cannot block a send or reach the check run — and
the whole tier is off unless a classifier is configured.

Turning it on is one package, one option and one secret. The classifier
package takes Effect 4 and the TypeSafe provider as peers, both still release
candidates, so install them with it:

```sh
npm install @maple-kit/classifier effect@rc @effect/ai-typesafe@rc
```

```ts
import { jevClassifier } from "@maple-kit/classifier";

const key = process.env.TYPESAFE_API_KEY;
// …on the same createMapleHandler call:
...(key ? { assist: { classifier: jevClassifier({ apiKey: key }) } } : {}),
```

`TYPESAFE_API_KEY` keeps the provider's name rather than a `MAPLE_` one, so a
rejected key says where to go. It is a real secret and it belongs wherever the
deployment keeps those — never in a ConfigMap beside the client id.

**Read it on the server and pass it in; never ship it to the browser.**
`/assist` is same-origin on the route that already exists, which is also what
keeps `connect-src` unchanged. Absent a key, drop the option: the endpoint
answers `404`, `/me` says nothing about it, and the composer draws what it drew
before. `docs/assist.md` is the design and `docs/configuration.md` has the
table.

## 5. Verify it end to end

Do all six. Stopping at the fourth is how a setup that looks finished turns out
not to be: linking succeeds whether or not the App is installed anywhere, so
the first four steps pass on an App that can read nothing.

1. Open a preview for a branch that has an open pull request — say `web-482`
   against `acme/web`.
2. Click **Link GitHub** in the overlay. You should see an eight-character code
   and a link to `https://github.com/login/device`.
3. Enter the code and authorise. The authorisation screen should show the
   Maple leaf, name your App, and list `Pull requests` and nothing else. A
   grey default avatar means section 1a was skipped; it costs nothing but the
   first impression, and it is fixed without anyone signing in again. If it also lists `Issues`, the
   permissions are wider than they need to be; fix them in section 1.
4. **Before writing anything, watch the comment list load.** It should say the
   surface has no comments yet. If it says the store refused the request, stop
   here and read the log: a `404` is a missing installation, section 2. Nobody
   signs in again either way.
5. Leave a comment in the overlay, then open the pull request on GitHub. The
   comment should be there, **authored by your own account**, not by the App.
6. Have a second person do steps 1 to 5 on the same preview. Their comment
   should be authored by them. That is the proof that tokens are per reviewer
   and not shared.

Configure `RouteOptions.logger` before you start. A connector's message is kept
out of the browser deliberately, so without a logger a store failure is a `500`
with its cause recorded nowhere — which turns each entry below into guesswork.

Then confirm the other half: fetch `/api/maple/comments?branch=web-482` against
a **production** build and expect a `404`. Maple should not exist there.

## 6. The second App, when you wire the gate

The comment App above is half of Maple. The merge gate publishes a
`maple/visual-review` check run, which needs `Checks: Read and write`, and it
authenticates **as itself** with an installation token rather than as any
reviewer.

**Run the gate in CI first, and register this App only if you want more.**
`maple-action` publishes `maple/visual-review` on the workflow's own
`GITHUB_TOKEN`, so the merge is gated with no App registered and nobody's
rights needed. This is the action's own workflow, permissions included: without
`checks: write` the gate cannot publish, and without read access to pull
requests it concludes `unreadable` and never blocks.

```yaml
name: Maple
on: pull_request

permissions:
  contents: read

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      checks: write # gate: the check run it reports
      pull-requests: write # sync writes the comment; gate reads them
    steps:
      - uses: maple-kit/maple-action@v0
        with:
          mode: sync
      - uses: maple-kit/maple-action@v0
        with:
          mode: gate
```

`@v0` follows every `v0.x.y` release; pin a full tag such as `@v0.3.0` to hold
one exactly.

**Requiring an approval is opt-in, in three places that must agree.** Add
`require-approval: "true"` to the `gate` step, set
`RouteOptions.requireApproval` on the route, and give the route an identity
connector. The action and the route publish the same check name, so if only
one of them requires an approval, a push clears a gate a reviewer is holding.
Without identity, anyone with the preview URL clears a required check as
"Guest".

What the second App adds is the other direction: a reviewer resolving the last
comment clears the check there and then, instead of waiting for a commit nobody
needs to make. Worth having, and worth having second.

Register the second App separately, when you come to wire the gate and not before. It is a
second **New GitHub App** with `Checks: Read and write`, Device Flow **off**,
and a private key — the opposite of the comment App on all three counts,
because it is the case the comment App exists to avoid. Install it on the same
repositories, and give it the same `app-logo.png` and `#fdf8e8` badge colour
from section 1a: the gate App's avatar is what sits beside
`maple/visual-review` in the checks list on every pull request, at about
twenty pixels, which is the size the mark was drawn to survive. `docs/gate.md` covers the rest.

The route reads no environment of its own. The host reads the App's three
values — `MAPLE_GATE_APP_ID`, `MAPLE_GATE_INSTALLATION_ID` and
`MAPLE_GATE_PRIVATE_KEY`, the last a real secret, unlike anything the comment
App needs — and passes a gate in:

```ts
import { createInstallationAuth } from "@maple-kit/core/auth";
import { githubGate } from "@maple-kit/core/connectors";

// One per process: it caches the hour-long installation token and re-mints it.
const installation = createInstallationAuth({
  appId: process.env.MAPLE_GATE_APP_ID!,
  installationId: process.env.MAPLE_GATE_INSTALLATION_ID!,
  privateKey: process.env.MAPLE_GATE_PRIVATE_KEY!,
});

// …on the same createMapleHandler call:
gate: async () =>
  githubGate({
    owner: "acme",
    repo: "web",
    token: await installation.token(),
    appId: process.env.MAPLE_GATE_APP_ID!,
  }),
// Lets an agent's `maple-mcp` ask for a republish with its own token.
gateRefresh: {
  owner: "acme",
  repo: "web",
  store: (token) => createCommentStore(githubStore({ owner: "acme", repo: "web", token })),
},
```

`gate` is a resolver so the token is asked for on every request; a connector
built once would hold a token that expired an hour later. `gateRefresh` turns
on `POST /api/maple/gate/refresh`, which an agent's `maple-mcp` calls with its
`GITHUB_TOKEN` when `MAPLE_URL` points here; the route checks that token can
push before it publishes, and hands it only to `store`. `appId` is what lets
it find its own check run beside the one GitHub Actions created, and
`docs/gate.md` says which of the two a ruleset should pin.

The reason the permissions cannot simply be added to the App you just made is
the one sentence this whole design rests on: **a user-to-server token carries
every permission its App holds, not just the ones in use.** Add `Checks` here
and every reviewer's cookie can write check runs from then on — with no
re-authorisation, no prompt and no error. Nothing visible changes, which is
exactly why it has to be two Apps rather than a note saying to be careful.

Until the gate is wired, registering only the comment App is complete and
correct. Setting up a second App now, for a gate that does not run yet, buys
the exposure and none of the benefit.

## What to tell your security team

Point them at `docs/github-auth.md`, which is written for exactly that reading.
The three facts that answer most of the questions:

1. **No GitHub secret exists in the preview environment.** Device Flow's token
   exchange needs only the `client_id`, which is public. There is no client
   secret, no private key and no shared token to leak.
2. **Every reviewer has their own token**, held in an `HttpOnly`, `Secure`,
   `SameSite=Lax` cookie scoped to the preview's own origin and to
   `/api/maple`. A stolen token is one person's, and they revoke it themselves
   from **Settings → Applications → Authorized GitHub Apps**.
3. **The permissions are the minimum.** `Pull requests: write` covers all of
   it — finding the pull request and listing, posting, reading and editing a
   comment on it — on only the repositories you installed the App on. No access
   to issues, no access to code, no merge, no settings.

## Troubleshooting

**The overlay says device flow is unsupported.** Device Flow is off on the App.
Turn it on under **Identifying and authorising users** and try again; no
reinstall is needed and nobody has to sign in twice.

**Sign-in works, but reading or posting a comment fails with a 404** — the log
shows `GitHub 404 on /repos/acme/web/pulls?head=…`. The App is not installed on
that repository. A user-to-server token only reaches repositories the App is
installed on, and GitHub answers `404` rather than `403` for a repository the
token cannot see, so "not installed" and "does not exist" are indistinguishable
from the outside. This is the single most common way this setup fails, because
sections 1, 3 and 4 all succeed without it. Install it from section 2 and
retry — the reviewer does not need to sign in again.

**Reading comments works, posting one fails with a 403** — the log shows
`GitHub 403 on /repos/acme/web/issues/42/comments: Resource not accessible by
integration`. Two causes, and this is the order to check them in.

_The App's permissions are wrong._ Every call Maple makes goes to an
`/issues/…` path, because a pull-request conversation comment is an issue
comment, so `Issues: Read and write` with `Pull requests` read-only looks
correct and is not: GitHub authorises a comment on a pull request under
`Pull requests`. Reading succeeds under either permission, which is why
sign-in, the branch lookup and the comment list are all green and only the
send fails. Set `Pull requests: Read and write` as section 1 says — and note
that changing permissions on an App people have already installed does not
take effect until the installation **accepts** them, from
**Settings → Applications → Installed GitHub Apps**. GitHub prompts for it;
until someone says yes the old permissions are still what the token carries.

_The reviewer cannot write to the repository._ A user-to-server token is
bounded by the App's permissions _and_ by what that person can already do, so
the App cannot grant access they do not have. If one reviewer gets a 403 and
another does not, this is why. Give them repository access, or accept that they
cannot comment. If **everyone** gets it, it is the first cause, not this one.

**"No pull request for branch …; Maple has nowhere to post."** The branch has no
open pull request. Maple stores comments as pull-request comments, so there is
nowhere to put one. Open the pull request, even as a draft, and the comment
posts.

**A reviewer is suddenly signed out, or every write fails with a 401.** Their
token was revoked — by them, or by the App being uninstalled. The cookie is
cleared on the first `401` and the overlay offers **Link GitHub** again. If it
happens to everyone at once, check whether the App is still installed on the
organisation.

**The codes never arrive and the route logs a GitHub 404 on
`/login/device/code`.** The `client_id` is wrong or empty. Check
`MAPLE_GITHUB_CLIENT_ID` in the preview environment — it is the **Client ID**
from the App's settings page, not the App ID.
