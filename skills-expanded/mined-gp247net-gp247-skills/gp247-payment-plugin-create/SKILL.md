---
name: gp247-payment-plugin-create
description: Scaffolds a brand-new GP247 PAYMENT plugin (a payment method shown at checkout — a hosted card/wallet gateway, a bank-transfer or QR method, or a cash-on-delivery style method) and implements it on gp247/shop's money contract — the checkout hand-off, the order payment ledger (money recorded once, even when a webhook is delivered twice), status changes through the order's own transition, a signature-checked webhook, and optionally payment links and refunds through the shop's payment-gateway registry. It probes the installation first and uses only what the site's gp247/shop actually has, keeps credentials encrypted, and builds the plugin the update-safe way so a 1-click version update never wipes the site owner's settings. Always use this skill when the user asks to create, build, integrate or connect a payment plugin, payment gateway, payment method, wallet, QR or bank-transfer payment, or a payment provider's API for GP247 — for example "make a GP247 payment plugin for <gateway>", "integrate <gateway> into S-Cart", "tạo plugin thanh toán", "tích hợp cổng thanh toán", "làm plugin payment cho GP247", "kết nối ví điện tử". Trigger on Vietnamese, Japanese, or English phrasing of this intent — the team usually writes in Vietnamese, so do not wait for an exact English keyword match. Do not use this skill for a shipping method or carrier (use gp247-shipping-plugin-create), for any other kind of plugin (use gp247-plugin-create), or to change gp247/shop itself.
---

# gp247-payment-plugin-create — Build a payment plugin on gp247/shop's money contract

## Purpose

Create a GP247 payment plugin that takes money the way gp247/shop expects: the order is created by the
shop, the plugin sends the shopper to pay, and the money that **really** arrived is written to the order's
payment ledger **exactly once** — whether the shopper comes back, the provider's webhook arrives, arrives
twice, or arrives late. Status moves only through the order's own transition, which also handles stock and
history.

gp247/shop owns the order, its totals, the payment ledger (`received`, balance and payment status are
derived from it), the status transitions, and — when the site has it — payment requests (pay links and
refunds outside checkout). **A payment plugin only talks to one provider and reports what the provider
confirmed.** Writing an order's status, paid amount or payment status directly is the mistake that loses
money.

**Never assume a core version.** Step 0 reads what the site's gp247/shop offers; every later step
branches on those facts.

## Output language

**English throughout** — code, questions to the user, progress notes and the final summary. The user may
write in Vietnamese, Japanese or English; you answer in English. Never translate code identifiers or the
language keys passed to `trans(...)` / `gp247_language_render(...)`; only the values in `Lang/vi/lang.php`
and `Lang/en/lang.php` are localized.

## When NOT to use

- A **shipping method or carrier** — use `gp247-shipping-plugin-create`.
- A coupon, points or other checkout total-method, or any non-payment plugin — use `gp247-plugin-create`.
- Changing gp247/shop's checkout or ledger — a plugin never edits `vendor/gp247/shop`.

## Input

Ask for whatever the prompt leaves unclear — **never guess the provider's API or the money rules**:

1. **Name** — PascalCase (e.g. `PaymentAcme`). Folder name = `configKey`; never changes after release.
2. **Kind of method**
   - **Offline / cash on delivery / manual transfer** — no provider call; the order completes at once and
     money is recorded later by the admin (for cash on delivery, optionally by the shop when the carrier
     settles the cash — a site-owner setting, off by default).
   - **Hosted redirect** — the shopper pays on the provider's page and comes back (most gateways).
   - **Embedded** — the provider's script collects the card on the shop's page; still confirmed
     server-side.
3. **Provider API** — documentation, sandbox, authentication, how it signs webhooks, which currencies,
   amount format (minor units?), refund API.
4. **Notifications** — does it send a webhook / IPN? (Strongly preferred: a shopper who closes the tab
   must still produce a paid order.)
5. **Payment links / refunds** — should the plugin also collect money for the shop's payment requests and
   refund through the provider? (Only if `capabilities.shop_payment_gateway`.)
