---
name: gp247-shipping-plugin-create
description: Scaffolds a brand-new GP247 SHIPPING plugin (a carrier or a delivery method shown at checkout) and implements it on gp247/shop's standard shipping layer — a `ShippingProvider` driver that quotes every service of the carrier for the shopper's address, plus the optional capabilities the carrier really offers (book a shipment, cancel it, print the label, track it, receive status webhooks, collect cash on delivery). It probes the installation first and follows the contract the site's gp247/shop actually has, falling back to the older fee-only contract on a shop that predates the shipping layer, and builds the plugin the update-safe way so a 1-click version update never wipes the site owner's settings. Always use this skill when the user asks to create, build, integrate or connect a shipping plugin, a carrier, a delivery or courier service, shipping rates or a shipping API for GP247 — for example "make a GP247 shipping plugin for <carrier>", "integrate <carrier> API into S-Cart", "tạo plugin vận chuyển", "tích hợp hãng giao hàng", "làm plugin ship hàng cho GP247", "kết nối API đơn vị vận chuyển". Trigger on Vietnamese, Japanese, or English phrasing of this intent — the team usually writes in Vietnamese, so do not wait for an exact English keyword match. Do not use this skill for a payment method (use gp247-payment-plugin-create), for any other kind of plugin (use gp247-plugin-create), or to change gp247/shop itself.
---

# gp247-shipping-plugin-create — Build a shipping plugin on gp247/shop's shipping contract

## Purpose

Create a GP247 shipping plugin that plugs into checkout and the order screen the way gp247/shop expects:
the shopper sees **every service** of the carrier with its price and delivery estimate for **their**
address, the price on the order is exactly the one they chose, and — when the carrier has an API for it —
the admin books, cancels, prints and tracks shipments from the order, with status updates arriving by
webhook and no cron.

gp247/shop owns everything common to all carriers: the checkout step, the quote cache and the cool-down of
a failing carrier, currency conversion, the rate the shopper chose (kept on the order), the shipment
records, the webhook route, de-duplication of events, the order's shipping status and the cash-on-delivery
money. **A shipping plugin only translates between that contract and one carrier.** Writing any of the
shared parts again inside the plugin is the most common mistake.

**Never assume a core version.** Step 0 reads what the site's gp247/shop offers; every later step
branches on those facts.

## Output language

**English throughout** — code, questions to the user, progress notes and the final summary. The user may
write in Vietnamese, Japanese or English; you answer in English. Never translate code identifiers or the
language keys passed to `trans(...)` / `gp247_language_render(...)`; only the values in `Lang/vi/lang.php`
and `Lang/en/lang.php` are localized.

## When NOT to use

- A **payment method** (card gateway, bank transfer, cash on delivery as a payment choice) — use
  `gp247-payment-plugin-create`.
- Any other plugin (coupon/total-method, admin feature, storefront block) — use `gp247-plugin-create`.
- Changing gp247/shop's shipping layer itself — a plugin never edits `vendor/gp247/shop`.

## Input

Ask for whatever the prompt leaves unclear — **never guess the carrier's API or the business rules**:

1. **Name** — PascalCase, no spaces (e.g. `ShippingAcme`). Folder name = `configKey`; never changes after release.
2. **How the price is made** — a fixed rule the site owner types in (flat fee, free above an amount,
   by weight band), or a **carrier API** that quotes. For an API: its documentation (link or pasted text),
   sandbox availability, and the authentication scheme.
3. **Services** — one service, or several (e.g. road / express / same-day) shown as separate choices.
4. **Carrier currency** — the currency the carrier prices in (the site must have it in its currency list).
5. **Capabilities** — which of these the carrier really offers: book a shipment, cancel, printable label,
   track by API, status webhook, cash on delivery. Offer only what exists.
6. **Settings** — credentials (always secret), pick-up options, which services to offer, per-store or
   one account for the whole site.

## Workflow

Steps 0–4 and 10 always run; the others depend on the Input and on the probe.

