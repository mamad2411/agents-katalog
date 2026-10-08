---
name: connector-twilio
description: >-
  EXPERIMENTAL, NOT YET VERIFIED AGAINST LIVE TWILIO, and it spends real money —
  every message is billed, and a US-bound production number additionally needs
  A2P 10DLC registration (fees, weeks of lead time). Say both things to the user
  before building. That said, if a Caffeine build does send SMS or MMS, or
  configures Twilio messaging, from a canister, the `twilio-client` mops package
  (Twilio REST API) with a canister-held HTTP Basic credential is the only
  supported path. Hand-rolling `ic.http_request` calls to `api.twilio.com` or
  `messaging.twilio.com` is a FORBIDDEN anti-pattern — it bypasses the typed
  bindings, the per-operation host routing, the Basic-Auth header construction,
  and above all the non-replicated outcall default that stops one `send` from
  becoming ~13 billed messages. Load this skill whenever the user, spec, or any
  prior task mentions SMS, MMS, "text message", "send a text", phone numbers,
  Twilio, a Messaging Service, A2P 10DLC, toll-free verification, short codes, or
  an alphanumeric sender — and BEFORE writing any code that touches a Twilio
  endpoint.
version: 0.1.1
caffeineai-subscription: [none]
compatibility:
  mops:
    twilio-client: "~0.1.2"
    caffeineai-authorization: "~1.0.1"
---

# Twilio Connector (experimental)

Send SMS / MMS and configure Twilio messaging from a Caffeine canister.

> ⚠️ **Experimental (`twilio-client@0.1.2`) — no call has ever been made from this
> client.** Its write path could work at all only recently: before, every write
> discarded its arguments and posted an empty body. The wire format now matches
> what Twilio documents (form-encoded body, percent-encoded values, optional
> fields omitted) and all 118 files typecheck, but *structurally correct* is not
> *verified*. Treat the first successful send as the acceptance
> test, and do not present Twilio to a user as a fully supported platform feature
> until one has happened. Sends cost money, so a failed experiment is not free.

> **Scope — the package is the messaging surface only.** `twilio-client` is
> pruned to **35 API modules** (all of Messaging v1 plus the v2010 messaging path:
> Account, Message, Media, IncomingPhoneNumber and its variants,
> AvailablePhoneNumber, the A2P registries). Voice/calls, recordings, conferences,
> queues, applications, SIP and usage records are **not in the package** — if a
> build needs those, they are outside this connector. (Counts: 35 API modules, 82
> models, **118 files**, all typechecking.)

## Orchestrator routing notes

Load this skill when the user, spec, or a prior task mentions sending a text
message, SMS/MMS, notifying someone by phone, buying or listing phone numbers, or
any Twilio messaging concept. Raw `ic.http_request` to `*.twilio.com` is an
anti-pattern that re-implements auth, host routing, percent-encoding and JSON
parsing by hand — and, done naively, sends every message ~13 times.

Intent → capability mapping:

| User intent | Capability |
| --- | --- |
| Send an SMS | `Api20100401MessageApi.createMessage` with `from` = a Twilio number |
| Send an MMS (image) | same, with `mediaUrl = ["https://…"]` and `sendAsMms = true` |
| Send via a Messaging Service (recommended for US traffic) | same, `from = ""` + `messagingServiceSid` |
| Check delivery status | `fetchMessage` (`status`, `error_code`) |
| List / search sent messages | `listMessage` (paginated) |
| Own or browse phone numbers | `Api20100401IncomingPhoneNumberApi`, `…AvailablePhoneNumberCountryApi` |
| Set up a Messaging Service | `MessagingV1ServiceApi.createService` |
| Register for US A2P 10DLC | `MessagingV1BrandRegistrationApi` → `MessagingV1UsAppToPersonApi` → `MessagingV1PhoneNumberApi` (in that order — see *US A2P 10DLC*) |
| Verify a toll-free number | `MessagingV1TollfreeVerificationApi` |