6. **Settings** — sandbox and live credentials, test-mode switch, the order status after payment,
   per-store accounts or one account for the site.

## Workflow

Steps 0–5 and 10 always run; the others depend on the Input and the probe.

0. **Probe the installation.** From the site root run the bundled read-only probe and keep its JSON:

   ```bash
   php <this-skill-dir>/scripts/gp247-probe.php
   ```

   - `bootstrapped: false` → read `bootstrap_error`; with `core` still set continue but treat every
     capability as unknown and say so; with `core: null` stop — not a GP247 site root.
   - `packages.shop.db` not `true` → stop: checkout is not installed.
   - `capabilities.shop_order_record_payment` / `shop_order_change_status` **false** → this shop has no
     payment ledger / transition seam. Tell the user what that means (the plugin cannot record money
     safely) and recommend raising `requireCore` to a core that has them; do not write directly to the
     order instead.
   - `capabilities.secret_cast` false → the core cannot encrypt credentials: tell the user before going on.
   - Never take the version from composer; use the probe.

1. **Confirm the spec.** Restate the Input answers, the probe facts that matter, and which optional parts
   you will build. This is the plan.

2. **Scaffold.**

   ```bash
   php artisan gp247:make-plugin --name=<Name> --download=0
   ```

   Exit code 0 = success (add `--json` when `capabilities.json_output`). On error stop and show it.