0. **Probe the installation.** From the site root run the bundled read-only probe and keep its JSON:

   ```bash
   php <this-skill-dir>/scripts/gp247-probe.php
   ```

   - `bootstrapped: false` → read `bootstrap_error`; with `core` still set you may continue, treating every
     capability as unknown and saying so; with `core: null` stop — not a GP247 site root.
   - `packages.shop.db` not `true` → stop: checkout is not installed (a composer package alone is not
     enough).
   - `capabilities.shop_shipping_provider` **false** → this shop predates the shipping contract. Tell the
     user, and build the **legacy fee-only** plugin of `references/shipping-contract.md` §9 (or raise
     `requireCore` to a core that has the contract, if they prefer). Skip steps 5–8.
   - `capabilities.shop_shipping_capabilities` lists the optional capabilities this shop understands;
     never implement one that is not listed.
   - `capabilities.shop_shipping_tables` **false** (while `shop_shipping_provider` is true) → the shop's code
     is newer than its database: quoting works, but shipments cannot be stored. Tell the user to run
     `php artisan gp247:update` (or `gp247:shop-update`) before testing booking, tracking or webhooks.
   - Never take the version from composer; use the probe.

1. **Confirm the spec.** Restate the Input answers, the probe facts that matter, and which capabilities
   you will implement. This is the plan.

2. **Scaffold.**

   ```bash
   php artisan gp247:make-plugin --name=<Name> --download=0
   ```

   Exit code 0 = success (add `--json` when `capabilities.json_output`). On error stop and show the
   message — never hand-create the folder.

3. **`gp247.json`** (field rules: `references/file-templates.md` §1):
   `configGroup: "Plugins"`, **`configCode: "Shipping"`** (this is how checkout finds the plugin),
   `configKey: "<Name>"`, `version: "1.0"`, `requireCore` = the probe's `require_core`,
   `requireComposerPackages: ["gp247/shop"]`, and `storeScope: "store"` when each store may use its own
   carrier account (usual), else `"global"`.

4. **Settings — update-safe, credentials secret.** Model A of `references/file-templates.md` §3: one
   `admin_config` row per setting keyed `<Name>_<setting>`, seeded in `install()`, topped up in `update()`,
   shown by a `ConfigForm` screen. Every credential (API token, password, webhook secret) is a `password`
   field with `security = 1` (`references/file-templates.md` §6). Group the screen with `sections()` when
   `capabilities.config_form_sections` (account · services · pick-up · webhook). Inside the driver, read
   settings **for the store of the request** — `gp247_config('<Name>_<setting>', $request->storeId)` —
   never from the session.

   **Check before use (required).** On the same screen override `readiness()` and merge the shop's shipping conditions with the
   carrier's own: `array_merge(ShippingSettings::readiness($this->readinessStoreId(), '<Name>'), $own)` (class
   `GP247\Shop\Shipping\ShippingSettings`, when `capabilities.shop_shipping_readiness`). The shop part covers: shipping switched on,
   province and ward/district fields on customer addresses, the pick-up warehouse, and this carrier enabled for the store. Add the
   carrier's own: credentials filled, the carrier's currency present and enabled in the shop, the webhook URL not on a local domain
   (`localhost`, `*.local`, `*.test`, private IP — a warning). Turn the shop's `origin` item into a warning only when the carrier can
   fall back to an address stored on its side. Local settings only — test the credentials against the carrier on save. Template:
   `references/file-templates.md` §3A.

5. **The driver — quoting (required).** Create `Services/<Name>Provider.php` implementing
   `GP247\Shop\Shipping\Contracts\ShippingProvider` and its one required method `rates()`; contract,
   value objects and rules in `references/shipping-contract.md` §2–4. Return one `ShippingRate` per
   service, priced in the **carrier's currency** — the core converts once. An ordinary failure (address
   incomplete, not configured, carrier said no) is returned with `RateResult::error()`; a carrier outage
   (timeout, 5xx) is thrown, so the shop pauses that carrier. Give every HTTP call a short timeout.

6. **Register the driver** in `Provider.php`, inside the `gp247_extension_check_active(...)` block and
   behind `interface_exists(...)` so the plugin still boots on an older shop
   (`references/shipping-contract.md` §1). Declare in `capabilities` only what the driver implements; the
   shop ignores a declared capability whose interface is missing and logs it.