Twilio credentials are something a **human must go and fetch from a console**, so
the build is not done when the backend compiles — it is done when the app tells
the admin where to get the credential and gives them somewhere to paste it. See
*Auth model*, then *Frontend* for the page that MUST ship, and repeat the steps in
the completion message.

**Ask before writing code:** which number sends? A US-bound production app needs a
Messaging Service + A2P registration (weeks of lead time, real fees); a
demo/internal app can send from a single trial number to *verified* recipients
only. Report the choice and its consequences back to the prompting user.

## Auth model — HTTP Basic, two flavours

Both flavours are the same `#basicAuth { user; password }` credential and the
client treats them identically; they differ in blast radius.

| Flavour | `user` / `password` | When |
| --- | --- | --- |
| **API Key** *(default — prefer this)* | API Key **SID** (`SK…`) / its **Secret** | Production. Revocable and scoped: leaking one does not surrender the account. |
| **Account SID + Auth Token** | Account **SID** (`AC…`) / **Auth Token** | Dev only. The Auth Token *is* the account — it can create sub-accounts, buy numbers, and spend money. |

The **Account SID** (`AC…`) is *also* a required positional argument to every
v2010 operation (it is in the URL path), regardless of which flavour is used. So
an app using an API Key stores **three** values: Account SID, Key SID, Key Secret.

### Obtaining credentials

1. Sign in at <https://console.twilio.com>.
2. The **Account SID** (`AC…`) is on the console dashboard — copy it.
3. For production, **Account → API keys & tokens → Create API key** (Standard);
   copy the **SID** (`SK…`) and the **Secret**. **The Secret is shown once** — if
   the admin navigates away it cannot be recovered, only replaced.
   For dev only, take the **Auth Token** from the dashboard instead.
4. Buy a sending number: **Phone Numbers → Manage → Buy a number**, with the
   **SMS** capability ticked (not every number has it).
5. On a **trial** account: verify each recipient under **Phone Numbers → Verified
   Caller IDs**, or sends fail with `21608`; trial messages also carry a
   "Sent from your Twilio trial account" prefix.

### Handing the credentials to the canister

The admin pastes them through an **admin-gated** setter — gated on
`AccessControl.hasPermission(state, caller, #admin)`. They are held by the
canister only and **never** returned to the frontend.

> ⚠️ **Never gate the setter on a first-caller-claims-ownership scheme.** On the
> IC every unauthenticated caller is the *same* anonymous principal, so if an
> anonymous call claims ownership first, every anonymous caller passes the
> `caller == owner` check and can overwrite the credential — and this one spends
> money.

The canister hands them to the client **only** through
`config.auth = ?#basicAuth { user; password }`, which every method turns into an
`Authorization: Basic …` header. No method takes a credential argument and none
puts it in the URL, so it cannot leak through a logged query string.

## Outcalls are already non-replicated — and this CORRECTS earlier guidance

`defaultConfig` ships `is_replicated = ?false`, so anything derived from it by
record update is correct as-is. Nothing to remember, nothing to add.

> ⚠️ **Do not set it to `?true` or `null`, and disregard any older advice to do
> so.** An older version of this SKILL claimed writes should stay
> replicated "so IC consensus dedups retries". **That is false and expensive.** A
> replicated outcall is performed by *every* node in the subnet: the request is
> sent ~13 times, so **~13 SMS are sent and ~13 are billed**, the credential
> leaves every node, and consensus fails anyway because Twilio stamps each reply
> with a unique `sid` (so the responses never agree byte-for-byte). This is the
> same defect that produced ~13 duplicate emails via the Gmail connector and drove
> `slack-client` 0.1.0.

Reads (`fetch*` / `list*`) are equally fine non-replicated: one node's view of a
message log is what you want, and it is the cheaper path.

# Backend

## Add dependencies

The admin gate in the recipe below needs the authorization component alongside the
client:

```bash
mops add twilio-client@0.1.2
mops add caffeineai-authorization@1.0.1
```

## Calling shape — free functions or the class facade

Every module offers both. The free function takes `config` first and is `async*`;
the `module class` captures `config` and is `async`:

<!-- motoko-check:skip -->
```motoko filepath=src/backend/calling-shape.mo
// Illustrative sketch, not a file to copy: `cfg`/`accountSid` are assumed to
// exist and the argument lists are elided. Marked motoko-check:skip for that
// reason — the compiled examples are the three mixins below.
import MessageApi "mo:twilio-client/Apis/Api20100401MessageApi";

// free function — config passed explicitly
let m = await* MessageApi.createMessage(cfg, accountSid, /* … */);

// class facade — config captured once
let messages = MessageApi.Api20100401MessageApi(cfg);
let m2 = await messages.createMessage(accountSid, /* … */);
```

**All parameters are positional and there are 27 of them on `createMessage`.**
Pass `""` / `false` / `0` / `0.0` / `[]` / **`null`** for the ones you do not
use — the optional enum parameters are `?T` precisely so that `null` omits them
from the wire. Count carefully; a misplaced empty string silently sends the
wrong field. The order is:

`config, accountSid, to, statusCallback, applicationSid, maxPrice,
provideFeedback, attempt, validityPeriod, forceDelivery, contentRetention,
addressRetention, smartEncoded, persistentAction, trafficType, shortenUrls,
scheduleType, sendAt, sendAsMms, contentVariables, riskCheck, from, fallbackFrom,
messagingServiceSid, body, mediaUrl, contentSid`

## The recipe

```motoko filepath=src/backend/main.mo
import AccessControl "mo:caffeineai-authorization/access-control";
import MixinAuthorization "mo:caffeineai-authorization/MixinAuthorization";
import MixinTwilioConfig "mixins/twilio-config";
import MixinTwilioMessaging "mixins/twilio-messaging";

actor {
  let accessControlState : AccessControl.AccessControlState;
  include MixinAuthorization(accessControlState, null);

  // Admin-held Twilio credentials — never returned to the frontend.
  let twilioConfig : {
    var accountSid : Text;   // AC… — also a positional arg on every v2010 call
    var keySid : Text;       // SK… (or the Account SID again, in dev)
    var keySecret : Text;    // the API-key secret (or the Auth Token, in dev)
    var fromNumber : Text;   // E.164, e.g. "+15551234567"
  };
  include MixinTwilioConfig(accessControlState, twilioConfig);
  include MixinTwilioMessaging(twilioConfig);
};
```

The migration chain head:

```motoko filepath=src/backend/migrations/00000000_000000.mo
import AccessControl "mo:caffeineai-authorization/access-control";

module {
  type NewActor = {
    accessControlState : AccessControl.AccessControlState;
    twilioConfig : {
      var accountSid : Text;
      var keySid : Text;
      var keySecret : Text;
      var fromNumber : Text;
    };
  };

  public func migration(_old : {}) : NewActor {
    {
      accessControlState = AccessControl.initState();
      twilioConfig = {
        var accountSid = "";
        var keySid = "";
        var keySecret = "";
        var fromNumber = "";
      };
    };
  };
};
```