3. **`gp247.json`** (field rules: `references/file-templates.md` §1): `configGroup: "Plugins"`,
   **`configCode: "Payment"`** (this is how checkout finds it), `configKey: "<Name>"`, `version: "1.0"`,
   `requireCore` = the probe's `require_core`, `requireComposerPackages: ["gp247/shop"]`, `storeScope:
   "store"` when each store may use its own provider account, else `"global"`.

4. **Settings — update-safe, credentials secret.** Model A of `references/file-templates.md` §3, one
   `admin_config` row per setting `<Name>_<setting>`. **Sandbox and live credentials are separate
   `password` rows with `security = 1`** (§6), plus a test-mode switch and the order status to set after
   payment. Group them with `sections()` when `capabilities.config_form_sections`. Payment settings
   decide where the money goes: unless the user asks otherwise, do **not** let store-admins edit them
   (leave the admin segment out of `gp247-config.admin.store_scoped_segments`).

   **Check before use (required).** Override `readiness()` on the same screen (when `capabilities.core_config_form_readiness`) and
   merge the shop's payment conditions with the gateway's own:
   `array_merge(PaymentSettings::readiness($this->readinessStoreId(), '<Name>'), $own)` (class `GP247\Shop\Payment\PaymentSettings`,
   when `capabilities.shop_payment_readiness`). The shop part covers: the payment step switched on at checkout (`payment_enabled`)
   and this plugin enabled for the store being checked (`provider_enabled`) — do not re-implement them. Without that capability
   (older gp247/shop) compute the same two checks yourself, under the same keys. Add the gateway's own: the credentials of the
   **active** mode (sandbox or live) filled, at least one shop currency the gateway accepts, the webhook URL not on a local domain
   (`localhost`, `*.local`, `*.test`, private IP — a warning), the order status set after payment still exists. Local settings
   only — verify the keys against the gateway on save. Template: `references/file-templates.md` §3A.

5. **Checkout hand-off.** `AppConfig::getInfo()` keeps the scaffold's keys (`title`, `image`, …); add a
   `note` key when the method shows instructions to the shopper (bank account, QR) — a plain-text string,
   read per store; checkout (gp247/shop 3.1.4+) prints it escaped under the selected method and on the
   confirm step. Amount/order number need the plugin's own page after the order. Then
   (`references/payment-contract.md` §1–2):
   - **Offline method** — no `processOrder()`: the shop completes the order directly.
   - **Gateway** — `Controllers\FrontController::processOrder()` reads `session('orderID')`, creates the
     provider session **idempotently per order**, stores the provider's reference, and redirects. Return
     and cancel routes finish with the shop's `completeOrder()` / `cancelOrder()`.

6. **Record the money — the core rule** (`references/payment-contract.md` §3). Only from data the
   provider **confirmed** (a verified webhook, or the provider API read back on return — never the
   query string): compare amount and currency with the order, record what the provider actually took
   with `$order->recordPayment(...)` keyed by the provider's transaction id, then move a still-new order
   with `$order->changeStatus(...)` and check its result. Refunds made at the provider are mirrored with
   `recordRefund(...)`; the order's status does not follow by itself — move a fully refunded order to
   `REFUNDED` with `changeStatus(...)`.

7. **Webhook** (`references/payment-contract.md` §4): a route **outside** the storefront middleware group,
   generous throttle, **signature verified before anything touches the database**, idempotent handling,
   500 on an internal error so the provider retries.

8. **(Optional) Payment links and refunds** — if `capabilities.shop_payment_gateway` and the user wants
   it: a driver implementing `GP247\Shop\Payment\Contracts\PaymentGateway`, registered in
   `gp247-config.payment.gateways` (`references/payment-contract.md` §5).

9. **(Optional) Cash on delivery** — a method paid in cash to the courier adds its key to
   `gp247-config.shop.cod_payment_methods` (if `capabilities.shop_cod_payment_methods`), so shipments of
   its orders collect the balance (`references/payment-contract.md` §6).

10. **Admin screen, tests, lifecycle.** Settings screen = the plugin's `/` admin route; text via
    `trans('Plugins/<Name>::lang.…')` with vi + en values; `<x-gp247::*>`, Livewire, Alpine — no jQuery.
    Delete the scaffold's legacy admin controller, `Seo.php` and its registration. Write the tests of
    `references/payment-contract.md` §7 (never call the real provider). Then, with the user's OK (these
    commands write the DB):

    ```bash
    php artisan optimize:clear
    php artisan gp247:ext-install   --type=plugin --key=<Name>
    php artisan gp247:ext-uninstall --type=plugin --key=<Name> --only-data   # KEEP the source files
    php artisan gp247:ext-install   --type=plugin --key=<Name>
    ```

    **Always `--only-data` on the plugin you are building** — a plain uninstall deletes its source folder.
    Then pay a sandbox order end to end, including the webhook (the provider's CLI or dashboard can
    replay one).

**Update-safety invariants** (`references/file-templates.md` §4–5): `version` only increases, `configKey`
never changes, editable values live in `admin_config`, `update(?string $fromVersion)` is idempotent and
handles `null`. **Money already recorded belongs to the store's accounts** — uninstall removes the
plugin's settings and menu only, never ledger rows.

## Output format

Apply the edits, then give a short English summary (`[x]` done, `[ ]` skipped — say why):

```
Created payment plugin <Name> on gp247/core <probe.core>:
- [x] Probed: shop usable; ledger <yes/no>, changeStatus <yes/no>, payment gateway registry <yes/no>, secrets <encrypted/NOT available>
- [x] Scaffolded + gp247.json → configCode Payment, storeScope <store/global>, requireCore <probe.require_core>
- [x] Settings: <keys>; secrets: <keys> (encrypted, sandbox + live)
- [x] Check before use: shop conditions (PaymentSettings::readiness) + readiness() lists <gateway conditions>
- [x] Checkout: <offline / processOrder → hosted page / embedded>; return + cancel routes
- [x] Money: recordPayment keyed by <provider txn id>; amount + currency checked; changeStatus → <status>
- [ ] Webhook: <route, signature scheme — or skipped, why>
- [ ] Payment links / refunds: <PaymentGateway capabilities — or skipped, why>
- [ ] Cash on delivery: <registered — or not applicable>
- [x] Tests: <what is covered>
- [ ] Installed / lifecycle tested: <… / skipped — user will test>
Next step: enter sandbox credentials, pay a test order (and replay its webhook), then switch to live.
```

## Examples

**Example 1 — bank transfer with instructions.** "Tạo plugin thanh toán chuyển khoản, hiện số tài khoản
cho khách." → Offline method: no `processOrder()`, `getInfo()` note shows the account; no webhook;
money is recorded by the admin from the order screen. Mirror the public `CashPayment` plugin.

**Example 2 — hosted gateway with webhook.** "Integrate <gateway> checkout into S-Cart." → Ask for API
docs, sandbox and the webhook signing scheme. `processOrder()` creates the session with an idempotency key
per order; return route reads the session back from the provider; webhook outside the storefront group
verifies the signature, records with `recordPayment()` keyed by the provider's payment id, then
`changeStatus()`. Public references: `StripePayment`, `PaypalExpress`.

**Example 3 — also pay links.** "…and let the shop send pay links and refund." → Probe has
`shop_payment_gateway`: add a `PaymentGateway` driver with `['collect', 'refund']`, record link payments
with `PaymentRequestService::recordMovement()`, mirror provider-side refunds via `findGatewayCollect()`.

## Common mistakes

| Mistake | Why it hurts / how to avoid |
| --- | --- |
| Running API keys, secrets, webhook payloads or gateway references through `gp247_clean()` or another cleaning function | Encoding turns `&` into `&amp;`: the provider rejects the key or the signature no longer matches. Store them exactly as received (secrets encrypted); clean only the text a person types with `gp247_text_plain()` and print with `{ }`. |
| A settings screen that does not say what is still missing | The owner enables the plugin, nothing happens, and they must hunt for the cause on other screens. Implement `readiness()` with every local condition the plugin needs, each with the reason and a link to where to fix it (`references/file-templates.md` §3A). |
| `$order->update(['status' => …, 'payment_status' => …, 'received' => …])` | Skips stock, history and events; `received` is derived from the ledger and is overwritten. Use `recordPayment()` + `changeStatus()`. |
| Trusting the return URL's query string | Anyone can type it. Read the payment back from the provider (or wait for the verified webhook). |
| Recording the order total instead of what the provider took | Hides a mismatch. Record the provider's amount; add a note and report when it differs. |
| Recording money in the display currency or float noise | `recordPayment()` takes the **order's** currency; convert minor units with the currency's precision. |
| Webhook inside the storefront middleware group | Session/CSRF/maintenance middleware can answer with a redirect or 200 page the provider counts as delivered — the payment is lost. |
| Verifying the signature after reading the database | An unsigned flood reaches the DB. Verify first, on the raw body. |
| Treating a duplicate-key error on a concurrent second delivery as a failure | The ledger is idempotent on the transaction id; a concurrent replay can still raise a unique-key error — catch it as "already recorded". |
| Moving an order that is no longer new | A late webhook must not undo what the admin did (shipped, completed). Only move `NEW` orders; otherwise add history. |
| Ignoring `changeStatus()`'s return value | It returns a reason when it refuses (e.g. not enough stock to reopen). Check it. |
| Credentials in `config.php`, `.env` shipped with the plugin, logs or exception text | `password` fields with `security = 1`; never echo them. |
| Calling the real provider from tests | Fake HTTP and post signed sample webhooks. |
| Deleting ledger rows on uninstall | Recorded money belongs to the store's books. |

## Bundled resources

- `scripts/gp247-probe.php` — step 0. Read-only; one JSON object (core version, `require_core`, usable
  packages, `gp247:*` commands, capabilities). Identical copies ship with every gp247-* skill.
- `references/payment-contract.md` — steps 5–10: checkout hand-off, ledger, status, webhook, payment
  gateway registry, cash on delivery, tests.
- `references/file-templates.md` — steps 3–4 and 10: `gp247.json`, settings and secrets, `update()`, menu.
  Identical copies ship with every GP247 plugin skill.

---

## Skill info

| Field | Value |
| --- | --- |
| Lần cuối cập nhật / Last updated | `2026-11-13` |
| Skill repo | https://github.com/gp247net/gp247-skills |
| GP247 shop repo | https://github.com/gp247net/shop |
| source | https://github.com/gp247net/shop/tree/master/src/Payment |