7. **(Optional) Shipments.** For each capability the carrier really offers, implement its interface on the
   same driver (`references/shipping-contract.md` §5): `CreatesShipments` (book + the extra fields of the
   booking form), `CancelsShipments`, `ProvidesShippingDocuments`, `TracksShipments`. Map every carrier
   status onto `ShipmentStatus` in one place (§6). Throw `ShippingException` with an admin-safe message
   when the carrier refuses. Cash on delivery: declare `'cod'` and send the amount the shop computed in
   `ShipmentRequest::$codAmount` — it is in the **order's** currency, so convert it to the carrier's
   currency first (§7). Never recompute it.

8. **(Optional) Webhook.** Implement `HandlesShippingWebhooks` (`references/shipping-contract.md` §8).
   The shop already serves the route `/shipping/webhook/<Name>` (the prefix is configurable); **do not add
   a webhook route to the plugin**. Verify the caller before trusting anything, and show the webhook URL (built with
   `route('shop.shipping.webhook', ['pluginKey' => '<Name>'])`) on the settings screen.

9. **Admin screen & menu.** The settings screen is the plugin's `/` admin route
   (`admin_<url_key>.index`); add `'settings_route' => 'admin_<url_key>.index'` to the registry entry so the
   shop's shipping settings link to it. Text through `trans('Plugins/<Name>::lang.…')` with vi + en values;
   only `<x-gp247::*>` components, Livewire and Alpine — no jQuery. Delete the scaffold's legacy admin
   controller, `Seo.php` and its registration, and the front controller/route (a shipping plugin has no
   storefront page of its own).

10. **Tests and lifecycle.** Write tests before calling it done (`references/shipping-contract.md` §10):
    never call the real carrier — fake HTTP. Then, with the user's OK (these commands write the DB):

    ```bash
    php artisan optimize:clear
    php artisan gp247:ext-install   --type=plugin --key=<Name>
    php artisan gp247:ext-uninstall --type=plugin --key=<Name> --only-data   # KEEP the source files
    php artisan gp247:ext-install   --type=plugin --key=<Name>
    ```

    **Always `--only-data` on the plugin you are building** — a plain uninstall deletes its source folder.
    Then place a test order: the checkout shows each service with price and estimate, the order keeps the
    chosen rate, and (if implemented) book → label → sync → cancel work from the order screen.

**Update-safety invariants** (details in `references/file-templates.md` §4–5): `version` only increases,
`configKey` never changes, editable values live in `admin_config`, `update(?string $fromVersion)` is
idempotent and handles `null`. Shipments booked through the plugin belong to the shop's records — uninstall
removes the plugin's settings and menu only.

## Output format

Apply the edits, then give a short English summary (`[x]` done, `[ ]` skipped — say why):

```
Created shipping plugin <Name> on gp247/core <probe.core> (shop shipping contract: <yes / legacy fee-only>):
- [x] Probed: shop usable; shipping capabilities offered by the shop: <list>
- [x] Scaffolded + gp247.json → configCode Shipping, storeScope <store/global>, requireCore <probe.require_core>
- [x] Settings: <keys>; secrets: <keys> (encrypted)
- [x] Check before use: shop conditions (ShippingSettings::readiness) + <carrier conditions>
- [x] Quoting: <n> service(s) in <currency>; refusals returned as RateResult errors, outages thrown; HTTP timeout <s>
- [ ] Shipments: <shipments / cancel / documents / tracking / cod — or skipped, why>
- [ ] Webhook: <verification method — or skipped, why>
- [x] Registered in gp247-config.shop.shipping_providers with capabilities <list>
- [x] Tests: <what is covered>
- [ ] Installed / lifecycle tested: <… / skipped — user will test>
Next step: enter sandbox credentials, place a test order, then switch to live.
```

## Examples

**Example 1 — flat-rate method, no API.** "Tạo plugin vận chuyển nội thành giá 20.000đ, miễn phí đơn từ
500.000đ." → One service. Settings in base currency (`fee`, `free_from`); `rates()` compares
`RateRequest::$declaredValue` (base currency) with the threshold and returns one rate in the base currency.
Capabilities `['rates']`. Mirror the public `ShippingStandard` plugin.