```motoko filepath=src/backend/mixins/twilio-config.mo
import AccessControl "mo:caffeineai-authorization/access-control";
import Runtime "mo:core/Runtime";

mixin (
  accessControlState : AccessControl.AccessControlState,
  twilioConfig : {
    var accountSid : Text;
    var keySid : Text;
    var keySecret : Text;
    var fromNumber : Text;
  },
) {
  // All THREE are required, and this must agree with the guard in
  // twilio-messaging.mo: `keySid` is the Basic-Auth *username*, so a blank one
  // means every request goes out unauthenticated and Twilio answers 20003 —
  // while the UI cheerfully reports "Configured".
  public query func isTwilioConfigured() : async Bool {
    twilioConfig.accountSid.size() > 0 and twilioConfig.keySid.size() > 0 and twilioConfig.keySecret.size() > 0;
  };

  // The sending number is not a secret — the UI may display it.
  public query func getTwilioFromNumber() : async Text {
    twilioConfig.fromNumber;
  };

  // Admin-only. NOTE `#admin` — never a first-caller-claims-ownership check,
  // which the shared anonymous principal would defeat.
  public shared ({ caller }) func setTwilioCredentials(
    accountSid : Text,
    keySid : Text,
    keySecret : Text,
  ) : async () {
    if (not AccessControl.hasPermission(accessControlState, caller, #admin)) {
      Runtime.trap("Unauthorized: Only admins can set Twilio credentials");
    };
    twilioConfig.accountSid := accountSid;
    twilioConfig.keySid := keySid;
    twilioConfig.keySecret := keySecret;
  };

  public shared ({ caller }) func setTwilioFromNumber(number : Text) : async () {
    if (not AccessControl.hasPermission(accessControlState, caller, #admin)) {
      Runtime.trap("Unauthorized: Only admins can set the sending number");
    };
    twilioConfig.fromNumber := number;
  };
};
```

```motoko filepath=src/backend/mixins/twilio-messaging.mo
import Principal "mo:core/Principal";
import Runtime "mo:core/Runtime";
import { createMessage } "mo:twilio-client/Apis/Api20100401MessageApi";
import { defaultConfig; type Config } "mo:twilio-client/Config";

mixin (
  twilioConfig : {
    var accountSid : Text;
    var keySid : Text;
    var keySecret : Text;
    var fromNumber : Text;
  },
) {
  // Credentials ride config.auth; defaultConfig is already non-replicated.
  func twilioClientConfig() : Config {
    {
      defaultConfig with
      auth = ?#basicAuth { user = twilioConfig.keySid; password = twilioConfig.keySecret };
      max_response_bytes = ?(200_000 : Nat64);
    };
  };

  /// Send an SMS to `to` (E.164). Returns the message SID.
  public shared ({ caller }) func sendSms(to : Text, body : Text) : async Text {
    if (caller.isAnonymous()) Runtime.trap("Sign in to send messages");
    // Same three-way check as isTwilioConfigured(): accountSid goes in the URL
    // path, keySid is the Basic-Auth user, keySecret the password. Missing any
    // one of them fails at Twilio, not here, so check before spending cycles.
    if (
      twilioConfig.accountSid.size() == 0 or twilioConfig.keySid.size() == 0 or twilioConfig.keySecret.size() == 0
    ) {
      Runtime.trap("Twilio is not configured (an admin must set all three credentials)");
    };
    let msg = await* createMessage(
      twilioClientConfig(),
      twilioConfig.accountSid, // accountSid — in the URL path, not the credential
      to,                      // to (E.164)
      "", "",                  // statusCallback, applicationSid
      0.0,                     // maxPrice (0 = no cap)
      false,                   // provideFeedback
      0, 0,                    // attempt, validityPeriod
      false,                   // forceDelivery
      null, null,              // contentRetention, addressRetention (omitted)
      false,                   // smartEncoded
      [],                      // persistentAction
      null,                    // trafficType (omitted)
      false,                   // shortenUrls
      null,                    // scheduleType — MUST be null for an immediate send
      "",                      // sendAt (scheduled sends only)
      false,                   // sendAsMms
      "",                      // contentVariables
      null,                    // riskCheck (omitted)
      twilioConfig.fromNumber, // from  (use EITHER from OR messagingServiceSid)
      "",                      // fallbackFrom
      "",                      // messagingServiceSid
      body,                    // body
      [],                      // mediaUrl (set for MMS)
      "",                      // contentSid (Content API templates)
    );
    // `sid` is optional in the generated model because the spec marks it
    // nullable, though Twilio always sets it on a successful create. Fall back
    // to "" rather than trapping: the outcall has already happened, so a trap
    // would roll back this canister's own state while the SMS stays delivered.
    switch (msg.sid) { case (?sid) sid; case null "" };
  };
};
```

For MMS: `mediaUrl = ["https://example.com/image.jpg"]` and `sendAsMms = true`.
To send through a Messaging Service, leave `from = ""` and set
`messagingServiceSid` instead.

## Addressing — E.164, and which sender

- **`to` must be E.164**: `+`, country code, no spaces, dashes or parentheses —
  `"+15551234567"`. `"555-1234"` fails with `21211`. Normalize in the frontend and
  again in the canister; do not trust either alone.
- **`from` vs `messagingServiceSid` — exactly one.** Setting both is an error.
  A bare `from` number is fine for non-US traffic and demos; **US-bound
  production traffic should go through a Messaging Service** (sender pool,
  sticky sender, and it is what A2P registration attaches to).
- **The sending number needs the SMS capability**, which not every purchasable
  number has. Filter on it when browsing
  `Api20100401AvailablePhoneNumberCountryApi`.

## US A2P 10DLC — three resources, in this order

Before any US long code can text US destinations, all three must exist. Without
them US carriers reject the traffic outright.

1. **Brand registration** — `MessagingV1BrandRegistrationApi.createBrandRegistrations`,
   referencing Trust Hub `customerProfileBundleSid` + `a2PProfileBundleSid`
   (created out of band). Pass `mock = true` in dev to skip the fee. Status starts
   `PENDING` and settles to `APPROVED` / `FAILED` over hours to days; it fails if
   business details are incomplete, inconsistently formatted, or do not match
   registry data.
2. **A2P campaign** — `MessagingV1UsAppToPersonApi.createUsAppToPerson`,
   referencing both the Messaging Service and the brand. **Most onboarding
   failures land here.** T-Mobile rejects campaigns whose `messageFlow` does not
   describe opt-in, or whose `messageSamples` do not match the declared
   `usAppToPersonUsecase`.
3. **Number → service assignment** —
   `MessagingV1PhoneNumberApi.createPhoneNumber(cfg, serviceSid, phoneNumberSid)`.
   A number lives in exactly one Messaging Service at a time; reassignment needs
   `deletePhoneNumber` first.

**Registration deadline in force:** campaigns without working `privacyPolicyUrl`
*and* `termsAndConditionsUrl` hard-400 since 2026-06-30. Both are positional
arguments on `createUsAppToPerson` and `""` fails; the URLs must resolve to public
HTTPS pages, because Twilio fetches them during registration.

Toll-free numbers use a **separate** flow —
`MessagingV1TollfreeVerificationApi` — not A2P.

## Available API surface

Documented and messaging-focused (this recipe):

| Module | For |
| --- | --- |
| `Api20100401MessageApi` | send / fetch / list / update / delete messages |
| `Api20100401MediaApi`, `…MediaInstanceApi` | MMS media on a message |
| `Api20100401IncomingPhoneNumberApi` (+ `Local`/`Mobile`/`TollFree`) | numbers you own; delete = release |
| `Api20100401AvailablePhoneNumberCountryApi` | browse numbers to buy |
| `Api20100401BalanceApi`, `…AccountApi` | account balance and account records |
| `Api20100401UserDefinedMessageApi` (+ `Subscription`) | user-defined message events |
| `MessagingV1ServiceApi` | Messaging Services (sender pools) |
| `MessagingV1BrandRegistrationApi` (+ `Otp`, `BrandVettingApi`) | A2P brand |
| `MessagingV1UsAppToPersonApi` (+ `UsecaseApi`) | A2P campaigns |
| `MessagingV1PhoneNumberApi`, `…ShortCodeApi`, `…AlphaSenderApi`, `…ChannelSenderApi` | sender pool membership |
| `MessagingV1TollfreeVerificationApi` | toll-free verification |
| `MessagingV1Linkshortening*`, `…DomainConfig*`, `…DomainCertsApi` | branded link shortening |
| `MessagingV1DeactivationsApi` | carrier deactivation list |

**Not in the package** (pruned from the generated surface): calls, recordings,
conferences, participants, queues, applications, SIP domains and credentials,
usage records and triggers, addresses, keys, tokens, balance transactions. The
package ships the messaging surface only — for anything above, this connector is
not the path.

## Errors and pagination

- Methods return the decoded record on 2xx and `throw Error.reject("HTTP <status> body[…]: …")`
  on 4xx/5xx. `diagnostics` is on, so the reject text carries Twilio's own error
  body (`code`, `message`, `more_info`). Wrap in
  `try { … } catch (e) { Error.message(e) }`.
- Codes worth mapping to real UI text: **20003** authenticate failed (bad
  credential), **21211** invalid `To`, **21408** region not permissioned (enable
  the destination country's geo permissions in the console), **21608** unverified
  recipient on a trial account, **21610** recipient has unsubscribed (STOP),
  **21703** sender pool exhausted, **21704** the Messaging Service has no numbers,
  **21714** pool size capped.
- **A 2xx does not mean delivered.** `createMessage` returns `status = #queued`
  or `#accepted`; delivery is asynchronous. Poll `fetchMessage` for
  `#delivered` / `#undelivered` / `#failed` and read `error_code`, or configure a
  `statusCallback` URL (needs an inbound HTTP endpoint — out of scope here).
- **Pagination differs between the two API versions.** v2010 lists — `listMessage`
  and every other `Api20100401*` list — return **top-level** `next_page_uri` /
  `previous_page_uri` (`?Text`, and a *path* such as `/2010-04-01/…`, not a full
  URL). Messaging v1 lists (`listService`, `listPhoneNumber`, the A2P registries)
  instead nest pagination under `meta`, as `next_page_url` / `previous_page_url`
  (full URLs) plus `page_size`. Only 10 of the 70 list responses use the `meta`
  form; `listMessage` is **not** one of them. The `meta` field is typed
  `?ListAlphaSenderResponseMeta` on *every* v1 list, including
  `ListServiceResponse` — identical records are deduplicated to one shared module
  at codegen time, so the name reflects whichever list sorted first, not the
  endpoint you called.
- `pageSize` defaults to 50 and caps at 1000. Bound every list call — an unbounded
  `listMessage` on a busy account will blow `max_response_bytes`.

Reading the two shapes:

<!-- motoko-check:skip -->
```motoko filepath=src/backend/pagination-shape.mo
// Illustrative sketch, not a file to copy — `res` is assumed to be the decoded
// list response. Marked motoko-check:skip for that reason.

// v2010 (listMessage and every other Api20100401* list): top-level, a path
switch (res.next_page_uri) { case (?path) { /* fetch the next page */ }; case null {} };

// Messaging v1 (listService, listPhoneNumber, the A2P registries): nested, a full URL
switch (res.meta) { case (?m) { m.next_page_url }; case null null };
```

## Field gotchas

- `usecase` on `createService` is **`Text`, not a variant**. Valid: `notifications`,
  `marketing`, `verification`, `discussion`, `poll`, `undeclared`. Anything else 400s.
- `usAppToPersonUsecase` is a *different*, brand-tier-dependent enum — query
  `MessagingV1UsAppToPersonUsecaseApi.fetchUsAppToPersonUsecase` for what a given
  brand may use.
- **Optional enum arguments are `?T` — pass `null` to omit them, and prefer that.**
  The variants are *closed*: `contentRetention` `#retain`/`#discard`,
  `addressRetention` `#retain`/`#obfuscate`, `trafficType` `#free`,
  `scheduleType` `#fixed`, `riskCheck` `#enable`/`#disable`. There is **no
  `#Text` escape hatch** — a value the spec does not list cannot be expressed.
  Passing `?#fixed` for `scheduleType` on an immediate send is a **400**:
  Twilio reads it as a scheduled message and then finds no `SendAt`. `null` is
  the correct value for every one of these unless you specifically want the
  behaviour.
- **`maxPrice` is omitted when `0.0`, which is what you want.** Sending
  `MaxPrice=0` would cap the message price at zero and make Twilio refuse paid
  delivery; omitting it means "no cap". Pass `0.0` to omit.
- `xTwilioApiVersion` (on the `UsAppToPerson` methods) — pass `""` unless Twilio
  support asks otherwise.
- **Throughput is per sender:** long code 1 message/second, toll-free ~3,
  international long code ~10, short code 100. Per-number MPS cannot be raised —
  scale by adding numbers to the Messaging Service's sender pool.
- `stickySender` / `areaCodeGeomatch` are US + Canada only.
- `Config.baseUrl` is **unused**. Every operation carries a hardcoded host
  (`api.twilio.com` for v2010, `messaging.twilio.com` for v1), pinned at codegen
  time from the merged spec. Do not set it and do not expect it to redirect
  traffic.

# Frontend

Twilio needs **no OAuth**: the credential is a long-lived pair the admin pastes,
so there is no redirect URI, no `/connect/twilio` route, and no per-user
handshake. Do not build one. What a Twilio build MUST ship is the page that lets
the admin *get* and *enter* the credentials — **acceptance criteria, not
suggestions**; a build missing them is **broken, not merely incomplete**:

- **The credentials page exists and is reachable.** A "send SMS" feature with
  nowhere to enter a credential is unusable. A signed-in admin must reach
  `/settings/twilio` from the nav or from the not-configured prompt.
- **The console steps are in the UI**, not only in the chat reply — the admin
  returns weeks later, after the chat is gone.
- **The API-Key secret is shown once by Twilio.** Say so next to the input, or
  admins will navigate away and have to create a second key.

1. **A login flow — required.** `setTwilioCredentials` gates on `#admin`, so the
   app needs non-anonymous callers. Take login, `useInternetIdentity` / `useActor`
   plumbing and the admin-role gate from
   [`extension-authorization`](../extension-authorization/SKILL.md).

2. **An admin settings page** — `/settings/twilio` (admin-gated). Required:
   - A "How to get your Twilio credentials" panel **above** the inputs, framed as
     a one-time ~5-minute setup, with these numbered steps (the completion message
     must repeat them verbatim):
     1. sign in at <https://console.twilio.com>;
     2. copy the **Account SID** (`AC…`) from the dashboard;
     3. **Account → API keys & tokens → Create API key** (Standard); copy the
        **SID** (`SK…`) and the **Secret** — *the Secret is displayed only once*;
     4. **Phone Numbers → Manage → Buy a number** with the **SMS** capability;
     5. paste the three values plus the number below and save;
     6. on a trial account, verify each recipient under **Verified Caller IDs**.
     Include a convenience link that opens the Twilio console.
   - **Three inputs**: Account SID (plain text — not a secret), Key SID, Key
     Secret (password input). Bound to `setTwilioCredentials`; clear the secret on
     success; keep the form re-submittable, because keys get rotated.
   - **A sending-number field** bound to `setTwilioFromNumber`, with an E.164
     example (`+15551234567`) beside it and client-side validation.
   - Status driven by `isTwilioConfigured()` (`Bool`) — "Configured" / "Not
     configured". That predicate requires **all three** values, Key SID
     included: it is the Basic-Auth username, so a blank one means every request
     is unauthenticated and Twilio answers `20003` while the page claims to be
     configured. **Never** render the secret back, not even masked. The sending
     number may be displayed (`getTwilioFromNumber`); it is not a secret.
   - **Make the page reachable.** The shared Layout nav MUST link here when
     `isCallerAdmin` is true and hide it otherwise. Add the link where the nav is
     defined, not inside this page.

3. **Empty-state nudges.** When `isTwilioConfigured()` is `false`, never render a
   dead "Send" button: admins get a "Set up Twilio" link to `/settings/twilio`;
   non-anonymous non-admins get an explanation — e.g. "Texting isn't set up yet —
   an administrator needs to add Twilio credentials in Settings."

4. **Translate Twilio's errors.** Failures arrive as *rejected* calls carrying
   Twilio's `code`. Map at least these to an action rather than showing the raw
   reject:
   - `20003` → "The Twilio credentials are wrong — an admin should re-paste them"
   - `21211` → "That phone number isn't valid — use the +15551234567 format"
   - `21408` → "Texting that country isn't enabled on this Twilio account"
   - `21608` → "On a trial account the recipient must be verified in Twilio first"
   - `21610` → "That number has replied STOP and cannot be texted"

5. **Never promise delivery.** A successful call means *queued*, not delivered.
   Word the UI accordingly ("Message queued") and, if delivery matters, show the
   polled `status` from `fetchMessage`.

Suggested route layout:

```
/                 →  Main UI (any signed-in user; empty-state when unconfigured)
/settings/twilio  →  Admin credentials + sending number (admin-only)
# No /connect/twilio: Twilio uses pasted long-lived credentials, not a redirect flow.
```

## What the composer must tell the Caffeine user

The app cannot send anything until a human creates a Twilio account, buys a
number and pastes credentials — so the **completion message is part of the
deliverable**, not a summary of it. It MUST contain, in this order:

1. **That credentials are required, and who enters them** — an admin, on
   `/settings/twilio`, reachable from the nav once signed in.
2. **The six numbered steps verbatim** from *Frontend* item 2, including that the
   API-key **Secret is shown only once**.
3. **That Twilio costs money** — per-message pricing plus a monthly number fee,
   and that a trial account can only text **verified** numbers and prefixes every
   message with a trial notice.
4. **For US-bound traffic: the A2P 10DLC requirement**, named as weeks of lead
   time and additional fees, with the three ordered resources — otherwise the
   user will ship an app that silently fails to reach US phones.
5. **The failure map, one line each**: `20003` → re-paste credentials; `21211` →
   E.164 format; `21408` → enable the destination country; `21608` → verify the
   recipient (trial); `21610` → recipient unsubscribed.

Do not compress this to "configure Twilio in Settings" and do not substitute a
link to Twilio's documentation. Use the same wording here as in the settings-page
panel so the two cannot drift.

## Known limitations

- **Only the messaging surface is shipped.** The package is pruned to the
  messaging path; voice/recordings/SIP/usage and the rest are not in it.
- **Inbound messages are out of scope.** Receiving SMS, and `statusCallback`
  delivery receipts, need an inbound HTTP endpoint on the canister — a different
  component, not this client.
- **Binary media is not uploadable.** `mediaUrl` takes a *public URL* Twilio
  fetches; the canister cannot POST image bytes through this client.
- **No idempotency key.** Twilio's messaging API has none, so a retry after a
  timeout may send twice. Guard at the application level (a stable-variable
  dedupe key per logical send) rather than retrying blindly. The non-replicated
  default removes the ~13× amplification, not retry semantics.
- **One dropped field.** `POST …/IncomingPhoneNumbers/{Sid}.json` accepts an
  `AccountSid` *form* field (used to move a number between subaccounts) while
  `AccountSid` is also its path parameter. The generator has a single namespace
  for both, so the form copy is dropped and **transferring a number to a
  subaccount is not reachable** through this client. Every other endpoint is
  unaffected.
- **Nothing here has been exercised against live Twilio.** The wire format is at
  least structurally right — writes send an `application/x-www-form-urlencoded`
  body with percent-encoded parameters, which is what Twilio requires — but no
  call has been made. Treat a first successful send as the real acceptance test.
- **Spec vintage:** generated from Twilio's published OpenAPI specs merged by
  `spec-merge` (Messaging v1 + API v2010), then pruned to the messaging surface.
  Newer Twilio features absent from those specs are absent here.

## Related

- [`mops add twilio-client@0.1.2`](https://mops.one/twilio-client) — the generated Twilio REST bindings (35 messaging modules).
- [Twilio Messaging docs](https://www.twilio.com/docs/messaging) — the API this wraps.
- [`chat`-free quickstart: sending SMS](https://www.twilio.com/docs/messaging/api/message-resource) — the `Message` resource, its fields and statuses.
- [Twilio error codes](https://www.twilio.com/docs/api/errors) — the numeric codes surfaced in reject messages.
- [A2P 10DLC overview](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc) — brand, campaign, number assignment.
- [API keys vs Auth Token](https://www.twilio.com/docs/iam/api-keys) — why production uses `SK…`.
- [extension-authorization](../extension-authorization/SKILL.md) — **required prerequisite**. Internet Identity login, `useInternetIdentity` / `useActor` plumbing, and the `#admin` gate the credential setter needs.