**Example 2 — carrier with a full API.** "Integrate <carrier> into S-Cart: quote, create order, label,
webhook." → Ask for the API docs and sandbox. Driver implements `ShippingProvider`, `CreatesShipments`,
`CancelsShipments`, `ProvidesShippingDocuments`, `TracksShipments`, `HandlesShippingWebhooks`; a status
map class; capabilities `['rates','shipments','cancel','documents','tracking','webhook','cod']` limited to
what the carrier offers; webhook secret generated on install and shown as part of the webhook URL.

**Example 3 — older shop.** Probe: `shop_shipping_provider` false. → Tell the user; build the legacy
`getInfo()` plugin (§9 of the contract) or stop if they would rather upgrade the shop first.

## Common mistakes

| Mistake | Why it hurts / how to avoid |
| --- | --- |
| Running API tokens, secrets, webhook payloads or tracking codes through `gp247_clean()` or another cleaning function | Encoding turns `&` into `&amp;`: the provider rejects the key or the signature no longer matches. Store them exactly as received (secrets encrypted); clean only the text a person types with `gp247_text_plain()` and print with `{ }`. |
| A settings screen that does not say what is still missing | The owner enables the plugin, nothing happens, and they must hunt for the cause on other screens. Implement `readiness()` with every local condition the plugin needs, each with the reason and a link to where to fix it (`references/file-templates.md` §3A). |
| Converting the carrier price to the display currency in the plugin | The shop converts carrier → base → display once; a second conversion doubles it. Return `Money` in the carrier's currency. |
| Throwing from `rates()` on a normal failure | Return `RateResult::error()` for an expected refusal (address, not configured). Reserve exceptions for an outage: the shop logs them and pauses that carrier for a minute. |
| No HTTP timeout on the quote call | A slow carrier stalls the checkout step for every new cart or address. Keep the timeout short (a few seconds). |
| Reading settings from the session / current store | Quotes are re-made for other stores and in the admin. Use `RateRequest::$storeId` / the `$storeId` argument. |
| Adding a webhook route in the plugin | The shop serves `/shipping/webhook/<Name>` with throttling and de-duplication. Implement `HandlesShippingWebhooks`. |
| Trusting a webhook body | Anyone can POST to it. Verify a signature or secret first; confirm money-bearing states (delivered, COD settled) from the carrier API. |
| Writing the order's shipping status or recording COD money in the plugin | Return `TrackingEvent`s; the shop folds them into the order and (when the site owner enabled it) records COD once. |
| Sending the COD amount without converting it | `ShipmentRequest::$codAmount` is in the order's currency; the carrier would collect the wrong amount. Convert with `ShippingCurrency::convert()` and refuse when it returns null. |
| A dedupe-unstable event (`occurredAt = time()`) | A replayed webhook must produce the same event; use the carrier's own event time. |
| Declaring a capability the driver does not implement | The shop drops it and logs a warning; the admin never sees the button. |
| Reusing the order id as the carrier booking id after a cancel | Carriers refuse a reused id. Send `ShipmentRequest::bookingReference()`. |
| Secrets in `config.php`, logs or exception messages | Credentials are `password` fields (encrypted); exception messages are shown to admins as-is. |
| Rebuilding the parcel weight from products | `ShippingItem` already carries grams and cm (with the shop's default weight applied); use it, or `ShipmentRequest::$parcel` when the admin measured the box. |

## Bundled resources

- `scripts/gp247-probe.php` — step 0. Read-only; one JSON object (core version, `require_core`, usable
  packages, `gp247:*` commands, capabilities). Identical copies ship with every gp247-* skill.
- `references/shipping-contract.md` — steps 5–8 and 10: registry, value objects, rules, optional
  capabilities, status map, COD, webhook, legacy contract, tests.
- `references/file-templates.md` — steps 3–4 and 9: `gp247.json`, settings and secrets, `update()`, menu.
  Identical copies ship with every GP247 plugin skill.

---

## Skill info

| Field | Value |
| --- | --- |
| Lần cuối cập nhật / Last updated | `2026-11-13` |
| Skill repo | https://github.com/gp247net/gp247-skills |
| GP247 shop repo | https://github.com/gp247net/shop |
| source | https://github.com/gp247net/shop/tree/master/src/Shipping |
